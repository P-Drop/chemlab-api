## Status

Accepted - 2026-06-01

## Context

The Vision Document defines the ChemLab project: a virtual chemistry laboratory accessible from the browser. For the MVP (Phase 1), a REST API must be built to serve structured information about the elements of the periodic table. It is essential to implement a scalable solution that serves as the foundation for building learning modules and exercises with compounds and reactions.

The priority decision at this point is the technology stack, which will condition the rest of the development. It is worth doing this precisely, since changing the stack in a later phase may entail costly refactors or, in the worst case, complete rewrites.

Likewise, the stack must be consistent with the constraints set out in the Vision Document: solo development on a part-time schedule, the author's main proficiency in Python, and the need to comply with GDPR in future phases.

This ADR covers the decisions regarding:

- Python version
- Backend framework
- Dependency management
- ORM and relational database
- Data validation
- Testing and code-quality tools (linter/formatter)
- ASGI server
- Containerization

Out of scope and to be documented in their own ADRs:

- Frontend framework
- Database migration strategy
- Authentication and authorization strategy
- Deployment platform and CI/CD

## Decision

##### 1. Language and runtime - Python 3.12

Python 3.12 is chosen as a consolidated stable version, with official support until October 2028 and mature compatibility with the stack's library ecosystem (FastAPI, SQLAlchemy 2.0, Pydantic v2).

##### 2. Backend framework - FastAPI

FastAPI is chosen for its API-first approach with native async/await support (relevant for scaling concurrent I/O and for future integration with a decoupled frontend). FastAPI generates the OpenAPI specification automatically, which reduces the maintenance cost of keeping the API documentation in sync.

##### 3. Dependency manager - uv

uv is chosen as a unified manager of dependencies, virtual environments, and Python versions. It replaces the traditional pip + virtualenv + pyenv stack with a single tool, with reproducibility via `uv.lock` and far superior performance thanks to its Rust core. Its consistency with Ruff —both from the same provider (Astral)— is valued positively, as it reduces the heterogeneity of the stack.

##### 4. ORM and database - SQLAlchemy 2.0 (async) + PostgreSQL

To implement a relational data model for chemical elements, PostgreSQL is chosen as the DBMS due to the robustness provided by its relational structure and strong typing. In addition, native JSONB support allows storing semi-structured data (variable properties, exercise metadata) without giving up the relational model, and its extensibility features make scaling toward new scientific data models easier. Its permissive open-source license (PostgreSQL License), with no costs or vendor lock-in, is also valued positively.

To implement an ORM, the Python standard SQLAlchemy 2.0 is chosen, as it provides consolidated maturity for CRUD operations, asynchronous queries, and automatic prevention of SQL injection by using parameterized queries. This solution is database-engine agnostic, which makes it compatible with scaling toward a complementary non-relational data model.

##### 5. Validation - Pydantic v2

Pydantic v2 is chosen for its native integration with FastAPI (input validation and declarative output serialization via type hints) and its performance, thanks to a core rewritten in Rust that significantly reduces validation cost compared to v1.

##### 6. ASGI server - Uvicorn (dev) | Gunicorn + Uvicorn workers (production)

Uvicorn is the reference ASGI implementation and the server officially recommended by FastAPI. In development it is run directly (`uvicorn --reload`). In production it runs under Gunicorn as a process manager, which allows spawning multiple workers to take advantage of several cores, handling automatic restarts on failure, and decoupling the process lifecycle from the ASGI server.

##### 7. Containerization - Docker + Docker Compose

Docker + Docker Compose is adopted from the start of the project. It provides parity across development, CI, and production environments. Compose orchestrates the required services (API, PostgreSQL, future: cache, messaging) and reduces contributor onboarding to a single command (`docker compose up`). It also lays the technical groundwork for the future integration of CI/CD and containerized deployment.

##### 8. Testing - pytest + pytest-asyncio + pytest-cov + httpx

pytest is chosen as the testing framework for its maturity in the Python ecosystem, its declarative syntax, and its fixture system, which allows injecting reusable dependencies into the tests (HTTP client, test DB session, seed data) in an explicit and composable way.

Additional plugins:

- **pytest-asyncio:** allows writing asynchronous tests. It is necessary since FastAPI is an async framework.
- **pytest-cov:** measures the code coverage executed by the tests and generates reports (terminal, HTML, XML for CI). It allows setting a minimum coverage threshold as a quality criterion.
- **httpx:** HTTP client used to invoke FastAPI endpoints from the tests (via `TestClient` or `AsyncClient`), validating the API's end-to-end behavior without needing to spin up a real server.

##### 9. Code quality - Ruff (linter + formatter) + mypy

Ruff is adopted as a unified linter and formatter. It replaces the traditional Black (formatting) + isort (import sorting) + Flake8 and its plugins (linting) stack, centralizing everything in a single tool configurable via `pyproject.toml`. Its Rust core offers execution times several orders of magnitude below the tools it replaces, which allows integrating it smoothly into pre-commit hooks and CI. Additionally, it shares its provider (Astral) with uv, which reduces tooling heterogeneity.

mypy is adopted as a static type checker. Unlike Pydantic (which validates external data at runtime), mypy analyzes the source code without executing it and detects type inconsistencies at development time (unchecked `None` variables, calls with incorrect types, etc.). Combined use with Pydantic v2 is especially smooth, since its models generate types that mypy interprets natively.

## Consequences

##### Positive

- **Environment reproducibility:** Docker + uv guarantee that any contributor (or the CI/CD pipeline) can spin up exactly the same environment with a single command, eliminating machine-dependent runtime errors.

- **Functional extensibility:** FastAPI's API-first approach allows adding a decoupled frontend (Vue/React) or integrating additional consumers (mobile, scripts, other APIs) without modifying the logic layer. PostgreSQL, in turn, supports growth of the data model without migrating to another engine.

- **Technical quality safeguarded from day 1:** linter, formatter, typed validation (mypy), and automated testing are applied in pre-commit and CI, catching errors before they reach production and enforcing a homogeneous quality standard throughout development.

- **Automatic API documentation:** endpoints are documented automatically by FastAPI via OpenAPI/Swagger at `/docs`. This removes the need to maintain API documentation in external tools and guarantees that the documentation never falls out of sync with the code.

- **Async from day 1:** The chosen stack allows handling multiple concurrent I/O operations without blocking. This foundation is essential for future integration of calls to external APIs (PubChem, chemical datasets) or long asynchronous processes without needing to refactor.

- **Learning aligned with the market:** The stack chosen for this project (FastAPI, Pydantic v2, SQLAlchemy 2.0 async, Ruff, uv) matches tools commonly found in current Python backend development job postings. This aligns the project's solo development with the author's professional path, turning the invested learning into an employability asset.

##### Trade-offs assumed

- **Services not included in the framework:** FastAPI does not provide a ready-to-use admin panel, authentication system, or user manager. These components will have to be built manually or integrated via external libraries (SQLAdmin, fastapi-users, etc.) in the corresponding phases. **Decisions deferred to their specific ADRs.**

- **Initial configuration cost:** professional tooling (Docker, pre-commit, mypy, Ruff, pytest, CI configuration) requires a significant investment of time in the first weeks before starting to produce business code. This cost is amortized over the course of the project, but it penalizes the initial pace.

- **Continuous friction from typing and strict quality:** mypy in strict mode and the linter will reject code that would pass in more lax projects. This raises the average quality but occasionally slows development, especially while internalizing the conventions.

- **Uneven tooling maturity:** Although the bulk of the stack is mature (FastAPI, SQLAlchemy, PostgreSQL, Docker), some tools are more recent (such as uv and, to a lesser extent, Ruff). The risk of disruptive changes in their APIs or loss of momentum is assumed. It is mitigated by pinning versions in `pyproject.toml` and monitoring the official repositories.

- **Technical learning curve:** The stack includes several technologies the author does not yet master (SQLAlchemy 2.0 async, asyncio in depth, strict mypy, advanced Docker configuration). This learning cost is accepted as a formative investment aligned with the project's professional goal.

## Considered alternatives

##### Backend framework

- **Django (+ Django REST Framework):** a mature, batteries-included framework (its own ORM, auto-generated admin panel, authentication system, templates, middleware), widely adopted in the Spanish job market. Discarded because ChemLab is an API-first project with a planned decoupled frontend, which leaves much of the Django ecosystem unused (templates, forms system, traditional middleware). Additionally, async support, typed validation with Pydantic, and automatic OpenAPI generation would require additional layers on top of Django, whereas FastAPI offers them out of the box. It is acknowledged that Django Admin would be a real asset for the Phase 3 teaching panel; this trade-off is already documented in the Consequences section.

- **Flask:** a minimalist Python web framework, with a large ecosystem of extensions and a very consolidated community. Discarded because it lacks first-class async support, native typed validation, and automatic OpenAPI generation; all these features, key to the project, would require integrating external libraries (Marshmallow, flask-async, flasgger, etc.). The result would end up reproducing what FastAPI offers natively, but with higher maintenance cost and less coherence.

##### Dependency manager

- **Poetry:** a mature dependency manager with a lockfile, virtual-environment management, integrated PyPI publishing, and highly valued features that have made it a de facto standard in recent years. uv is chosen because its Rust core makes it several orders of magnitude faster than Poetry (Python). In addition, uv brings extra benefits to this project, such as integrated Python version management and consistency with Ruff, with which it shares a provider. Poetry is considered a solid alternative, although the decision is to assume the risk of uv's youth in exchange for simplicity and speed.

- **Traditional pip + venv:** the historical standard combination from Python's stdlib. Discarded for this project because, without additional tools such as `pip-tools`, it does not provide a reproducible lockfile or deterministic dependency resolution, and it requires orchestrating several tools (pip, venv, pyenv) separately.

##### Code quality

- **Black + isort + Flake8 (+pylint):** a traditional stack with specialized components for formatting, import sorting, and linting respectively. Discarded because Ruff replaces all three with a single tool, with centralized configuration in `pyproject.toml` and far superior speed (Rust core). Speed is key to integrating verification into pre-commit hooks without penalizing the workflow.
