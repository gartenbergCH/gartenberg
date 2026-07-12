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
