# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added

- Ruff linter and formatter configured in `pyproject.toml`
- mypy strict mode configured in `pyproject.toml`
- Pre-commit hooks (`ruff`, `mypy`, file-hygiene checks, `no-commit-to-branch`)
- `pre-commit install` instructions and code quality commands in `README.md`
- FastAPI and Uvicorn as production dependencies
- Modular application structure (`core/`, `api/v1/endpoints/`)
- `GET /api/v1/health` endpoint with typed Pydantic response model
- Centralised application settings via `pydantic-settings`
- API metadata (title, description, version) wired into Swagger UI and ReDoc
- Local API startup instructions in `README.md`
- pytest, pytest-asyncio, pytest-cov and httpx as dev dependencies
- Test suite scaffolding under `tests/` with shared `AsyncClient` fixture
- First tesst suite for the `/health` endpoint
- Pytest and coverage configuration in `pyproject.toml` (asyncio mode, branch coverage, HTML + XML reports, 80% threshold)
- `py.typed` marker exposing the package's type information to mypy
- Testing instructions in `README.md`
- Multi-stage `Dockerfile` for the API image (uv-based install, non-root runtime stage)
- `docker-compose.yml` with an `api` service (hot-reload, healthcheck, `API_PORT`-configurable host port)
- `.dockerignore` to scope the Docker build context
- `.env.example` template documenting supported environment variables
- "Running with Docker" guide in `README.md`
- GitHub Actions CI pipeline runnig Ruff (lint + format check), mypy and pytest with coverage on every push to `main` and pull request; coverage report uploaded as a workflow artifact
- CI status badge in `README.md`

### Changed

- Translate all GitHub issue and PR templates to English for repository-wide language consistency
- Fix issue template YAML frontmatter so the templante chooser is displayed at /issue/new/choose
- Local development now documented to run on port `8030` for parity with the Docker setup


---

## [0.1.0] - 2026-06-02

### Added

- `README.md` with project overview, stack, and getting started guide
- `ROADMAP.md` with phased delivery plan and current status
- `CHANGELOG.md` following Keep a Changelog convention
- `docs/vision/vision-document.md` — product vision, target audience, success metrics, and constraints
- `docs/adr/ADR-0001-use-of-architecture-decision-records.md` — ADR format adoption
- `docs/adr/ADR-0002-backend-technology-stack.md` — backend stack decision (Python 3.12, FastAPI, PostgreSQL, SQLAlchemy 2.0, Pydantic v2, uv, Ruff, mypy, Docker)
- MIT License

[Unreleased]: https://github.com/P-Drop/chemlab-api/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/P-Drop/chemlab-api/releases/tag/v0.1.0
