# Use Case: Rundmail an Mitgliedergruppen versenden

## Übersicht

**Use-Case-ID:** UC-005  
**Use-Case-Name:** Rundmail an Mitgliedergruppen versenden  
**Primärer Akteur:** Administrator/in  
**Ziel:** Die Koordination informiert eine gezielt ausgewählte Gruppe von Mitgliedern und hinterlässt dabei einen nachvollziehbaren Beleg, wer wann was an wen verschickt hat.  
**Status:** Implementiert

## Vorbedingungen

- Die Administratorin ist angemeldet und berechtigt, Nachrichten an Mitgliedergruppen zu versenden.
- Der Nachrichtenversand der Plattform ist betriebsbereit.

## Hauptablauf

1. Die Administratorin ruft das Formular für den Versand an Mitgliedergruppen auf.
2. Die Administratorin wählt die Empfängergruppen aus: alle Abo-Bezieher/innen, alle Anteilschein-Besitzer/innen, einzelne Mitglieder, Tätigkeitsbereiche, Einsätze oder Depots.
3. Das System zeigt die Anzahl der so erreichten Empfänger/innen an.
4. Die Administratorin erfasst Absenderadresse, Betreff und Nachrichtentext und entscheidet, ob sie eine Kopie an sich selbst erhalten will.
5. Die Administratorin löst den Versand aus.
6. Das System hält Zeitpunkt, Absenderadresse, Betreff und die angeschriebenen Empfängergruppen im Versandprotokoll fest.
7. Das System stellt die Nachricht mit der Signatur der Genossenschaft an die ermittelten Empfänger/innen zu und zeigt die Bestätigungsseite an.

## Alternativabläufe

### A1: Empfängerkreis vorab prüfen

**Auslöser:** Die Administratorin will die Auswahl vor dem Versand kontrollieren (Schritt 3)  
**Ablauf:**

1. Die Administratorin lässt die Empfängerauswahl in das Formular übernehmen, ohne den Versand auszulösen.
2. Das System füllt das Formular vor und legt keinen Protokolleintrag an.
3. Der Use Case wird bei Schritt 4 fortgesetzt.

### A2: Angaben zur Nachricht unvollständig

**Auslöser:** Absenderadresse, Betreff oder Nachrichtentext fehlen (Schritt 5)  
**Ablauf:**

1. Das System zeigt das Formular erneut mit den beanstandeten Feldern an.
2. Die Administratorin ergänzt die Angaben.
3. Der Use Case wird bei Schritt 5 fortgesetzt.

### A3: Versand auf der Testumgebung

**Auslöser:** Der Versand erfolgt auf der Staging-Umgebung (Schritt 7)  
**Ablauf:**

1. Das System verwirft die Nachricht, statt sie zuzustellen, damit keine Mitglieder erreicht werden.
2. Der Use Case endet.

## Nachbedingungen

### Erfolgsfall

- Die Nachricht ist den Mitgliedern der gewählten Gruppen zugestellt.
- Im Versandprotokoll steht ein Eintrag mit Zeitpunkt, Absender, Betreff und Empfängergruppen.

### Fehlerfall

- Es wurde keine Nachricht zugestellt.
- Ein Fehler beim Schreiben des Protokolleintrags verhindert den Versand nicht.

## Geschäftsregeln

### GR-001: Protokollierung nur echter Versandvorgänge

Ein Protokolleintrag entsteht ausschliesslich beim tatsächlichen Absenden einer Nachricht. Das blosse Vorbefüllen des Formulars mit einer Empfängerauswahl und das Ermitteln der Empfängerzahl werden nicht protokolliert.

### GR-002: Protokollierte Angaben

Festgehalten werden Zeitpunkt, Absenderadresse, Betreff, die angeschriebenen Empfängergruppen und der verwendete Versandweg. Der Nachrichtentext und die einzelnen Empfängeradressen werden nicht protokolliert.

### GR-003: Bezeichnung der Empfängergruppen

Die Empfängergruppen werden im Protokoll in der Sprache der Genossenschaft festgehalten: Abo-BezieherInnen, Anteilsschein-BesitzerInnen, Einzelne Mitglieder, Tätigkeitsbereiche, Einsätze, Depots sowie die Kopie an den Absender. Fehlt eine Angabe, wird ein Platzhalter eingetragen.

### GR-004: Protokollierung darf den Versand nicht verhindern

Scheitert das Schreiben des Protokolleintrags, wird die Nachricht trotzdem versendet.

### GR-005: Kein Versand auf der Staging-Umgebung

Auf der Staging-Umgebung werden Nachrichten nicht zugestellt, damit Tests keine Mitglieder erreichen.

### GR-006: Signatur ausgehender Nachrichten

Jede versendete Nachricht wird um die Signatur der Genossenschaft ergänzt (siehe UC-002 GR-004).
