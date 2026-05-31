# Command Cheatsheet

`/cow` means **Codex Obsidian Wiki**.

Natural language works, but these explicit commands are easier to remember and easier for Codex to route.

## Commands

| Command | Purpose |
|---|---|
| `/cow:init <wiki-root> "<topic>"` | Initialize a new Obsidian-compatible Markdown wiki. |
| `/cow:ingest <source> <wiki-root>` | Ingest one file, folder, URL, or pasted source. |
| `/cow:batch <wiki-root>` | Ingest new or changed files under `raw/`, using `.wiki-cache.json` to skip unchanged files. |
| `/cow:query <wiki-root> "<question>"` | Answer from the wiki with citations. |
| `/cow:lint <wiki-root>` | Run health checks and fix deterministic issues. |
| `/cow:graph <wiki-root>` | Create or update `wiki/knowledge-graph.md`. |
| `/cow:review <wiki-root>` | Process open files in `wiki/review/`. |
| `/cow:help` | Show this command list. |

## Examples

```text
/cow:init D:\Wiki\my-wiki "工程知识库"
/cow:ingest D:\Notes\debug-crash.md D:\Wiki\my-wiki
/cow:batch D:\Wiki\my-wiki
/cow:query D:\Wiki\my-wiki "这个 crash 的根因是什么？"
/cow:lint D:\Wiki\my-wiki
```

## Script Helpers

The skill bundles deterministic helpers:

```bash
python scripts/init_wiki.py <wiki-root> "<topic>"
python scripts/lint_wiki.py <wiki-root>
python scripts/cache.py check <raw-file>
python scripts/cache.py update <raw-file> <source-page>
python scripts/cache.py list <wiki-root>
python scripts/cache.py stale <wiki-root>
```

`cache.py update` requires both the raw file and source page to exist. `lint_wiki.py` treats open review files as warnings and duplicate page names as errors.
