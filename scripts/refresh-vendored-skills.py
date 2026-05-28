"""
Refresh the vendored superpowers skills inside the scaffolder template.

Reads the pinned `superpowers_skills_tag` value from copier.yml, fetches
(or reuses) a clone of `obra/superpowers-skills` at that tag, and copies
the curated Tier-1 / Tier-2 skill directories into
`template/{{ project_slug }}/{{ ai_folder }}/skills/`.

Tier 1 (always rendered, no conditional in filename):
  test-driven-development, systematic-debugging,
  verification-before-completion, writing-plans, executing-plans,
  requesting-code-review, receiving-code-review, writing-skills,
  finishing-a-development-branch

Tier 2 (Copier filename-conditional gates the SKILL.md):
  brainstorming            -> {% raw %}{% if include_brainstorming %}SKILL.md{% endif %}.jinja{% endraw %}
  using-git-worktrees      -> {% raw %}{% if enable_worktrees %}SKILL.md{% endif %}.jinja{% endraw %}
  dispatching-parallel-agents
  subagent-driven-development
                           -> {% raw %}{% if enable_parallel_agents %}SKILL.md{% endif %}.jinja{% endraw %}

The script does not commit. Review the diff and commit manually.

Usage:
  python scripts/refresh-vendored-skills.py [--source <path>]

If `--source` is omitted, the script clones the upstream repo into a
temp dir. If a local path is given (e.g. an existing checkout or the
plugin cache at `~/.claude/plugins/cache/.../superpowers/<ver>`),
the script reads skills from there instead.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
COPIER_YML = REPO_ROOT / "copier.yml"
TEMPLATE_SKILLS_DIR = (
    REPO_ROOT / "template" / "{{ project_slug }}" / "{{ ai_folder }}" / "skills"
)
ATTRIBUTION_FILE = (
    REPO_ROOT
    / "template"
    / "{{ project_slug }}"
    / "{{ ai_folder }}"
    / "skills"
    / "ATTRIBUTION.md.jinja"
)
UPSTREAM_URL = "https://github.com/obra/superpowers-skills.git"

# Tier 1: always rendered, plain SKILL.md.jinja filename.
TIER_1 = [
    "test-driven-development",
    "systematic-debugging",
    "verification-before-completion",
    "writing-plans",
    "executing-plans",
    "requesting-code-review",
    "receiving-code-review",
    "writing-skills",
    "finishing-a-development-branch",
]

# Tier 2: filename is Copier-conditional on a quiz variable.
TIER_2: dict[str, str] = {
    "brainstorming": "include_brainstorming",
    "using-git-worktrees": "enable_worktrees",
    "dispatching-parallel-agents": "enable_parallel_agents",
    "subagent-driven-development": "enable_parallel_agents",
}


def read_pinned_tag() -> str:
    text = COPIER_YML.read_text(encoding="utf-8")
    # Naive parse: find the `superpowers_skills_tag:` block and pluck its default.
    match = re.search(
        r"^superpowers_skills_tag:\s*\n(?:.*\n)*?\s*default:\s*\"([^\"]+)\"",
        text,
        re.MULTILINE,
    )
    if not match:
        sys.exit(
            "ERROR: could not find superpowers_skills_tag default in copier.yml"
        )
    return match.group(1)


def find_skills_root(source_root: Path) -> Path:
    """The skills directory inside either a superpowers-skills checkout or the
    plugin cache. Both layouts expose `<root>/skills/<skill-name>/SKILL.md`."""
    candidate = source_root / "skills"
    if candidate.is_dir():
        return candidate
    # Some checkouts may put skills at the root. Fall back to that.
    if (source_root / "SKILL.md").exists() or any(
        (source_root / name).is_dir() for name in TIER_1 + list(TIER_2)
    ):
        return source_root
    sys.exit(f"ERROR: could not locate a skills/ directory under {source_root}")


def clone_upstream(tag: str, dest: Path) -> Path:
    subprocess.run(
        [
            "git",
            "clone",
            "--depth",
            "1",
            "--branch",
            tag,
            UPSTREAM_URL,
            str(dest),
        ],
        check=True,
    )
    return dest


def copy_skill_dir(source_skill_dir: Path, dest_skill_dir: Path, skill_filename: str) -> None:
    """Copy a skill directory. SKILL.md takes the (possibly conditional)
    `skill_filename`; supporting files keep their names without `.jinja`."""
    if dest_skill_dir.exists():
        shutil.rmtree(dest_skill_dir)
    dest_skill_dir.mkdir(parents=True)
    for entry in source_skill_dir.iterdir():
        if entry.name == "SKILL.md":
            # Wrap body in {% raw %} to keep any incidental `{{` / `{%` in
            # upstream content from breaking Jinja rendering.
            body = entry.read_text(encoding="utf-8")
            wrapped = "{% raw %}\n" + body.rstrip() + "\n{% endraw %}\n"
            (dest_skill_dir / skill_filename).write_text(wrapped, encoding="utf-8")
        elif entry.is_file():
            # Support files (e.g. testing-anti-patterns.md) — copy verbatim,
            # no .jinja extension so Copier doesn't try to render them.
            (dest_skill_dir / entry.name).write_text(
                entry.read_text(encoding="utf-8"), encoding="utf-8"
            )
        elif entry.is_dir():
            shutil.copytree(entry, dest_skill_dir / entry.name)


def write_attribution(tag: str, vendored: list[str]) -> None:
    body_lines = [
        "# Vendored skills attribution",
        "",
        f"This directory contains skills vendored from",
        f"[obra/superpowers-skills](https://github.com/obra/superpowers-skills)",
        f"at tag `{tag}`.",
        "",
        "Original work is MIT-licensed. The MIT terms are reproduced below.",
        "Modifications: each SKILL.md body has been wrapped in `{% raw %}` /",
        "`{% endraw %}` so the Copier templating engine treats it as literal",
        "content. No semantic changes.",
        "",
        "## Vendored skills",
        "",
    ]
    for name in vendored:
        body_lines.append(f"- `{name}/`")
    body_lines.extend(
        [
            "",
            "## Upstream license",
            "",
            "```",
            "MIT License",
            "",
            "Copyright (c) Jesse Vincent and the superpowers-skills contributors",
            "",
            "Permission is hereby granted, free of charge, to any person obtaining a copy",
            "of this software and associated documentation files (the \"Software\"), to deal",
            "in the Software without restriction, including without limitation the rights",
            "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell",
            "copies of the Software, and to permit persons to whom the Software is",
            "furnished to do so, subject to the following conditions:",
            "",
            "The above copyright notice and this permission notice shall be included in all",
            "copies or substantial portions of the Software.",
            "",
            "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR",
            "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,",
            "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE",
            "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER",
            "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,",
            "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE",
            "SOFTWARE.",
            "```",
        ]
    )
    ATTRIBUTION_FILE.write_text("\n".join(body_lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        type=Path,
        help=(
            "Path to a local superpowers-skills checkout or the plugin "
            "cache directory. If omitted, the upstream repo is cloned at "
            "the pinned tag."
        ),
    )
    args = parser.parse_args()

    tag = read_pinned_tag()
    print(f"Pinned tag: {tag}")

    if args.source:
        source_root = args.source
        if not source_root.is_dir():
            sys.exit(f"ERROR: --source {source_root} does not exist")
        print(f"Reading from local source: {source_root}")
        skills_root = find_skills_root(source_root)
        cleanup_dir: Path | None = None
    else:
        cleanup_dir = Path(tempfile.mkdtemp(prefix="superpowers-skills-"))
        print(f"Cloning {UPSTREAM_URL}@{tag} into {cleanup_dir}")
        clone_upstream(tag, cleanup_dir)
        skills_root = find_skills_root(cleanup_dir)

    vendored: list[str] = []
    try:
        TEMPLATE_SKILLS_DIR.mkdir(parents=True, exist_ok=True)

        # Tier 1
        for name in TIER_1:
            src = skills_root / name
            if not src.is_dir():
                print(f"WARNING: Tier 1 skill {name!r} not found in source; skipping")
                continue
            dst = TEMPLATE_SKILLS_DIR / name
            copy_skill_dir(src, dst, "SKILL.md.jinja")
            vendored.append(name)
            print(f"  vendored Tier 1: {name}")

        # Tier 2
        for name, flag in TIER_2.items():
            src = skills_root / name
            if not src.is_dir():
                print(f"WARNING: Tier 2 skill {name!r} not found in source; skipping")
                continue
            dst = TEMPLATE_SKILLS_DIR / name
            filename = f"{{% if {flag} %}}SKILL.md{{% endif %}}.jinja"
            copy_skill_dir(src, dst, filename)
            vendored.append(name)
            print(f"  vendored Tier 2: {name} (gated by {flag})")

        write_attribution(tag, vendored)
        print(f"\nWrote attribution to {ATTRIBUTION_FILE}")
        print(f"Vendored {len(vendored)} skills.")
    finally:
        if cleanup_dir is not None:
            shutil.rmtree(cleanup_dir, ignore_errors=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
