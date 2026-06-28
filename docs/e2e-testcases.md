# E2E-Test-Abdeckung

Überblick über die Funktionalitäten, die durch die Playwright-E2E-Tests (`e2e/tests/`) abgedeckt
sind — gruppiert nach Funktionsblock. Es geht hier bewusst **nicht** um die genauen Abläufe oder
Assertions, sondern um einen schnellen Überblick, was grob getestet wird.

> Diese Datei aktuell halten, wenn sich die Testabdeckung ändert — insbesondere beim Hinzufügen
> neuer Testfälle. Implementierungs-Fallstricke siehe [e2e-reference.md](e2e-reference.md).

---

## Registrierung & Mitgliedschaft

- **Signup-/Abo-Wizard** (`test_registration.py`, plus implizit über das `member_context`-Fixture
  in jedem Member-Test): kompletter Anmeldeflow — Personendaten, Abo-Bestandteile, Depotwahl,
  Startdatum, Co-Member, Anteilscheine, Zusammenfassung, Welcome-Seite.
- **Eingeloggt nach Signup**: gültige Session und korrekt befülltes Profil direkt nach der
  Registrierung.
- **Mitgliedschaft kündigen** (`test_membership_cancel.py`): Kündigung wird bei aktivem/zukünftigem
  Abo blockiert (Danger-Alert statt Formular).

## Profil & Passwort

- **Profil bearbeiten** (`test_profile.py`): Telefonnummer ändern, Persistenz über Reload; Name und
  E-Mail als (deaktivierte) Felder vorhanden.
- **Passwort ändern** (`test_z_password.py`): Passwortwechsel und anschliessender Login mit dem
  neuen Passwort in frischem Browser-Kontext. (Läuft als letzter Test — `z`-Präfix.)

## Einsätze / Jobs

- **Job-Anmeldung** (`test_jobs.py`): Job-Detail (Titel, Zeit, Beschreibung), Anmeldung erhöht
  belegte Slots.
- **Einsatz melden** (`test_assignment_request.py`): Mitglied meldet einen geleisteten Einsatz.
- **Tätigkeitsbereiche** (`test_areas.py`): Bereichsliste und -detail, Bereich beitreten und wieder
  verlassen.

## Abo, Depot & Anteilscheine (Member-Sicht)

- **Depot-Details** (`test_depot.py`): Depot-Detailseite mit Abschnittslabels und konkretem
  Depot-Namen.
- **Anteilscheine** (`test_shares.py`): zusätzlichen Anteilschein bestellen, Status „unbezahlt“.

## Kontakt & E-Mail

- **Kontaktformular** (`test_contact.py`): Nachricht senden, Zustellung via MailHog verifiziert;
  Organisationsadresse auf der Kontaktseite sichtbar.

## Konfiguration & Templates (GartenBerg-spezifisch)

- **Konfiguration** (`test_config.py`): Anteilscheinpreis (750), Probe-Mitgliedschaft ohne
  Pflicht-Anteilschein, Bankverbindung, Organisationsadresse.
- **Custom-Templates** (`test_templates.py`): Statistik-/Plausible-Snippet (`base.html`),
  Signup-Template (Probe-Mitgliedschaft, Probe-Abo-Preise, Statuten-/Betriebsreglement-Links),
  Custom-Intro auf der Startdatum-Auswahl.

## Administration (Admin-Sicht)

- **Mitglieder & Abos** (`test_admin_subscription.py`): Mitgliederliste mit Admin-Edit-Links,
  jüngste und ausstehende Abo-Änderungen.
- **Impersonation** (`test_admin_impersonate.py`): Admin übernimmt eine Mitglieder-Session und
  beendet sie wieder.
- **Wiederkehrende Einsätze** (`test_admin_jobs.py`): Admin legt einen wiederkehrenden Job an,
  Member findet ihn und meldet sich an.
- **Depot-Listen** (`test_admin_list.py`): Depot-Listen erzeugen und abrufen.
- **E-Mail-Versand** (`test_admin_mail.py`): realer Mailversand inkl. Regressionsschutz für den
  `EmailAuditMiddleware` (Eintrag im EmailAuditLog).
- **Rechnungen** (`test_admin_billing.py`): offene Rechnungen einsehen.
- **SQL-Konsole** (`test_admin_pg.py`): DB-Abfrage über die jpg-Admin-Konsole ausführen.
