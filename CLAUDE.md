# Project context

This project follows the AI Unified Process. Before making product, domain, or architecture decisions, read:

- the use case or test case you work on, under `docs/use_cases/` and `docs/test_cases/`
- only the `FR-*`, `NFR-*`, and `C-*` rows of `docs/requirements.md` that the use case links on its
  `**Requirements:**` line, never the whole catalog
- `docs/entity_model.md`, and `docs/glossary.md` when it exists
- the accepted architecture decision records under `docs/architecture/decisions/`
- `docs/architecture/stack.md` when the project combines layer plugins
- `docs/open_questions.md` when it exists
- `docs/vision.md` and the whole `docs/requirements.md` only when you work on the requirements themselves

## Workflow rules

1. Derive requirements from the product vision.
2. Reconcile the entity model and use case diagram when requirements change.
3. Do not implement a use case before its `UC-*.md` specification exists and its `**Status:**` is `Approved`.
4. Keep requirement, use case, and test case identifiers stable and traceable in code and tests.
5. Build and test with the installed plugins: with layer plugins, run `/use-case-implement` and `/use-case-test`,
   which follow the layers in `docs/architecture/stack.md` (set it up with `/stack`); with a combined stack plugin,
   run its `/implement` and test skills.
6. Review and preserve the conventions already established in the codebase.
7. Record a gap or contradiction in a specification with `/open-questions` instead of assuming an answer.
8. Follow the accepted architecture decision records; record a new architecture decision with
   `/architecture-decision`, linked to the non-functional requirement or constraint it serves.

## Verification

Run the project's documented build, static analysis, and test commands after implementation. Report any verification
that could not be completed.

# GartenBerg

Projekt-spezifische Anpassungen rund um die [Juntagrico](https://juntagrico.org/)-Plattform
für die Genossenschaft GartenBerg.

## Workflow

- **Keine Feature Branches.** Es wird direkt auf `main` gearbeitet und committet.

## Dokumentation

- [docs/e2e-reference.md](docs/e2e-reference.md) — Nicht-offensichtliche Fallstricke (Lessons
  Learned) aus der Implementierung der Playwright-E2E-Tests. **Bitte diese Referenz
  konsultieren, sobald E2E-Tests geschrieben oder angepasst werden sollen.**
- [docs/e2e-testcases.md](docs/e2e-testcases.md) — Überblick über die durch die E2E-Tests
  abgedeckten Funktionalitäten, gruppiert nach Funktionsblock. **Bitte aktuell halten, wenn
  sich die Testabdeckung ändert — insbesondere wenn neue Testfälle geschrieben werden.**

## E2E-Tests

- Bei allen E2E-Tests, die geschrieben werden, an Schlüsselmomenten Screenshots erstellen.

## Tooling

All runtime commands must be run via `tooling/docker.sh` — never call `python`/`pip`/`manage.py`
directly. This ensures a consistent environment without requiring a local Python installation.

Available commands:
- `tooling/docker.sh test`            — run the Django test suite
- `tooling/docker.sh manage ...`      — arbitrary Django management command

For one-off scripts outside these commands (e.g. `docker run ... manage.py shell`), watch out for:
- Bind-mounting a script into a path already inside the project's own mount (a second `-v` under
  `/opt`) makes Docker create an empty file at that path on the **host** as a mount-point side
  effect. Pipe the script via stdin instead (`cat script.py | docker run -i ...`).
- Plain `docker run` (not through this wrapper) executes as root, so anything Django writes
  (`gartenberg.db`, `gartenberg.log`) lands root-owned in the repo and can't be `rm`'d without
  another container. Point `JUNTAGRICO_DATABASE_NAME` at a path outside `/opt` (e.g.
  `/tmp/preview.db`) for throwaway runs.
