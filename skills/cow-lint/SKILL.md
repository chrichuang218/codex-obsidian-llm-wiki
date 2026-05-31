---
name: cow-lint
description: Run health checks for a Codex Obsidian Wiki. Use when the user types cow lint, asks to check/fix wiki health, broken wikilinks, missing index entries, source traceability, stale cache entries, duplicate page names, or review queue warnings.
---

# Cow Lint

Use `codex-obsidian-llm-wiki` for the full lint workflow.

Run the main skill's helper:

```bash
python scripts/lint_wiki.py <wiki-root>
```

Fix deterministic issues directly. Put ambiguous issues into `wiki/review/`.

