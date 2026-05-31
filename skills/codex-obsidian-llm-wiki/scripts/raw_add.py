#!/usr/bin/env python3
"""Add external files or folders to a Codex Obsidian Wiki raw directory."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".json",
    ".jsonl",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".env",
    ".ps1",
    ".sh",
    ".py",
    ".js",
    ".ts",
    ".html",
    ".css",
}

SENSITIVE_PATTERNS = [
    re.compile(r"\bsk-[A-Za-z0-9_-]{8,}\b"),
    re.compile(r"(?i)(api[-_ ]?key\s*[:=]\s*[\"']?)([^\"'\s]+)"),
    re.compile(r"(?i)(authorization\s*[:=]\s*[\"']?bearer\s+)([^\"'\s]+)"),
    re.compile(r"(?i)(token\s*[:=]\s*[\"']?)([^\"'\s]+)"),
]


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9._\-\u4e00-\u9fff]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-._")
    return value or "source"


def is_text(path: Path) -> bool:
    return path.suffix.lower() in TEXT_SUFFIXES


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def has_sensitive_text(text: str) -> bool:
    return any(pattern.search(text) for pattern in SENSITIVE_PATTERNS)


def sanitize_text(text: str) -> str:
    text = re.sub(r"\bsk-[A-Za-z0-9_-]{8,}\b", "<REDACTED_API_KEY>", text)
    text = re.sub(r"(?i)(api[-_ ]?key\s*[:=]\s*[\"']?)([^\"'\s]+)", r"\1<REDACTED_API_KEY>", text)
    text = re.sub(r"(?i)(authorization\s*[:=]\s*[\"']?bearer\s+)([^\"'\s]+)", r"\1<REDACTED_TOKEN>", text)
    text = re.sub(r"(?i)(token\s*[:=]\s*[\"']?)([^\"'\s]+)", r"\1<REDACTED_TOKEN>", text)
    return text


def load_cache(root: Path) -> dict[str, Any]:
    cache_path = root / ".wiki-cache.json"
    if not cache_path.exists():
        return {"version": 1, "entries": {}}
    return json.loads(cache_path.read_text(encoding="utf-8"))


def save_cache(root: Path, data: dict[str, Any]) -> None:
    (root / ".wiki-cache.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def rel(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def source_hash(root: Path, source: Path) -> str:
    source_rel = rel(root, source).encode("utf-8")
    digest = hashlib.sha256(source_rel + b"\0" + source.read_bytes()).hexdigest()
    return f"sha256:{digest}"


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    index = 2
    while True:
        candidate = parent / f"{stem}-{index}{suffix}"
        if not candidate.exists():
            return candidate
        index += 1


def target_base(source: Path, root: Path, section: str, name: str | None) -> Path:
    raw_root = root / "raw"
    section_dir = raw_root / slugify(section)
    if source.is_dir():
        return unique_path(section_dir / slugify(name or source.name))
    filename = source.name
    if name:
        filename = slugify(name) + source.suffix
    return unique_path(section_dir / filename)


def copy_file(source: Path, target: Path, sanitize: bool, allow_sensitive: bool) -> Path:
    target.parent.mkdir(parents=True, exist_ok=True)
    if is_text(source):
        text = read_text(source)
        sensitive = has_sensitive_text(text)
        if sensitive and not sanitize and not allow_sensitive:
            raise SystemExit(f"Refusing to copy possible sensitive text without --sanitize or --allow-sensitive: {source}")
        if sanitize:
            text = sanitize_text(text)
            if sensitive and target.suffix.lower() == source.suffix.lower() and ".sanitized" not in target.stem:
                target = target.with_name(f"{target.stem}.sanitized{target.suffix}")
                target = unique_path(target)
            target.write_text(text, encoding="utf-8")
            return target
    shutil.copy2(source, target)
    return target


def copy_source(source: Path, target: Path, sanitize: bool, allow_sensitive: bool) -> list[Path]:
    copied: list[Path] = []
    if source.is_file():
        copied.append(copy_file(source, target, sanitize, allow_sensitive))
        return copied
    target.mkdir(parents=True, exist_ok=True)
    for item in source.rglob("*"):
        if not item.is_file():
            continue
        relative = item.relative_to(source)
        copied.append(copy_file(item, unique_path(target / relative), sanitize, allow_sensitive))
    return copied


def update_cache(root: Path, copied: list[Path]) -> None:
    data = load_cache(root)
    entries = data.setdefault("entries", {})
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    for file_path in copied:
        entries[rel(root, file_path)] = {
            "hash": source_hash(root, file_path),
            "ingested_at": timestamp,
            "source_page": "",
        }
    save_cache(root, data)


def append_log(root: Path, source: Path, copied: list[Path], sanitized: bool) -> None:
    log_path = root / "log.md"
    if not log_path.exists():
        return
    today = datetime.now().strftime("%Y-%m-%d")
    lines = [
        "",
        f"## {today} raw-add | Add raw material",
        "",
        f"- Source: `{source}`.",
        f"- Added {len(copied)} file(s) under `raw/`.",
    ]
    if sanitized:
        lines.append("- Sanitization: enabled.")
    for file_path in copied[:10]:
        lines.append(f"- `{rel(root, file_path)}`")
    if len(copied) > 10:
        lines.append(f"- ... and {len(copied) - 10} more file(s).")
    log_path.write_text(log_path.read_text(encoding="utf-8").rstrip() + "\n" + "\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Add files or folders to a wiki raw directory.")
    parser.add_argument("source")
    parser.add_argument("wiki_root")
    parser.add_argument("--section", default="notes", help="raw subdirectory, e.g. notes, articles, pdfs, assets, configs")
    parser.add_argument("--name", help="target file stem or folder name")
    parser.add_argument("--sanitize", action="store_true", help="sanitize supported text files before writing")
    parser.add_argument("--allow-sensitive", action="store_true", help="copy possible sensitive text without sanitizing")
    args = parser.parse_args(argv[1:])

    source = Path(args.source).expanduser().resolve()
    root = Path(args.wiki_root).expanduser().resolve()
    if not source.exists():
        print(f"Source does not exist: {source}", file=sys.stderr)
        return 2
    if not (root / ".wiki-schema.md").exists():
        print(f"Wiki root does not look valid: {root}", file=sys.stderr)
        return 2

    target = target_base(source, root, args.section, args.name)
    copied = copy_source(source, target, args.sanitize, args.allow_sensitive)
    update_cache(root, copied)
    append_log(root, source, copied, args.sanitize)
    for file_path in copied:
        print(rel(root, file_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
