#!/usr/bin/env python3
"""Source cache for Codex Obsidian LLM Wiki."""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def find_wiki_root(path: Path) -> Path:
    current = path if path.is_dir() else path.parent
    for candidate in [current, *current.parents]:
        if (candidate / ".wiki-cache.json").exists() or (candidate / ".wiki-schema.md").exists():
            return candidate
    raise SystemExit(f"Cannot find wiki root from: {path}")


def load_cache(root: Path) -> dict[str, Any]:
    cache_path = root / ".wiki-cache.json"
    if not cache_path.exists():
        return {"version": 1, "entries": {}}
    return json.loads(cache_path.read_text(encoding="utf-8"))


def save_cache(root: Path, data: dict[str, Any]) -> None:
    cache_path = root / ".wiki-cache.json"
    cache_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def rel(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def source_hash(root: Path, source: Path) -> str:
    source_rel = rel(root, source).encode("utf-8")
    digest = hashlib.sha256(source_rel + b"\0" + source.read_bytes()).hexdigest()
    return f"sha256:{digest}"


def cmd_check(source_arg: str) -> int:
    source = Path(source_arg).expanduser().resolve()
    if not source.exists():
        print(f"MISS:not_found {source}")
        return 1
    root = find_wiki_root(source)
    data = load_cache(root)
    source_rel = rel(root, source)
    entry = data.get("entries", {}).get(source_rel)
    if not entry:
        print(f"MISS:no_entry {source_rel}")
        return 1
    if entry.get("hash") != source_hash(root, source):
        print(f"MISS:hash_changed {source_rel}")
        return 1
    source_page = entry.get("source_page", "")
    if source_page and not (root / source_page).exists():
        print(f"MISS:no_source_page {source_rel} -> {source_page}")
        return 1
    print(f"HIT {source_rel} -> {source_page}")
    return 0


def cmd_update(source_arg: str, source_page_arg: str) -> int:
    source = Path(source_arg).expanduser().resolve()
    if not source.exists():
        print(f"Source does not exist: {source}", file=sys.stderr)
        return 2
    root = find_wiki_root(source)
    source_page = Path(source_page_arg)
    source_page_rel = source_page.as_posix()
    if source_page.is_absolute():
        source_page_rel = rel(root, source_page.resolve())
    data = load_cache(root)
    data.setdefault("entries", {})[rel(root, source)] = {
        "hash": source_hash(root, source),
        "ingested_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_page": source_page_rel,
    }
    save_cache(root, data)
    print(f"UPDATED {rel(root, source)} -> {source_page_rel}")
    return 0


def cmd_list(root_arg: str) -> int:
    root = Path(root_arg).expanduser().resolve()
    data = load_cache(root)
    entries = data.get("entries", {})
    if not entries:
        print("EMPTY")
        return 0
    for source_rel, entry in sorted(entries.items()):
        print(f"{source_rel}\t{entry.get('source_page', '')}\t{entry.get('ingested_at', '')}")
    return 0


def cmd_stale(root_arg: str) -> int:
    root = Path(root_arg).expanduser().resolve()
    data = load_cache(root)
    stale = 0
    for source_rel, entry in sorted(data.get("entries", {}).items()):
        source = root / source_rel
        reason = ""
        if not source.exists():
            reason = "missing_raw"
        elif entry.get("hash") != source_hash(root, source):
            reason = "hash_changed"
        elif entry.get("source_page") and not (root / entry["source_page"]).exists():
            reason = "missing_source_page"
        if reason:
            stale += 1
            print(f"STALE:{reason} {source_rel}")
    if stale == 0:
        print("OK no stale entries")
    return 0 if stale == 0 else 1


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: cache.py check <raw-file> | update <raw-file> <source-page> | list <wiki-root> | stale <wiki-root>", file=sys.stderr)
        return 2
    command = argv[1]
    if command == "check" and len(argv) == 3:
        return cmd_check(argv[2])
    if command == "update" and len(argv) == 4:
        return cmd_update(argv[2], argv[3])
    if command == "list" and len(argv) == 3:
        return cmd_list(argv[2])
    if command == "stale" and len(argv) == 3:
        return cmd_stale(argv[2])
    print("Usage: cache.py check <raw-file> | update <raw-file> <source-page> | list <wiki-root> | stale <wiki-root>", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

