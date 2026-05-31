#!/usr/bin/env python3
"""Mechanical health checks for a Codex Obsidian LLM Wiki."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED_DIRS = [
    "raw",
    "wiki/sources",
    "wiki/topics",
    "wiki/entities",
    "wiki/comparisons",
    "wiki/synthesis",
    "wiki/queries",
    "wiki/review",
]

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")


def page_names(wiki_dir: Path) -> set[str]:
    return {p.stem for p in wiki_dir.rglob("*.md")}


def lint(root: Path) -> int:
    issues = 0
    wiki_dir = root / "wiki"
    index_path = root / "index.md"

    for rel in REQUIRED_DIRS:
        if not (root / rel).exists():
            print(f"MISSING_DIR {rel}")
            issues += 1

    for rel in [".wiki-schema.md", "purpose.md", "index.md", "log.md", ".wiki-cache.json"]:
        if not (root / rel).exists():
            print(f"MISSING_FILE {rel}")
            issues += 1

    if not wiki_dir.exists():
        return issues or 1

    names = page_names(wiki_dir)
    broken = []
    inbound: dict[str, int] = {name: 0 for name in names}

    for md in wiki_dir.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        for link in WIKILINK_RE.findall(text):
            target = link.strip()
            if target not in names:
                broken.append((md.relative_to(root), target))
            else:
                inbound[target] = inbound.get(target, 0) + 1

    if broken:
        for source, target in broken:
            print(f"BROKEN_LINK {source} -> [[{target}]]")
        issues += len(broken)

    index_text = index_path.read_text(encoding="utf-8") if index_path.exists() else ""
    for md in wiki_dir.rglob("*.md"):
        if "wiki/queries" in md.as_posix() or "wiki/review" in md.as_posix():
            continue
        name = md.stem
        if name != "overview" and f"[[{name}]]" not in index_text:
            print(f"NOT_IN_INDEX {md.relative_to(root)}")
            issues += 1

    for name, count in sorted(inbound.items()):
        if name == "overview":
            continue
        if count == 0:
            print(f"ORPHAN_PAGE {name}")
            issues += 1

    if issues == 0:
        print("OK wiki is healthy")
    else:
        print(f"FOUND {issues} issue(s)")
    return 0 if issues == 0 else 1


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: lint_wiki.py <wiki-root>", file=sys.stderr)
        return 2
    return lint(Path(sys.argv[1]).expanduser().resolve())


if __name__ == "__main__":
    raise SystemExit(main())

