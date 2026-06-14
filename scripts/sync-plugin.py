#!/usr/bin/env python3
"""Sync the feature pipeline from this template (canonical) into the standalone
`ideal-workflow` Claude Code plugin.

The template and the plugin express the SAME pipeline but in different wiring:

  * Template  -> a generated project: skills are vendored under `.claude/skills/`,
                 conventions live in an instruction tree, test/lint run via `just`.
  * Plugin    -> install-anywhere: skills are global (`superpowers:*`,
                 `grill-with-docs`, `engineering:documentation`), config lives in
                 `CONSTITUTION.md`, hooks are plugin-scoped.

This script keeps the two in step where it is safe and high-value:

  1. **Hook scripts** (`block-locked-tests.py`, `autoformat.py`) are copied
     from the template sources (which are template-free) and stamped with a
     GENERATED header. This is the main drift risk.
  2. **The five split agents** (test-writer/implementer/verifier/debugger/
     documenter) are rendered from their Jinja sources with a canonical
     "plugin" answer set, then passed through structure-preserving token
     rewrites (skill paths -> global skill names, instruction-tree refs ->
     CONSTITUTION.md, `just` -> project commands, `.claude/hooks` -> `hooks`).

It deliberately does NOT touch plugin-specific files (orchestrator command,
planner/reviewer agents, CONSTITUTION.md, templates) — those have no 1:1
template source because the plugin reuses different agents.

Usage:
  python scripts/sync-plugin.py [--plugin-dir <path>] [--check]

`--plugin-dir` defaults to ``../ideal-workflow`` next to this repo.
`--check` renders + diffs but writes nothing (exit 1 if anything is stale).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    from jinja2 import Template
except ImportError:
    sys.exit("ERROR: jinja2 is required. Run `uv run python ...` or `pip install jinja2`.")

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_PROJECT = REPO_ROOT / "template" / "{{ project_slug }}"
AGENTS_DIR = TEMPLATE_PROJECT / "{{ ai_folder }}" / "agents"
HOOKS_DIR = TEMPLATE_PROJECT / ".claude" / "hooks"

# Canonical answer set for rendering the template files as the plugin.
CTX = {
    "ai_folder": ".claude",
    "ai_agent": "claude",
    "agent_file_style": "canonical",
    "languages": ["python", "rust", "cpp"],
    "include_feature_pipeline": True,
    "include_brainstorming": True,
    "use_spec_kit": False,
    "project_name": "ideal-workflow",
    "project_slug": "ideal-workflow",
}

AGENT_NAMES = ["test-writer", "implementer", "verifier", "debugger", "documenter"]
HOOK_FILES = ["block-locked-tests.py", "autoformat.py"]

# Vendored / project-local skill dir-name -> global skill reference.
SKILL_MAP = {
    "test-driven-development": "superpowers:test-driven-development",
    "tdd-cycle": "superpowers:test-driven-development",
    "systematic-debugging": "superpowers:systematic-debugging",
    "requesting-code-review": "superpowers:requesting-code-review",
    "verification-before-completion": "superpowers:verification-before-completion",
    "run-tests": "superpowers:verification-before-completion",
    "lint-and-format": "superpowers:verification-before-completion",
    "writing-plans": "superpowers:writing-plans",
    "brainstorming": "superpowers:brainstorming",
    "update-changelog": "engineering:documentation",
    "grilling": "grill-with-docs",
}


def agent_src(name: str) -> Path:
    return AGENTS_DIR / ("{% if include_feature_pipeline %}" + name + ".md{% endif %}.jinja")


def hook_src(name: str) -> Path:
    return HOOKS_DIR / (
        "{% if include_feature_pipeline and ai_agent in ['claude', 'universal'] %}" + name + "{% endif %}"
    )


def rewrite_agent(text: str) -> str:
    """Structure-preserving token rewrites: template wiring -> plugin wiring."""
    def skill_sub(m: re.Match) -> str:
        name = m.group(1)
        return "`" + SKILL_MAP.get(name, name) + "`"

    def join_refs(refs: list[str]) -> str:
        seen: list[str] = []
        for r in refs:
            if r not in seen:
                seen.append(r)
        if len(seen) <= 1:
            return seen[0] if seen else ""
        if len(seen) == 2:
            return f"{seen[0]} and {seen[1]}"
        return ", ".join(seen[:-1]) + f", and {seen[-1]}"

    # Collapse "N. Load the conventions for this task:\n<bullets>" (each bullet
    # points into the instruction tree the plugin lacks) into one pointer.
    text = re.sub(
        r"(?P<n>\d+)\. Load the conventions for this task:\n"
        r"(?:(?![ \t]*\d+\. ).*\n)*",
        lambda m: f"{m.group('n')}. Skim `CONSTITUTION.md` for the conventions "
        "relevant to this task (test framework, style, layering).\n",
        text,
    )
    # `.claude/skills/<name>/SKILL.md` -> `global:skill`
    text = re.sub(r"`?\.claude/skills/([a-z-]+)/SKILL\.md`?", skill_sub, text)
    # `.claude/instructions/<anything>` -> `CONSTITUTION.md`
    text = re.sub(r"`?\.claude/instructions/[^\s`]+`?", "`CONSTITUTION.md`", text)
    # plugin hooks live in hooks/, not .claude/hooks/
    text = text.replace(".claude/hooks/", "hooks/")
    # test/lint run from CONSTITUTION.md commands, not just recipes
    text = text.replace("`just test`", "the project's test command")
    text = text.replace("`just lint`", "the project's lint command")
    text = text.replace("just test", "the project's test command")
    text = text.replace("just lint", "the project's lint command")
    # Any other `just <recipe>` reference -> a generic phrasing.
    text = re.sub(r"`just [a-z-]+`", "the project's tooling", text)
    # any stray playbook filename -> the plugin's config doc
    text = text.replace("feature-pipeline.md", "CONSTITUTION.md")
    # Documenter artifact paths: the scaffolder's "Where things live" layout
    # (docs/manual, docs/design, spec-kit specs/) -> the plugin's flat layout
    # declared in CONSTITUTION.md (docs/specs, docs/plans, docs/<slug>.md).
    text = re.sub(
        r"the spec — `specs/<slug>/spec\.md` if spec-kit\s+is in use, else "
        r"`docs/design/<slug>-spec\.md` —",
        "the spec — `docs/specs/<date>-<slug>-spec.md` —",
        text,
    )
    text = text.replace("`docs/manual/<slug>.md`", "`docs/<slug>.md`")
    text = text.replace("docs/manual/<slug>.md", "docs/<slug>.md")
    text = text.replace("`docs/plans/<date>-<slug>.md`", "`docs/plans/<date>-<slug>-plan.md`")
    # De-duplicate the skills sentence ("announce them: `A` and `A`." -> "`A`.").
    text = re.sub(
        r"(announce (?:them|it): )([^\n.]*)\.",
        lambda m: m.group(1) + join_refs(re.findall(r"`[^`]+`", m.group(2))) + ".",
        text,
    )
    return text


BANNER = (
    "<!-- GENERATED by ideal-project-scaffolder/scripts/sync-plugin.py from the "
    "template agent source. Do NOT hand-edit — edit the template and re-sync. -->"
)


def banner_py(text: str) -> str:
    """Insert a `#`-comment banner after the shebang of a Python hook file."""
    comment = (
        "# GENERATED by ideal-project-scaffolder/scripts/sync-plugin.py — do NOT\n"
        "# hand-edit; edit the template hook source and re-sync.\n"
    )
    lines = text.splitlines(keepends=True)
    if lines and lines[0].startswith("#!"):
        return lines[0] + comment + "".join(lines[1:])
    return comment + text


def add_banner(text: str) -> str:
    """Insert the generated-file banner right after the YAML frontmatter."""
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            head = text[: end + len("\n---\n")]
            rest = text[end + len("\n---\n") :].lstrip("\n")
            return f"{head}\n{BANNER}\n\n{rest}"
    return f"{BANNER}\n\n{text}"


def render_agent(name: str) -> str:
    src = agent_src(name)
    if not src.is_file():
        sys.exit(f"ERROR: template agent source not found: {src}")
    rendered = rewrite_agent(Template(src.read_text(encoding="utf-8")).render(**CTX))
    return add_banner(rendered)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--plugin-dir",
        type=Path,
        default=REPO_ROOT.parent / "ideal-workflow",
        help="Path to the standalone ideal-workflow plugin (default: ../ideal-workflow).",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Render + compare only; write nothing. Exit 1 if anything is stale.",
    )
    args = parser.parse_args()

    plugin = args.plugin_dir.resolve()
    if not plugin.is_dir():
        sys.exit(f"ERROR: plugin dir not found: {plugin}")

    stale: list[str] = []

    def reconcile(dest: Path, content: str) -> None:
        current = dest.read_text(encoding="utf-8") if dest.exists() else None
        if current == content:
            print(f"  ok    {dest.relative_to(plugin)}")
            return
        if args.check:
            stale.append(str(dest.relative_to(plugin)))
            print(f"  STALE {dest.relative_to(plugin)}")
            return
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")
        print(f"  wrote {dest.relative_to(plugin)}")

    print("Hooks (verbatim + banner):")
    for hook in HOOK_FILES:
        src = hook_src(hook)
        if not src.is_file():
            sys.exit(f"ERROR: template hook source not found: {src}")
        reconcile(plugin / "hooks" / hook, banner_py(src.read_text(encoding="utf-8")))

    print("Agents (rendered + rewritten):")
    for name in AGENT_NAMES:
        reconcile(plugin / "agents" / f"{name}.md", render_agent(name))

    print(
        "\nLeft untouched (plugin-specific, no 1:1 template source): "
        "commands/feature.md, agents/planner.md, agents/reviewer.md, "
        "CONSTITUTION.md, templates/."
    )

    if args.check and stale:
        print(f"\n{len(stale)} file(s) stale. Run without --check to sync.")
        return 1
    print("\nDone.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
