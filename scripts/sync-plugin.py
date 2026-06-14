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
     CONSTITUTION.md, the playbook ref -> PIPELINE.md, role names
     ddd-architect/code-reviewer -> planner/reviewer, `just` -> project
     commands, `.claude/hooks` -> `hooks`).
  3. **The commands** (orchestrator `feature` + the split commands
     `spec`/`plan`/`implement`/`review`/`ship`) are rendered the same way into
     `commands/`. This is the main orchestrator-drift risk.
  4. **The pipeline playbook** is rendered from `feature-pipeline.md.jinja` into
     `PIPELINE.md` (its YAML config front-matter stripped — the plugin keeps
     config in CONSTITUTION.md). It is the single source of phase definitions
     that every command points at.

It deliberately does NOT touch the genuinely plugin-specific files
(planner/reviewer agents, CONSTITUTION.md, templates) — those have no 1:1
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
COMMANDS_DIR = TEMPLATE_PROJECT / ".claude" / "commands"
PLAYBOOK_SRC = (
    TEMPLATE_PROJECT
    / "{{ ai_folder }}"
    / "instructions"
    / "general"
    / "{% if include_feature_pipeline %}feature-pipeline.md{% endif %}.jinja"
)

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
    # True only for this plugin sync — gates plugin-only bits (e.g. the `--init`
    # bootstrap) that generated projects don't need (Copier scaffolds them).
    "plugin_build": True,
}

AGENT_NAMES = ["test-writer", "implementer", "verifier", "debugger", "documenter"]
HOOK_FILES = ["block-locked-tests.py", "autoformat.py"]
COMMAND_NAMES = ["feature", "spec", "plan", "implement", "review", "ship"]

# The plugin names two roles differently than the template does. Same idea as
# SKILL_MAP: structure-preserving token swaps applied during the rewrite.
AGENT_MAP = {
    "ddd-architect": "planner",
    "code-reviewer": "reviewer",
}

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


def command_src(name: str) -> Path:
    return COMMANDS_DIR / (
        "{% if include_feature_pipeline and ai_agent in ['claude', 'universal'] %}"
        + name
        + ".md{% endif %}.jinja"
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
    # Playbook references -> the plugin's shipped PIPELINE.md. Must run BEFORE the
    # generic instructions-tree rule below, which would otherwise route it to
    # CONSTITUTION.md.
    text = re.sub(
        r"`?(?:\$\{CLAUDE_PLUGIN_ROOT\}/|\.claude/)?(?:instructions/general/)?"
        r"feature-pipeline\.md`?",
        "`${CLAUDE_PLUGIN_ROOT}/PIPELINE.md`",
        text,
    )
    # `.claude/skills/<name>/SKILL.md` -> `global:skill`
    text = re.sub(r"`?\.claude/skills/([a-z-]+)/SKILL\.md`?", skill_sub, text)
    # `.claude/instructions/<anything>` -> `CONSTITUTION.md`
    text = re.sub(r"`?\.claude/instructions/[^\s`]+`?", "`CONSTITUTION.md`", text)
    # plugin commands live in commands/, hooks in hooks/ (not under .claude/)
    text = text.replace(".claude/commands/", "commands/")
    text = text.replace(".claude/hooks/", "hooks/")
    # plugin uses different agent names for two roles than the template
    for src_name, dst_name in AGENT_MAP.items():
        text = re.sub(rf"\b{re.escape(src_name)}\b", dst_name, text)
    # test/lint run from CONSTITUTION.md commands, not just recipes
    text = text.replace("`just test`", "the project's test command")
    text = text.replace("`just lint`", "the project's lint command")
    text = text.replace("just test", "the project's test command")
    text = text.replace("just lint", "the project's lint command")
    # Any other `just <recipe>` reference -> a generic phrasing.
    text = re.sub(r"`just [a-z-]+`", "the project's tooling", text)
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


def render_command(name: str) -> str:
    src = command_src(name)
    if not src.is_file():
        sys.exit(f"ERROR: template command source not found: {src}")
    rendered = rewrite_agent(Template(src.read_text(encoding="utf-8")).render(**CTX))
    return add_banner(rendered)


def rewrite_playbook(text: str) -> str:
    """Template playbook -> plugin PIPELINE.md. Drop the YAML config front-matter
    (the plugin keeps config in CONSTITUTION.md), apply the shared rewrites, then
    the playbook's own relative-path forms (`skills/<name>`, `instructions/...`)."""
    text = re.sub(
        r"\A---\n.*?\n---\n",
        "> Pipeline config — loop bound, `plan_grill`, the security gate, and the\n"
        "> test/lint commands — lives in `CONSTITUTION.md` for the plugin.\n",
        text,
        count=1,
        flags=re.DOTALL,
    )
    text = rewrite_agent(text)
    text = re.sub(
        r"`skills/([a-z-]+)`",
        lambda m: "`" + SKILL_MAP.get(m.group(1), m.group(1)) + "`",
        text,
    )
    text = re.sub(r"`instructions/general/[^\s`]+`", "`CONSTITUTION.md`", text)
    # Distinct template skills can collapse to the same global skill (e.g.
    # tdd-cycle + test-driven-development); drop the resulting duplicates in a list.
    text = re.sub(r"(`[^`]+`)(?:, \1)+", r"\1", text)
    return text


def render_playbook() -> str:
    if not PLAYBOOK_SRC.is_file():
        sys.exit(f"ERROR: template playbook source not found: {PLAYBOOK_SRC}")
    rendered = rewrite_playbook(Template(PLAYBOOK_SRC.read_text(encoding="utf-8")).render(**CTX))
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

    print("Commands (rendered + rewritten):")
    for name in COMMAND_NAMES:
        reconcile(plugin / "commands" / f"{name}.md", render_command(name))

    print("Playbook (rendered + stripped):")
    reconcile(plugin / "PIPELINE.md", render_playbook())

    print(
        "\nLeft untouched (plugin-specific, no 1:1 template source): "
        "agents/planner.md, agents/reviewer.md, CONSTITUTION.md, templates/."
    )

    if args.check and stale:
        print(f"\n{len(stale)} file(s) stale. Run without --check to sync.")
        return 1
    print("\nDone.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
