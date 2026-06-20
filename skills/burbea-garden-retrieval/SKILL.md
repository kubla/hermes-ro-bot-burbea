---
name: burbea-garden-retrieval
description: Retrieve and summarize Rob Burbea digital garden material from the local clone and SQLite index with source citations.
---

# Burbea Garden Retrieval

Use this whenever Rob Burbea's teachings, the digital garden, or a source-grounded practice recommendation is relevant.

## First Check

If `knowledge/indexes/ro-bot-burbea.sqlite` is missing, suggest:

```bash
python3 scripts/clone_or_update_garden.py
python3 scripts/build_garden_index.py
```

## Retrieval Style

- Prefer local source paths over unsupported memory.
- Cite document paths.
- Distinguish source summary from coaching inference.
- Use short quotations only when needed.
- Do not dump long passages.

## Useful Queries

Use the SQLite index to search:

- `documents` by title and path
- `topics` by name
- `guided_meditations` by retreat or talk
- `chunks` by heading and text
- `links` for neighboring concepts

When applying a teaching to practice, say "A source-grounded way to explore this is..." rather than implying Rob would prescribe it.
