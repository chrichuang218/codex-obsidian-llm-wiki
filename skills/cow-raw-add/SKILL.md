---
name: cow-raw-add
description: Add files or folders into a Codex Obsidian Wiki raw directory without creating knowledge pages. Use when the user types cow raw add, asks to add/copy/import a file or folder into raw/, choose or create a raw subfolder, sanitize material before raw storage, or stage material for later cow batch processing.
---

# Cow Raw Add

Add source material to `raw/` only. Do not create `wiki/sources/`, `wiki/topics/`, or `wiki/entities/`.

Use the main `codex-obsidian-llm-wiki` skill for the directory contract and cache rules.

## Workflow

1. Read `<wiki-root>/.wiki-schema.md`, `purpose.md`, and `index.md` when present.
2. Inspect `<wiki-root>/raw/` one level deep before choosing a target.
3. Choose a target:
   - `raw/notes/` for single notes, debug records, meeting notes, and small Markdown/text files.
   - `raw/articles/<slug>/` for long articles, article bundles, exported web pages, or multi-file source folders.
   - `raw/pdfs/` for PDF files.
   - `raw/assets/` for images or supporting binary assets.
   - create a clear new subfolder such as `raw/configs/` or `raw/reports/` only when existing folders do not fit.
4. Check for secrets, account identifiers, private paths, API keys, tokens, or other sensitive personal data. If present, write a sanitized copy and prefer a `.sanitized` filename.
5. Avoid overwriting existing raw files; use a slug or numeric suffix.
6. Update `.wiki-cache.json` for the added raw file(s) with an empty `source_page`; this marks the file as staged but not yet ingested.
7. Append a short entry to `log.md`.
8. Run the most relevant validation: cache JSON parse plus `cow lint` / `lint_wiki.py` when practical.

## Helper Script

Prefer the bundled helper when available:

```bash
python scripts/raw_add.py <source> <wiki-root> --section notes
python scripts/raw_add.py <source-folder> <wiki-root> --section articles --name my-source
python scripts/raw_add.py <source> <wiki-root> --section notes --sanitize
```

Use `--sanitize` when the source contains credentials or private machine paths. Use `--allow-sensitive` only when the user explicitly wants the raw file copied as-is.

After raw add, tell the user that `cow batch <wiki-root>` can digest the staged raw material later.
