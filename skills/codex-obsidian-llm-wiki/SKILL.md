---
name: codex-obsidian-llm-wiki
description: Chinese-first Codex skill for building and maintaining an Obsidian-compatible Markdown LLM Wiki. Use when the user asks to initialize a wiki/vault, ingest files or raw materials into a knowledge base, query an existing Markdown wiki, run health checks, create knowledge graphs, manage review queues, or maintain a Codex + Obsidian + Markdown workflow without a desktop client.
---

# Codex Obsidian LLM Wiki

Build and maintain an Obsidian-compatible Markdown LLM Wiki using Codex.

Default language: Simplified Chinese. Keep key names, tools, protocols, config fields, and technical concepts in English.

## Required Context

Before any operation, read these files from the target wiki root when present:

1. `.wiki-schema.md`
2. `purpose.md`
3. `index.md`

## Operations

## Explicit Commands

Treat these command aliases as direct operation requests:

| Command | Meaning |
|---|---|
| `cow init <wiki-root> "<topic>"` | Initialize a new wiki. |
| `cow raw add <source> <wiki-root>` | Add files or folders to `raw/` only, without creating knowledge pages. |
| `cow ingest <source> <wiki-root>` | Ingest one file, folder, URL, or pasted source. |
| `cow batch <wiki-root>` | Ingest new or changed files under `raw/`. |
| `cow query <wiki-root> "<question>"` | Answer from the wiki with citations. |
| `cow lint <wiki-root>` | Run health checks and fix deterministic issues. |
| `cow graph <wiki-root>` | Create or update `wiki/knowledge-graph.md`. |
| `cow review <wiki-root>` | Process open files in `wiki/review/`. |
| `cow help` | Show the command cheatsheet. |

`cow` means Codex Obsidian Wiki.

### init

Use `scripts/init_wiki.py` to create a new vault:

```bash
python scripts/init_wiki.py <wiki-root> "<topic>"
```

Then ask the user to open the folder in Obsidian if they want backlinks and graph view.

### raw add

Use `scripts/raw_add.py` to stage external files or folders under `raw/` without digesting them into wiki pages:

```bash
python scripts/raw_add.py <source> <wiki-root> --section notes
python scripts/raw_add.py <source-folder> <wiki-root> --section articles --name my-source
python scripts/raw_add.py <source> <wiki-root> --section notes --sanitize
```

Choose an existing raw subfolder when it fits: `notes`, `articles`, `pdfs`, or `assets`. Create a clear new subfolder such as `configs` or `reports` only when existing folders do not fit. Use `--sanitize` for credentials, account identifiers, private paths, API keys, tokens, or other sensitive personal data. Raw add updates `.wiki-cache.json` with an empty `source_page` and appends to `log.md`; `cache.py check` must still report a MISS until ingest writes the matching source page. Use `cow batch` later to digest staged raw material.

### ingest

Use a two-step ingest:

1. **Analyze only**: identify source type, entities, topics, claims, conflicts, target pages, and review items.
2. **Write pages**: update `wiki/sources/`, `wiki/topics/`, `wiki/entities/`, `index.md`, `.wiki-cache.json`, `log.md`, and `wiki/review/` when needed.

Do not invent missing facts. If a claim is uncertain, file it under `wiki/review/`.

For `cow batch`, use `scripts/cache.py check` to skip unchanged raw files and `scripts/cache.py update` after writing the source page.

### query

Answer from the wiki, not general memory:

1. Read `purpose.md` and `index.md`.
2. Search `wiki/` with `rg`.
3. Read relevant pages and follow one level of wikilinks.
4. Read related `wiki/sources/` pages for source traceability.
5. Answer in Chinese and cite wiki pages inline with `[[Page Name]]`.

Save durable answers to `wiki/queries/` when useful.

### lint

Run:

```bash
python scripts/lint_wiki.py <wiki-root>
```

Fix deterministic issues directly: broken links, missing index entries, missing required folders, missing cache file, missing `source_path`, missing `sources`, and missing raw source references. Put ambiguous issues into `wiki/review/`.

### cache

Use the cache helper for batch ingest:

```bash
python scripts/cache.py check <raw-file>
python scripts/cache.py update <raw-file> <source-page>
python scripts/cache.py list <wiki-root>
python scripts/cache.py stale <wiki-root>
python scripts/raw_add.py <source> <wiki-root> --section notes
```

### graph

Create or update `wiki/knowledge-graph.md` using Mermaid. Include:

- key nodes
- important links
- bridge nodes
- isolated pages
- knowledge gaps

## Directory Contract

```text
<wiki-root>/
├── raw/
├── wiki/
│   ├── sources/
│   ├── topics/
│   ├── entities/
│   ├── comparisons/
│   ├── synthesis/
│   ├── queries/
│   └── review/
├── index.md
├── purpose.md
├── .wiki-schema.md
├── .wiki-cache.json
└── log.md
```

## References

- For detailed workflow rules, read `references/workflows.md`.
- For page schema and templates, read `references/schema.md`.
