# Knowledge Dependency

This directory is for local knowledge-base artifacts.

The Rob Burbea digital garden is not committed to this repository. Clone it locally with:

```bash
python3 scripts/clone_or_update_garden.py
```

Then build the local SQLite index:

```bash
python3 scripts/build_garden_index.py
```

Runtime outputs:

```text
knowledge/rob-burbea-garden/
knowledge/manifests/garden-source.json
knowledge/indexes/ro-bot-burbea.sqlite
```

The cloned garden and indexes are ignored by git.
