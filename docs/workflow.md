# Workflow

This project keeps the workflow intentionally small:

1. Put raw material in `raw/`.
2. Ask Codex to ingest it.
3. Codex analyzes first, then writes durable pages.
4. Read and edit the vault in Obsidian.
5. Run lint when the graph starts growing.

The goal is not to replace Obsidian. Obsidian is the front end; Markdown is the data; Codex is the maintainer.

## Explicit Commands

Use natural language or these stable `cow` trigger phrases:

| Command | Purpose |
|---|---|
| `cow init <wiki-root> "<topic>"` | Initialize a new wiki. |
| `cow raw add <source> <wiki-root>` | Add files or folders to `raw/` only. |
| `cow ingest <source> <wiki-root>` | Ingest one source. |
| `cow batch <wiki-root>` | Ingest new or changed raw files. |
| `cow query <wiki-root> "<question>"` | Query the wiki. |
| `cow lint <wiki-root>` | Run health checks. |
| `cow graph <wiki-root>` | Generate a Mermaid knowledge graph. |
| `cow review <wiki-root>` | Process review queue items. |
| `cow help` | Show command help. |

Example:

```text
cow init D:\Wiki\my-wiki "工程知识库"
cow raw add D:\Notes\debug-crash.md D:\Wiki\my-wiki
cow ingest D:\Notes\debug-crash.md D:\Wiki\my-wiki
cow query D:\Wiki\my-wiki "这个 crash 的根因是什么？"
```

## Cache-Aware Batch Ingest

Use `.wiki-cache.json` to avoid re-ingesting unchanged raw files.

The bundled helper supports:

```bash
python scripts/raw_add.py <source> <wiki-root> --section notes
python scripts/cache.py check <raw-file>
python scripts/cache.py update <raw-file> <source-page>
python scripts/cache.py list <wiki-root>
python scripts/cache.py stale <wiki-root>
```

Batch ingest should:

1. Walk `raw/`.
2. Run `cache.py check` for each candidate source.
3. Ingest only cache misses.
4. Run `cache.py update` after writing the matching `wiki/sources/` page.
5. Run `lint_wiki.py` at the end.
