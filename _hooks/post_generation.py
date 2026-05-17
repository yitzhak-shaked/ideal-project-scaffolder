"""
Post-generation cleanup for the project scaffolder.

Walks the rendered project tree and:
  1. Renames any empty directory (or one containing only `.gitkeep`)
     to `_<name>/` so it is visibly inert until something is added.
  2. Removes the `.gitkeep` sentinels it relied on for that detection.

Invoked by Copier's `_tasks:` hook with:
    python post_generation.py <dst_path> <ai_agent> <agent_file_style>

ai_agent / agent_file_style are reserved for future use (e.g. moving
.ai/skills/ into .claude/skills/ for canonical Claude projects). They
are currently consumed but unused.
"""
from __future__ import annotations

import os
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
    import shutil

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
    if len(sys.argv) < 2:
        print("usage: post_generation.py <dst_path> [ai_agent] [agent_file_style]", file=sys.stderr)
        return 2
    dst = Path(sys.argv[1]).resolve()
    if not dst.is_dir():
        print(f"destination not found: {dst}", file=sys.stderr)
        return 2

    underscore_empty_dirs(dst)
    strip_gitkeeps_from_populated_dirs(dst)
    prune_empty_hidden_top_level_dirs(dst)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
