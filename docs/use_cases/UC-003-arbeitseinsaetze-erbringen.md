# Use Case: Arbeitseinsätze erbringen und anrechnen lassen

## Übersicht

**Use-Case-ID:** UC-003  
**Use-Case-Name:** Arbeitseinsätze erbringen und anrechnen lassen  
**Primärer Akteur:** Mitglied  
**Sekundäre Akteure:** Einsatzverantwortliche/r  
**Ziel:** Ein Mitglied erfüllt die mit seinem Abo verbundene Mitarbeitspflicht, indem es sich für ausgeschriebene Einsätze anmeldet und selbständig geleistete Arbeit zur Anrechnung meldet.  
**Status:** Implementiert

## Vorbedingungen

- Das Mitglied ist angemeldet und einem aktiven Abo zugeordnet.
- Es bestehen Tätigkeitsbereiche mit Personen, die gemeldete Einsätze bestätigen dürfen.

## Hauptablauf

1. Das Mitglied ruft die Übersicht der ausgeschriebenen Einsätze auf und filtert sie nach Zeitraum oder Jahr.
2. Das Mitglied öffnet einen Einsatz und sieht Zeitpunkt, Ort, Beschreibung und die Zahl der bereits belegten Plätze.
3. Das Mitglied meldet sich für den Einsatz an und gibt die Anzahl Teilnehmender an.
4. Das System bestätigt die Anmeldung, erhöht die Zahl der belegten Plätze und benachrichtigt das Mitglied.
5. Das Mitglied leistet zusätzlich selbständig Arbeit ausserhalb der ausgeschriebenen Einsätze.
6. Das Mitglied ruft das Meldeformular für geleistete Einsätze auf.
7. Das Mitglied erfasst Zeitpunkt, Anzahl Einsätze, Dauer in Stunden, Tätigkeitsbereich, Ansprechperson, Ort und eine Beschreibung der Arbeit.
8. Das System prüft die Angaben, nimmt die Meldung als beantragt entgegen, benachrichtigt die gewählte Ansprechperson und führt die Meldung beim Mitglied in der Liste der pendenten Anfragen.
9. Die Ansprechperson beurteilt die Meldung (siehe UC-009).
10. Das System benachrichtigt das Mitglied über den Entscheid und weist eine bestätigte Meldung als angerechneten Einsatz auf der persönlichen Einsatzübersicht aus.

## Alternativabläufe

### A1: Einsatz bereits ausgebucht

**Auslöser:** Für den gewählten Einsatz sind keine Plätze mehr frei (Schritt 3)  
**Ablauf:**

1. Das System lässt keine weitere Anmeldung zu und weist auf die fehlenden Plätze hin.
2. Das Mitglied wählt einen anderen Einsatz.
3. Der Use Case wird bei Schritt 2 fortgesetzt.

### A2: Abmeldung von einem Einsatz gewünscht

**Auslöser:** Das Mitglied möchte eine bestehende Anmeldung zurückziehen (Schritt 4)  
**Ablauf:**

1. Das System bietet dem Mitglied keine Möglichkeit zur Selbstabmeldung an.
2. Das Mitglied wendet sich an die Koordination oder den Einsatzkontakt, die die Anmeldung in der Teilnehmerliste anpassen.
3. Der Use Case wird bei Schritt 5 fortgesetzt.

### A3: Ansprechperson passt nicht zum Tätigkeitsbereich

**Auslöser:** Die gewählte Ansprechperson darf im gewählten Tätigkeitsbereich nicht bestätigen (Schritt 8)  
**Ablauf:**

1. Das System weist die Auswahl als ungültig zurück und zeigt das Meldeformular erneut an.
2. Das Mitglied wählt eine passende Ansprechperson oder einen anderen Tätigkeitsbereich.
3. Der Use Case wird bei Schritt 8 fortgesetzt.

### A4: Meldung nachträglich korrigieren

**Auslöser:** Das Mitglied stellt fest, dass seine Angaben unvollständig oder falsch sind (Schritt 9)  
**Ablauf:**

1. Das Mitglied öffnet die Meldung aus der Liste der pendenten Anfragen und ändert die Angaben.
2. Das System speichert die Änderung; erhöht sie den beantragten Wert, wird die Meldung erneut als beantragt geführt und die Ansprechperson erneut benachrichtigt.
3. Der Use Case wird bei Schritt 9 fortgesetzt.

### A5: Meldung zurückziehen

**Auslöser:** Das Mitglied möchte eine noch nicht angerechnete Meldung entfernen (Schritt 9)  
**Ablauf:**

1. Das Mitglied löscht die Meldung aus der Liste der pendenten Anfragen.
2. Das System entfernt die Meldung; sie erscheint bei der Ansprechperson nicht mehr.
3. Der Use Case endet.

### A6: Meldung abgelehnt

**Auslöser:** Die Ansprechperson lehnt die gemeldete Arbeit ab (Schritt 9)  
**Ablauf:**

1. Das System führt die Meldung als abgelehnt und rechnet keinen Einsatz an.
2. Das System benachrichtigt das Mitglied mit der Begründung der Ansprechperson.
3. Der Use Case endet.

## Nachbedingungen

### Erfolgsfall

- Die Anmeldung zum ausgeschriebenen Einsatz ist erfasst und dem Mitglied bestätigt.
- Die selbständig geleistete Arbeit ist bestätigt und dem Mitglied als Einsatz angerechnet.
- Der Einsatzstand des Mitglieds ist auf der persönlichen Einsatzübersicht nachvollziehbar.

### Fehlerfall

- Es wird weder eine Anmeldung noch eine Anrechnung erfasst.
- Abgelehnte oder zurückgezogene Meldungen bleiben ohne Wirkung auf den Einsatzstand.

## Geschäftsregeln

### GR-001: Keine Selbstabmeldung von Einsätzen

Mitglieder können sich nicht selbständig von einem angemeldeten Einsatz abmelden und die Teilnehmerzahl nicht selbst ändern. Diese Einschränkung beruht auf einem Entscheid der Koordination vom 08.08.2025; Anpassungen nehmen Gärtner/innen oder die Koordination direkt in der Teilnehmerliste vor.

### GR-002: Bestätigungspflicht gemeldeter Einsätze

Selbständig geleistete Arbeit wird erst angerechnet, wenn eine dazu berechtigte Person sie bestätigt hat. Bis dahin gilt die Meldung als beantragt.

### GR-003: Zulässige Ansprechpersonen

Als Ansprechperson wählbar sind Personen, die Einsätze allgemein bestätigen dürfen, sowie die Koordinatorinnen und Koordinatoren des gewählten Tätigkeitsbereichs. Andere Kombinationen weist das System zurück.

### GR-004: Meldung ohne Ansprechperson

Die Ansprechperson darf leer bleiben. Die Meldung geht dann an alle Personen, die über nicht abgesprochene Einsätze informiert werden.

### GR-005: Wert einer Meldung

Der angerechnete Wert ergibt sich aus der Anzahl beantragter Einsätze. Zählt die Genossenschaft Einsätze in Stunden, wird die Anzahl zusätzlich mit der erfassten Dauer multipliziert.

### GR-006: Änderungen mit höherem Wert erfordern erneute Bestätigung

Erhöht das Mitglied den beantragten Wert einer bereits beurteilten Meldung, gilt sie wieder als beantragt und muss erneut bestätigt werden. Bei gleichbleibendem oder tieferem Wert bleibt der bisherige Entscheid bestehen.

### GR-007: Löschen nur vor der Anrechnung

Eine Meldung kann das Mitglied nur löschen, solange daraus noch keine Anrechnung entstanden ist, und nur bei den eigenen Meldungen.

### GR-008: Umfang der eigenen Meldungsliste

Auf dem Meldeformular sieht das Mitglied alle noch nicht beurteilten Meldungen sowie zusätzlich alle eigenen Meldungen, deren Einsatz im laufenden Geschäftsjahr liegt.

### GR-009: Einsatzpflicht aus dem Abo

Wie viele Einsätze und wie viele Einsätze im Kernbereich zu leisten sind, ergibt sich aus den Bestandteilen des Abos. Einsätze können auch in Bruchteilen ausgeschrieben und angerechnet werden.

### GR-010: Einsätze von Mitbezüger/innen

Die Einsätze von Mitbezüger/innen desselben Abos zählen auf dasselbe Abo. Die persönliche Einsatzübersicht weist darauf hin und verlinkt die Übersicht über die Einsätze der Mitbezüger/innen.
