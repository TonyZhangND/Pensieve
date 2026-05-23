# Pensieve

An LLM-powered personal knowledge base, inspired by [Karpathy's approach](https://x.com/karpathy/status/2039805659525644595?s=20). Raw sources go in, an interconnected wiki comes out — compiled and maintained entirely by Claude Code, viewed in Obsidian.

## How It Works

1. **Ingest** raw material (articles, papers, repos, notes) using the `/project:ingest` command in Claude Code
2. Claude saves the raw content, identifies concepts, and **compiles** wiki articles with `[[wikilinks]]` connecting them into a knowledge graph
3. Claude auto-maintains **index files** (catalog, concept graph, source registry, tag indices) so future sessions can efficiently navigate the vault
4. **Query** the knowledge base by asking Claude questions — it reads the indices, finds relevant articles, and synthesizes answers
5. The wiki grows incrementally — every ingestion and exploration adds to it

## Setup

1. Clone this repo
2. Open the folder as an Obsidian vault
3. Open a Claude Code session in the same directory
4. Start ingesting: `/project:ingest <url, file, or paste content>`

## Vault Structure

```
pensieve/
├── CLAUDE.md           # System prompt — how Claude operates the vault
├── _commands/          # Claude Code skills (visible in Obsidian)
│   └── ingest.md       # Ingestion pipeline
├── raw/                # Raw ingested source material
│   ├── articles/       # Web articles as markdown
│   ├── papers/         # PDFs and paper notes
│   ├── repos/          # Repo excerpts
│   ├── notes/          # Personal notes
│   └── images/         # Downloaded images
├── wiki/               # Compiled knowledge base (flat, graph-connected)
├── _index/             # Index system for Claude navigation
│   ├── catalog.md      # Master catalog of all wiki articles
│   ├── graph.md        # Concept relationship graph
│   ├── sources.md      # Registry of all raw ingested sources
│   └── tags/           # Per-tag article listings
└── output/             # Generated outputs (reports, slides, charts)
```

## Key Ideas

- **Graph over tree**: Articles connect laterally via wikilinks and tags, not through folder hierarchy
- **Bidirectional source tracking**: Every wiki article lists the raw sources it was compiled from (in frontmatter and a Sources section). Conversely, `_index/sources.md` maps every raw source to the wiki articles it fed into. You can traverse in either direction — from a concept to its evidence, or from a source to every concept it contributed to.
- **Index-first navigation**: Claude reads compact index files to find what it needs, rather than scanning the entire wiki
- **Incremental compilation**: Each ingestion enriches the existing wiki — articles are updated, not rebuilt
- **LLM-maintained**: You rarely edit the wiki directly. Claude writes, organizes, and cross-links everything

## Usage

All operations are performed by talking to Claude Code inside the vault directory.

- **Ingest content**: `/project:ingest <url, file path, or pasted text>` — saves the raw source, compiles wiki articles, and updates all indices
- **Ask questions**: Ask Claude anything about your knowledge base. It reads the indices, pulls up relevant articles, and synthesizes an answer with citations.
- **Generate output**: Ask Claude to produce reports, comparisons, or summaries. Outputs are saved to `output/` and can be filed back into the wiki.
- **Health check**: Ask Claude to lint the wiki — it will find orphaned articles, broken wikilinks, missing summaries, tag inconsistencies, and suggest new connections.
- **Browse**: Open the vault in Obsidian to explore the wiki visually, follow wikilinks, and use the graph view to see concept relationships.

## License

MIT
