#!/usr/bin/env python3
"""Build a local SQLite index for the Rob Burbea digital garden."""

import argparse
import re
import sqlite3
from pathlib import Path


DEFAULT_GARDEN_PATH = Path("knowledge/rob-burbea-garden")
DEFAULT_DB_PATH = Path("knowledge/indexes/ro-bot-burbea.sqlite")
WIKILINK_RE = re.compile(r"\[\[([^\]#|]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


def title_for(path):
    return path.stem


def read_text(path):
    return path.read_text(encoding="utf-8", errors="replace")


def iter_markdown(garden_path):
    for path in sorted(Path(garden_path).rglob("*.md")):
        if ".git" not in path.parts:
            yield path


def retreat_for(relative_path):
    parts = relative_path.parts
    if len(parts) > 1 and parts[0] not in {"Index", "Help", "Images", "css-snippets"}:
        return parts[0]
    return ""


def split_chunks(text):
    chunks = []
    current_heading = "Document"
    current_lines = []
    for line in text.splitlines():
        match = HEADING_RE.match(line)
        if match:
            if current_lines:
                chunks.append((current_heading, "\n".join(current_lines).strip()))
            current_heading = match.group(2).strip()
            current_lines = []
        else:
            current_lines.append(line)
    if current_lines:
        chunks.append((current_heading, "\n".join(current_lines).strip()))
    return [(heading, body) for heading, body in chunks if body]


def create_schema(conn):
    conn.executescript(
        """
        drop table if exists documents;
        drop table if exists links;
        drop table if exists topics;
        drop table if exists guided_meditations;
        drop table if exists retreats;
        drop table if exists chunks;

        create table documents (
            path text primary key,
            title text not null,
            folder text not null,
            retreat text not null,
            word_count integer not null
        );
        create table links (
            source_path text not null,
            target text not null
        );
        create table topics (
            name text primary key,
            path text not null
        );
        create table guided_meditations (
            retreat text not null,
            talk text not null,
            source_path text not null
        );
        create table retreats (
            name text primary key
        );
        create table chunks (
            document_path text not null,
            heading text not null,
            text text not null
        );
        """
    )


def parse_guided_meditations(text):
    rows = []
    for line in text.splitlines():
        if "|" not in line or "[[" not in line or line.strip().startswith("-"):
            continue
        links = WIKILINK_RE.findall(line)
        if len(links) >= 2:
            rows.append((links[0].strip(), links[1].strip()))
    return rows


def build_index(garden_path=DEFAULT_GARDEN_PATH, db_path=DEFAULT_DB_PATH):
    garden_path = Path(garden_path)
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    try:
        create_schema(conn)
        stats = {
            "documents": 0,
            "links": 0,
            "topics": 0,
            "guided_meditations": 0,
            "retreats": 0,
            "chunks": 0,
        }
        retreats = set()

        for path in iter_markdown(garden_path):
            relative = path.relative_to(garden_path)
            relative_text = str(relative)
            text = read_text(path)
            title = title_for(path)
            folder = str(relative.parent) if str(relative.parent) != "." else ""
            retreat = retreat_for(relative)
            if retreat:
                retreats.add(retreat)

            conn.execute(
                "insert into documents(path, title, folder, retreat, word_count) values (?, ?, ?, ?, ?)",
                (relative_text, title, folder, retreat, len(text.split())),
            )
            stats["documents"] += 1

            if relative.parts and relative.parts[0] == "Index":
                conn.execute("insert or replace into topics(name, path) values (?, ?)", (title, relative_text))
                stats["topics"] += 1

            for target in WIKILINK_RE.findall(text):
                conn.execute("insert into links(source_path, target) values (?, ?)", (relative_text, target.strip()))
                stats["links"] += 1

            if relative_text == "Guided meditations.md":
                for retreat_name, talk in parse_guided_meditations(text):
                    conn.execute(
                        "insert into guided_meditations(retreat, talk, source_path) values (?, ?, ?)",
                        (retreat_name, talk, relative_text),
                    )
                    stats["guided_meditations"] += 1

            for heading, body in split_chunks(text):
                conn.execute(
                    "insert into chunks(document_path, heading, text) values (?, ?, ?)",
                    (relative_text, heading, body),
                )
                stats["chunks"] += 1

        for retreat in sorted(retreats):
            conn.execute("insert or replace into retreats(name) values (?)", (retreat,))
            stats["retreats"] += 1

        conn.commit()
        return stats
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--garden", default=str(DEFAULT_GARDEN_PATH), help="Local garden clone path.")
    parser.add_argument("--output", default=str(DEFAULT_DB_PATH), help="SQLite output path.")
    args = parser.parse_args()

    stats = build_index(garden_path=Path(args.garden), db_path=Path(args.output))
    for key, value in stats.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
