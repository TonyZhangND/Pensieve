# Delete

Delete a wiki article or a raw source and clean up all references across the vault. Your argument is: $ARGUMENTS

The argument should be a wiki article slug (e.g., `transformer-architecture`), a raw source path (e.g., `raw/articles/karpathy-llm-knowledge-bases.md`), or a partial name to search for.

## Step 1: Identify the Target

- If the argument matches a file in `wiki/`, follow **Path A: Delete Wiki Article**
- If the argument matches a file in `raw/`, follow **Path B: Delete Source**
- If ambiguous, list matches and ask the user to confirm

---

## Path A: Delete Wiki Article

### A1: Read the Article

Read the article's frontmatter to get its tags and sources.

### A2: Delete the Article File

Remove the file from `wiki/`.

### A3: Update Indices

#### catalog.md
Remove the article's entry from `_index/catalog.md`.

#### graph.md
- Remove the article's own section from `_index/graph.md`
- Remove all references to the article from other articles' sections

#### sources.md
Remove the article from the `→` target list of any source entries in `_index/sources.md`. If a source entry's target list becomes empty, keep the source entry but remove the `→ ...` suffix. Update the inline tags on affected source entries to reflect the union of tags from their remaining wiki article targets.

#### tags/*.md
- Remove the article's entry from every tag file in `_index/tags/`
- If a tag file becomes empty (no articles left), delete the tag file

#### meta.md
Update the totals header (decrement article count, adjust tag count if tags were removed). Update tag entries — decrement counts, remove tags that no longer have any articles.

### A4: Remove Wikilinks from Other Wiki Articles

Search all remaining files in `wiki/` for `[[slug]]` or `[[slug|...]]` wikilinks pointing to the deleted article. For each occurrence:
- If the wikilink is inline in a sentence, replace `[[slug]]` or `[[slug|display text]]` with just the plain display text
- If the wikilink is a standalone bullet or list item that only exists to reference this article, remove the entire line
- If removing the link leaves an empty section, remove the section header too

### A5: Summary

Report:
- Article deleted
- Index entries removed (catalog, graph, tags, sources)
- Wikilinks cleaned up in other articles (list which files were modified)
- Any tag files that were deleted because they became empty

---

## Path B: Delete Source

### B1: Read the Source Entry

Find the source's entry in `_index/sources.md` to identify which wiki articles it fed into.

### B2: Delete the Raw Files

Remove the source's files from `raw/` — both the `.md` metadata file and any companion files (`.pdf`, images, etc.).

### B3: Update Indices

#### sources.md
Remove the source's entry from `_index/sources.md`. Update the totals header in `meta.md` (decrement source count).

#### Wiki article frontmatter
For each wiki article that listed this source in its `sources` frontmatter:
- Remove the source path from the `sources` array
- Remove the source from the article's Sources section (the wikilink line)
- If the article has no remaining sources, flag it for the user's attention — it may need a new source or deletion

### B4: Summary

Report:
- Raw files deleted
- Source entry removed from `sources.md`
- Wiki articles updated (list which files were modified)
- Any wiki articles left with no sources (flag for review)
