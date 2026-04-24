# E2E Test Lessons Learned

Erkenntnisse aus der Implementierung der Playwright E2E Tests für GartenBerg / Juntagrico.

---

## Cookie-Consent-Banner

Der Juntagrico-Browser lädt beim ersten Seitenaufruf einen Cookie-Consent-Banner (`cc-window`, Position: bottom). Dieser überlagert Elemente am unteren Seitenrand und blockiert Klick-Aktionen.

**Fix:** Cookie vor dem ersten Seitenaufruf im Browser-Kontext setzen, damit der Banner nie erscheint:

```python
context.add_cookies([{
    "name": "cookieconsent_status",
    "value": "dismiss",
    "domain": urlparse(BASE_URL).hostname,
    "path": "/",
}])
```

---

## Bootstrap 4 Custom Checkboxes

Juntagrico rendert Checkboxen (u.a. AGB) als Bootstrap 4 Custom Controls:

```html
<input type="checkbox" id="id_agb" class="custom-control-input" />
<label for="id_agb" class="custom-control-label">...</label>
```

Das `<input>` hat `opacity: 0` und ist damit für Playwright nicht klickbar. `page.locator("label[for='id_agb']").click()` trifft oft einen Link im Label-Text statt den Toggle.

**Fix:** `force=True` auf dem Hidden-Input:

```python
page.locator("input[name='agb']").check(force=True)
```

---

## bootstrap-input-spinner

Auf den Seiten für Subscription-Auswahl (`/my/create/subscription/`) und Shares (`/my/share/manage/`) wird das `<input type="number">` durch die `bootstrap-input-spinner`-Bibliothek ersetzt. Das originale Input wird versteckt (`display: none` o.ä.); Playwright kann es nicht füllen.

**Fix:** Den `+`-Button des Spinners anklicken statt das Input zu füllen:

```python
page.wait_for_load_state("networkidle")  # Spinner muss initialisiert sein
page.locator(".btn-increment").first.click()  # Wert von 0 auf 1 erhöhen
```

Für Shares ist der Default-Wert already auf das benötigte Minimum gesetzt (`value="{{ shares.total_required }}"`) — dort reicht ein direktes Klicken auf "Weiter".

---

## Mailhog MIME-Struktur

Mailhog liefert für einfache (nicht-Multipart) E-Mails `"MIME": null` zurück. `msg.get("MIME", {})` gibt in diesem Fall `None` zurück (der Key existiert, sein Wert ist `null`), nicht `{}`.

**Fix:** Immer `or {}` als Fallback verwenden:

```python
mime = msg.get("MIME") or {}
parts = mime.get("Parts") or []
# Bei keinen MIME-Parts liegt der Body in Content.Body:
content = msg.get("Content") or {}
body = content.get("Body", "")
```

---

## Juntagrico Signup: kein Passwort-Feld

Die Signup-Seite (`/my/signup/`) enthält **kein Passwort-Feld**. Das Passwort wird nach Abschluss des Wizards auto-generiert und per E-Mail verschickt.

**Folge:** Nach dem Wizard muss die Welcome-E-Mail aus Mailhog gelesen werden, um:
1. Das generierte Passwort zu extrahieren (`Passwort: XXXXXXXX`)
2. Den Bestätigungslink zu extrahieren und aufzurufen (`Bestätigungslink: http://...`)

Danach erst ist ein Login möglich.

---

## Signup-Formular: POST 200 vs. 302

Ein erfolgreicher Signup gibt HTTP **302** zurück (Redirect auf `/my/create/subscription/`). Bei Validierungsfehlern wird HTTP **200** zurückgegeben (Seite neu gerendert mit Fehlermeldungen).

`wait_for_url("**/my/create/subscription/")` hängt ewig wenn der POST 200 zurückgab. Nach dem Klick auf "Anmelden" besser explizit prüfen:

```python
page.wait_for_load_state("networkidle")
if "/my/signup/" in page.url:
    errors = page.locator(".alert-danger, .invalid-feedback, .errorlist").all_text_contents()
    raise AssertionError(f"Signup fehlgeschlagen: {errors}")
```

---

## Docker Container-Wiederverwendung / E-Mail-Kollision

Docker Compose stoppt Container bei `--abort-on-container-exit`, löscht sie aber nicht. Beim nächsten `docker compose up` werden dieselben gestoppten Container neugestartet — die SQLite-Datenbank enthält dann noch den Benutzer vom vorherigen Run.

**Fixes:**
1. **Pro Run eine eindeutige E-Mail** generieren:
   ```python
   import uuid
   MEMBER_EMAIL = f"e2e.{uuid.uuid4().hex[:8]}@gartenberg-e2e.local"
   ```

2. **`--force-recreate`** in der `docker compose`-Befehlszeile erzwingt neue Container aus dem Image:
   ```bash
   docker compose -f e2e/compose-e2e.yml up --build --force-recreate \
     --exit-code-from playwright --abort-on-container-exit
   ```

---

## Django Admin Autocomplete (Select2)

Das Admin-Formular für Wiederkehrende Einsätze (`recuringjob`) rendert das Feld `type` als Django-Admin-Autocomplete-Widget (Select2). Das eigentliche `<select>` hat `aria-hidden="true"` und `class="select2-hidden-accessible"` — `select_option()` darauf schlägt fehl.

**Fix:** Den sichtbaren Select2-Trigger anklicken, auf AJAX-Ergebnisse warten und erste Option auswählen:

```python
self.page.locator(".field-type .select2-selection--single").click()
first_option = self.page.locator(".select2-results__option:not(.select2-results__option--disabled)").first
first_option.wait_for(state="visible", timeout=10000)
first_option.click()
```

---

## `get_by_role("button", name=...)` ist kein exakter Match

Playwright's `name=`-Parameter bei `get_by_role` ist standardmässig ein **Substring-Match**. Im Django-Admin gibt es drei Submit-Buttons: "Sichern", "Sichern und neu hinzufügen", "Sichern und weiter bearbeiten". `name="Sichern"` trifft alle drei → strict mode violation.

**Fix:** `exact=True` verwenden:

```python
page.get_by_role("button", name="Sichern", exact=True).click()
```

---

## generate_testdata: type_2 Jobs haben Build-Zeitstempel

`generate_testdata` enthält einen Bug: Die 10 "Jäten"-Jobs werden alle mit `time = timezone.now()` zum Build-Zeitpunkt erstellt (statt mit inkrementiertem Datum). Sie erscheinen in der Jobs-Liste **zuerst** (aufsteigend sortiert), haben aber `can_interact=False`, weil sie zum Testzeitpunkt in der Vergangenheit liegen — kein "Bestätigen"-Button wird gerendert.

**Fix:** Zeilen überspringen, deren Datum dem heutigen Tag entspricht, und nur künftige Jobs anklicken:

```python
today_str = date.today().strftime("%d.%m.%Y")
rows = page.locator("#filter-table tbody tr")
for i in range(rows.count()):
    row = rows.nth(i)
    if today_str not in row.locator("td:first-child").inner_text():
        row.locator("td:nth-child(2) a").click()
        break
```

---

## `window.confirm` überschreiben statt `page.on("dialog", ...)`

`initJob.js` feuert `window.confirm(message)` beim Absenden des Job-Anmelde-Formulars. `page.on("dialog", lambda d: d.accept())` hat eine Race Condition im Playwright-Sync-API: Der Default (Dismiss) kann greifen, bevor der Python-Callback ausgeführt wird.

**Fix:** `window.confirm` im Seitenkontext direkt überschreiben, bevor der Button geklickt wird:

```python
page.evaluate("window.confirm = () => true")
```

---

## `expect_navigation()` statt `wait_for_load_state()` bei Form-Submits

`wait_for_load_state("networkidle")` prüft den **aktuellen** Zustand der Seite. Wenn die Seite zum Zeitpunkt des Aufrufs bereits im Idle-Zustand ist (kurze Lücke zwischen Click-Delivery und Browser-Verarbeitung), kehrt die Methode sofort zurück — bevor das POST überhaupt gestartet hat. Auf langsamen CI-Runnern ist diese Lücke grösser.

**Fix:** `expect_navigation()` **vor** dem Klick starten; es setzt den Watcher auf, bevor die Navigation beginnt:

```python
with page.expect_navigation(wait_until="networkidle"):
    page.get_by_role("button", name="Bestätigen").click()
```

---

## Session-scoped Fixtures

Um wiederholten Login über mehrere Tests zu vermeiden, werden `browser` und `BrowserContext` als `scope="session"`-Fixtures angelegt. Jeder Test erhält über `context.new_page()` eine neue Tab-Instanz — Cookies/Auth bleiben im Context erhalten.

Der `playwright`-Fixture aus `pytest-playwright` ist bereits session-scoped und kann direkt für `playwright.chromium.launch()` genutzt werden.
