# ChemLab API

[![CI](https://github.com/P-Drop/chemlab-api/actions/workflows/ci.yml/badge.svg)](https://github.com/P-Drop/chemlab-api/actions/workflows/ci.yml)
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

---

## Architecture decisions

Significant technical decisions are recorded as Architecture Decision Records (ADRs) in [`docs/adr/`](./docs/adr/), following the MADR format:

- [ADR-0001 — Use of Architecture Decision Records](./docs/adr/ADR-0001-use-of-architecture-decision-records.md)
- [ADR-0002 — Backend technology stack](./docs/adr/ADR-0002-backend-technology-stack.md)
- [ADR-0003 — Chemical elements dataset selection](./docs/adr/ADR-0003-chemical-elements-dataset-selection.md)

---

## Project structure

```
chemlab-api/
├── .github
│    ├── ISSUE_TEMPLATE             # Issue templates and chooser config
│    │   ├── bug.md
│    │   ├── chore.md
│    │   ├── config.yml
│    │   └── feature.md
│    ├── pull_request_template.md   # Pull request template
│    └── workflows
│        └── ci.yml                 # CI pipeline (lint, type-check, tests)
├── docs/
│   ├── adr/                        # Architecture Decision Records
│   └── vision/                     # Product Vision document
├── src/
│   └── chemlab_api/
|       ├── main.py                 # Application entry point (composition)
|       ├── py.typed                # PEP 561 marker
|       ├── core/
|       |   └── config.py           # Application settings (Pydantic)
|       └── api/
|           └── v1/
|               ├── router.py       # Aggregator for v1 endpoints
|               └── endpoints/
|                   └── health.py   # /health endpoint
├── tests/
|   ├── conftest.py                 # Shared fixtures (async HTTP client)
|   └── api/
|       └── v1/
|           └── test_health.py      # Tests for /health endpoint
├── scripts/                        # Utility scripts (seed, migrations, etc.)
├── docker-compose.yml              # Local development services
├── Dockerfile                      # API container definition
├── .dockerignore
├── pyproject.toml                  # Dependencies, Ruff, mypy config
├── uv.lock                         # Locked dependency versions
├── .pre-commit-config.yaml         # Git hooks configuration
├── .env.example                    # Environment variables template
├── .python-version                 # Python version pin (3.12)
├── CHANGELOG.md
├── ROADMAP.md
└── README.md
```


---

## Setup

> ℹ️ A containerised setup for the API is available — see [Running with Docker](#running-with-docker). PostgreSQL integration arrives in Phase 1; the current image runs the API with no database yet.

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

> **Windows users:** `uvicorn[standard]` includes `uvloop`, a high-performance
> event loop that is **not available on native Windows**. The package will
> install without errors, but `uvloop` is silently skipped on that platform —
> Uvicorn falls back to the standard asyncio loop. There is no functional
> impact, only a minor performance difference. For full parity with Linux/macOS
> development, we recommend using [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install).

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

### Testing

The test suite uses **pytest** with async support and enforces a minimum coverage threshold of 80%.

```bash
# Run the full test suite
uv run pytest

# Run a specific test file
uv run pytest tests/api/v1/test_health.py

# Run with verbose output
uv run pytest -v

# Skip coverage measurement (faster iteration during development)
uv run pytest --no-cov
```

After each run, an HTML coverage report is generated under `htmlcov/`. Open `htmlcov/index.html` in a browser to inspect which lines are covered.

> **Coverage in CI.** The same suite produces a `coverage.xml` report consumed by the CI pipeline (see Phase 0 roadmap). Coverage below the configured threshold will cause the pipeline to fail.

### Running the API

Start the development server with hot reload:

```bash
uv run uvicorn chemlab_api.main:app --reload --port 8030
```

Once the server is running, the following endpoints are available:

| URL | Description |
| --- | ---|
| `http://127.0.0.1:8030/api/v1/health` | Health check (returns `{"status": "ok"}`) |
| `http://127.0.0.1:8030/docs` | Swagger UI - interactive API documentation |
| `http://127.0.0.1:8030/redoc` | ReDoc - alternative API documentation |
| `http://127.0.0.1:8030/openapi.json` | Raw OpenAPI specification |

> The `--reload` flag is for development only. It restarts the server
> automatically when source files change. **Do not use `--reload` in production.**

### Running with Docker

The API ships with a multi-stage `Dockerfile` and a `docker-compose.yml` for a one-command local setup, with the closest parity to the future production environment.

**Prerequisites:** Docker and Docker Compose v2 (v2.24+).

```bash
# Create your local env file from the template (first time only)
cp .env.example .env

# Build the image and start the API
docker compose up --build
```

The API is then available at `http://localhost:8030/api/v1/health` (Swagger UI at `/docs`).

**What you get out of the box:**

- **Hot reload:** `./src` is mounted into the container, so editing code reloads the server automatically - no rebuild needed.
- **Health check:** `docker compose ps` reports the service as `healthy` once `/api/v1/health` responds.
- **Configurable host port:** the container always listens on `8030` internally. To expose it on a different port, set `API_PORT` in `.env` (e.g. `API_PORT=9000` → `http://localhost:9000`).


Stop and remove the containers with:

```bash
docker compose down
```

> Changing dependencies (`pyproject.toml` / `uv.lock`) requires a rebuild (`docker compose up --build`). Editing application code does not.


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
