# Use Case: Eigene Rechnungen einsehen

## Übersicht

**Use-Case-ID:** UC-012  
**Use-Case-Name:** Eigene Rechnungen einsehen  
**Primärer Akteur:** Mitglied  
**Sekundäre Akteure:** Administrator/in  
**Anforderungen:** FR-051  
**Ziel:** Ein Mitglied sieht seine freigegebenen Rechnungen samt Zahlungsstand jederzeit selbst ein, bezahlt sie mit dem angezeigten Einzahlungsschein und legt sie als PDF ab, ohne bei der Koordination nachfragen zu müssen.  
**Status:** Implementiert

## Vorbedingungen

- Das Mitglied ist angemeldet.
- Für das Mitglied besteht mindestens eine freigegebene Rechnung aus dem Rechnungslauf (UC-007).
- Die Zahlungsart der Genossenschaft mit der Kontoverbindung für den Einzahlungsschein ist erfasst.

## Hauptablauf

1. Das Mitglied ruft in seinem Menü die Rechnungen auf.
2. Das System listet die freigegebenen Rechnungen des Mitglieds mit Rechnungsnummer, Rechnungsdatum, Art der Positionen, Betrag und Zahlungsstand auf, die neueste zuerst.
3. Das Mitglied öffnet eine Rechnung.
4. Das System zeigt die Rechnung mit Empfänger, verrechnetem Zeitraum, den einzelnen Positionen, dem Gesamtbetrag und — sofern ein Steuersatz gesetzt ist — dem Steueranteil samt Mehrwertsteuernummer an.
5. Das System weist die bisher verbuchten Zahlungen mit Datum und Betrag sowie den zum heutigen Tag noch offenen Betrag aus.
6. Das System zeigt zum offenen Betrag den Einzahlungsschein mit Zahlungsempfänger, Kontoverbindung und Referenznummer an.
7. Das Mitglied lädt die Rechnung als PDF herunter und begleicht den offenen Betrag.
8. Die Administratorin verbucht den Zahlungseingang (UC-007).
9. Das System führt die Rechnung als bezahlt und zeigt sie dem Mitglied ohne Einzahlungsschein an.

## Alternativabläufe

### A1: Keine Rechnungen vorhanden

**Auslöser:** Für das Mitglied besteht keine freigegebene Rechnung, etwa weil das Abo erst im nächsten Geschäftsjahr beginnt (Schritt 2)  
**Ablauf:**

1. Das System zeigt die Rechnungsliste ohne Einträge an.
2. Der Use Case endet.

### A2: Rechnung noch nicht freigegeben

**Auslöser:** Die Rechnung des Mitglieds ist erzeugt, aber noch nicht freigegeben (Schritt 2)  
**Ablauf:**

1. Das System führt die Rechnung nicht in der Liste.
2. Der Use Case wird fortgesetzt, sobald die Administratorin die Rechnung freigegeben hat (UC-007 Schritt 5).

### A3: Teilzahlung

**Auslöser:** Die verbuchten Zahlungen decken den Rechnungsbetrag nicht vollständig (Schritt 5)  
**Ablauf:**

1. Das System weist die Rechnung weiterhin als nicht bezahlt aus und zeigt den verbleibenden offenen Betrag.
2. Der Einzahlungsschein lautet auf den offenen Betrag statt auf den Rechnungsbetrag.
3. Der Use Case wird bei Schritt 7 fortgesetzt.

### A4: Zugriff auf eine fremde oder stornierte Rechnung

**Auslöser:** Das Mitglied ruft eine Rechnung auf, die einem anderen Mitglied gehört oder storniert wurde (Schritt 3)  
**Ablauf:**

1. Das System verweigert den Zugriff.
2. Der Use Case endet.

## Nachbedingungen

### Erfolgsfall

- Das Mitglied kennt seine freigegebenen Rechnungen, deren Positionen und den offenen Betrag.
- Das Mitglied verfügt über Einzahlungsschein und PDF, um die Rechnung zu begleichen und abzulegen.
- Am Rechnungsbestand und an den verbuchten Zahlungen hat sich nichts geändert.

### Fehlerfall

- Dem Mitglied werden keine Rechnungsdaten angezeigt.
- Rechnungen und Zahlungen bleiben unverändert.

## Geschäftsregeln

### GR-001: Sichtbarkeit erst nach Freigabe

Dem Mitglied werden ausschliesslich freigegebene Rechnungen angezeigt. Erzeugte, aber noch nicht freigegebene Rechnungen sind nicht Teil der Liste; stornierte Rechnungen sind für das Mitglied weder sichtbar noch abrufbar.

### GR-002: Zugriff nur auf eigene Rechnungen

Ein Mitglied sieht ausschliesslich die an es selbst gerichteten Rechnungen. Nur Konten mit der Berechtigung zur Rechnungsbearbeitung können jede Rechnung öffnen.

### GR-003: Einzahlungsschein nur bei offenem Betrag

Der Einzahlungsschein wird nur ausgewiesen, solange ein Betrag offen ist, und lautet auf diesen offenen Betrag (siehe UC-007 GR-006). Er trägt die Referenznummer der Rechnung, damit die Zahlung automatisch zugeordnet werden kann (siehe UC-007 GR-005).

### GR-004: Neueste Rechnung zuerst

Die Rechnungen werden nach Rechnungsdatum absteigend aufgelistet, damit die aktuelle Rechnung zuoberst steht.

### GR-005: Zahlungsstand aus verbuchten Zahlungen

Zahlungsstand und offener Betrag ergeben sich allein aus den von der Koordination verbuchten Zahlungen (UC-007). Das Mitglied kann keine Zahlung erfassen und den Zahlungsstand nicht verändern.
