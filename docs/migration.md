# Migration Guide

Use this guide when you already have a Markdown LLM Wiki and want to move it into the `codex-obsidian-llm-wiki` layout.

This is a **manual, file-based migration**. It does not modify your old vault. Copy into a new folder, verify, then decide whether to archive the old one.

## Target Layout

```text
<new-wiki-root>/
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

## Common Directory Mapping

| Old layout | New layout | Notes |
|---|---|---|
| `raw/` | `raw/` | Copy original sources as-is. |
| `wiki/summaries/` | `wiki/sources/` | One source summary per raw item. |
| `wiki/concepts/` | `wiki/topics/` | Durable topic pages. |
| `wiki/entities/` | `wiki/entities/` | Keep entity pages. |
| `outputs/queries/` | `wiki/queries/` | Saved query answers. |
| `audit/` | `wiki/review/` | Human feedback and unresolved questions. |
| `log/YYYYMMDD.md` | `log.md` | Combine or summarize operation history. |
| `CLAUDE.md` / `AGENTS.md` | `.wiki-schema.md` + `purpose.md` + `AGENTS.md` | Split schema, purpose, and Codex project instructions. |

## Step 1: Create a New Wiki

Use the skill or script to initialize a clean target folder:

```text
cow init D:\Wiki\my-wiki "我的知识库"
```

Or run:

```bash
python skills/codex-obsidian-llm-wiki/scripts/init_wiki.py <new-wiki-root> "我的知识库"
```

## Step 2: Copy Raw Sources

Copy the old `raw/` folder into the new wiki.

Keep raw files unchanged. If a file is too large for Git, keep it outside the vault and create a small Markdown pointer under `raw/notes/`.

## Step 3: Move Generated Wiki Pages

Copy pages according to the mapping table:

```text
old/wiki/summaries/*  -> new/wiki/sources/
old/wiki/concepts/*   -> new/wiki/topics/
old/wiki/entities/*   -> new/wiki/entities/
old/outputs/queries/* -> new/wiki/queries/
old/audit/*           -> new/wiki/review/
```

Then scan page frontmatter:

- Source pages should include `source_path`.
- Topic/entity pages should include `sources`.
- Links should use Obsidian wikilinks: `[[Page Name]]`.

## Step 4: Rebuild Index and Purpose

Update:

- `index.md`: list every durable page once.
- `purpose.md`: describe the research goal and scope.
- `.wiki-schema.md`: keep directory rules, language preference, and aliases.
- `log.md`: add a migration entry.

Good `index.md` sections:

```text
## 素材摘要
## 主题页
## 实体页
## 对比分析
## 综合分析
## Review
```

## Step 5: Update Cache

For each raw file that already has a source page:

```bash
python skills/codex-obsidian-llm-wiki/scripts/cache.py update <raw-file> <source-page>
```

Example:

```bash
python skills/codex-obsidian-llm-wiki/scripts/cache.py update D:\Wiki\my-wiki\raw\notes\debug.md wiki/sources/debug.md
```

Then check:

```bash
python skills/codex-obsidian-llm-wiki/scripts/cache.py stale <new-wiki-root>
```

## Step 6: Run Lint

Run:

```bash
python skills/codex-obsidian-llm-wiki/scripts/lint_wiki.py <new-wiki-root>
```

Fix deterministic issues:

- `BROKEN_LINK`: create the missing page or fix the link.
- `NOT_IN_INDEX`: add the page to `index.md`.
- `ORPHAN_PAGE`: link it from a relevant page or `wiki/overview.md`.
- `MISSING_SOURCE_PATH`: add `source_path` to a source page.
- `MISSING_RAW_SOURCE`: restore the raw file or update `source_path`.
- `MISSING_SOURCES`: add source references to topic/entity pages.
- `MISSING_SOURCE_REF`: fix or restore the referenced source page.

Put ambiguous issues into `wiki/review/`.

## After Migration Checklist

- [ ] New wiki opens cleanly in Obsidian.
- [ ] `index.md` links to all important pages.
- [ ] `purpose.md` describes what belongs in the wiki.
- [ ] `.wiki-cache.json` contains entries for migrated raw files.
- [ ] `lint_wiki.py` reports `OK wiki is healthy`.
- [ ] Old wiki is archived or kept read-only.

## What Not To Migrate

Do not migrate:

- API keys, tokens, cookies, or credentials.
- Private personal data.
- Build artifacts or generated caches from unrelated tools.
- Large binaries that should live outside Git.
