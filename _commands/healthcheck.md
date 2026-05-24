# Health Check

Run a health check on the Pensieve knowledge base. Identify issues and optionally fix them. Your argument is: $ARGUMENTS

## Step 1: Read All Indices

Read `_index/meta.md`, `_index/catalog.md`, `_index/graph.md`, `_index/sources.md`, and all files in `_index/tags/`.

## Step 2: Scan Wiki and Raw Directories

List all files in `wiki/` and `raw/` to compare against what the indices claim exists.

## Step 3: Run Checks

Perform each of the following checks and report findings:

### Orphaned articles
Wiki articles in `wiki/` that are missing from `_index/catalog.md`, or that no other wiki article links to.

### Broken wikilinks
`[[wikilinks]]` in wiki articles that point to non-existent files. These are candidates for new articles — flag them as such.

### Missing or empty summaries
Wiki articles with no `summary` field in frontmatter, or where the summary is empty.

### Stale index entries
Entries in `catalog.md`, `graph.md`, or `sources.md` that point to files that no longer exist.

### Tag inconsistencies
- Tags used in article frontmatter that have no corresponding `_index/tags/<tag>.md` file
- Tag index files that list articles which don't carry that tag in their frontmatter
- Tag index files that are missing articles which do carry that tag

### Graph integrity
- Articles listed in `graph.md` that have relationships missing the reverse entry (A→B exists but B→A doesn't)
- Wiki articles with no entry in `graph.md` at all

### Source tracking
- Raw files in `raw/` not listed in `_index/sources.md`
- Source entries in `sources.md` pointing to deleted raw files
- Wiki articles whose `sources` frontmatter references raw files that don't exist
- Source entries in `sources.md` missing inline tags, or whose tags don't match the union of tags from the wiki articles they feed into

### Meta-index consistency
- Article count in `meta.md` doesn't match actual number of files in `wiki/`
- Tag counts in `meta.md` don't match actual number of articles in each `_index/tags/<tag>.md`
- Tags listed in `meta.md` that have no corresponding tag file, or vice versa

### Suggested connections
Look for wiki articles that likely relate but aren't linked — based on shared tags, overlapping content in summaries, or common sources.

## Step 4: Report

Present findings as a checklist grouped by check type. For each issue, note the severity:
- **Error**: Broken reference, data loss risk
- **Warning**: Missing metadata, incomplete index
- **Suggestion**: Potential new connection or article

## Step 5: Fix (if requested)

If the user asks to fix issues (or passes `--fix` as an argument), resolve all errors and warnings automatically:
- Add missing catalog/graph/tag/source entries
- Remove stale entries pointing to deleted files
- Add reverse graph relationships
- Populate missing summaries by reading the article content

Report what was fixed. Leave suggestions for the user to approve.
