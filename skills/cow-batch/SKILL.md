---
name: cow-batch
description: Batch ingest new or changed raw files into a Codex Obsidian Wiki. Use when the user types cow batch, asks to ingest raw/, batch process raw materials, or reprocess changed sources with the cow workflow.
---

# Cow Batch

Use `codex-obsidian-llm-wiki` for the full workflow.

Process files under `raw/`. Use the main skill's cache helper:

```bash
python scripts/cache.py check <raw-file>
python scripts/cache.py update <raw-file> <source-page>
```

Skip unchanged files. After batch ingest, run lint and update `log.md`.

