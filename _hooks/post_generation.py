"""
Post-generation cleanup for the project scaffolder.

Copier renders everything into <dst>/<project_slug>/ (so the user's chosen
project name becomes the new folder, regardless of what destination they
passed on the CLI). Copier sets the task's cwd to <dst>, so the hook
takes <project_slug> as its single argument and treats <cwd>/<slug>/ as
the project root.

The script:
  1. Removes `.gitkeep` sentinels from any directory that now has real
     content.
  2. Prunes top-level hidden dirs (.claude/, .github/, ...) that ended up
     with no real content because every conditional inside them skipped.
  3. Prunes empty *optional* dirs (the per-language instruction folders
     and per-skill folders) so an unselected language leaves no
     `_python/`-style artifact behind. A dir containing only `.gitkeep`
     is also considered empty (these sentinels are placed in language
     dirs so Copier always creates the directory even when all filenames
     are conditional).

Invoked as:
    python post_generation.py <project_slug>
"""
from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path


SENTINEL = ".gitkeep"


def is_effectively_empty(directory: Path) -> bool:
    entries = list(directory.iterdir())
    if not entries:
        return True
    return len(entries) == 1 and entries[0].name == SENTINEL


def strip_gitkeeps_from_populated_dirs(root: Path) -> None:
    # Any directory that ended up with real content alongside its .gitkeep
    # sentinel no longer needs the sentinel -- remove it.
    for sentinel in root.rglob(SENTINEL):
        parent = sentinel.parent
        if any(e.name != SENTINEL for e in parent.iterdir()):
            sentinel.unlink()


def has_any_file(directory: Path) -> bool:
    for entry in directory.rglob("*"):
        if entry.is_file():
            return True
    return False


# Parent dirs whose children are feature-gated: when a child ends up empty
# (the language / skill was not selected) the dir is *deleted*, not kept as
# an underscore-prefixed placeholder. Matched by directory name anywhere in
# the tree (e.g. .claude/instructions/, .ai/skills/).
#
# A child is considered empty when it has no files at all OR contains only a
# .gitkeep sentinel. The sentinel is placed in each language instruction dir
# so Copier unconditionally creates the directory; when the language is not
# selected, only the sentinel remains and the whole dir is pruned here.
OPTIONAL_PARENT_DIRS = {"instructions", "skills"}


def prune_empty_optional_dirs(root: Path) -> None:
    # Bottom-up so a pruned child can let its parent be pruned too.
    for current_root, dir_names, _ in os.walk(root, topdown=False):
        current = Path(current_root)
        rel_parts = current.relative_to(root).parts
        if rel_parts and rel_parts[0] == ".git":
            continue
        if current.name not in OPTIONAL_PARENT_DIRS:
            continue
        for dir_name in dir_names:
            child = current / dir_name
            if child.is_dir() and is_effectively_empty(child):
                shutil.rmtree(child)


def prune_skill_dirs_missing_skill_md(root: Path) -> None:
    # Vendored Tier-2 skills gate their SKILL.md filename behind a Copier
    # conditional. When the flag is off the SKILL.md is not rendered, but
    # any support files (`*-prompt.md`, scripts/, etc.) still get copied,
    # leaving a half-vendored skill directory. Such a directory is
    # functionally useless (no SKILL.md means Claude Code can't discover
    # the skill), so wipe it.
    for skills_dir in root.rglob("skills"):
        if not skills_dir.is_dir():
            continue
        rel_parts = skills_dir.relative_to(root).parts
        if rel_parts and rel_parts[0] == ".git":
            continue
        for child in skills_dir.iterdir():
            if not child.is_dir():
                continue
            if not (child / "SKILL.md").exists():
                shutil.rmtree(child)


def prune_empty_hidden_top_level_dirs(root: Path) -> None:
    # Top-level dotted dirs (.claude, .github, .vscode, .ai...) exist because
    # a path under them was templated. If the conditional skipped every leaf,
    # the dir is left as a hollow shell -- delete it rather than show garbage.
    for entry in root.iterdir():
        if not entry.is_dir():
            continue
        if not entry.name.startswith("."):
            continue
        if entry.name == ".git":
            continue
        if not has_any_file(entry):
            shutil.rmtree(entry)


def main() -> int:
    if len(sys.argv) < 2 or not sys.argv[1]:
        print("usage: post_generation.py <project_slug>", file=sys.stderr)
        return 2
    root = Path.cwd() / sys.argv[1]
    if not root.is_dir():
        print(f"project root not found: {root}", file=sys.stderr)
        return 2
    prune_skill_dirs_missing_skill_md(root)
    prune_empty_optional_dirs(root)
    strip_gitkeeps_from_populated_dirs(root)
    prune_empty_hidden_top_level_dirs(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
