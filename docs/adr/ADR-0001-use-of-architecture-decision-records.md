## Status

Accepted — 2026-05-24

## Context

During the project's development, significant technical decisions will be made (stack choice, architecture patterns, libraries, deployment strategies) that will affect the long-term design. Without a structured record, these decisions get lost or are reinterpreted over time, making it harder to onboard new contributors and to review decisions retrospectively.

## Decision
The ADR (Architecture Decision Record) format proposed by Michael Nygard will be adopted to document every relevant architectural decision. ADRs:

- Will be stored in `/docs/adr/` within the repository.

- Will follow the naming convention `NNNN-title-in-kebab-case.md`.

- Will be immutable once accepted: if a decision changes, a new ADR is created to supersede the previous one (status: "Superseded by ADR-NNNN").

- Will contain the sections: Status, Context, Decision, Consequences, Considered alternatives.

## Consequences

**Positive**

- Historical traceability of technical decisions.
- Faster onboarding for future contributors.
- Reinforces structured thinking before deciding.

**Negative**

- Time overhead in writing them.
- Risk of documentation bloat if the format is overused.

## Considered alternatives

- **GitHub Wiki:** discarded due to decoupling from the code.
- **Commit comments:** discarded due to low visibility.
- **No documentation:** discarded due to long-term loss of context.
