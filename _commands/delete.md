# Delete Wiki Article

Delete a wiki article and clean up all references across the vault. Your argument is: $ARGUMENTS

The argument should be a wiki article slug (e.g., `test-time-compute-scaling`) or a partial name to search for.

## Step 1: Identify the Article

- If the argument matches a file in `wiki/`, use that
- If ambiguous, list matches and ask the user to confirm

Read the article's frontmatter to get its tags and sources.

## Step 2: Delete the Article File

Remove the file from `wiki/`.

## Step 3: Update Indices

### catalog.md
Remove the article's entry from `_index/catalog.md`.

### graph.md
- Remove the article's own section from `_index/graph.md`
- Remove all references to the article from other articles' sections

### sources.md
Remove the article from the `→` target list of any source entries in `_index/sources.md`. If a source entry's target list becomes empty, keep the source entry but remove the `→ ...` suffix.

### tags/*.md
- Remove the article's entry from every tag file in `_index/tags/`
- If a tag file becomes empty (no articles left), delete the tag file

### meta.md
Update the totals header (decrement article count, adjust tag count if tags were removed). Update tag entries — decrement counts, remove tags that no longer have any articles.

## Step 4: Remove Wikilinks from Other Wiki Articles

Search all remaining files in `wiki/` for `[[slug]]` or `[[slug|...]]` wikilinks pointing to the deleted article. For each occurrence:
- If the wikilink is inline in a sentence, replace `[[slug]]` or `[[slug|display text]]` with just the plain display text
- If the wikilink is a standalone bullet or list item that only exists to reference this article, remove the entire line
- If removing the link leaves an empty section, remove the section header too

## Step 5: Summary

Report:
- Article deleted
- Index entries removed (catalog, graph, tags, sources)
- Wikilinks cleaned up in other articles (list which files were modified)
- Any tag files that were deleted because they became empty
