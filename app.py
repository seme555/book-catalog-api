"""Small Flask + SQLite book catalog API."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from flask import Flask, jsonify, request

DB_PATH = Path(__file__).with_name("books.db")

app = Flask(__name__)


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER
            )
            """
        )


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/books")
def list_books():
    with get_db() as conn:
        rows = conn.execute(
            "SELECT id, title, author, year FROM books ORDER BY id"
        ).fetchall()
    return jsonify([dict(row) for row in rows])


@app.get("/books/<int:book_id>")
def get_book(book_id: int):
    with get_db() as conn:
        row = conn.execute(
            "SELECT id, title, author, year FROM books WHERE id = ?",
            (book_id,),
        ).fetchone()
    if row is None:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(dict(row))


@app.post("/books")
def create_book():
    payload = request.get_json(silent=True) or {}
    title = (payload.get("title") or "").strip()
    author = (payload.get("author") or "").strip()
    year = payload.get("year")

    if not title or not author:
        return jsonify({"error": "title and author are required"}), 400

    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO books (title, author, year) VALUES (?, ?, ?)",
            (title, author, year),
        )
        book_id = cursor.lastrowid
        row = conn.execute(
            "SELECT id, title, author, year FROM books WHERE id = ?",
            (book_id,),
        ).fetchone()
    return jsonify(dict(row)), 201


@app.put("/books/<int:book_id>")
def update_book(book_id: int):
    payload = request.get_json(silent=True) or {}
    title = (payload.get("title") or "").strip()
    author = (payload.get("author") or "").strip()
    year = payload.get("year")
