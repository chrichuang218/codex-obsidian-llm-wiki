---
name: cow-ingest
description: Ingest one source into a Codex Obsidian Wiki. Use when the user types cow ingest, asks to整理/消化/import/ingest a file, folder, URL, pasted note, PDF, article, or raw material into an Obsidian-compatible Markdown wiki.
---

# Cow Ingest

Use `codex-obsidian-llm-wiki` for the full ingest workflow.

Follow the main skill's two-step ingest:

1. Analyze source type, claims, entities, topics, target pages, conflicts, and review items.
2. Write durable pages under `wiki/sources/`, `wiki/topics/`, `wiki/entities/`, update `index.md`, `.wiki-cache.json`, and `log.md`.

Do not invent missing facts. Put uncertain items in `wiki/review/`.

