"""Local JSON persistence for books, users, and damage reports."""

import json
from pathlib import Path

from book import Book

DATA_DIR = Path(__file__).resolve().parent / "data"


def _read_json(filename: str, default):
    path = DATA_DIR / filename
    if not path.exists():
        return default
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def _write_json(filename: str, data) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = DATA_DIR / filename
    temporary_path = path.with_suffix(path.suffix + ".tmp")
    temporary_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    temporary_path.replace(path)


def load_books() -> dict:
    data = _read_json("books.json", {})
    return {book_id: Book.from_dict(record) for book_id, record in data.items()}


def save_books(books: dict) -> None:
    _write_json("books.json", {book_id: book.to_dict() for book_id, book in books.items()})


def load_users() -> dict:
    return _read_json("users.json", {})


def save_users(users: dict) -> None:
    _write_json("users.json", users)


def log_damage(message: str) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with (DATA_DIR / "damage_reports.log").open("a", encoding="utf-8") as file:
        file.write(message.rstrip() + "\n")
