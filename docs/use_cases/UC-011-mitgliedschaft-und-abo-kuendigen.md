# Use Case: Mitgliedschaft und Abo kündigen

## Übersicht

**Use-Case-ID:** UC-011  
**Use-Case-Name:** Mitgliedschaft und Abo kündigen  
**Primärer Akteur:** Mitglied  
**Sekundäre Akteure:** Administrator/in  
**Anforderungen:** FR-047, FR-048, FR-049  
**Ziel:** Ein Mitglied beendet sein Engagement bei der Genossenschaft GartenBerg — Abo, Mitgliedschaft und Anteilscheine gemeinsam oder einzeln — und kennt dabei den jeweils geltenden Kündigungstermin und die Folgen der Kündigung.  
**Status:** Genehmigt

## Vorbedingungen

- Das Mitglied ist angemeldet.
- Das Mitglied ist Hauptperson oder Mitbezüger/in eines laufenden oder künftigen Abos, hat eine beantragte oder aktive Mitgliedschaft oder hält Anteilscheine.
- Die Kündigungstermine der Genossenschaft — Kündigungsmonat des Abos und Ende der Mitgliedschaft — sind hinterlegt.

## Hauptablauf

1. Das Mitglied ruft auf seinem Profil die Kündigung auf.
2. Das System zeigt auf einer gemeinsamen Kündigungsseite für jedes eigene Abo den nächsten regulären Kündigungstermin, die Wahl zwischen Kündigen und Behalten der Mitgliedschaft, die Anzahl kündbarer Anteilscheine, die Tätigkeitsbereiche, in denen das Mitglied bleiben möchte, sowie die für die Rückerstattung nötige Zahlungsverbindung und Adresse an.
3. Das Mitglied wählt, was es kündigt, überprüft Zahlungsverbindung und Adresse, erfasst optional eine Mitteilung an die Genossenschaft und bestätigt die Kündigung verbindlich.
4. Das System prüft, dass die Mitgliedschaft für kein behaltenes Abo mehr benötigt wird und genügend Anteilscheine für die behaltenen Abos verbleiben.
5. Das System führt die gewählten Abos samt Bestandteilen als auf ihren Termin gekündigt, die Mitgliedschaft als auf das Ende der Mitgliedschaft gekündigt und die gewählten Anteilscheine als gekündigt, trägt das Mitglied aus den abgewählten Tätigkeitsbereichen aus und benachrichtigt die Koordination mit der Mitteilung des Mitglieds.
6. Das System bestätigt dem Mitglied jede erfasste Kündigung und zeigt auf seinem Profil die gekündigte Mitgliedschaft mit dem Kündigungsdatum an, womit die Kündigung vollständig erfasst ist.

## Alternativabläufe

### A1: Mitgliedschaft noch für ein behaltenes Abo benötigt

**Auslöser:** Das Mitglied kündigt die Mitgliedschaft, behält aber ein Abo, das eine Mitgliedschaft erfordert (Schritt 4)  
**Ablauf:**

1. Das System weist darauf hin, dass die Mitgliedschaft noch für das Abo benötigt wird, und lässt die Kündigung nicht zu.
2. Das Mitglied kündigt das Abo mit oder behält die Mitgliedschaft.
3. Der Use Case wird bei Schritt 3 fortgesetzt.

### A2: Anteilscheine noch für ein behaltenes Abo benötigt

**Auslöser:** Nach der Kündigung blieben weniger Anteilscheine, als die behaltenen Abos benötigen (Schritt 4)  
**Ablauf:**

1. Das System weist auf die noch benötigten Anteilscheine hin und lässt die Kündigung nicht zu.
2. Das Mitglied verringert die Anzahl zu kündigender Anteilscheine oder kündigt das Abo mit.
3. Der Use Case wird bei Schritt 3 fortgesetzt.

### A3: Zahlungsverbindung fehlt

**Auslöser:** Das Mitglied kündigt Anteilscheine, ohne dass eine Zahlungsverbindung und Adresse für die Rückerstattung hinterlegt sind (Schritt 4)  
**Ablauf:**

1. Das System weist die Kündigung zurück und verlangt Zahlungsverbindung und Adresse.
2. Das Mitglied trägt Zahlungsverbindung und Adresse nach.
3. Der Use Case wird bei Schritt 3 fortgesetzt.

### A4: Nichts zur Kündigung gewählt

**Auslöser:** Das Mitglied bestätigt, ohne etwas zur Kündigung gewählt zu haben (Schritt 4)  
**Ablauf:**

1. Das System fordert das Mitglied auf zu wählen, was es kündigen möchte, und verwirft eine allfällige Mitteilung nicht.
2. Der Use Case wird bei Schritt 3 fortgesetzt.

### A5: Kündigung nach dem Kündigungstermin

**Auslöser:** Das Mitglied kündigt das Abo nach dem Kündigungstermin des laufenden Geschäftsjahres (Schritt 2)  
**Ablauf:**

1. Das System weist als Kündigungstermin das Ende des nächsten Geschäftsjahres aus.
2. Der Use Case wird bei Schritt 3 fortgesetzt.

### A6: Austritt als Mitbezüger/in

**Auslöser:** Das Mitglied ist Mitbezüger/in und nicht Hauptperson eines Abos (Schritt 2)  
**Ablauf:**

1. Das System bietet für dieses Abo keine Kündigung an, sondern den Austritt auf ein wählbares Datum mit einer Mitteilung an die Hauptperson.
2. Das Mitglied wählt den Austritt; das Abo der übrigen Bezüger/innen bleibt bestehen und die Hauptperson wird benachrichtigt.
3. Der Use Case wird bei Schritt 3 fortgesetzt.

### A7: Nur einzelner Abo-Bestandteil gekündigt

**Auslöser:** Das Mitglied will nur einen Bestandteil abbestellen und das Abo behalten (Schritt 1)  
**Ablauf:**

1. Das Mitglied kündigt den einzelnen Abo-Bestandteil auf der Übersicht seines Abos.
2. Das System führt den Bestandteil als gekündigt und benachrichtigt die Koordination; das übrige Abo bleibt bestehen.
3. Der Use Case endet.

### A8: Überzähligen Anteilschein kündigen

**Auslöser:** Das Mitglied will einen einzelnen Anteilschein zurückgeben, ohne die Mitgliedschaft zu beenden (Schritt 1)  
**Ablauf:**

1. Das Mitglied ruft die Übersicht seiner Anteilscheine auf.
2. Das System bietet die Kündigung nur bei noch nicht bezahlten Anteilscheinen an, die für kein Abo benötigt werden, und nur solange eine Zahlungsverbindung hinterlegt ist.
3. Das Mitglied kündigt den überzähligen Anteilschein und bestätigt den angezeigten Kündigungstermin.
4. Das System führt den Anteilschein als gekündigt und benachrichtigt die Koordination.
5. Der Use Case endet.

### A9: Kündigung der Mitgliedschaft zurückziehen

**Auslöser:** Das Mitglied hat die Mitgliedschaft gekündigt und möchte doch bleiben (Schritt 6)  
**Ablauf:**

1. Das Mitglied zieht auf seinem Profil die Kündigung der Mitgliedschaft zurück und bestätigt die Beitrittserklärung erneut.
2. Das System führt die Mitgliedschaft wieder als ungekündigt und benachrichtigt die Koordination.
3. Der Use Case endet.

### A10: Kündigung von Abo oder Anteilschein rückgängig machen

**Auslöser:** Das Mitglied hat ein Abo oder einen Anteilschein versehentlich gekündigt und meldet sich bei der Koordination (Schritt 6)  
**Ablauf:**

1. Die Administratorin entfernt das Kündigungsdatum in der Verwaltung.
2. Das System führt Abo beziehungsweise Anteilschein wieder als ungekündigt.
3. Der Use Case endet.

## Nachbedingungen

### Erfolgsfall

- Die gewählten Abos und ihre Bestandteile sind auf den ausgewiesenen Kündigungstermin gekündigt.
- Eine gekündigte Mitgliedschaft ist auf das Ende der Mitgliedschaft gekündigt, gewählte Anteilscheine sind gekündigt.
- Das Mitglied ist aus den abgewählten Tätigkeitsbereichen ausgetragen.
- Die Koordination ist über jede Kündigung samt der Mitteilung des Mitglieds informiert.
- Für die Rückerstattung gekündigter Anteilscheine liegen Zahlungsverbindung und Adresse vor.

### Fehlerfall

- Weder Abo noch Mitgliedschaft noch Anteilscheine sind gekündigt.
- Das Mitglied bleibt mit unveränderten Daten Mitglied und kann die Kündigung erneut auslösen.

## Geschäftsregeln

### GR-001: Kündigungstermin des Abos

Ein Abo kann bis zum 30. September auf das Ende des laufenden Geschäftsjahres gekündigt werden. Nach diesem Datum wirkt die Kündigung auf das Ende des nächsten Geschäftsjahres. Das Geschäftsjahr endet bei GartenBerg am 31. Dezember (siehe UC-007 GR-001).

### GR-002: Kündigungsfrist der Mitgliedschaft

Die Mitgliedschaft endet jeweils am 31. Dezember bei einer Kündigungsfrist von drei Monaten. Eine bis Ende September erklärte Kündigung wirkt somit auf das Ende desselben Jahres, eine spätere auf das Ende des Folgejahres.

### GR-003: Mitgliedschaft und Abo

Die Mitgliedschaft lässt sich nur kündigen, wenn kein behaltenes Abo sie erfordert; Abo und Mitgliedschaft können in derselben Kündigung gemeinsam gekündigt werden. Probe-Abos erfordern keine Mitgliedschaft (siehe UC-001 GR-007).

### GR-004: Für ein Abo gebundene Anteilscheine

Anteilscheine, die für ein laufendes oder künftiges Abo benötigt werden, können nicht gekündigt werden. Wie viele Anteilscheine gebunden sind, ergibt sich aus den Bestandteilen des Abos (siehe UC-001 GR-003).

### GR-005: Anteilscheine und Mitgliedschaft

Die Mitgliedschaft selbst bindet keinen Anteilschein (siehe UC-001 GR-002). Kündbar sind deshalb alle Anteilscheine, die für kein behaltenes Abo gebunden sind, auch wenn die Mitgliedschaft bestehen bleibt.

### GR-006: Rückerstattung der Anteilscheine

Anteilscheine werden beim Austritt zum Ausgabepreis von CHF 750 zurückerstattet (siehe UC-001 GR-001). Eine Kündigung von Anteilscheinen ist deshalb nur möglich, wenn Zahlungsverbindung und Adresse des Mitglieds hinterlegt sind.

### GR-007: Kündigung des Abos nur durch die Hauptperson

Das Abo kann nur die Hauptperson kündigen. Mitbezüger/innen können sich lediglich aus dem Abo austragen; das Abo bleibt für die übrigen Bezüger/innen bestehen.

### GR-008: Benachrichtigung der Koordination

Jede Kündigung — Abo, einzelner Abo-Bestandteil, Mitgliedschaft und Anteilschein — wird der Koordination gemeldet, damit sie die Folgearbeiten auslösen kann. Bei der Kündigung von Abo und Mitgliedschaft wird die Mitteilung des Mitglieds mitgeliefert.

### GR-009: Wirkung erst auf den Kündigungstermin

Eine Kündigung wirkt auf den ausgewiesenen Termin. Bis dahin bleiben Bezugsrecht, Beitragspflicht und Einsatzpflicht des Mitglieds unverändert bestehen.

### GR-010: Rücknahme einer Kündigung

Die Kündigung der Mitgliedschaft kann das Mitglied auf seinem Profil selbst zurückziehen. Eine versehentliche Kündigung von Abo oder Anteilschein kann nur die Administration rückgängig machen, indem sie das Kündigungsdatum in der Verwaltung entfernt.
