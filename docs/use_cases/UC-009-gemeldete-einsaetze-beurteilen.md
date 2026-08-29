# Use Case: Gemeldete Einsätze beurteilen

## Übersicht

**Use-Case-ID:** UC-009  
**Use-Case-Name:** Gemeldete Einsätze beurteilen  
**Primärer Akteur:** Einsatzverantwortliche/r  
**Sekundäre Akteure:** Mitglied  
**Ziel:** Eine für Einsätze verantwortliche Person entscheidet über die selbständig geleistete Arbeit, die ihr Mitglieder gemeldet haben, und sorgt dafür, dass anerkannte Arbeit als Einsatz angerechnet wird.  
**Status:** Implementiert

## Vorbedingungen

- Die verantwortliche Person ist angemeldet und darf Einsätze allgemein oder in ihrem Tätigkeitsbereich bestätigen.
- Es liegen gemeldete Einsätze vor (siehe UC-003).

## Hauptablauf

1. Die verantwortliche Person ruft die Liste der offenen Anfragen auf.
2. Das System zeigt die an sie gerichteten Anfragen mit Einsatzdatum, meldendem Mitglied, Ansprechperson, Stand und Beschreibung.
3. Die verantwortliche Person öffnet die Anfrage, die sie beurteilen will.
4. Das System zeigt die gemeldeten Angaben zur Beurteilung an.
5. Die verantwortliche Person korrigiert bei Bedarf Anzahl Einsätze, Dauer, Tätigkeitsbereich und Ort und erfasst eine Rückmeldung an das Mitglied.
6. Die verantwortliche Person bestätigt die Anfrage.
7. Das System hält den Entscheid mit Datum und der entscheidenden Person fest und rechnet dem Mitglied den Einsatz an.
8. Das System benachrichtigt das meldende Mitglied über den Entscheid.
9. Das System entfernt die Anfrage aus den offenen Anfragen und führt sie im Archiv der beantworteten Anfragen.

## Alternativabläufe

### A1: Anfrage ablehnen

**Auslöser:** Die verantwortliche Person erkennt die gemeldete Arbeit nicht an (Schritt 6)  
**Ablauf:**

1. Die verantwortliche Person lehnt die Anfrage mit einer Begründung ab.
2. Das System hält den Entscheid fest, rechnet keinen Einsatz an und benachrichtigt das Mitglied.
3. Der Use Case wird bei Schritt 9 fortgesetzt.

### A2: Nur Rückfrage stellen

**Auslöser:** Die verantwortliche Person braucht vor dem Entscheid weitere Angaben (Schritt 6)  
**Ablauf:**

1. Die verantwortliche Person sendet nur die Rückmeldung, ohne zu entscheiden.
2. Das System benachrichtigt das Mitglied; die Anfrage bleibt offen.
3. Der Use Case endet.

### A3: Ohne Prüfung im Detail bestätigen

**Auslöser:** Die verantwortliche Person will eine Anfrage direkt aus der Liste bestätigen (Schritt 3)  
**Ablauf:**

1. Die verantwortliche Person bestätigt die Anfrage unmittelbar aus der Liste heraus.
2. Das System übernimmt die gemeldeten Angaben unverändert und verzichtet auf eine Rückmeldung.
3. Der Use Case wird bei Schritt 7 fortgesetzt.

### A4: Anfrage bereits beantwortet

**Auslöser:** Eine andere berechtigte Person hat die Anfrage bereits beurteilt (Schritt 4)  
**Ablauf:**

1. Das System weist darauf hin, dass die Anfrage bereits beantwortet ist, und führt zurück zur Liste.
2. Der Use Case endet.

### A5: Nicht zuständig

**Auslöser:** Die verantwortliche Person darf nur im eigenen Tätigkeitsbereich bestätigen und die Anfrage ist nicht an sie gerichtet (Schritt 3)  
**Ablauf:**

1. Das System verweigert die Beurteilung und führt zurück zur Liste der offenen Anfragen.
2. Der Use Case endet.

### A6: Bestätigung zurücknehmen

**Auslöser:** Ein bereits bestätigter Einsatz erweist sich nachträglich als nicht anrechenbar (Schritt 9)  
**Ablauf:**

1. Die Administration setzt die Anfrage in der Verwaltung wieder auf beantragt oder abgelehnt.
2. Das System entfernt die Anrechnung und den dafür erzeugten Einsatz wieder.
3. Der Use Case endet.

## Nachbedingungen

### Erfolgsfall

- Die Anfrage trägt einen Entscheid mit Datum und der entscheidenden Person.
- Bei einer Bestätigung ist dem meldenden Mitglied ein Einsatz angerechnet.
- Das meldende Mitglied ist über den Entscheid benachrichtigt.

### Fehlerfall

- Die Anfrage bleibt unverändert offen und wird weiterhin in der Liste geführt.
- Es wird kein Einsatz angerechnet.

## Geschäftsregeln

### GR-001: Zuständigkeit für die Beurteilung

Wer Einsätze allgemein bestätigen darf, kann jede Anfrage beurteilen. Wer nur im eigenen Tätigkeitsbereich bestätigen darf, kann ausschliesslich die an ihn gerichteten Anfragen beurteilen.

### GR-002: Anfragen ohne Ansprechperson

Anfragen ohne genannte Ansprechperson erscheinen bei allen Personen, die über nicht abgesprochene Einsätze informiert werden (siehe UC-003 GR-004).

### GR-003: Ein Entscheid je Anfrage

Eine bereits beantwortete Anfrage lässt sich nicht ein zweites Mal beurteilen. Wer entschieden hat, wird auf der Anfrage festgehalten; die übrigen zuständigen Personen werden darüber informiert.

### GR-004: Anrechnung über einen erzeugten Einsatz

Die Anrechnung erfolgt über einen automatisch erzeugten, nicht sichtbaren Einsatz im betroffenen Tätigkeitsbereich. Fehlt der Tätigkeitsbereich, wird der versteckte Bereich für selbständige Einsätze verwendet.

### GR-005: Rücknahme einer Bestätigung

Wird eine bestätigte Anfrage wieder auf beantragt oder abgelehnt gesetzt, entfernt das System die Anrechnung und den dafür erzeugten Einsatz.

### GR-006: Offene Anfragen und Archiv

Als offen gelten Anfragen mit dem Stand beantragt. Sobald eine Anfrage bestätigt oder abgelehnt ist, wechselt sie ins Archiv der beantworteten Anfragen; das Archiv ist zeitlich nicht eingeschränkt.
