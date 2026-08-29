# Use Case: Mailversand nachvollziehen

## Übersicht

**Use-Case-ID:** UC-006  
**Use-Case-Name:** Mailversand nachvollziehen  
**Primärer Akteur:** Administrator/in  
**Ziel:** Die Koordination klärt anhand des Versandprotokolls, welche Rundmails wann von wem an welche Mitgliedergruppen verschickt wurden, etwa bei einer Rückfrage eines Mitglieds oder beim Verdacht auf einen Doppelversand.  
**Status:** Implementiert

## Vorbedingungen

- Die Administratorin ist am Verwaltungsbereich angemeldet und berechtigt, das Versandprotokoll einzusehen.
- Es wurden bereits Rundmails versendet (siehe UC-005).

## Hauptablauf

1. Die Administratorin ruft das Versandprotokoll im Verwaltungsbereich auf.
2. Das System zeigt die Einträge, neueste zuerst, mit Zeitpunkt, Absender, Betreff, Empfängergruppen und Versandweg.
3. Die Administratorin schränkt die Liste nach Absender oder Versandweg ein oder sucht nach Absender oder Betreff.
4. Das System zeigt die passenden Einträge an.
5. Die Administratorin öffnet den fraglichen Eintrag und liest die festgehaltenen Angaben.
6. Die Administratorin beantwortet die Rückfrage auf Basis der Protokollangaben.

## Alternativabläufe

### A1: Kein passender Eintrag vorhanden

**Auslöser:** Zur Suchanfrage besteht kein Protokolleintrag (Schritt 4)  
**Ablauf:**

1. Das System zeigt eine leere Liste an.
2. Die Administratorin schliesst daraus, dass über die Rundmail-Funktion kein solcher Versand erfolgt ist.
3. Der Use Case endet.

### A2: Korrektur eines Eintrags gewünscht

**Auslöser:** Die Administratorin möchte einen Eintrag ändern, ergänzen oder von Hand anlegen (Schritt 5)  
**Ablauf:**

1. Das System bietet weder das Anlegen noch das Ändern von Einträgen an; alle Felder sind schreibgeschützt.
2. Der Use Case endet.

## Nachbedingungen

### Erfolgsfall

- Die Administratorin kennt Zeitpunkt, Absender, Betreff und Empfängergruppen des gesuchten Versands.
- Das Protokoll ist unverändert.

### Fehlerfall

- Das Protokoll ist unverändert; die Frage bleibt anhand des Protokolls unbeantwortet.

## Geschäftsregeln

### GR-001: Unveränderliches Protokoll

Protokolleinträge können weder von Hand angelegt noch nachträglich geändert werden. Alle Felder sind schreibgeschützt, damit das Protokoll als Beleg taugt.

### GR-002: Sortierung nach Aktualität

Das Protokoll wird immer mit dem jüngsten Eintrag zuoberst angezeigt.

### GR-003: Auswertbarkeit

Das Protokoll lässt sich nach Absender und Versandweg filtern sowie nach Absender und Betreff durchsuchen.

### GR-004: Umfang der Protokollangaben

Das Protokoll enthält keine Nachrichtentexte und keine einzelnen Empfängeradressen (siehe UC-005 GR-002). Für inhaltliche Fragen ist die versendete Nachricht selbst heranzuziehen.
