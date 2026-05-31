---
name: cow-query
description: Query a Codex Obsidian Wiki and answer from its Markdown pages. Use when the user types cow query, asks questions against a wiki/vault/knowledge base, or wants cited answers from an Obsidian-compatible Markdown LLM Wiki.
---

# Cow Query

Use `codex-obsidian-llm-wiki` for the full query workflow.

Answer from the wiki, not general memory:

1. Read `purpose.md` and `index.md`.
2. Search `wiki/` with `rg`.
3. Read relevant pages and follow one level of wikilinks.
4. Read linked `wiki/sources/` pages for traceability.
5. Answer in Chinese and cite pages inline with `[[Page Name]]`.

Save durable answers to `wiki/queries/` when useful.

