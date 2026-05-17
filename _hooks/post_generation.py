"""
Post-generation cleanup for the project scaffolder.

Copier renders everything into <dst>/<project_slug>/ (so the user's chosen
project name becomes the new folder, regardless of what destination they
passed on the CLI). Copier sets the task's cwd to <dst>, so the hook
takes <project_slug> as its single argument and treats <cwd>/<slug>/ as
the project root.

The script:
  1. Renames empty directories (or those holding only `.gitkeep`) to
     `_<name>/` so they're visibly inert until something is added.
  2. Removes `.gitkeep` sentinels from any directory that now has real
     content.
  3. Prunes top-level hidden dirs (.claude/, .github/, …) that ended up
     with no real content because every conditional inside them skipped.

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


def underscore_empty_dirs(root: Path) -> None:
    # Walk bottom-up so renaming a parent does not invalidate child paths.
    for current_root, dir_names, _ in os.walk(root, topdown=False):
        current = Path(current_root)
        # Skip everything under .git.
        rel_parts = current.relative_to(root).parts
        if rel_parts and rel_parts[0] == ".git":
            continue

        for dir_name in dir_names:
            child = current / dir_name
            if not child.is_dir():
                continue
            if dir_name.startswith("_") or dir_name.startswith("."):
                continue
            if is_effectively_empty(child):
                sentinel = child / SENTINEL
                if sentinel.exists():
                    sentinel.unlink()
                target = current / f"_{dir_name}"
                if not target.exists():
                    child.rename(target)


def strip_gitkeeps_from_populated_dirs(root: Path) -> None:
    # Any directory that ended up with real content alongside its .gitkeep
    # sentinel no longer needs the sentinel — remove it.
    for sentinel in root.rglob(SENTINEL):
        parent = sentinel.parent
        if any(e.name != SENTINEL for e in parent.iterdir()):
            sentinel.unlink()


def has_any_file(directory: Path) -> bool:
    for entry in directory.rglob("*"):
        if entry.is_file():
            return True
    return False


def prune_empty_hidden_top_level_dirs(root: Path) -> None:
    # Top-level dotted dirs (.claude, .github, .vscode, .ai...) exist because
    # a path under them was templated. If the conditional skipped every leaf,
    # the dir is left as a hollow shell — delete it rather than show garbage.
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
    underscore_empty_dirs(root)
    strip_gitkeeps_from_populated_dirs(root)
    prune_empty_hidden_top_level_dirs(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
