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

## Wegwerf-Testinstanz (manuelles Testen)

Für einen manuellen Test im Browser, ohne Postgres-Dump (siehe README für die Variante mit Dump):

1. MailHog starten: `docker run -d --rm --name gb-mailhog -p 127.0.0.1:8025:8025 mailhog/mailhog`.
   Mails lesen unter http://localhost:8025.
2. SQLite-DB unter `/data` anlegen (`.docker-cache/data/gartenberg/`) und Demo-Daten per
   `tooling/docker.sh gartenberg manage shell < script.py` einspielen (stdin geht, kein eigenes `docker run`).
   `JUNTAGRICO_DATABASE_NAME=/data/preview.db` setzen, `migrate`, Benutzer `test`/`test` anlegen
   (`createsuperuser --noinput` mit `DJANGO_SUPERUSER_*`; existiert er schon, Passwort in der Shell setzen).
3. Server starten: `JUNTAGRICO_DATABASE_NAME=/data/preview.db JUNTAGRICO_EMAIL_HOST=<mailhog-ip> JUNTAGRICO_EMAIL_PORT=1025 JUNTAGRICO_HTTPS_ONLY=False tooling/docker.sh gartenberg runserver 8000`
   (im Hintergrund starten, Log umleiten).
4. Aufräumen: `docker stop juntagrico-tooling-gartenberg-8000 gb-mailhog`.

Fallstricke:
- **SMTP-Host:** `172.17.0.1` stimmt nicht zwingend. Die Container laufen im Bridge-Netz, dessen Gateway
  hier `10.200.0.1` ist, und der Host-Weg war blockiert (Timeout, der Versand "hängt"). Zuverlässig ist die
  IP des MailHog-Containers im selben Netz: `docker inspect gb-mailhog -f '{{.NetworkSettings.Networks.bridge.IPAddress}}'`.
- **Whitelist:** `runserver` läuft mit DEBUG, dann versendet das Mail-Backend nur an `WHITELIST_EMAILS`
  (`settings.py`). Demo-Mitglieder mit anderen Adressen ergeben "E-Mail(s) konnten nicht gesendet werden".
  Demo-Mitglieder deshalb mit einer Adresse aus der Whitelist anlegen. Die Empfängerzahl am Senden-Button
  zählt trotzdem alle, der Filter greift erst beim Versand.
- **Standarddaten:** Ein frisches `migrate` legt von juntagrico die Kategorie "Kategorie 1" mit dem Paket
  "Normales Abo" an; sie erscheint in Auswahlfeldern, in der Produktion nicht.
- **Abo-Testdaten:** juntagrico validiert Datumsangaben streng (Enddatum braucht Kündigungsdatum, Bestandteile
  müssen zum Aktivierungsdatum des Abos passen, ein nicht gekündigtes Abo braucht einen aktiven Bestandteil).
  `gartenberg/tests/test_email_category.py` zeigt funktionierende Beispiele.
- Für automatisierte Browser-Tests stattdessen `e2e/run.sh` (eigener Compose-Stack mit MailHog).
