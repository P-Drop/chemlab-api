# ChemLab API

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Code style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

**ChemLab** is an open-source virtual chemistry laboratory REST API designed for Secondary Education students in Spain (ESO and Bachillerato). It powers interactive simulations, a periodic table explorer, and curriculum-aligned exercises — all accessible from the browser, no lab required.

> 🚧 **Early development.** The API is not yet publicly deployed. Follow the [Roadmap](./ROADMAP.md) for progress updates.

---

## Why ChemLab?

Most public secondary schools in Spain lack the resources, space, or time for regular lab sessions. ChemLab fills that gap with a browser-based virtual lab where students can explore chemical elements, observe simulated reactions, and practice exercises aligned with the official curriculum.

---

## Tech stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Framework | FastAPI |
| Database | PostgreSQL 16 |
| ORM | SQLAlchemy 2.0 (async) |
| Validation | Pydantic v2 |
| ASGI server | Uvicorn / Gunicorn |
| Dependency manager | uv |
| Linter & formatter | Ruff |
| Type checker | mypy |
| Testing | pytest + pytest-asyncio + httpx |
| Containerisation | Docker + Docker Compose |

Architecture decisions are documented in [`docs/adr/`](./docs/adr/).

---

## Project structure

```
chemlab-api/
├── docs/
│   ├── adr/                  # Architecture Decision Records
│   └── vision/               # Product Vision document
├── src/
│   └── chemlab/              # Application source (coming in Phase 0)
├── tests/                    # Test suite (coming in Phase 1)
├── scripts/                  # Utility scripts (seed, migrations, etc.)
├── docker-compose.yml        # Local development services
├── Dockerfile                # API container definition
├── pyproject.toml            # Dependencies, Ruff, mypy config
├── uv.lock                   # Locked dependency versions
├── .python-version           # Python version pin (3.12)
├── CHANGELOG.md
├── ROADMAP.md
└── README.md
```

> Folders marked as "coming in Phase X" are planned but not yet created.

---

## Setup

> ⚠️ Full local setup (Docker, environment variables, database) will be documented once Phase 0 infrastructure is complete (v0.2.0).

### Prerequisites
- [uv](https://docs.astral.sh/uv/) - dependency and environment manager

### Local development

```bash
# Clone the repository
git clone https://github.com/P-Drop/chemlab-api.git
cd chemlab-api

# Create virtual environment and install dependencies (including dev tools)
uv sync

# Install pre-commit hooks (run once after cloning)
uv run pre-commit install

# Verify setup
uv run python --version

```

> **Why `pre-commit install`?** This activates the Git hooks defined in
> `.pre-commit-config.yaml`. From this point on, every `git commit` automatically
> runs the linter, formatter, type checker and a set of file-hygiene checks.
> Commits that fail any of these checks are aborted before they are created.

### Code quality

The project enforces a strict quality baseline via pre-commit hooks and CI. You can run the same checks manually at any time:


```bash
# Run all pre-commit hooks against the entire repository
uv run pre-commit run --all-files

# Linter
uv run ruff check --fix .

# Formatter
uv run ruff format .

# Static type checker
uv run mypy src/
```


Check back once the `v0.2.0` milestone is closed for a working local setup guide.

---

## Roadmap

See [ROADMAP.md](./ROADMAP.md) for the full delivery plan across three phases:

- **Phase 1 (Month 2):** Periodic table REST API — 118 elements, OpenAPI docs, deployed.
- **Phase 2 (Month 4):** Exercise engine with automatic feedback.
- **Phase 3 (Month 6):** Student progress persistence and teacher dashboard.

---

## Contributing

This project is in early development and not yet ready for external contributions. A `CONTRIBUTING.md` guide will be added at the start of Phase 1.

---

## License

Distributed under the [MIT License](./LICENSE). © 2026 P-Drop.
