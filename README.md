# Codex Obsidian LLM Wiki

Chinese-first Codex skill for building an Obsidian-compatible Markdown LLM Wiki.

No desktop app. No database lock-in. Just Codex, a skill, Obsidian, and Markdown files you own.

[中文说明](README.zh-CN.md)

## Why This Exists

Many LLM Wiki tools are full desktop apps. This project is intentionally lighter:

- **Codex does the work**: ingest, query, lint, review, graph.
- **Obsidian is the reading UI**: backlinks, graph view, search, editing.
- **Markdown is the database**: portable, local-first, Git-friendly.
- **The skill is the workflow**: two-step ingest, source traceability, review queue, and health checks.

## Install

Ask Codex:

```text
Install this skill:
https://github.com/chrichuang218/codex-obsidian-llm-wiki/tree/main/skills/codex-obsidian-llm-wiki
```

Or run the standard Codex skill installer:

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo chrichuang218/codex-obsidian-llm-wiki \
  --path skills/codex-obsidian-llm-wiki
```

On Windows, the script is usually at:

```powershell
python $env:USERPROFILE\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py --repo chrichuang218/codex-obsidian-llm-wiki --path skills/codex-obsidian-llm-wiki
```

Restart Codex after installation.

## Quick Start

Ask Codex:

```text
用 codex-obsidian-llm-wiki 初始化一个知识库到 D:\Wiki\my-wiki
```

Then add raw materials:

```text
把这个文件整理进 D:\Wiki\my-wiki 知识库：D:\Notes\debug-crash.md
```

Query it:

```text
基于 D:\Wiki\my-wiki 知识库回答：Android AIDL hidden API collision 是什么？
```

Maintain it:

```text
检查 D:\Wiki\my-wiki 知识库健康状态，并修复确定的问题
```

## Command Cheatsheet

Natural language works, but explicit commands are easier to remember:

```text
/cow:init D:\Wiki\my-wiki "My Wiki"
/cow:ingest D:\Notes\debug-crash.md D:\Wiki\my-wiki
/cow:batch D:\Wiki\my-wiki
/cow:query D:\Wiki\my-wiki "What is Android AIDL hidden API collision?"
/cow:lint D:\Wiki\my-wiki
/cow:graph D:\Wiki\my-wiki
/cow:review D:\Wiki\my-wiki
/cow:help
```

`cow` means **Codex Obsidian Wiki**.

## Vault Layout

```text
my-wiki/
├── raw/                 # immutable source material
├── wiki/
│   ├── sources/         # one summary per source
│   ├── topics/          # durable topic pages
│   ├── entities/        # tools, people, protocols, components
│   ├── comparisons/     # comparison pages
│   ├── synthesis/       # cross-source synthesis
│   ├── queries/         # saved query answers
│   └── review/          # human review queue
├── index.md             # catalog
├── purpose.md           # research direction
├── .wiki-schema.md      # maintenance rules
├── .wiki-cache.json     # source cache
└── log.md               # operation log
```

## Core Workflow

The skill uses a two-step ingest pattern:

1. **Analyze** the source: entities, concepts, claims, conflicts, target pages.
2. **Write** durable pages: `sources`, `topics`, `entities`, `index`, `log`.

Uncertain items go to `wiki/review/` instead of being silently guessed.

## Obsidian

Open the vault folder directly in Obsidian. Wikilinks, backlinks, graph view, and Markdown editing work without a custom client.

## License

MIT
