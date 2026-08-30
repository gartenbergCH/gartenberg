# Requirements

Anforderungskatalog für die GartenBerg-Anpassungen an der juntagrico-Plattform, abgeleitet aus
[vision.md](vision.md) und den Use Cases unter [use_cases/](use_cases/). Die Spalte **UC** stellt die
Rückverfolgbarkeit zu den Use-Case-Spezifikationen her; die dort dokumentierten Geschäftsregeln (GR-*)
sind die verbindliche Detaillierung der hier genannten Anforderungen.

Abgegrenzt wird wie in der Vision: erfasst sind die GartenBerg-eigenen Anpassungen und die
Plattformabläufe, auf denen sie aufbauen — nicht der übrige Funktionsumfang von juntagrico.

## Funktionale Anforderungen

### Anmeldung und Mitgliedschaft

| ID     | Titel                              | User Story                                                                                                                                                                                              | UC     | Priorität | Status       |
|--------|------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|-----------|--------------|
| FR-001 | Einstiegsinformationen Anmeldung   | Als Interessent/in möchte ich auf der Anmeldeseite die Probe-Varianten mit ihren Preisen, den Anteilscheinpreis und die Verweise auf Statuten und Betriebsreglement sehen, damit ich weiss, worauf ich mich einlasse. | UC-001 | Hoch      | Verifiziert  |
| FR-002 | Abo-Bestandteile und Depot wählen  | Als Interessent/in möchte ich im Anmeldeprozess die gewünschten Abo-Bestandteile und ein Depot samt allfälliger Zusatzkosten wählen, damit meine Bestellung meinem Bedarf entspricht.                     | UC-001 | Hoch      | Verifiziert  |
| FR-003 | Startdatum ausserhalb Jahresbeginn | Als Interessent/in möchte ich mein Abo bei freien Plätzen auf den nächsten Monatsbeginn starten lassen, damit ich nicht bis zum nächsten Geschäftsjahr warten muss.                                       | UC-001 | Hoch      | Verifiziert  |
| FR-004 | Anmeldung ohne Anteilschein        | Als Interessent/in möchte ich eine Probe-Mitgliedschaft ohne Anteilschein abschliessen, damit ich die Genossenschaft drei Monate lang unverbindlich kennenlernen kann.                                    | UC-001 | Hoch      | Verifiziert  |
| FR-005 | Mitbezüger/innen erfassen          | Als Interessent/in möchte ich bei der Anmeldung Mitbezüger/innen erfassen, damit wir ein Abo gemeinsam beziehen und die Einsätze zusammen leisten können.                                                 | UC-001 | Hoch      | Verifiziert  |
| FR-006 | Anmeldekommentar aufbewahren       | Als Administrator/in möchte ich den bei der Anmeldung hinterlassenen Kommentar dauerhaft am Mitglied gespeichert haben, damit er später noch einsehbar ist und nicht nur in einer E-Mail steht.           | UC-001 | Mittel    | Implementiert |
| FR-007 | Benachrichtigung der Koordination  | Als Administrator/in möchte ich über neue Anmeldungen und neu gezeichnete Anteilscheine benachrichtigt werden, damit ich Abo und Anteilscheine zeitnah bearbeiten kann.                                   | UC-001 | Hoch      | Implementiert |

### Kontakt und Grundlagendokumente

| ID     | Titel                            | User Story                                                                                                                                                                                   | UC     | Priorität | Status        |
|--------|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|-----------|---------------|
| FR-008 | Kontaktangaben anzeigen          | Als Interessent/in möchte ich auf der Kontaktseite die vollständige Adresse und die allgemeine Kontaktadresse der Genossenschaft sehen, damit ich weiss, an wen ich mich wenden kann.          | UC-002 | Hoch      | Verifiziert   |
| FR-009 | Nachricht an die Genossenschaft  | Als Interessent/in möchte ich über ein Formular eine Nachricht an die allgemeine Kontaktadresse senden, damit meine Frage bei der zuständigen Stelle ankommt.                                  | UC-002 | Hoch      | Verifiziert   |
| FR-010 | Zahlungsangaben für Anteilscheine| Als Mitglied möchte ich zu meinen unbezahlten Anteilscheinen die Bankverbindung und den Zahlungsempfänger sehen, damit ich sie ohne Rückfrage einzahlen kann.                                  | UC-002 | Mittel    | Implementiert |
| FR-011 | Verweis auf Grundlagendokumente  | Als Mitglied möchte ich Statuten, Betriebsreglement und häufige Fragen aus der Plattform heraus verlinkt finden, damit ich sie nicht auf der Webseite suchen muss.                             | UC-002 | Mittel    | Verifiziert   |
| FR-012 | Signatur ausgehender Nachrichten | Als Administrator/in möchte ich jede ausgehende Nachricht mit der Signatur der Genossenschaft versehen lassen, damit Empfänger/innen den Absender und die Webseite erkennen.                   | UC-002 | Mittel    | Implementiert |
| FR-013 | Erfassung der Seitenaufrufe      | Als Administrator/in möchte ich die Aufrufe aller ausgelieferten Seiten über den eigenen Statistikdienst zählen lassen, damit ich die Nutzung der Plattform auswerten kann.                    | UC-002 | Niedrig   | Verifiziert   |

### Arbeitseinsätze

| ID     | Titel                              | User Story                                                                                                                                                                                          | UC     | Priorität | Status        |
|--------|------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|-----------|---------------|
| FR-014 | Ausgeschriebene Einsätze finden    | Als Mitglied möchte ich die ausgeschriebenen Einsätze nach Zeitraum oder Jahr filtern und im Detail sehen, damit ich einen passenden Einsatz auswählen kann.                                          | UC-003 | Hoch      | Verifiziert   |
| FR-015 | Für einen Einsatz anmelden         | Als Mitglied möchte ich mich mit einer Anzahl Teilnehmender für einen Einsatz anmelden, damit mein Platz reserviert ist und die Koordination planen kann.                                              | UC-003 | Hoch      | Verifiziert   |
| FR-016 | Anmeldungen nur durch Koordination ändern | Als Administrator/in möchte ich, dass Mitglieder sich nicht selbst von Einsätzen abmelden und die Teilnehmerzahl nicht selbst ändern können, damit die Einsatzplanung verbindlich bleibt.       | UC-003 | Mittel    | Implementiert |
| FR-017 | Geleisteten Einsatz melden         | Als Mitglied möchte ich selbständig geleistete Arbeit mit Zeitpunkt, Dauer, Tätigkeitsbereich, Ansprechperson, Ort und Beschreibung melden, damit sie mir angerechnet werden kann.                    | UC-003 | Hoch      | Verifiziert   |
| FR-018 | Eigene Meldung korrigieren         | Als Mitglied möchte ich eine noch nicht angerechnete Meldung ändern oder löschen, damit ich falsche Angaben korrigieren kann, ohne die Koordination zu belasten.                                       | UC-003 | Mittel    | Implementiert |
| FR-019 | Persönliche Einsatzübersicht       | Als Mitglied möchte ich meinen Einsatzstand samt den Einsätzen meiner Mitbezüger/innen sehen, damit ich weiss, wie viele Einsätze ich noch leisten muss.                                               | UC-003 | Hoch      | Implementiert |
| FR-020 | Offene Anfragen einsehen           | Als Einsatzverantwortliche/r möchte ich die an mich gerichteten Einsatzmeldungen mit Datum, Mitglied, Stand und Beschreibung sehen, damit ich weiss, was ich zu beurteilen habe.                      | UC-009 | Hoch      | Verifiziert   |
| FR-021 | Meldung beurteilen                 | Als Einsatzverantwortliche/r möchte ich eine Meldung mit korrigierten Angaben und einer Rückmeldung bestätigen oder ablehnen, damit nur tatsächlich geleistete Arbeit angerechnet wird.                | UC-009 | Hoch      | Verifiziert   |
| FR-022 | Meldung direkt aus der Liste bestätigen | Als Einsatzverantwortliche/r möchte ich eine unstrittige Meldung direkt aus der Liste bestätigen, damit ich viele Meldungen zügig abarbeiten kann.                                               | UC-009 | Mittel    | Implementiert |
| FR-023 | Entscheid mitteilen                | Als Mitglied möchte ich über den Entscheid zu meiner Meldung samt Begründung benachrichtigt werden, damit ich weiss, ob der Einsatz angerechnet wurde.                                                 | UC-009 | Hoch      | Verifiziert   |
| FR-024 | Bestätigung zurücknehmen           | Als Administrator/in möchte ich eine bestätigte Meldung wieder auf beantragt oder abgelehnt setzen, damit eine irrtümlich angerechnete Arbeit samt erzeugtem Einsatz wieder entfernt wird.             | UC-009 | Mittel    | Implementiert |
| FR-025 | Teilnehmerliste künftiger Einsätze | Als Einsatzverantwortliche/r möchte ich alle künftigen Einsätze chronologisch mit Datum, Zeitfenster, Einsatzart, Ort und Platzbelegung auf einer Seite sehen, damit ich keinen Einsatz einzeln öffnen muss. | UC-010 | Hoch  | Verifiziert   |
| FR-026 | Kontaktangaben der Eingeschriebenen| Als Einsatzverantwortliche/r möchte ich zu jedem Einsatz die eingeschriebenen Personen mit Name, Telefonnummer und E-Mail-Adresse sehen, damit ich sie bei Bedarf direkt kontaktieren kann.             | UC-010 | Hoch      | Verifiziert   |
| FR-027 | Teilnehmerliste einschränken       | Als Einsatzverantwortliche/r möchte ich die Teilnehmerliste auf einen Tätigkeitsbereich oder eine Einsatzart einschränken, damit ich nur meinen Ablauf — etwa die Verteilfahrten — vor mir habe.       | UC-010 | Hoch      | Verifiziert   |

### Depotlisten

| ID     | Titel                            | User Story                                                                                                                                                                                     | UC     | Priorität | Status        |
|--------|----------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|-----------|---------------|
| FR-028 | Listen auf Knopfdruck erzeugen   | Als Administrator/in möchte ich die Depotlisten zu einem frei gewählten Stichtag auf Knopfdruck erzeugen und abrufen, damit ich sie unabhängig von festen Wochentagen erhalte.                   | UC-004 | Hoch      | Verifiziert   |
| FR-029 | Hauptlisten nur mit Gemüse       | Als Administrator/in möchte ich Hauptliste, Depot- und Mengenübersicht auf das Produkt Gemüse beschränkt haben, damit die Übersichten durch die Hofprodukte nicht unlesbar werden.               | UC-004 | Hoch      | Implementiert |
| FR-030 | Eigene Liste je Hofprodukt       | Als Administrator/in möchte ich für Kartoffeln, Mehl und Glarner Alpkäse je eine eigene Liste, damit im Depot pro Produkt ersichtlich ist, wer welche Grösse bezieht.                            | UC-004 | Hoch      | Implementiert |
| FR-031 | Kompaktes Layout breiter Sortimente | Als Administrator/in möchte ich Mehl und Glarner Alpkäse im Querformat ohne Kontrollspalten gedruckt bekommen, damit alle Produktgrössen auf die Seite passen.                                | UC-004 | Mittel    | Implementiert |

### Rundmail und Versandprotokoll

| ID     | Titel                          | User Story                                                                                                                                                                                 | UC     | Priorität | Status        |
|--------|--------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|-----------|---------------|
| FR-032 | Rundmail an Mitgliedergruppen  | Als Administrator/in möchte ich eine Nachricht an ausgewählte Gruppen — Abo-Bezieher/innen, Anteilschein-Besitzer/innen, einzelne Mitglieder, Tätigkeitsbereiche, Einsätze oder Depots — senden, damit ich gezielt informiere. | UC-005 | Hoch | Verifiziert   |
| FR-033 | Empfängerkreis vorab prüfen    | Als Administrator/in möchte ich vor dem Versand die Anzahl der erreichten Empfänger/innen sehen und die Auswahl ins Formular übernehmen, damit ich die Auswahl kontrollieren kann.           | UC-005 | Mittel    | Implementiert |
| FR-034 | Versand protokollieren         | Als Administrator/in möchte ich zu jedem tatsächlichen Versand Zeitpunkt, Absender, Betreff, Empfängergruppen und Versandweg protokolliert haben, damit ich den Versand später belegen kann. | UC-005 | Hoch      | Verifiziert   |
| FR-035 | Versandprotokoll auswerten     | Als Administrator/in möchte ich das Protokoll neueste-zuerst sehen sowie nach Absender und Versandweg filtern und nach Absender und Betreff durchsuchen, damit ich eine Rückfrage rasch klären kann. | UC-006 | Hoch | Implementiert |
| FR-036 | Protokoll schreibgeschützt     | Als Administrator/in möchte ich Protokolleinträge weder anlegen noch ändern können, damit das Protokoll als Beleg taugt.                                                                     | UC-006 | Hoch      | Implementiert |

### Rechnungen

| ID     | Titel                          | User Story                                                                                                                                                                                     | UC     | Priorität | Status        |
|--------|--------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|-----------|---------------|
| FR-037 | Rechnungslauf je Geschäftsjahr | Als Administrator/in möchte ich für ein Geschäftsjahr aus den verrechenbaren Abo-Bestandteilen Rechnungen mit Positionen und Gesamtbetrag erzeugen, damit ich den Jahresbeitrag stellen kann.    | UC-007 | Hoch      | Verifiziert   |
| FR-038 | Rechnungen zustellen           | Als Administrator/in möchte ich Rechnungen freigeben und den Mitgliedern mit Einzahlungsschein und Referenznummer zustellen lassen, damit Zahlungen automatisch zugeordnet werden können.        | UC-007 | Hoch      | Verifiziert   |
| FR-039 | Zahlungen verbuchen            | Als Administrator/in möchte ich Zahlungseingänge mit Datum, Betrag und Zahlungsart auf einer Rechnung verbuchen, damit der offene Betrag jederzeit stimmt.                                       | UC-007 | Hoch      | Verifiziert   |
| FR-040 | Differenzen ausgleichen        | Als Administrator/in möchte ich Über- und Unterzahlungen mit einer Ausgleichsposition bereinigen und den Mehrwertsteuersatz einer Rechnung nachträglich setzen, damit die Rechnung aufgeht.       | UC-007 | Mittel    | Implementiert |
| FR-041 | Position ohne Abo-Bezug        | Als Administrator/in möchte ich eine Rechnung um eine Position eines eigenen Positionstyps ergänzen, damit ich auch Beträge ohne Abo-Bezug verrechnen kann.                                       | UC-007 | Mittel    | Implementiert |

### Abo-Verwaltung

| ID     | Titel                            | User Story                                                                                                                                                                                    | UC     | Priorität | Status        |
|--------|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|-----------|---------------|
| FR-042 | Pendente Abo-Änderungen          | Als Administrator/in möchte ich die Abos mit fehlendem Aktivierungs- oder Deaktivierungsdatum aufgelistet sehen, damit ich weiss, was noch nachzuführen ist.                                    | UC-008 | Hoch      | Verifiziert   |
| FR-043 | Eindeutige Abo-Bestandteile      | Als Administrator/in möchte ich jeden Abo-Bestandteil mit Abo-Paket und bestellter Produktgrösse bezeichnet sehen, damit sich die verschiedenen Mehl-, Kartoffel- und Käsegrössen unterscheiden lassen. | UC-008 | Hoch | Implementiert |
| FR-044 | Jüngste Abo-Änderungen           | Als Administrator/in möchte ich die Abo-Änderungen eines wählbaren Zeitraums einsehen, damit ich eine Rückfrage zum Verlauf eines Abos beantworten kann.                                        | UC-008 | Mittel    | Verifiziert   |
| FR-045 | Mitgliedersicht übernehmen       | Als Administrator/in möchte ich die Sicht eines Mitglieds übernehmen und wieder beenden, damit ich sehe, was das Mitglied sieht, wenn es eine Frage stellt.                                     | UC-008 | Mittel    | Verifiziert   |
| FR-046 | Lesende Ad-hoc-Auswertung        | Als Administrator/in möchte ich über eine Abfragekonsole lesende Auswertungen auf den Betriebsdaten ausführen, damit ich Fragen über mehrere Mitglieder hinweg beantworten kann.                | UC-008 | Niedrig   | Verifiziert   |

### Kündigungen

FR-050 ergibt sich aus der GartenBerg-Konfiguration und der bestehenden Testabdeckung, ist aber noch
durch keine Use-Case-Spezifikation abgedeckt (siehe [Offene Punkte](#offene-punkte)).

| ID     | Titel                          | User Story                                                                                                                                                                            | UC | Priorität | Status              |
|--------|--------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----|-----------|---------------------|
| FR-047 | Abo kündigen                   | Als Mitglied möchte ich mein Abo bis Ende September auf das Ende des Geschäftsjahres kündigen, damit ich im Folgejahr keine Beiträge mehr schulde.                                      | UC-011 | Hoch      | Implementiert |
| FR-048 | Mitgliedschaft kündigen        | Als Mitglied möchte ich meine Mitgliedschaft kündigen und dabei verständlich erklärt bekommen, weshalb das bei einem laufenden Abo nicht möglich ist, damit ich weiss, was zuerst zu tun ist. | UC-011 | Hoch | Verifiziert |
| FR-049 | Überzähligen Anteilschein kündigen | Als Mitglied möchte ich einen unbezahlten, für kein Abo benötigten Anteilschein kündigen, damit eine versehentliche Bestellung rückgängig gemacht werden kann.                     | UC-011 | Mittel    | Implementiert |
| FR-050 | Depot wechseln                 | Als Mitglied möchte ich mein Depot wechseln und den Wechsel bestätigt bekommen, damit ich meine Produkte am passenden Ort abhole.                                                       | —  | Mittel    | Nachzudokumentieren |

## Nicht-funktionale Anforderungen

| ID      | Titel                             | Anforderung                                                                                                                                          | Kategorie       | Priorität | Status         |
|---------|-----------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|-----------|----------------|
| NFR-001 | Sprache                           | 100 % der Oberflächen, Listen und systemseitigen Nachrichten sind deutsch (`LANGUAGE_CODE = 'de'`).                                                    | Usability       | Hoch      | Verifiziert    |
| NFR-002 | Zeitzone und Datumsformat         | 100 % der Datums- und Zeitangaben werden in der Zeitzone Europe/Zurich dargestellt, inklusive Sommerzeitumstellung.                                                                          | Usability       | Hoch      | Implementiert  |
| NFR-003 | Kein Versand auf Staging          | Auf der Staging-Umgebung werden 0 E-Mails zugestellt.                                                                                                  | Security        | Hoch      | Implementiert  |
| NFR-004 | Protokollierung ohne Rückwirkung  | Scheitert das Schreiben eines Protokolleintrags, werden dennoch 100 % der Nachrichten versendet.                                                        | Availability    | Hoch      | Implementiert  |
| NFR-005 | Unveränderliches Versandprotokoll | Über die Oberfläche ist keine Schreiboperation auf Protokolleinträgen möglich (0 Anlege-, Änderungs- oder Löschmasken).                                 | Security        | Hoch      | Implementiert  |
| NFR-006 | Schutz der Kontaktangaben         | Für Konten ohne die Berechtigung zur Einsicht in Einsatzanmeldungen werden in 0 Fällen Telefonnummern oder E-Mail-Adressen von Mitgliedern ausgeliefert.    | Security        | Hoch      | Implementiert  |
| NFR-007 | Kein Passwort-Reset für Deaktivierte | Deaktivierte Konten können in 0 Fällen ein Zurücksetzen des Passworts auslösen.                                                                      | Security        | Hoch      | Implementiert  |
| NFR-008 | Druckfertige Depotlisten          | Jede Depotliste passt ohne manuelle Nacharbeit auf A4; Mehl und Glarner Alpkäse im Querformat mit allen Produktgrössen auf einer Seitenbreite.          | Usability       | Hoch      | Implementiert  |
| NFR-009 | Zählung ohne JavaScript           | Seitenaufrufe werden auch bei deaktiviertem JavaScript über ein Zählbild erfasst (100 % der ausgelieferten Seiten binden den Zählmechanismus ein).      | Usability       | Niedrig   | Verifiziert    |
| NFR-010 | Betriebsprotokoll                 | Anwendungs- und Mailer-Protokoll werden ab Stufe INFO in rotierende Dateien von je 5 MB mit 5 Generationen geschrieben.                                 | Maintainability | Mittel    | Implementiert  |
| NFR-011 | E2E-Abdeckung der Use Cases       | Jeder Use Case UC-001 bis UC-010 ist durch mindestens einen Playwright-E2E-Test mit Screenshots an den Schlüsselmomenten abgedeckt.                     | Maintainability | Hoch      | In Bearbeitung |
| NFR-012 | Datenbankunabhängigkeit           | Dieselbe Codebasis läuft mit 0 Codeänderungen auf SQLite (lokal) und PostgreSQL (produktiv); die Auswahl erfolgt allein über Umgebungsvariablen.           | Portability     | Mittel    | Implementiert  |
| NFR-013 | Ladezeit der Einsatzübersicht     | Die Einsatzübersicht und die Einsatz-Teilnehmerliste werden bei bis zu 500 künftigen Einsätzen innerhalb von 2 Sekunden ausgeliefert.                   | Performance     | Mittel    | Zu bestätigen  |
| NFR-014 | Nutzungsspitzen                   | Am Tag der Depotabholung müssen 50 gleichzeitige Sitzungen ohne spürbare Verzögerung bedient werden.                                                    | Scalability     | Niedrig   | Zu bestätigen  |
| NFR-015 | Verfügbarkeit                     | Die Plattform ist zu 99 % im Monatsmittel erreichbar; Unterbrüche für Versionswechsel werden vorgängig angekündigt.                                     | Availability    | Mittel    | Zu bestätigen  |

> **Hinweis:** NFR-013 bis NFR-015 sind aus dem Betrieb hergeleitete Vorschläge. Die Schwellenwerte sind
> in keinem Quelldokument festgehalten und von der Koordination zu bestätigen oder anzupassen.

## Rahmenbedingungen

| ID    | Titel                          | Rahmenbedingung                                                                                                                                | Kategorie   | Priorität | Status        |
|-------|--------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|-------------|-----------|---------------|
| C-001 | Plattformbasis juntagrico      | Die Lösung baut auf juntagrico auf (aktuell 2.0.9); ein Fork der Plattform wird nicht geführt.                                                    | Technical   | Hoch      | Implementiert |
| C-002 | Eingesetzte Erweiterungen      | Rechnungsstellung, Einsatzmeldungen und Abfragekonsole stammen aus juntagrico-billing, juntagrico-assignment-request und juntagrico-pg (je 2.0.0). | Technical   | Hoch      | Implementiert |
| C-003 | Art der Anpassungen            | GartenBerg-Anpassungen erfolgen ausschliesslich als Konfiguration, Template-Überschreibung oder eigene Django-App unter `gartenberg/`.            | Technical   | Hoch      | Implementiert |
| C-004 | Laufzeitumgebung               | Die Anwendung läuft in einem Container auf Python 3.14.                                                                                          | Technical   | Hoch      | Implementiert |
| C-005 | Datenhaltung                   | Produktiv wird PostgreSQL eingesetzt, lokal SQLite.                                                                                              | Technical   | Hoch      | Implementiert |
| C-006 | Hosting und Hostnamen          | Betrieb als gehostete Instanz auf juntagrico.science; erreichbar unter `my.gartenberg.ch` und den konfigurierten Staging-Hostnamen.               | Operational | Hoch      | Implementiert |
| C-007 | Containerisiertes Tooling      | Alle Laufzeit- und Testkommandos laufen über `tooling/docker.sh`; `python`, `pip` und `manage.py` werden nicht direkt aufgerufen.                 | Operational | Hoch      | Implementiert |
| C-008 | Exakt gepinnte Abhängigkeiten  | Alle Abhängigkeiten in `requirements.txt` sind mit `==` gepinnt, damit Upgrades über die CI-Pipeline gehen.                                       | Technical   | Hoch      | Implementiert |
| C-009 | Trunk-based Development        | Es wird ohne Feature-Branches direkt auf `main` entwickelt und committet.                                                                         | Operational | Hoch      | Implementiert |
| C-010 | E2E-Testwerkzeug               | End-to-End-Tests werden mit Playwright und pytest geschrieben und erzeugen an Schlüsselmomenten Screenshots.                                      | Technical   | Hoch      | Implementiert |
| C-011 | Externe Grundlagendokumente    | Statuten, Betriebsreglement und häufige Fragen werden auf gartenberg.ch gepflegt und aus der Plattform nur verlinkt.                              | Business    | Mittel    | Implementiert |
| C-012 | Anteilscheinpreis              | Ein Anteilschein kostet CHF 750 und wird beim Austritt zurückerstattet.                                                                           | Business    | Hoch      | Implementiert |
| C-013 | Geschäftsjahr                  | Das Geschäftsjahr entspricht dem Kalenderjahr und beginnt am 1. Januar.                                                                           | Business    | Hoch      | Implementiert |
| C-014 | Kündigungsfristen              | Abos können bis Ende September gekündigt werden; die Mitgliedschaft endet am 31. Dezember bei einer Frist von 3 Monaten.                          | Business    | Hoch      | Implementiert |
| C-015 | Probe-Mitgliedschaft           | Die Probe-Mitgliedschaft ist auf drei Monate befristet, wird in den Grössen ganz, halb und mini angeboten und verlängert sich nicht automatisch.   | Business    | Hoch      | Implementiert |
| C-016 | Datenschutz Mitgliederdaten    | Mitgliederdaten werden ausschliesslich für den Betrieb der Genossenschaft verwendet und nicht an Dritte weitergegeben.                            | Regulatory  | Hoch      | Implementiert |

## Offene Punkte

- **Fehlender Use Case:** FR-050 (Depotwechsel) ist konfiguriert und durch E2E-Tests abgedeckt, aber in
  keiner `UC-*.md` spezifiziert. Er ist als UC-012 nachzuführen und anschliessend im Use-Case-Diagramm
  ([use_cases.puml](use_cases.puml)) zu ergänzen.
- **Fehlende Test Cases:** `CLAUDE.md` verweist auf `docs/test_cases/`; dieses Verzeichnis existiert noch
  nicht. Die in [e2e-testcases.md](e2e-testcases.md) beschriebene Abdeckung ist als `TC-*.md` zu
  formalisieren, damit NFR-011 nachweisbar wird.
- **Unbestätigte Schwellenwerte:** NFR-013 bis NFR-015 sind mit der Koordination zu verifizieren.
