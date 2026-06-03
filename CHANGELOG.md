# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

> Changes staged for the next release will appear here.

---

## [0.1.0] - 2026-06-02

### Added

- `pre-commit install` instructions and code quality commands in `README.md`
- Pre-commit hooks (`ruff`, `mypy`, file-hygiene checks, `no-commit-to-branch`)
- mypy strict mode configured in `pyproject.toml`
- Ruff linter and formatter configured in `pyproject.toml`
- `README.md` with project overview, stack, and getting started guide
- `ROADMAP.md` with phased delivery plan and current status
- `CHANGELOG.md` following Keep a Changelog convention
- `docs/vision/vision-document.md` — product vision, target audience, success metrics, and constraints
- `docs/adr/ADR-0001-use-of-architecture-decision-records.md` — ADR format adoption
- `docs/adr/ADR-0002-backend-technology-stack.md` — backend stack decision (Python 3.12, FastAPI, PostgreSQL, SQLAlchemy 2.0, Pydantic v2, uv, Ruff, mypy, Docker)
- MIT License

[Unreleased]: https://github.com/P-Drop/chemlab-api/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/P-Drop/chemlab-api/releases/tag/v0.1.0
