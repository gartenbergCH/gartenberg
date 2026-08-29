# Use Case: Kontakt zur Genossenschaft aufnehmen

## Übersicht

**Use-Case-ID:** UC-002  
**Use-Case-Name:** Kontakt zur Genossenschaft aufnehmen  
**Primärer Akteur:** Interessent/in  
**Sekundäre Akteure:** Mitglied  
**Ziel:** Eine interessierte Person oder ein Mitglied findet die verbindlichen Angaben der Genossenschaft GartenBerg — Adresse, Bankverbindung und Grundlagendokumente — und stellt eine Frage, die bei der zuständigen Stelle ankommt.  
**Status:** Implementiert

## Vorbedingungen

- Die Kontaktangaben, die Postadresse und die Bankverbindung der Genossenschaft sind hinterlegt.
- Der Nachrichtenversand der Plattform ist betriebsbereit.

## Hauptablauf

1. Der Akteur ruft die Kontaktseite auf.
2. Das System zeigt die vollständige Adresse der Genossenschaft sowie die allgemeine Kontaktadresse an.
3. Der Akteur erfasst seine Nachricht und sendet sie ab.
4. Das System stellt die Nachricht an die allgemeine Kontaktadresse der Genossenschaft zu und ergänzt sie um die Signatur mit dem Verweis auf die Webseite der Genossenschaft.
5. Das System bestätigt dem Akteur den Versand.

## Alternativabläufe

### A1: Zahlungsangaben werden benötigt

**Auslöser:** Ein Mitglied ruft die Übersicht seiner unbezahlten Anteilscheine auf, statt eine Nachricht zu senden (Schritt 3)  
**Ablauf:**

1. Das System zeigt die offenen Anteilscheine zusammen mit der Bankverbindung und dem Zahlungsempfänger der Genossenschaft an.
2. Der Use Case endet.

### A2: Grundlagendokumente werden benötigt

**Auslöser:** Der Akteur sucht Statuten, Betriebsreglement oder die häufigen Fragen, statt eine Nachricht zu senden (Schritt 3)  
**Ablauf:**

1. Das System verweist von der Anmelde-, Abo- und Mitgliedschaftsseite auf die extern abgelegten Dokumente.
2. Der Akteur ruft das gewünschte Dokument auf.
3. Der Use Case endet.

### A3: Nachricht unvollständig

**Auslöser:** Pflichtangaben der Nachricht fehlen (Schritt 4)  
**Ablauf:**

1. Das System zeigt das Kontaktformular erneut mit den beanstandeten Feldern an.
2. Der Akteur ergänzt die Angaben.
3. Der Use Case wird bei Schritt 4 fortgesetzt.

## Nachbedingungen

### Erfolgsfall

- Die Nachricht ist bei der allgemeinen Kontaktadresse der Genossenschaft eingegangen.
- Der Akteur hat eine Versandbestätigung erhalten.

### Fehlerfall

- Es wurde keine Nachricht zugestellt; die erfassten Angaben bleiben zur Korrektur erhalten.

## Geschäftsregeln

### GR-001: Allgemeine Kontaktadresse

Anfragen ohne bestimmte Zuständigkeit gehen an die allgemeine Kontaktadresse der Genossenschaft. Diese ist auch Absenderadresse für systemseitige Nachrichten wie das Zurücksetzen des Passworts.

### GR-002: Postadresse der Genossenschaft

Als Adresse wird die Genossenschaft GartenBerg mit ihrer Zustelladresse in 5000 Aarau ausgewiesen, ergänzt um die Angabe der aktuell zuständigen Person.

### GR-003: Bankverbindung

Zahlungen erfolgen auf die hinterlegte IBAN der Genossenschaft; als Zahlungsempfänger wird die Genossenschaft mit ihrer Zustelladresse angegeben. Postkonto, BIC und ESR-Teilnehmernummer werden nicht geführt.

### GR-004: Signatur ausgehender Nachrichten

Ausgehende Nachrichten enden mit einem Verweis auf die Webseite der Genossenschaft. Eine Postadresse wird in der Signatur bewusst nicht mehr geführt.

### GR-005: Verlinkte Grundlagendokumente

Statuten, Betriebsreglement und die häufigen Fragen liegen auf der Webseite der Genossenschaft und werden aus der Plattform heraus verlinkt, statt in ihr gepflegt zu werden.

### GR-006: Erfassung der Seitenaufrufe

Jede ausgelieferte Seite bindet den Zählmechanismus des von der Genossenschaft betriebenen Statistikdienstes ein. Ist im Browser kein JavaScript aktiv, erfolgt die Zählung über ein Zählbild. Diese Regel gilt für alle Seiten der Plattform, nicht nur für die Kontaktseite.
