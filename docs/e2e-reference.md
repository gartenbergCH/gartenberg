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

Auf den Seiten für Subscription-Auswahl (`/subscription/create/parts/`, ab 2.0), Anteilscheine im Wizard (`/subscription/create/shares/`) und Shares (`/my/share/manage/`) versteckt die `bootstrap-input-spinner`-Bibliothek das native `<input type="number">`. Playwright kann es nicht füllen.

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

## Django-Admin "Sichern" leitet auf Changelist weiter, nicht auf Change-Formular

Der Standard-Submit-Button "Sichern" im Django-Admin speichert das Objekt und leitet
**zurück zur Changelist** (`/admin/app/model/`). Das Change-Formular ist danach nicht
mehr aktiv — `input[name='slots']` oder andere Felder existieren auf der Changelist nicht.

**Konsequenz:** Assertions auf Formularfeld-Werte nach `save()` schlagen mit Timeout fehl,
obwohl der Save erfolgreich war (Success-Banner ist auf der Changelist sichtbar, daher gibt
`was_saved_successfully()` trotzdem `True` zurück).

**Fix:** Entweder "Sichern und weiter bearbeiten" verwenden (hält den User auf dem
Change-Formular), oder die Assertions gegen den **Changelist-Inhalt** richten:

```python
# Changelist-Inhalt prüfen (nach normalem "Sichern")
assert "5" in admin_page.content()       # Slot-Wert taucht in der Listenzeile auf
assert "2027" in admin_page.content()    # Jahr taucht in der Listenzeile auf
```

---

## Subscription-Single-View für bestellte Abos rendert keinen Seiteninhalt

`/my/subscription/{id}/` für ein noch **nicht aktiviertes** Abo (z.B. Startdatum 2027,
Status "ordered") liefert HTTP 200 und hat `<body id="subscription-single">`, aber der
eigentliche Seiteninhalt (Depot-Name, Abo-Bestandteile, etc.) fehlt im HTML — der Body
ist nach dem Cookie-Consent-Skript leer.

**Konsequenz:** Assertions wie `assert depot_name in member_page.content()` schlagen fehl,
auch wenn das Abo korrekt angelegt ist und der Depot-Name in der Datenbank stimmt.

**Kein Fix nötig** — das ist das erwartete Server-Rendering. Depot- und Abo-Informationen
für bestellte (zukünftige) Abos müssen über eine andere Route geprüft werden, z.B. über
die Depot-Detailseite (`/my/depot/{id}/`) oder die Admin-Abo-Übersicht.

---

## `/my/memberjobs` filtert per Default auf das aktuelle Geschäftsjahr

`BusinessYearForm` setzt `year = get_business_year()` (= aktuelles Jahr), wenn kein
GET-Parameter übergeben wird. Test-Jobs mit Datum 2027+ werden daher nicht angezeigt,
obwohl die Assignments in der DB existieren.

**Wichtig:** Der Vergleich `latest != current` reicht nicht. Wenn der Member nur Assignments
in 2027 hat, ist 2027 die einzige Choice — aber `self.data['year']` = '2026' ist ungültig,
`is_valid()` = False, und die Tabelle zeigt nichts. Das Select rendert trotzdem '2027' als
aktuellen Wert, weil es die einzige Option ist. `input_value()` gibt also '2027' zurück,
obwohl die Seite leer ist. Deshalb immer mit dem year-Parameter neu navigieren:

```python
options = year_select.evaluate("el => Array.from(el.options).map(o => o.value).filter(v => v)")
if options:
    self.page.goto(f"/my/memberjobs?year={max(options, key=int)}")
    self.page.wait_for_load_state("networkidle")
```

---

## DataTables `tbody` ist nach `networkidle` noch nicht gerendert

`wait_for_load_state("networkidle")` feuert, sobald keine ausstehenden Netzwerkanfragen mehr
laufen — DataTables kann danach noch client-seitig initialisieren: Es entfernt alle `<tr>` aus
dem DOM und rendert nur die aktuelle Seite neu. Auf einem langsamen CI-Runner kann `.count()`
oder `.inner_text()` in diesem Zwischenzustand aufgerufen werden und gibt 0 zurück, obwohl die
Daten vorhanden sind.

**Fix:** `wait_for(state="visible", timeout=10000)` statt `.count() > 0` verwenden:

```python
try:
    self.page.locator("#assignments-table a:has-text('Ernten')").wait_for(
        state="visible", timeout=10000
    )
    return True
except Exception:
    return False
```

Dieses Muster gilt für alle DataTables-Tabellen, auf denen nach dem Navigieren sofort
Assertions gemacht werden.

---

## jpg SQL-Ergebnis ist eine ASCII-Tabelle, kein reiner Text

`AdminPgPage.execute_sql()` liest den Inhalt von `textarea#textarea_id` aus. jpg rendert
das Ergebnis als ASCII-Tabelle:

```
+----------+
| COUNT(*) |
+==========+
| 8        |
+----------+
ROWS: -1
```

`line.strip().isdigit()` findet daher keine Treffer — die Zahl steht zwischen Pipes.

**Fix:** Regex auf Tabellenzellen anwenden:

```python
import re
cell_values = re.findall(r'\|\s*(\d+)\s*\|', result)
count = int(cell_values[0])
```

---

## DataTables: alphabetische Sortierung ist nicht chronologisch

Die Jobs-Tabelle (`#filter-table`) hat keine `data-order`-Attribute auf den Datumszellen. DataTables sortiert deshalb alphabetisch nach dem Zellentext (`"D d.m.Y"`, z.B. `"Di 01.06.2027"`). Das Tageskürzel steht vorne — `"Di"` (Dienstag) < `"Do"` (Donnerstag) — daher landet ein Dienstag-2027-Job **vor** einem Donnerstag-2026-Job in der sortierten Tabelle.

**Konsequenz:** Den ersten DOM-Row zu nehmen reicht nicht. Stattdessen alle Rows scannen, das kleinste zukünftige Datum bestimmen und den Job über seinen `href` (nicht über die DOM-Position) ansprechen — so in `JobsPage._nearest_future_job_href()` implementiert.

---

# Juntagrico 2.0 Upgrade (von 1.7)

Erkenntnisse aus der Migration der E2E-Tests von Juntagrico 1.7.x auf 2.0.7.

## Signup-/Subscription-Wizard: alle URLs umbenannt

Der komplette Anmelde-/Abo-Flow wurde in 2.0 unter `/subscription/create/` neu strukturiert. Die `wait_for_url`-Aufrufe in `conftest.py` (`member_context`) und `pages/wizard_page.py` mussten angepasst werden:

| Schritt | 1.7 | 2.0 |
|---|---|---|
| Abo-Teile | `/my/create/subscription/` | `/subscription/create/parts/` |
| (neu) Extras | – | `/subscription/create/extras/` |
| Depot | `/selectdepot/` | `/subscription/create/depot/` |
| Startdatum | `/start/` | `/subscription/create/start/` |
| Co-Member | `/addmembers/` | `/subscription/create/comembers/` |
| Anteilscheine | `/shares/` | `/subscription/create/shares/` |
| Zusammenfassung | `/summary/` | `/subscription/create/summary/` |
| Welcome | `/my/welcome` | `/signup/welcome` |
| Abbrechen | `/my/create/subscription/cancel/` | `/subscription/create/cancel/` |

Die Signup-Einstiegs-URL `/my/signup/` existiert in 2.0 als Backwards-Compat-Alias weiter (kanonisch ist `/signup/`).

## Wizard-Flow ist dynamisch (`signup_manager.get_next_page()`)

Welche Schritte erscheinen, entscheidet `get_next_page()` zur Laufzeit. Der **Extras-Schritt** erscheint nur, wenn ein Extra-Abo existiert (`SubscriptionType.objects.is_extra().visible().exists()`). Die `generate_testdata` legt **kein** Extra-Abo an → der Extras-Schritt wird übersprungen. Bei eigener Testdaten-Anpassung muss der Wizard-Pfad ggf. adaptiv (URL prüfen statt feste Sequenz) navigieren.

## Co-Member-Seite: kein "Überspringen"-Link mehr

In 2.0 (`add_member.html`) gibt es keinen `Überspringen`-Link. Ohne Co-Member weiterzukommen erfolgt über den `?next`-Link. Robust per href ansprechen, nicht per Text (übersetzungsabhängig):

```python
page.locator("a[href='?next']").first.click()
```

## Projekt-Template-Overrides: Pfade haben sich geändert

Custom-Templates wurden in 2.0 verschoben/umbenannt. Ein Projekt-Override am alten Pfad wird **stillschweigend nicht mehr verwendet** (kein Fehler, der Custom-Inhalt verschwindet einfach):

| Zweck | 1.7-Template | 2.0-Template |
|---|---|---|
| Signup-Formular | `signup.html` | `juntagrico/signup/member.html` |
| Startdatum | `createsubscription/select_start_date.html` | `juntagrico/subscription/create/select_start_date.html` |

Die Block-Struktur ist identisch geblieben — Override 1:1 auf den neuen Pfad verschieben.

## Submit-Buttons über `#submit-id-submit` ansprechen, nicht über das Label

juntagrico/crispy-forms rendert den Submit-Button mit der stabilen id `submit-id-submit`.
Das Button-**Label** ist dagegen nicht stabil: In 2.0.8 wurde der Submit-Button des
Signup-Personendaten-Formulars (`/my/signup/`) von "Anmelden" auf "Weiter" umbenannt — ein
reiner Patch-Release, der über ein loses Pinning (`~=2.0.7`) stillschweigend hereinkam und
`get_by_role("button", name="Anmelden")` in den Timeout laufen liess.

**Fix:** Auf Wizard-/Crispy-Formularen per id ansprechen:

```python
page.locator("#submit-id-submit").click()
```

(Die Login-Seite `/accounts/login/` ist kein Crispy-Form und heisst weiterhin "Anmelden".)

## Mail-Form: `/my/mails` → `/email/write/`, neue Empfänger-Logik

Die Mail-Versand-Seite ist von `/my/mails` auf `/email/write/` umgezogen (Crispy-Form `juntagrico/email/write.html`). Das frühere "Einzeladresse senden" (`#allsingleemail`/`#singleemail`) gibt es nicht mehr — Empfänger sind jetzt Mitglieder/Tätigkeitsbereiche/Einsätze/Depots (select2) bzw. Listen (`to_list`-Checkboxen: `all_subscriptions`, `all_shares`) oder eine **Kopie an sich selbst** (`copy`-Checkbox). Für einen Test-Mailversand an den Admin ist `copy` am robustesten (Admin = Absender = Empfänger).

Weitere Stolpersteine:
- **Editor:** djrichtextfield nutzt weiterhin **TinyMCE** (`init_template: tinymce.js`), `tinymce.activeEditor.setContent(...)` + `tinymce.triggerSave()` funktionieren weiter. Aber: TinyMCE lädt **nur, wenn `DJRICHTEXTFIELD_CONFIG = richtextfield_config(LANGUAGE_CODE)` in `settings.py` gesetzt ist** (`from juntagrico.defaults import richtextfield_config`). Fehlt das, lädt das lokale `tinymce.min.js` nicht und der Editor initialisiert nie — `wait_for_function` auf `tinymce` läuft in den Timeout.
- **Submit-Button:** Label wird per AJAX (`emailForm.js`) durch die Empfängerzahl ersetzt → per `#submit-id-submit` ansprechen, nicht per `name="Senden"`.
- **Erfolg:** redirect auf `/email/sent` (kein `/result/<n>/` mehr) → Erfolg über die Ziel-URL prüfen.

## Depot-Listen-Form: `/manage/list` → `/list`

Die Depot-Listen-Seite ist auf `/list` umgezogen (`name='lists'`); `/manage/list` liefert **404**. Das Datumsfeld `input[name='for_date']` (`GenerateListForm`) und der Button "Listen Erzeugen" existieren weiter.

Zwei Fallstricke nach erfolgreichem Submit (POST → 302):
- juntagrico macht `HttpResponseRedirect('')` (leerer Location-Header). Chromium **folgt dem nicht** → leere Seite. Nach dem Submit explizit `goto("/list")`, um Ergebnis/Meldungen zu sehen.
- Die Erfolgsmeldung lautet `Listen erfolgreich erstellt.` (nicht "Listen erstellt") und ist transient. Robuster: Erfolg über die generierten Download-Links (`a[href*='/list/']`) im `depot_lists`-Block prüfen, nicht über `.alert-success`.

## EmailAuditMiddleware muss an neue Mail-URLs/Felder angepasst werden

Der gartenberg-eigene `EmailAuditMiddleware` (`gartenberg/middleware.py`) hängt an den Mail-Versand-POSTs. In 2.0 änderten sich URLs (`/email/write/`, `/email/{to,depot,area,job}/<id>/`) **und** Feldnamen (`from_email` statt `sender`; Empfänger via `to_list`/`to_members`/`to_areas`/`to_jobs`/`to_depots`/`copy` statt `all*`/`recipients`). Echte Sends erkennt man am Submit-Feld `submit` im POST (Vorbefüll-POSTs mit `members` haben das nicht).

**Regressions-Erkennung — zwei Ebenen nötig:** Die Unit-Tests (`gartenberg/tests.py`) prüfen die Middleware-Logik isoliert gegen **hartkodierte** POST-Daten — sie fangen Code-Fehler, aber **nicht** ein erneutes stilles Ändern der juntagrico-Mailform. Dafür braucht es den **Integrationscheck** in `tests/test_admin_mail.py`: nach dem realen Versand das EmailAuditLog-Admin-Changelist (`/admin/gartenberg/emailauditlog/`) öffnen und den Betreff verifizieren (echtes Formular → Middleware → Log).
