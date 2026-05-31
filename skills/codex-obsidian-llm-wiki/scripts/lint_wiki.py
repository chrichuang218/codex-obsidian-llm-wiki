#!/usr/bin/env python3
"""Mechanical health checks for a Codex Obsidian LLM Wiki."""

from __future__ import annotations

import re
import sys
from collections import defaultdict
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
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def page_map(wiki_dir: Path) -> dict[str, list[Path]]:
    pages: dict[str, list[Path]] = defaultdict(list)
    for page in wiki_dir.rglob("*.md"):
        pages[page.stem].append(page)
    return dict(pages)


def read_frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    data: dict[str, object] = {}
    current_key = ""
    for raw_line in match.group(1).splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            continue
        if line.startswith("  - ") and current_key:
            data.setdefault(current_key, [])
            if isinstance(data[current_key], list):
                data[current_key].append(line[4:].strip().strip('"').strip("'"))
            continue
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            current_key = key.strip()
            value = value.strip()
            if value == "[]":
                data[current_key] = []
            elif value.startswith("[") and value.endswith("]"):
                items = [item.strip().strip('"').strip("'") for item in value[1:-1].split(",") if item.strip()]
                data[current_key] = items
            elif value:
                data[current_key] = value.strip('"').strip("'")
            else:
                data[current_key] = []
    return data


def list_value(frontmatter: dict[str, object], key: str) -> list[str]:
    value = frontmatter.get(key)
    if isinstance(value, list):
        return [str(item) for item in value if str(item)]
    if isinstance(value, str) and value:
        return [value]
    return []


def lint(root: Path) -> int:
    issues = 0
    warnings = 0
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

    pages = page_map(wiki_dir)
    names = set(pages)
    broken = []
    inbound: dict[str, int] = {name: 0 for name in names}

    for name, paths in sorted(pages.items()):
        if len(paths) > 1:
            joined = ", ".join(str(path.relative_to(root)) for path in paths)
            print(f"DUPLICATE_PAGE_NAME {name}: {joined}")
            issues += 1

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
        paths = pages.get(name, [])
        if all("wiki/review" in path.as_posix() or "wiki/queries" in path.as_posix() for path in paths):
            continue
        if count == 0:
            print(f"ORPHAN_PAGE {name}")
            issues += 1

    for source_page in (wiki_dir / "sources").glob("*.md"):
        fm = read_frontmatter(source_page)
        source_path = fm.get("source_path")
        if not source_path or not isinstance(source_path, str):
            print(f"MISSING_SOURCE_PATH {source_page.relative_to(root)}")
            issues += 1
            continue
        if not (root / source_path).exists():
            print(f"MISSING_RAW_SOURCE {source_page.relative_to(root)} -> {source_path}")
            issues += 1

    for section in ["topics", "entities", "comparisons", "synthesis"]:
        section_dir = wiki_dir / section
        for page in section_dir.glob("*.md"):
            if page.name == "overview.md":
                continue
            fm = read_frontmatter(page)
            sources = list_value(fm, "sources")
            if not sources:
                print(f"MISSING_SOURCES {page.relative_to(root)}")
                issues += 1
                continue
            for source_ref in sources:
                if source_ref.startswith("raw/") or source_ref.startswith("wiki/"):
                    if not (root / source_ref).exists():
                        print(f"MISSING_SOURCE_REF {page.relative_to(root)} -> {source_ref}")
                        issues += 1

    review_files = [p for p in (wiki_dir / "review").glob("*.md")]
    if review_files:
        print(f"WARN_OPEN_REVIEW_ITEMS {len(review_files)}")
        warnings += len(review_files)

    cache_path = root / ".wiki-cache.json"
    if cache_path.exists():
        cache_text = cache_path.read_text(encoding="utf-8")
        if '"entries"' not in cache_text:
            print("INVALID_CACHE missing entries")
            issues += 1

    if issues == 0 and warnings == 0:
        print("OK wiki is healthy")
    elif issues == 0:
        print(f"OK wiki is healthy with {warnings} warning(s)")
    else:
        suffix = f" and {warnings} warning(s)" if warnings else ""
        print(f"FOUND {issues} issue(s){suffix}")
    return 0 if issues == 0 else 1


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: lint_wiki.py <wiki-root>", file=sys.stderr)
        return 2
    return lint(Path(sys.argv[1]).expanduser().resolve())


if __name__ == "__main__":
    raise SystemExit(main())
