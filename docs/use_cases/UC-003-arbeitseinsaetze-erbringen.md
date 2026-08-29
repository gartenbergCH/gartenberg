# Use Case: Arbeitseinsätze erbringen und anrechnen lassen

## Übersicht

**Use-Case-ID:** UC-003  
**Use-Case-Name:** Arbeitseinsätze erbringen und anrechnen lassen  
**Primärer Akteur:** Mitglied  
**Ziel:** Ein Mitglied erfüllt die mit seinem Abo verbundene Mitarbeitspflicht, indem es sich für ausgeschriebene Einsätze anmeldet und selbständig geleistete Arbeit zur Anrechnung meldet.  
**Status:** Implementiert

## Vorbedingungen

- Das Mitglied ist angemeldet und einem aktiven Abo zugeordnet.
- Es bestehen Tätigkeitsbereiche mit hinterlegten Verantwortlichen.

## Hauptablauf

1. Das Mitglied ruft die Übersicht der ausgeschriebenen Einsätze auf und filtert sie nach Zeitraum oder Jahr.
2. Das Mitglied öffnet einen Einsatz und sieht Zeitpunkt, Ort, Beschreibung und die Zahl der bereits belegten Plätze.
3. Das Mitglied meldet sich für den Einsatz an und gibt die Anzahl Teilnehmender an.
4. Das System bestätigt die Anmeldung, erhöht die Zahl der belegten Plätze und benachrichtigt das Mitglied.
5. Das Mitglied leistet zusätzlich selbständig Arbeit ausserhalb der ausgeschriebenen Einsätze.
6. Das Mitglied ruft das Meldeformular für geleistete Einsätze auf und erfasst Zeitpunkt, Tätigkeitsbereich und eine Beschreibung der Arbeit.
7. Das System nimmt die Meldung entgegen, stellt sie den Verantwortlichen des Tätigkeitsbereichs zur Genehmigung zu und führt sie beim Mitglied als pendent.
8. Der oder die Verantwortliche des Tätigkeitsbereichs genehmigt die Meldung.
9. Das System rechnet den Einsatz dem Mitglied an und weist ihn auf der persönlichen Einsatzübersicht aus.

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

### A3: Meldung unvollständig

**Auslöser:** Zeitpunkt, Tätigkeitsbereich oder Beschreibung der geleisteten Arbeit fehlen (Schritt 7)  
**Ablauf:**

1. Das System zeigt das Meldeformular erneut mit den beanstandeten Feldern an.
2. Das Mitglied ergänzt die Angaben.
3. Der Use Case wird bei Schritt 7 fortgesetzt.

### A4: Meldung abgelehnt

**Auslöser:** Der oder die Verantwortliche des Tätigkeitsbereichs lehnt die gemeldete Arbeit ab (Schritt 8)  
**Ablauf:**

1. Das System nimmt die Meldung aus den pendenten Meldungen und rechnet keinen Einsatz an.
2. Der Use Case endet.

## Nachbedingungen

### Erfolgsfall

- Die Anmeldung zum ausgeschriebenen Einsatz ist erfasst und dem Mitglied bestätigt.
- Die selbständig geleistete Arbeit ist genehmigt und dem Mitglied als Einsatz angerechnet.
- Der Einsatzstand des Mitglieds ist auf der persönlichen Einsatzübersicht nachvollziehbar.

### Fehlerfall

- Es wird weder eine Anmeldung noch eine Anrechnung erfasst.
- Abgelehnte Meldungen bleiben ohne Wirkung auf den Einsatzstand.

## Geschäftsregeln

### GR-001: Keine Selbstabmeldung von Einsätzen

Mitglieder können sich nicht selbständig von einem angemeldeten Einsatz abmelden und die Teilnehmerzahl nicht selbst ändern. Diese Einschränkung beruht auf einem Entscheid der Koordination vom 08.08.2025; Anpassungen nehmen Gärtner/innen oder die Koordination direkt in der Teilnehmerliste vor.

### GR-002: Genehmigungspflicht gemeldeter Einsätze

Selbständig geleistete Arbeit wird erst angerechnet, wenn der oder die Verantwortliche des betroffenen Tätigkeitsbereichs sie genehmigt hat. Bis dahin gilt die Meldung als pendent.

### GR-003: Einsatzpflicht aus dem Abo

Wie viele Einsätze und wie viele Einsätze im Kernbereich zu leisten sind, ergibt sich aus den Bestandteilen des Abos. Einsätze können auch in Bruchteilen ausgeschrieben und angerechnet werden.

### GR-004: Einsätze von Mitbezüger/innen

Die Einsätze von Mitbezüger/innen desselben Abos zählen auf dasselbe Abo. Die persönliche Einsatzübersicht weist darauf hin und verlinkt die Übersicht über die Einsätze der Mitbezüger/innen.
