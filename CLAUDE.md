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
