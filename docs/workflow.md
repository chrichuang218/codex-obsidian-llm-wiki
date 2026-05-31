# Workflow

This project keeps the workflow intentionally small:

1. Put raw material in `raw/`.
2. Ask Codex to ingest it.
3. Codex analyzes first, then writes durable pages.
4. Read and edit the vault in Obsidian.
5. Run lint when the graph starts growing.

The goal is not to replace Obsidian. Obsidian is the front end; Markdown is the data; Codex is the maintainer.

## Explicit Commands

Use natural language or these stable aliases:

| Command | Purpose |
|---|---|
| `/cow:init <wiki-root> "<topic>"` | Initialize a new wiki. |
| `/cow:ingest <source> <wiki-root>` | Ingest one source. |
| `/cow:batch <wiki-root>` | Ingest new or changed raw files. |
| `/cow:query <wiki-root> "<question>"` | Query the wiki. |
| `/cow:lint <wiki-root>` | Run health checks. |
| `/cow:graph <wiki-root>` | Generate a Mermaid knowledge graph. |
| `/cow:review <wiki-root>` | Process review queue items. |
| `/cow:help` | Show command help. |

Example:

```text
/cow:init D:\Wiki\my-wiki "工程知识库"
/cow:ingest D:\Notes\debug-crash.md D:\Wiki\my-wiki
/cow:query D:\Wiki\my-wiki "这个 crash 的根因是什么？"
```
