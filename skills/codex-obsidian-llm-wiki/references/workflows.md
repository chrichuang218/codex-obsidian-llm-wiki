# Workflows

## Two-Step Ingest

Always separate analysis from writing.

### Step 1: Analysis

Produce a short internal plan:

- source path and source type
- 3-7 key claims
- entities to create or update
- topics to create or update
- links to existing pages
- contradictions or uncertainty
- review items

### Step 2: Write

Write only after analysis:

- one page in `wiki/sources/`
- topic pages in `wiki/topics/`
- entity pages in `wiki/entities/`
- review notes in `wiki/review/` for uncertain items
- update `index.md`, `.wiki-cache.json`, and `log.md`

## Source Traceability

Every generated page must include frontmatter `sources`.

Prefer source pages as the durable citation surface:

```yaml
sources:
  - wiki/sources/example-source.md
```

Source pages must include `source_path` pointing to `raw/`.

## Review Queue

Use `wiki/review/` when:

- a claim is plausible but not proven by the source
- two sources conflict
- a page split or merge would be useful but needs human judgment
- a source appears to contain secrets or private data
- an entity name is ambiguous

Review files should be short and actionable.

## Query Retrieval

For queries:

1. Read `purpose.md`.
2. Read `index.md`.
3. Search `wiki/` with `rg`.
4. Read relevant topic/entity pages.
5. Follow one level of wikilinks.
6. Read linked source pages.
7. Answer with citations.

If the wiki lacks evidence, say what is missing and suggest what to ingest.

