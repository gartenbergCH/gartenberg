# Use Case: Mitgliedschaft und Abo kündigen

## Übersicht

**Use-Case-ID:** UC-011  
**Use-Case-Name:** Mitgliedschaft und Abo kündigen  
**Primärer Akteur:** Mitglied  
**Sekundäre Akteure:** Administrator/in  
**Anforderungen:** FR-047, FR-048, FR-049  
**Ziel:** Ein Mitglied beendet sein Engagement bei der Genossenschaft GartenBerg in der richtigen Reihenfolge — zuerst das Abo, dann die Mitgliedschaft mit den Anteilscheinen — und kennt dabei den jeweils geltenden Kündigungstermin und die Folgen der Kündigung.  
**Status:** Implementiert

## Vorbedingungen

- Das Mitglied ist angemeldet.
- Das Mitglied ist Hauptperson eines laufenden oder künftigen Abos oder hält Anteilscheine.
- Die Kündigungstermine der Genossenschaft — Kündigungsmonat des Abos und Ende der Mitgliedschaft — sind hinterlegt.

## Hauptablauf

1. Das Mitglied ruft die Übersicht seines Abos auf.
2. Das System zeigt das Abo mit seinen Bestandteilen und die Möglichkeit zur Kündigung an.
3. Das Mitglied ruft die Kündigung des Abos auf.
4. Das System zeigt den nächsten regulären Kündigungstermin des Abos an.
5. Das Mitglied erfasst eine Mitteilung an die Genossenschaft und bestätigt die Kündigung verbindlich.
6. Das System führt das Abo samt seinen Bestandteilen als auf diesen Termin gekündigt und benachrichtigt die Koordination mit der Mitteilung des Mitglieds.
7. Das Mitglied ruft die Mitgliedschaftsseite auf und wählt die Kündigung der Mitgliedschaft.
8. Das System stellt fest, dass weder ein laufendes noch ein künftiges Abo besteht und keine Anteilscheine mehr für ein Abo benötigt werden, und zeigt den nächsten Kündigungstermin sowie die Folgen der Kündigung an: keine weiteren Nachrichten, Austragung aus dem Abo und Kündigung der Anteilscheine.
9. Das Mitglied überprüft die für die Rückerstattung nötige Zahlungsverbindung und Adresse und bestätigt die Kündigung verbindlich.
10. Das System führt die Mitgliedschaft als auf das Ende der Mitgliedschaft gekündigt, kündigt die Anteilscheine des Mitglieds auf denselben Termin und benachrichtigt die Koordination.
11. Das System zeigt dem Mitglied auf seinem Profil die erfasste Kündigung mit dem Enddatum an, womit die Kündigung vollständig erfasst ist.

## Alternativabläufe

### A1: Mitgliedschaft wegen laufendem Abo nicht kündbar

**Auslöser:** Das Mitglied hat ein laufendes oder künftiges, nicht gekündigtes Abo (Schritt 8)  
**Ablauf:**

1. Das System zeigt statt des Kündigungsformulars einen Hinweis an, dass die Mitgliedschaft wegen des bestehenden Abos nicht gekündigt werden kann.
2. Das Mitglied kündigt zuerst das Abo.
3. Der Use Case wird bei Schritt 3 fortgesetzt.

### A2: Anteilschein wird noch für ein Abo benötigt

**Auslöser:** Die Anteilscheine des Mitglieds werden noch für ein laufendes oder künftiges Abo benötigt (Schritt 8)  
**Ablauf:**

1. Das System zeigt statt des Kündigungsformulars einen Hinweis an, dass die Anteilscheine noch für ein Abo gebunden sind.
2. Der Use Case endet.

### A3: Zahlungsverbindung fehlt

**Auslöser:** Für die Rückerstattung der Anteilscheine ist keine Zahlungsverbindung hinterlegt (Schritt 9)  
**Ablauf:**

1. Das System weist die Kündigung zurück und verlangt die Zahlungsverbindung.
2. Das Mitglied trägt Zahlungsverbindung und Adresse nach.
3. Der Use Case wird bei Schritt 9 fortgesetzt.

### A4: Kündigung nach dem Kündigungstermin

**Auslöser:** Das Mitglied kündigt das Abo nach dem Kündigungstermin des laufenden Geschäftsjahres (Schritt 4)  
**Ablauf:**

1. Das System weist als Kündigungstermin das Ende des nächsten Geschäftsjahres aus.
2. Der Use Case wird bei Schritt 5 fortgesetzt.

### A5: Kündigung durch Mitbezüger/in

**Auslöser:** Das Mitglied ist Mitbezüger/in und nicht Hauptperson des Abos (Schritt 3)  
**Ablauf:**

1. Das System bietet dem Mitglied keine Kündigung des Abos an, sondern nur den Austritt aus dem Abo.
2. Das Mitglied trägt sich aus dem Abo aus; das Abo der übrigen Bezüger/innen bleibt bestehen.
3. Der Use Case wird bei Schritt 7 fortgesetzt.

### A6: Nur einzelner Abo-Bestandteil gekündigt

**Auslöser:** Das Mitglied will nur einen Bestandteil abbestellen und das Abo behalten (Schritt 3)  
**Ablauf:**

1. Das Mitglied kündigt den einzelnen Abo-Bestandteil.
2. Das System führt den Bestandteil als gekündigt und benachrichtigt die Koordination; das übrige Abo bleibt bestehen.
3. Der Use Case endet.

### A7: Überzähligen Anteilschein kündigen

**Auslöser:** Das Mitglied hält mehr Anteilscheine als nötig und will einen zurückgeben, ohne die Mitgliedschaft zu beenden (Schritt 7)  
**Ablauf:**

1. Das Mitglied ruft die Übersicht seiner Anteilscheine auf.
2. Das System bietet die Kündigung nur bei noch nicht bezahlten Anteilscheinen an, die weder für ein Abo benötigt werden noch der letzte verbleibende Anteilschein sind, und nur solange eine Zahlungsverbindung hinterlegt ist.
3. Das Mitglied kündigt den überzähligen Anteilschein und bestätigt den angezeigten Kündigungstermin.
4. Das System führt den Anteilschein als gekündigt und benachrichtigt die Koordination.
5. Der Use Case endet.

### A8: Kündigung rückgängig machen

**Auslöser:** Das Mitglied hat versehentlich gekündigt und meldet sich bei der Koordination (Schritt 11)  
**Ablauf:**

1. Die Administratorin entfernt das Kündigungsdatum in der Verwaltung.
2. Das System führt Abo, Mitgliedschaft beziehungsweise Anteilschein wieder als ungekündigt.
3. Der Use Case endet.

## Nachbedingungen

### Erfolgsfall

- Abo und Abo-Bestandteile sind auf den ausgewiesenen Kündigungstermin gekündigt.
- Die Mitgliedschaft ist auf das Ende der Mitgliedschaft gekündigt und die Anteilscheine des Mitglieds sind auf denselben Termin gekündigt.
- Die Koordination ist über jede Kündigung samt der Mitteilung des Mitglieds informiert.
- Für die Rückerstattung der Anteilscheine liegen Zahlungsverbindung und Adresse vor.

### Fehlerfall

- Weder Abo noch Mitgliedschaft noch Anteilscheine sind gekündigt.
- Das Mitglied bleibt mit unveränderten Daten Mitglied und kann die Kündigung erneut auslösen.

## Geschäftsregeln

### GR-001: Kündigungstermin des Abos

Ein Abo kann bis zum 30. September auf das Ende des laufenden Geschäftsjahres gekündigt werden. Nach diesem Datum wirkt die Kündigung auf das Ende des nächsten Geschäftsjahres. Das Geschäftsjahr endet bei GartenBerg am 31. Dezember (siehe UC-007 GR-001).

### GR-002: Kündigungsfrist der Mitgliedschaft

Die Mitgliedschaft endet jeweils am 31. Dezember bei einer Kündigungsfrist von drei Monaten. Eine bis Ende September erklärte Kündigung wirkt somit auf das Ende desselben Jahres, eine spätere auf das Ende des Folgejahres.

### GR-003: Reihenfolge von Abo- und Mitgliedschaftskündigung

Die Mitgliedschaft lässt sich erst kündigen, wenn weder ein laufendes noch ein künftiges, nicht gekündigtes Abo besteht. Andernfalls zeigt das System einen Hinweis mit dem Grund an, statt das Kündigungsformular anzubieten.

### GR-004: Für ein Abo gebundene Anteilscheine

Anteilscheine, die für ein laufendes oder künftiges Abo benötigt werden, können nicht gekündigt werden. Wie viele Anteilscheine gebunden sind, ergibt sich aus den Bestandteilen des Abos (siehe UC-001 GR-003).

### GR-005: Verbleibender Anteilschein

Solange die Mitgliedschaft besteht, bleibt mindestens ein Anteilschein bestehen. Einzeln kündbar sind nur Anteilscheine, die darüber hinausgehen und für kein Abo gebunden sind. Alle Anteilscheine werden erst mit der Kündigung der Mitgliedschaft gekündigt.

### GR-006: Rückerstattung der Anteilscheine

Anteilscheine werden beim Austritt zum Ausgabepreis von CHF 750 zurückerstattet (siehe UC-001 GR-001). Eine Kündigung ist deshalb nur möglich, wenn Zahlungsverbindung und Adresse des Mitglieds hinterlegt sind.

### GR-007: Kündigung des Abos nur durch die Hauptperson

Das Abo kann nur die Hauptperson kündigen. Mitbezüger/innen können sich lediglich aus dem Abo austragen; das Abo bleibt für die übrigen Bezüger/innen bestehen.

### GR-008: Benachrichtigung der Koordination

Jede Kündigung — Abo, einzelner Abo-Bestandteil, Mitgliedschaft und Anteilschein — wird der Koordination gemeldet, damit sie die Folgearbeiten auslösen kann. Bei der Kündigung von Abo und Mitgliedschaft wird die Mitteilung des Mitglieds mitgeliefert.

### GR-009: Wirkung erst auf den Kündigungstermin

Eine Kündigung wirkt auf den ausgewiesenen Termin. Bis dahin bleiben Bezugsrecht, Beitragspflicht und Einsatzpflicht des Mitglieds unverändert bestehen.

### GR-010: Rücknahme einer Kündigung

Eine versehentlich erfasste Kündigung kann nur die Administration rückgängig machen, indem sie das Kündigungsdatum in der Verwaltung entfernt. Das Mitglied kann seine Kündigung nicht selbst zurückziehen.
