# Pensieve — LLM-Powered Knowledge Base

You are operating an Obsidian vault that serves as a personal knowledge base. Your role is to ingest raw source material, compile it into interconnected wiki articles, maintain index files, and answer questions against the knowledge base. You rarely receive manual edits — this wiki is your domain to write and maintain.

## Vault Structure

```
pensieve/
├── CLAUDE.md           # This file — your operating instructions
├── raw/                # Raw ingested source material
│   ├── articles/       # Web articles clipped as markdown
│   ├── papers/         # PDFs and paper notes
│   ├── repos/          # Repo snapshots, READMEs, code excerpts
│   ├── notes/          # Personal notes, freeform thoughts
│   └── images/         # Downloaded images referenced by raw sources
├── wiki/               # Compiled knowledge base (flat directory, graph-connected)
├── _index/             # Index system for navigation
│   ├── catalog.md      # Master catalog of all wiki articles
│   ├── graph.md        # Concept relationship graph (adjacency list)
│   └── tags/           # Per-tag article listings
└── output/             # Generated outputs (reports, slides, charts)
```

## Starting a Session

1. **Always read `_index/catalog.md` first.** This gives you a one-line summary of every wiki article.
2. **Read `_index/graph.md`** to understand how concepts relate to each other.
3. If the user's request is scoped to a topic, **read the relevant tag index** from `_index/tags/` to narrow your focus.
4. Only then read the specific wiki articles you need.

This avoids reading the entire wiki on every session. The index system is your table of contents.

## Ingestion Protocol

When the user provides raw content (a URL, pasted text, a file, a PDF, a repo link, or a personal note):

### Step 1: Save Raw Content
- Save the raw material to the appropriate `raw/` subdirectory
- Use descriptive kebab-case filenames: `raw/articles/attention-is-all-you-need.md`
- For web articles: save as markdown, download related images to `raw/images/` and update image references
- For PDFs: save the file directly; optionally create a companion `.md` with extracted key points
- For repos: save relevant excerpts (README, key source files, architecture notes)
- For personal notes: save as-is to `raw/notes/`

### Step 2: Identify Concepts
- Analyze the raw content and identify the key concepts it covers
- Check `_index/catalog.md` to see which concepts already have wiki articles
- Decide: create new articles or update existing ones

### Step 3: Create or Update Wiki Articles
- For each concept, create or update a wiki article in `wiki/`
- Follow the article format specified below
- Add `[[wikilinks]]` to connect to related existing concepts
- Reference the raw source in the article's frontmatter and Sources section

### Step 4: Update All Indices
- **`_index/catalog.md`**: Add/update the one-line entry for each article touched
- **`_index/graph.md`**: Add/update relationship entries for each article touched
- **`_index/tags/<tag>.md`**: Add/update entries in every relevant tag index; create new tag files as needed

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

### `_index/tags/<tag>.md`

```markdown
# tag-name

> Auto-maintained by Claude. Do not edit manually.

- [[slug]] — One-line summary
```

One file per tag. Lists all articles carrying that tag.

## Q&A Protocol

When the user asks a question about the knowledge base:

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

## Health Check / Linting Protocol

When the user asks for a health check, or periodically during large ingestion sessions:

1. **Orphan detection**: Find wiki articles not listed in `_index/catalog.md` or not linked from any other article
2. **Broken links**: Find `[[wikilinks]]` that point to non-existent articles — these are candidates for new articles
3. **Missing summaries**: Find articles with empty or missing `summary` in frontmatter
4. **Tag consistency**: Ensure every tag used in article frontmatter has a corresponding `_index/tags/<tag>.md` file, and vice versa
5. **Stale index entries**: Find catalog/graph entries pointing to deleted articles
6. **Bidirectional graph check**: Ensure every relationship in `graph.md` has a corresponding reverse entry
7. **Suggest connections**: Look for articles that likely relate but aren't linked, and suggest new edges

Report findings as a checklist and offer to fix issues automatically.

## General Principles

- **Graph over tree**: Concepts connect laterally, not hierarchically. An article can belong to many tags and relate to many other articles. Don't force hierarchy.
- **Atomic articles**: Each article covers one concept. If it grows beyond ~500 words, consider splitting.
- **Incremental compilation**: Each ingestion should enrich the existing wiki, not rebuild it. Update existing articles when new sources add to them.
- **Index-first navigation**: Always consult indices before reading articles. The indices are your map.
- **Compound growth**: The wiki should get more valuable over time. Queries and explorations should feed back into the wiki as new articles or enhanced existing ones.
