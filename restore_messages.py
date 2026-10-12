"""Rebuild a public-only SQLite database from the sanitized message export."""

import json
import sqlite3
import sys
from pathlib import Path


def restore(source: Path, destination: Path) -> None:
    if destination.exists():
        raise SystemExit(f"Refusing to overwrite existing database: {destination}")
    data = json.loads(source.read_text(encoding="utf-8"))
    messages = data["messages"]
    if not isinstance(messages, list):
        raise ValueError("messages must be a list")
    rows = []
    for item in messages:
        if set(item) != {"id", "name", "message", "created_at"}:
            raise ValueError("unexpected message fields")
        if type(item["id"]) is not int or any(not isinstance(item[key], str) for key in ("name", "message", "created_at")):
            raise ValueError("invalid message")
        rows.append((item["id"], item["name"], item["message"], item["created_at"]))
    if len({row[0] for row in rows}) != len(rows):
        raise ValueError("duplicate message id")
    try:
        with sqlite3.connect(destination) as database:
            database.execute("CREATE TABLE messages (id INTEGER PRIMARY KEY, name TEXT NOT NULL, message TEXT NOT NULL, created_at TEXT NOT NULL)")
            database.executemany("INSERT INTO messages VALUES (?, ?, ?, ?)", rows)
    except Exception:
        destination.unlink(missing_ok=True)
        raise
    print(f"Restored {len(rows)} public messages to {destination}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python3 restore_messages.py messages.json NEW_DATABASE_PATH")
    restore(Path(sys.argv[1]), Path(sys.argv[2]))
