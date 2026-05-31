---
name: cow-init
description: Initialize a new Codex Obsidian Wiki vault. Use when the user types cow init, wants to create a new Obsidian-compatible Markdown LLM Wiki, or asks to initialize a wiki/vault with the cow workflow.
---

# Cow Init

Use `codex-obsidian-llm-wiki` for the full workflow.

Initialize the target wiki with the bundled script:

```bash
python scripts/init_wiki.py <wiki-root> "<topic>"
```

If this companion skill is installed separately from the main skill, locate the main skill folder named `codex-obsidian-llm-wiki` and run its `scripts/init_wiki.py`.

