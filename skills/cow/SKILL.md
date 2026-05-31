---
name: cow
description: Entry point for Codex Obsidian Wiki commands. Use when the user types cow, cow help, cow init, cow raw add, cow ingest, cow batch, cow query, cow lint, cow graph, or cow review and wants to work with an Obsidian-compatible Markdown LLM Wiki.
---

# Cow

`cow` means Codex Obsidian Wiki.

Use the installed `codex-obsidian-llm-wiki` skill as the main implementation guide.

If the user only types `cow`, show the command cheatsheet:

```text
cow help
cow init <wiki-root> "<topic>"
cow raw add <source> <wiki-root>
cow ingest <source> <wiki-root>
cow batch <wiki-root>
cow query <wiki-root> "<question>"
cow lint <wiki-root>
cow graph <wiki-root>
cow review <wiki-root>
```

