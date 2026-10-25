# Use Case: Ausstehende Arbeitseinsätze nachfassen

## Übersicht

**Use-Case-ID:** UC-013  
**Use-Case-Name:** Ausstehende Arbeitseinsätze nachfassen  
**Primärer Akteur:** Administrator/in  
**Ziel:** Die Koordination erinnert gezielt die Abo-Bezüger/innen, die ihre Mitarbeitspflicht im
gewählten Zeitraum noch nicht erfüllt haben, ohne deren E-Mail-Adressen einzeln zusammenzusuchen.  
**Status:** Implementiert

## Kontext

Die Einsatzübersicht der Verwaltung (`/manage/assignments`) zeigt je Abo die geleisteten und die
benötigten Einsätze sowie den Erfüllungsgrad in Prozent. Um Bezüger/innen mit offenen Einsätzen
anzuschreiben, mussten bisher die Zeilen über den Suchfilter eingeschränkt oder von Hand
ausgewählt werden.

## Vorbedingungen

- Die Person ist angemeldet und darf Einsätze einsehen oder ändern.
- Die Person darf E-Mail-Adressen sehen bzw. Mails versenden.

## Hauptablauf

1. Die Person ruft die Einsatzübersicht der Verwaltung auf und wählt bei Bedarf den Zeitraum.
2. Das System zeigt je Abo die Einsätze, die benötigten Einsätze und den Arbeitseinsätze-Status.
3. Die Person klickt auf «E-Mails unter 100 % kopieren».
4. Das System kopiert die E-Mail-Adressen aller Abos mit einem Arbeitseinsätze-Status unter 100 %
   in die Zwischenablage, je Adresse eine Zeile, und bestätigt das Kopieren auf der Schaltfläche.
5. Die Person fügt die Adressen in ihr Mailprogramm ein und verschickt die Erinnerung.

## Alternativabläufe

### A1: Auswahl oder Filter aktiv

**Auslöser:** Die Person hat Zeilen ausgewählt oder die Tabelle über Suche bzw. Filter eingeschränkt (Schritt 3)  
**Ablauf:**

1. Das System berücksichtigt nur die ausgewählten bzw. sichtbaren Zeilen und kopiert davon die
   Adressen der Abos unter 100 %.
2. Der Use Case wird bei Schritt 5 fortgesetzt.

### A2: Alle Abos erfüllt

**Auslöser:** Kein berücksichtigtes Abo hat einen Status unter 100 % (Schritt 3)  
**Ablauf:**

1. Das System deaktiviert die Schaltfläche.
2. Der Use Case endet.

## Nachbedingungen

### Erfolgsfall

- Die Zwischenablage enthält jede betroffene E-Mail-Adresse genau einmal.

### Fehlerfall

- Ohne Berechtigung ist die Seite nicht zugänglich; es werden keine Adressen preisgegeben.

## Geschäftsregeln

### GR-001: Massgebender Status

Massgebend ist der in der Tabelle angezeigte Arbeitseinsätze-Status (alle Einsätze, nicht nur
Kernbereich) für den gewählten Zeitraum. Er zählt wie die Tabelle auch angemeldete, aber noch
nicht stattgefundene Einsätze im Zeitraum. Abos ohne Einsatzpflicht gelten als zu 100 % erfüllt.

### GR-002: Mitbezüger/innen

Es gelten dieselben Anzeigeschalter wie für «E-Mails kopieren»: Die Adressen der Mitbezüger/innen
werden nur kopiert, wenn «MitabonnentInnen anzeigen» eingeschaltet ist.
