# Ingest

Ingest raw source material into the Pensieve knowledge base. The user will provide one or more of: a URL, a file path, pasted text, or a personal note. Your argument is: $ARGUMENTS

## Step 1: Read Current State

Read `_index/catalog.md`, `_index/graph.md`, and `_index/sources.md` to understand what already exists in the wiki and what raw content has been ingested.

## Step 2: Save Raw Content

Save the raw material to the appropriate `raw/` subdirectory:
- **Web articles**: Fetch the content, convert to markdown, save to `raw/articles/<slug>.md`. Download any referenced images to `raw/images/` and update image paths.
- **PDFs/papers**: Save to `raw/papers/`. Create a companion `raw/papers/<slug>-notes.md` with extracted key points if useful.
- **Repo links**: Save relevant excerpts (README, architecture, key source files) to `raw/repos/<slug>.md`.
- **Personal notes / pasted text**: Save to `raw/notes/<slug>.md`.

Use descriptive kebab-case filenames.

## Step 3: Identify Concepts

Analyze the raw content and identify the distinct concepts it covers. For each concept:
- Check `_index/catalog.md` — does a wiki article already exist?
- If yes: plan to **update** it with new information from this source.
- If no: plan to **create** a new article.

Present the list of concepts to the user before proceeding: "I identified these concepts: X, Y, Z. I'll create new articles for X and Y, and update the existing article for Z. Sound right?"

## Step 4: Create or Update Wiki Articles

For each concept, write or update a wiki article in `wiki/`:

```markdown
---
title: Concept Title
tags: [tag1, tag2]
sources:
  - raw/path/to/source.md
created: YYYY-MM-DD
updated: YYYY-MM-DD
summary: "One-line summary"
---

# Concept Title

Body text. Use [[wikilinks]] to connect to related concepts.

## Sources

- [[raw/path/to/source.md|Source Title]]
```

Guidelines:
- Keep articles focused on a single concept.
- Add `[[wikilinks]]` to existing articles where relevant.
- When updating an existing article, add the new source to `sources` in frontmatter, update the `updated` date, and weave in the new information.
- Reuse existing tags from `_index/tags/` when possible.

## Step 5: Update All Indices

This step is mandatory — never skip it.

### catalog.md
Add or update entries. One line per article, sorted alphabetically:
```
- [[slug]] — One-line summary #tag1 #tag2
```

### graph.md
Add or update relationship entries for every article created or modified. Ensure bidirectionality — if A references B, B should reference A:
```
## slug
- [[related-slug]]: brief relationship description
```

### sources.md
Add an entry for every raw file saved. One line per source, sorted alphabetically:
```
- [[raw/path/to/file.md|Display Title]] — one-line description (type: article|paper|repo|note) → [[wiki-slug]], [[wiki-slug-2]]
```
The `→` arrow lists which wiki articles this source fed into.

### tags/*.md
For every tag used, ensure a `_index/tags/<tag>.md` file exists with the article listed. Create new tag files as needed:
```
# tag-name

> Auto-maintained by Claude. Do not edit manually.

- [[slug]] — One-line summary
```

## Step 6: Summary

Report what was done:
- Raw files saved
- Wiki articles created/updated (with links)
- New concepts identified
- Connections made to existing concepts
- Any gaps or follow-up suggestions (e.g., "This article mentions X which doesn't have an article yet — want me to research it?")
