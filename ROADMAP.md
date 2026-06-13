# Roadmap

This document describes the planned delivery phases for ChemLab. It is updated at the end of each phase.

For a detailed history of changes, see [CHANGELOG.md](./CHANGELOG.md).

---

## Current status

**Phase 0 — Repository % project foundation · ✅ Done (v0.2.0)**

Next up: **Phase 1 — MVP: Periodic table API** · 🔄 In progress · Target: Month 2

---

## Phase 0 — Repository & project foundation · ✅ Done

> Goal: professional repository baseline before writing any production code.

| Task | Status |
|---|---|
| Repository structure and `.gitignore` | ✅ Done |
| Product Vision document | ✅ Done |
| ADR-0001: Use of Architecture Decision Records | ✅ Done |
| ADR-0002: Backend technology stack | ✅ Done |
| `README.md`, `ROADMAP.md`, `CHANGELOG.md` | ✅ Done |
| `pyproject.toml` with uv, Ruff, mypy | ✅ Done |
| `Dockerfile` + `docker-compose.yml` (dev) | ✅ Done |
| CI pipeline — lint, type-check, test (GitHub Actions) | ✅ Done |
| Pre-commit hooks (Ruff, mypy) | ✅ Done |

---

## Phase 1 — MVP: Periodic table API · 🔄 In progress · Target: Month 2

> Goal: deployable REST API serving structured data for all 118 chemical elements, with automated tests and live documentation.

| Task | Status |
|---|---|
| Database schema for chemical elements | 🔄 In progress |
| Alembic migration strategy (ADR pending) | 🔄 In progress |
| Seed script — 118 elements dataset | 🔄 In progress |
| `GET /elements` — list all elements | 🔄 In progress |
| `GET /elements/{symbol}` — element detail | 🔄 In progress |
| Pydantic response schemas | 🔄 In progress |
| Unit and integration tests (≥ 80 % coverage) | 🔄 In progress |
| OpenAPI docs available at `/docs` | 🔄 In progress |
| Production deployment + CI/CD (ADR pending) | 🔄 In progress |

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
