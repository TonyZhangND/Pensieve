# Process Inbox

Batch-process all items in the offline queue (`raw/inbox/`), captured via Telegram, email, or other integrations. Your argument is: $ARGUMENTS

## Step 1: List Inbox Items

List all files in `raw/inbox/` (excluding the `processed/` subdirectory and `.gitkeep`). Group companion files together — a `.md` metadata file and its associated media file (image, PDF, audio) are one item.

If the inbox is empty, report "Inbox is empty" and stop.

Show the user a numbered list of inbox items with their type and a preview (first line of text content, or filename for media).

## Step 2: Process Each Item

For each inbox item, read its `.md` file to extract the content and metadata. Then run the standard `/ingest` pipeline on it — `/ingest` is the single source of truth for how to classify, store, and compile raw content into the wiki.

Pass the relevant context to the ingestion pipeline:
- For URLs: the `original_url` from frontmatter
- For text/forwards: the body text
- For media (photos, documents, voice): the file path and any caption

## Step 3: Archive Processed Items

After successfully processing each item, move its files (both `.md` and any associated media) from `raw/inbox/` to `raw/inbox/processed/`.

Do NOT delete inbox files — move them to `processed/` for safety.

## Step 4: Summary

Report:
- Total items processed
- Wiki articles created/updated
- Items that failed or need manual review
- Any suggestions for follow-up
