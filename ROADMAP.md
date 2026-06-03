# Roadmap

This document describes the planned delivery phases for ChemLab. It is updated at the end of each phase.

For a detailed history of changes, see [CHANGELOG.md](./CHANGELOG.md).

---

## Current status

**Phase 0 — Repository setup · 🔄 In progress**

---

## Phase 0 — Repository & project foundation

> Goal: professional repository baseline before writing any production code.

| Task | Status |
|---|---|
| Repository structure and `.gitignore` | ✅ Done |
| Product Vision document | ✅ Done |
| ADR-0001: Use of Architecture Decision Records | ✅ Done |
| ADR-0002: Backend technology stack | ✅ Done |
| `README.md`, `ROADMAP.md`, `CHANGELOG.md` | ✅ Done |
| `pyproject.toml` with uv, Ruff, mypy | 🔲 Planned |
| `Dockerfile` + `docker-compose.yml` (dev) | 🔲 Planned |
| CI pipeline — lint, type-check, test (GitHub Actions) | 🔲 Planned |
| Pre-commit hooks (Ruff, mypy) | 🔲 Planned |

---

## Phase 1 — MVP: Periodic table API · 🔲 Planned · Target: Month 2

> Goal: deployable REST API serving structured data for all 118 chemical elements, with automated tests and live documentation.

| Task | Status |
|---|---|
| Database schema for chemical elements | 🔲 Planned |
| Alembic migration strategy (ADR pending) | 🔲 Planned |
| Seed script — 118 elements dataset | 🔲 Planned |
| `GET /elements` — list all elements | 🔲 Planned |
| `GET /elements/{symbol}` — element detail | 🔲 Planned |
| Pydantic response schemas | 🔲 Planned |
| Unit and integration tests (≥ 80 % coverage) | 🔲 Planned |
| OpenAPI docs available at `/docs` | 🔲 Planned |
| Production deployment + CI/CD (ADR pending) | 🔲 Planned |

---

## Phase 2 — Exercises and automatic feedback · 🔲 Planned · Target: Month 4

> Goal: interactive exercise module with automated correction and student feedback.

| Task | Status |
|---|---|
| Exercise data model (questions, answers, hints) | 🔲 Planned |
| `POST /exercises/{id}/answer` — answer validation | 🔲 Planned |
| Automatic feedback engine | 🔲 Planned |
| First learning module aligned with ESO curriculum | 🔲 Planned |
| Authentication strategy (ADR pending) | 🔲 Planned |

---

## Phase 3 — Progress persistence and teacher panel · 🔲 Planned · Target: Month 6

> Goal: student progress tracking and a teacher-facing dashboard.

| Task | Status |
|---|---|
| User and progress data model | 🔲 Planned |
| `GET /students/{id}/progress` | 🔲 Planned |
| Teacher dashboard (read-only) | 🔲 Planned |
| GDPR compliance review | 🔲 Planned |

---

## Out of scope (v1)

- Replacing official curriculum or formal assessment
- Replacing real lab practice where available
- Content beyond the Spanish Secondary Education framework

---

## Legend

| Symbol | Meaning |
|---|---|
| ✅ Done | Merged to `main` |
| 🔄 In progress | Active development |
| 🔲 Planned | Scoped, not started |
| ⏸ On hold | Deprioritised |
