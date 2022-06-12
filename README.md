# Book Catalog API

Introductory Flask + SQLite CRUD API for a small book catalog.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/books` | List books |
| GET | `/books/<id>` | Get one book |
| POST | `/books` | Create book (`title`, `author`, optional `year`) |
| PUT | `/books/<id>` | Update book |
| DELETE | `/books/<id>` | Delete book |

## Setup