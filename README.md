# Pensieve

An LLM-powered personal knowledge base, inspired by [Karpathy's approach](https://x.com/karpathy/status/2039805659525644595?s=20). Raw sources go in, an interconnected wiki comes out — compiled and maintained entirely by Claude Code, viewed in Obsidian.

## How It Works

1. **Ingest** raw material (articles, papers, repos, notes) using the `/ingest` command in Claude Code
2. Claude saves the raw content, identifies concepts, and **compiles** wiki articles with `[[wikilinks]]` connecting them into a knowledge graph
3. Claude auto-maintains **index files** (catalog, concept graph, source registry, tag indices) so future sessions can efficiently navigate the vault
4. **Query** the knowledge base by asking Claude questions — it reads the indices, finds relevant articles, and synthesizes answers
5. The wiki grows incrementally — every ingestion and exploration adds to it

## Setup

1. Clone this repo
2. Open the folder as an Obsidian vault
3. Open a Claude Code session in the same directory
4. Start ingesting: `/ingest <url, file, or paste content>`

## Vault Structure

```
pensieve/
├── CLAUDE.md           # System prompt — how Claude operates the vault
├── _commands/          # Claude Code skills (visible in Obsidian)
│   └── ingest.md       # Ingestion pipeline
├── tools/              # Utilities (Telegram bot, etc.)
├── raw/                # Raw ingested source material
│   ├── inbox/          # Offline queue (Telegram, email, etc.)
│   ├── articles/       # Web articles as markdown
│   ├── papers/         # PDFs and paper notes
│   ├── repos/          # Repo excerpts
│   ├── notes/          # Personal notes
│   └── images/         # Downloaded images
├── wiki/               # Compiled knowledge base (flat, graph-connected)
├── _index/             # Index system for Claude navigation
│   ├── meta.md         # Meta-index: tag overview with article counts
│   ├── catalog.md      # Master catalog of all wiki articles
│   ├── graph.md        # Concept relationship graph
│   ├── sources.md      # Registry of all raw ingested sources
│   └── tags/           # Per-tag article listings
└── output/             # Generated outputs (reports, slides, charts)
```

## Key Ideas

- **Two query modes**: "What did I read about X?" searches the source index directly — every raw source is tagged and summarized for fast retrieval. "What do I know about X?" synthesizes across wiki articles, following the concept graph to build a cross-referenced answer. Sources and wiki serve different needs; the index system supports both as first-class use cases.
- **Graph over tree**: Articles connect laterally via wikilinks and tags, not through folder hierarchy
- **Bidirectional source tracking**: Every wiki article lists the raw sources it was compiled from (in frontmatter and a Sources section). Conversely, `_index/sources.md` maps every raw source to the wiki articles it fed into, with inline tags for direct topic search. You can traverse in either direction — from a concept to its evidence, or from a source to every concept it contributed to.
- **Tiered indexing**: A lightweight meta-index summarizes all tags with article counts, so Claude can decide which tag indices to drill into without reading the full catalog. This keeps navigation efficient as the wiki scales to hundreds of articles.
- **Index-first navigation**: Claude reads compact index files to find what it needs, rather than scanning the entire wiki
- **Incremental compilation**: Each ingestion enriches the existing wiki — articles are updated, not rebuilt
- **LLM-maintained**: You rarely edit the wiki directly. Claude writes, organizes, and cross-links everything

## Usage

All operations are performed by talking to Claude Code inside the vault directory.

- **Ingest content**: `/ingest <url, file path, or pasted text>` — saves the raw source, compiles wiki articles, and updates all indices
- **Find sources**: Ask "what did I read about X?" — Claude searches the source index by topic and returns matching raw sources with descriptions. No wiki hop needed.
- **Synthesize knowledge**: Ask "what do I know about X?" — Claude reads wiki articles, follows the concept graph, and synthesizes an answer with citations across multiple sources.
- **Generate output**: Ask Claude to produce reports, comparisons, or summaries. Outputs are saved to `output/` and can be filed back into the wiki.
- **Offline queue**: Capture content on the go via Telegram (with more integrations like email coming). Items queue in `raw/inbox/` and are batch-ingested when you run `/process-inbox`. See [tools/README.md](tools/README.md) for setup.
- **Health check**: `/healthcheck` — finds orphaned articles, broken wikilinks, missing summaries, tag inconsistencies, and suggests new connections. Use `/healthcheck --fix` to auto-resolve issues.
- **Browse**: Open the vault in Obsidian to explore the wiki visually, follow wikilinks, and use the graph view to see concept relationships.

## License

MIT
