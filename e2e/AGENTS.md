* make sure to take screenshots at key moments for all tests that you write.

# E2E Test Lessons Learned

Nicht-offensichtliche Fallstricke aus der Implementierung der Playwright E2E Tests für GartenBerg / Juntagrico.

---

## Cookie-Consent-Banner

Juntagrico zeigt beim ersten Seitenaufruf einen Cookie-Consent-Banner, der Elemente am unteren Rand überlagert und Klick-Aktionen blockiert. Deshalb wird der Cookie vor dem ersten Seitenaufruf im Browser-Kontext gesetzt:

```python
context.add_cookies([{"name": "cookieconsent_status", "value": "dismiss", ...}])
```

---

## Bootstrap 4 Custom Checkboxes

Juntagrico rendert Checkboxen als Bootstrap 4 Custom Controls mit `opacity: 0` auf dem `<input>`. Playwright kann sie nicht normal klicken; `label.click()` trifft oft einen Link im Label-Text.

**Fix:** `force=True` auf dem Hidden-Input:

```python
page.locator("input[name='agb']").check(force=True)
```

---

## bootstrap-input-spinner

Auf den Seiten für Subscription-Auswahl (`/my/create/subscription/`) und Shares (`/my/share/manage/`) versteckt die `bootstrap-input-spinner`-Bibliothek das native `<input type="number">`. Playwright kann es nicht füllen.

**Fix:** Den `+`-Button des Spinners anklicken:

```python
page.wait_for_load_state("networkidle")  # Spinner muss initialisiert sein
page.locator(".btn-increment").first.click()
```

---

## MailHog MIME-Struktur

MailHog liefert für einfache (nicht-Multipart) E-Mails `"MIME": null` zurück. `msg.get("MIME", {})` gibt in diesem Fall `None` zurück, nicht `{}`.

**Fix:** Immer `or {}` als Fallback verwenden:

```python
mime = msg.get("MIME") or {}
parts = mime.get("Parts") or []
```

---

## Docker Container-Wiederverwendung / E-Mail-Kollision

Docker Compose löscht Container bei `--abort-on-container-exit` nicht. Beim nächsten `up` läuft derselbe Container weiter — die SQLite-Datenbank enthält dann noch den Benutzer vom vorherigen Run.

**Fixes:**
1. Pro Run eine eindeutige E-Mail generieren (`uuid.uuid4()`) — bereits in `conftest.py`.
2. `--force-recreate` in `docker compose up` erzwingt neue Container aus dem Image — bereits in `build.yml`.

---

## Django Admin Autocomplete (Select2)

Das Admin-Formular für Wiederkehrende Einsätze rendert das `type`-Feld als Select2-Widget. Das eigentliche `<select>` hat `aria-hidden="true"` — `select_option()` schlägt darauf fehl.

**Fix:** Den sichtbaren Select2-Trigger anklicken und auf AJAX-Ergebnisse warten:

```python
self.page.locator(".field-type .select2-selection--single").click()
first_option = self.page.locator(".select2-results__option:not(.select2-results__option--disabled)").first
first_option.wait_for(state="visible", timeout=10000)
first_option.click()
```

---

## `get_by_role("button", name=...)` ist kein exakter Match

Playwright's `name=`-Parameter bei `get_by_role` ist standardmässig ein Substring-Match. Im Django-Admin gibt es drei Submit-Buttons ("Sichern", "Sichern und neu hinzufügen", …), und `name="Sichern"` trifft alle drei → strict mode violation.

**Fix:** `exact=True` verwenden:

```python
page.get_by_role("button", name="Sichern", exact=True).click()
```

---

## `window.confirm` überschreiben statt `page.on("dialog", ...)`

`initJob.js` ruft `window.confirm()` beim Absenden des Job-Formulars auf. `page.on("dialog", lambda d: d.accept())` hat eine Race Condition im Playwright-Sync-API: der Default (Dismiss) kann greifen, bevor der Python-Callback läuft.

**Fix:** `window.confirm` vor dem Klick direkt überschreiben:

```python
page.evaluate("window.confirm = () => true")
```

---

## `expect_response` auf GET statt POST bei Redirect-Formularen

Nach einem erfolgreichen POST antwortet der Server mit 302. Zwischen dem Empfang dieser 302-Antwort und dem Start des Follow-up-GETs gibt es eine kurze Phase, in der die Seite scheinbar im Idle-Zustand ist. Auf langsamen CI-Runnern kann `wait_for_load_state("networkidle")` in dieser Lücke feuern und zu früh zurückkehren.

**Fix:** Auf die GET 200-Antwort des Redirect-Ziels warten (nicht die POST-302):

```python
with page.expect_response(
    lambda r: "/my/jobs/" in r.url and r.request.method == "GET" and r.status == 200
):
    page.get_by_role("button", name="Bestätigen").click()
page.wait_for_load_state("networkidle")
```

---

## Django ForeignKey-Select: Index 0 ist die Leer-Option

Wenn ein Formularfeld ein `ForeignKey` mit `blank=True, null=True` ist, rendert Django automatisch eine leere Option als erste Wahl:

```html
<option value="">---------</option>
<option value="1">Ernten</option>
<option value="2">Jäten</option>
```

`select_option(index=0)` wählt deshalb die leere Option, nicht den ersten echten Wert. Für den ersten echten Eintrag `index=1` verwenden.

---

## `SignupView` loggt authentifizierte User aus

Juntagrico's `SignupView.dispatch` ruft `logout(request)` auf, wenn ein bereits eingeloggter
User `/my/signup/` besucht. Der Effekt ist tückisch: die Seite selbst lädt ohne Fehler (sie ist
öffentlich), aber die Session des eingeloggten Users wird ungültig. Der Schaden zeigt sich erst
beim **nächsten** Test, der dieselbe `admin_context`- oder `member_context`-Session verwendet —
dort schlägt dann ein scheinbar unverwandter Test mit einer Redirect-auf-Login-Seite fehl.

**Fix:** Niemals `admin_page` oder `member_page` für `/my/signup/` verwenden. Stattdessen einen
frischen anonymen Browser-Kontext mit dem `playwright`-Fixture erstellen:

```python
@contextmanager
def _anon_page(playwright: Playwright) -> Page:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(base_url=BASE_URL)
    context.add_cookies([_COOKIE_CONSENT_COOKIE])
    page = context.new_page()
    try:
        yield page
    finally:
        page.close()
        context.close()
        browser.close()
```

---

## Juntagrico `auth.User.username` ist nicht die E-Mail

Juntagrico erstellt den Django-`auth.User` mit einem zufällig generierten Username nach dem
Schema `{slugify(first_name)}_{slugify(last_name)}_{random_seed}` (max. 30 Zeichen), z.B.
`e2e_testperson_a3f9c1b2`. Die E-Mail-Adresse steckt am `Member`-Model (`member.email`),
**nicht** am `auth.User` — das Feld `auth.User.email` bleibt leer.

**Konsequenz:** Jede Suche oder Abfrage, die nach dem User über die E-Mail-Adresse sucht
(z.B. django-impersonate Search), findet nichts. Stattdessen nach dem slugifizierten
Nachnamen suchen, der fix im generierten Username enthalten ist:

```python
# Nicht: page.navigate_search(MEMBER_EMAIL)  → keine Treffer
page.navigate_search(MEMBER_LAST.lower())    # trifft 'e2e_testperson_...' via username__icontains
```

Login funktioniert trotzdem mit der E-Mail, weil Juntagrico einen eigenen
`AuthenticateWithEmail`-Backend registriert, der über `Member.objects.get(email=...)` geht.

---

## DataTables: alphabetische Sortierung ist nicht chronologisch

Die Jobs-Tabelle (`#filter-table`) hat keine `data-order`-Attribute auf den Datumszellen. DataTables sortiert deshalb alphabetisch nach dem Zellentext (`"D d.m.Y"`, z.B. `"Di 01.06.2027"`). Das Tageskürzel steht vorne — `"Di"` (Dienstag) < `"Do"` (Donnerstag) — daher landet ein Dienstag-2027-Job **vor** einem Donnerstag-2026-Job in der sortierten Tabelle.

**Konsequenz:** Den ersten DOM-Row zu nehmen reicht nicht. Stattdessen alle Rows scannen, das kleinste zukünftige Datum bestimmen und den Job über seinen `href` (nicht über die DOM-Position) ansprechen — so in `JobsPage._nearest_future_job_href()` implementiert.
