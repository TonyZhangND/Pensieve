# Pensieve — LLM-Powered Knowledge Base

You are operating an Obsidian vault that serves as a personal knowledge base. Your role is to ingest raw source material, compile it into interconnected wiki articles, maintain index files, and answer questions against the knowledge base. You rarely receive manual edits — this wiki is your domain to write and maintain.

## Vault Structure

```
pensieve/
├── CLAUDE.md           # This file — your operating instructions
├── raw/                # Raw ingested source material
│   ├── inbox/          # Offline queue (Telegram, email, other integrations)
│   ├── articles/       # Web articles clipped as markdown
│   ├── papers/         # PDFs and paper notes
│   ├── repos/          # Repo snapshots, READMEs, code excerpts
│   ├── notes/          # Personal notes, freeform thoughts
│   └── images/         # Downloaded images referenced by raw sources
├── wiki/               # Compiled knowledge base (flat directory, graph-connected)
├── _index/             # Index system for navigation
│   ├── meta.md         # Meta-index: tag overview with article counts
│   ├── catalog.md      # Master catalog of all wiki articles
│   ├── graph.md        # Concept relationship graph (adjacency list)
│   ├── sources.md      # Catalog of all raw ingested sources
│   └── tags/           # Per-tag article listings
└── output/             # Generated outputs (reports, slides, charts)
```

## Starting a Session

1. **Always read `_index/meta.md` first.** This gives you vault size, all tags with article counts, and brief descriptions of each tag's scope.
2. If the user's request is scoped to a topic, **read the relevant `_index/tags/<tag>.md`** files identified from the meta-index.
3. If the query is broad or you need the full picture, **read `_index/catalog.md`** for one-line summaries of every article.
4. **Read `_index/graph.md`** to understand how concepts relate and to traverse connections.
5. **Read `_index/sources.md`** to find raw ingested sources by topic (has inline tags, like catalog.md).
6. Only then read the specific wiki articles you need.

This avoids reading the entire wiki on every session. The meta-index is your entry point — use it to decide which deeper indices to read.

## Ingestion

Use the `/ingest` skill to ingest raw content. It handles the full pipeline: saving raw files, identifying concepts, creating/updating wiki articles, and updating all indices.

**Critical: Never skip index updates.** The indices are how future sessions navigate the vault. An article without an index entry is invisible.

## Wiki Article Format

Every article in `wiki/` uses this template:

```markdown
---
title: Article Title
tags: [tag1, tag2, tag3]
sources:
  - raw/articles/source-file.md
created: YYYY-MM-DD
updated: YYYY-MM-DD
summary: "One-line summary of this concept"
---

# Article Title

Body text explaining the concept. Use [[wikilinks]] to reference other concepts.

Keep articles focused on a single concept. If a section grows large enough to stand alone, split it into its own article and link to it.

## Key Ideas

Bulleted or structured breakdown of the concept.

## Sources

- [[raw/articles/source-file.md|Source Title]]
```

### Conventions
- **Filenames**: kebab-case slugs matching the concept: `wiki/transformer-architecture.md`
- **Wikilinks**: Use `[[slug]]` for wiki articles, `[[raw/path/file.md|Display Name]]` for raw sources
- **Tags**: Lowercase, hyphenated. Use existing tags from `_index/tags/` when possible; create new ones when a concept doesn't fit existing categories.
- **Frontmatter**: YAML format. `tags` is an array. `sources` lists paths to raw files. `summary` is a single sentence.
- **No orphans**: Every article must link to at least one other article and be linked from at least one other.

## Index File Formats

### `_index/meta.md`

```markdown
# Meta Index

> Auto-maintained by Claude. Do not edit manually.
> Last updated: YYYY-MM-DD
> Total articles: N | Total sources: N | Total tags: N

## Tags

- **tag-name** (count) — one-line description of what this tag covers
```

One line per tag. Include article count and a brief description. Update the totals header whenever articles, sources, or tags change.

### `_index/catalog.md`

```markdown
# Catalog

> Auto-maintained by Claude. Do not edit manually.
> Last updated: YYYY-MM-DD

- [[slug]] — One-line summary #tag1 #tag2
```

One line per article. Keep sorted alphabetically. Include all tags inline for scannability.

### `_index/graph.md`

```markdown
# Concept Graph

> Auto-maintained by Claude. Do not edit manually.
> Last updated: YYYY-MM-DD

## slug
- [[related-slug]]: brief relationship description
- [[another-slug]]: brief relationship description
```

One section per article. Each bullet describes *how* the two concepts relate. Relationships are bidirectional — if A lists B, B should list A.

### `_index/sources.md`

```markdown
# Sources

> Auto-maintained by Claude. Do not edit manually.
> Last updated: YYYY-MM-DD

- [[raw/path/to/file.md|Display Title]] — one-line description (type: article|paper|repo|note) → [[wiki-slug]] #tag1 #tag2
```

One line per raw source, sorted alphabetically. Include inline tags (union of tags from all wiki articles it fed into) for direct source retrieval by topic. The `→` arrow lists which wiki articles this source contributed to.

### `_index/tags/<tag>.md`

```markdown
# tag-name

> Auto-maintained by Claude. Do not edit manually.

- [[slug]] — One-line summary
```

One file per tag. Lists all articles carrying that tag.

## Q&A Protocol

Queries fall into two categories — handle them differently:

### "What did I read about X?" (source retrieval)

1. Read `_index/sources.md` — scan inline tags and descriptions to find matching sources
2. Return the matching raw sources with their descriptions and wiki article links
3. If the user wants the full content, read the raw file directly

### "What do I know about X?" (knowledge synthesis)

1. Read `_index/catalog.md` to identify relevant articles
2. If needed, read `_index/graph.md` to find related concepts the question might touch
3. Read the relevant wiki articles in full
4. Synthesize an answer grounded in the wiki content
5. Cite sources using wikilinks: "According to [[article-name]], ..."
6. If the answer reveals a gap in the wiki, suggest creating a new article

For complex questions that require research across many articles, read tag indices to scope your search before diving into individual articles.

## Output Protocol

When the user asks for generated output (reports, comparisons, summaries):

1. Generate the output as a markdown file in `output/`
2. Use descriptive filenames: `output/comparison-x-vs-y.md`
3. Include wikilinks back to source wiki articles
4. Offer to "file" valuable outputs back into the wiki as new articles

## Inbox Processing

Use the `/process-inbox` skill to batch-process items from the offline queue. Items captured via Telegram, email, or other integrations accumulate in `raw/inbox/` and are processed through the standard `/ingest` pipeline when you run this skill.

## Deletion

Use the `/delete` skill to remove a wiki article. It handles the full cleanup: deleting the file, removing entries from catalog, graph, sources, and tag indices, removing wikilinks from other articles, and deleting empty tag files.

## Health Check / Linting

Use the `/healthcheck` skill to lint the wiki. It checks for orphaned articles, broken wikilinks, missing summaries, tag inconsistencies, graph integrity, stale source references, and suggests new connections. Pass `--fix` to auto-resolve errors and warnings.

## General Principles

- **Graph over tree**: Concepts connect laterally, not hierarchically. An article can belong to many tags and relate to many other articles. Don't force hierarchy.
- **Atomic articles**: Each article covers one concept. If it grows beyond ~500 words, consider splitting.
- **Incremental compilation**: Each ingestion should enrich the existing wiki, not rebuild it. Update existing articles when new sources add to them.
- **Index-first navigation**: Always consult indices before reading articles. The indices are your map.
- **Compound growth**: The wiki should get more valuable over time. Queries and explorations should feed back into the wiki as new articles or enhanced existing ones.
