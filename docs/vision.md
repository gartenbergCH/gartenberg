# Vision: GartenBerg — juntagrico-Plattform der Genossenschaft GartenBerg

## Überblick

Die Genossenschaft GartenBerg betreibt eine solidarische Landwirtschaft in der Region Aarau: Mitglieder
zeichnen Anteilscheine, beziehen über ein Abo wöchentlich Gemüse sowie Hofprodukte (Kartoffeln, Mehl,
Glarner Alpkäse) in einem Depot ihrer Wahl und erbringen dafür Arbeitseinsätze.

Für die Abwicklung dieses Betriebs setzt GartenBerg die Open-Source-Plattform
[juntagrico](https://juntagrico.org/) ein. Dieses Projekt ist **nicht** eine Neuentwicklung, sondern die
GartenBerg-spezifische Ausprägung dieser Plattform: Konfiguration, angepasste Seiten, eigene Depotlisten
und die wenigen Erweiterungen, die GartenBerg selbst benötigt (Versandprotokoll für Rundmails,
Einsatz-Teilnehmerliste).

Ziel ist, dass die Plattform die **alleinige Quelle** für Mitglieder-, Abo-, Einsatz- und Rechnungsdaten
ist. Parallel geführte Excel-Listen und pCloud-Ablagen sollen entfallen, weil ihre doppelte Führung
fehleranfällig ist.

## Abgrenzung

Im Fokus stehen die GartenBerg-eigenen Anpassungen und jene Plattformabläufe, auf denen sie unmittelbar
aufbauen — Anmeldeprozess, Depotlisten, Arbeitseinsätze, Rundmailversand, Rechnungsstellung und
Abo-Verwaltung. Der übrige Funktionsumfang von juntagrico und seiner Erweiterungen wird verwendet, aber
in diesem Projekt weder spezifiziert noch verändert. Änderungen, die für alle juntagrico-Betreiber
sinnvoll sind, werden nach Möglichkeit stromaufwärts in juntagrico eingebracht statt hier nachgebaut.

## Nutzende und Rollen

- **Interessent/in**: Person ohne Mitgliedschaft, die sich über die Genossenschaft informiert, Kontakt
  aufnimmt und sich mit einem Abo anmeldet — als dreimonatige Probe-Mitgliedschaft ohne Anteilschein
  oder als volle Mitgliedschaft mit Anteilscheinen.
- **Mitglied**: Bezieht über ein Abo Produkte in einem Depot, meldet sich für ausgeschriebene Einsätze
  an, meldet selbständig geleistete Arbeit zur Anrechnung und verwaltet Profil, Abo und Anteilscheine.
- **Einsatzverantwortliche/r** (Gärtner/innen, Bereichskoordination): Beurteilt gemeldete Einsätze und
  braucht den Überblick, wer wann für welchen Einsatz eingeschrieben ist.
- **Administrator/in** (Koordination): Führt den Betrieb — erzeugt Depotlisten, versendet Rundmails,
  stellt Rechnungen und klärt Abo-Situationen einzelner Mitglieder ab.

## Kernfunktionen

- **Anmeldung und Mitgliedschaft**: Anmeldeprozess, der die auf drei Monate befristete
  Probe-Mitgliedschaft, den Anteilscheinpreis und die Grundlagendokumente sichtbar macht. Anteilscheine
  sind bei der Anmeldung nicht zwingend; der Start ist nicht nur zum Geschäftsjahr, sondern bei freien
  Plätzen auch auf den nächsten Monatsbeginn möglich.
- **Kontakt und Grundlagen**: Kontaktseite mit Adresse und Bankverbindung der Genossenschaft, Nachrichten
  an die allgemeine Kontaktadresse und Verweise auf Statuten, Betriebsreglement und häufige Fragen, die
  auf der Webseite der Genossenschaft gepflegt werden.
- **Arbeitseinsätze**: Anmeldung zu ausgeschriebenen Einsätzen, Meldung selbständig geleisteter Arbeit
  und deren Beurteilung durch eine verantwortliche Person. Angerechnet wird erst, was bestätigt ist.
- **Einsatzkoordination**: Eine Liste aller künftigen Einsätze mit den eingeschriebenen Personen und
  ihren Kontaktangaben, einschränkbar auf Tätigkeitsbereich oder Einsatzart.
- **Depotlisten**: Auf Knopfdruck zu einem frei gewählten Stichtag erzeugte, druckfertige Verteillisten —
  Hauptliste und Übersichten nur für Gemüse, je eine eigene Liste für Kartoffeln, Mehl und Glarner
  Alpkäse.
- **Rundmail mit Versandprotokoll**: Versand an gezielt gewählte Mitgliedergruppen; jeder tatsächliche
  Versand hinterlässt einen unveränderlichen Protokolleintrag, der Rückfragen und Verdacht auf
  Doppelversand klärt.
- **Rechnungen**: Rechnungslauf je Geschäftsjahr aus den Abo-Bestandteilen, Zustellung mit
  Referenznummer, Verbuchung der Zahlungseingänge und Ausgleich von Differenzen.
- **Abo-Verwaltung**: Übersicht pendenter und jüngster Abo-Änderungen, eindeutig bezeichnete
  Abo-Bestandteile und die Möglichkeit, die Sicht eines Mitglieds zu übernehmen.

## Qualitätsziele

Die Plattform wird von einer ehrenamtlichen Koordination betrieben und muss deshalb vor allem
**verlässlich** und **nachvollziehbar** sein: Versand und Entscheide hinterlassen Belege, und ein Fehler
in einer Nebenfunktion darf den eigentlichen Vorgang nicht verhindern. Sie ist durchgehend **deutsch**
und auf Schweizer Verhältnisse ausgelegt. Die Mitgliederdaten — insbesondere Kontaktangaben — sind
**geschützt** und nur Berechtigten zugänglich. Die Anpassungen bleiben **wartbar**, indem sie sich auf
Konfiguration und wenige eigene Bausteine beschränken und durch End-to-End-Tests abgesichert sind, damit
ein Versionswechsel von juntagrico beherrschbar bleibt. Auf der Testumgebung darf kein Mitglied
versehentlich erreicht werden.

## Rahmenbedingungen

- Basis ist juntagrico mit den Erweiterungen juntagrico-billing, juntagrico-assignment-request und
  juntagrico-pg. Eigene Anpassungen erfolgen als Django-App, Konfiguration und Template-Überschreibungen.
- Betrieb als gehostete Instanz (juntagrico.science) unter `my.gartenberg.ch` mit PostgreSQL; lokal wird
  mit SQLite gearbeitet.
- Alle Laufzeitkommandos laufen containerisiert über `tooling/docker.sh`; eine lokale Python-Installation
  wird nicht vorausgesetzt.
- Statuten, Betriebsreglement und häufige Fragen liegen auf der Webseite der Genossenschaft und werden
  nur verlinkt.
- Das Geschäftsjahr entspricht dem Kalenderjahr; ein Anteilschein kostet CHF 750.
- Entwickelt wird trunk-basiert direkt auf `main`, ohne Feature-Branches.
