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