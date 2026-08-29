# Use Case: Abo-Situation eines Mitglieds abklären

## Übersicht

**Use-Case-ID:** UC-008  
**Use-Case-Name:** Abo-Situation eines Mitglieds abklären  
**Primärer Akteur:** Administrator/in  
**Ziel:** Die Koordination klärt bei einer Rückfrage oder einer offenen Pendenz, welche Abo-Bestandteile ein Mitglied bezieht, was das Mitglied selbst sieht und welche Änderungen noch zu bearbeiten sind.  
**Status:** Implementiert

## Vorbedingungen

- Die Administratorin ist angemeldet und für Mitglieder- und Abo-Verwaltung berechtigt.
- Das betroffene Mitglied ist erfasst.

## Hauptablauf

1. Die Administratorin ruft die Übersicht der pendenten Abo-Änderungen auf.
2. Das System listet die Abos auf, bei denen ein Aktivierungs- oder Deaktivierungsdatum fehlt, und bezeichnet jeden Bestandteil mit Abo-Paket und bestellter Produktgrösse.
3. Die Administratorin sucht das betroffene Mitglied in der Mitgliederliste und öffnet dessen Abo.
4. Die Administratorin prüft in der Übersicht der jüngsten Abo-Änderungen, welche Änderungen im fraglichen Zeitraum vorgenommen wurden.
5. Die Administratorin übernimmt die Sicht des Mitglieds, um dessen Seiten so zu sehen wie das Mitglied selbst.
6. Das System zeigt die Plattform in der Sicht des Mitglieds und weist die Übernahme sichtbar aus.
7. Die Administratorin beendet die Übernahme und kehrt in ihre eigene Sitzung zurück.
8. Die Administratorin ergänzt das fehlende Datum beziehungsweise beantwortet die Rückfrage des Mitglieds.

## Alternativabläufe

### A1: Frage betrifft mehrere Mitglieder

**Auslöser:** Die Abklärung lässt sich nicht an einem einzelnen Abo beantworten, etwa bei einer Auswertung über alle Mitglieder (Schritt 4)  
**Ablauf:**

1. Die Administratorin ruft die Abfragekonsole der Verwaltung auf und formuliert eine lesende Auswertung auf den Betriebsdaten.
2. Das System führt die Auswertung aus und zeigt das Ergebnis als Tabelle an.
3. Der Use Case wird bei Schritt 8 fortgesetzt.

### A2: Bestandteile lassen sich nicht unterscheiden

**Auslöser:** Mehrere Bestandteile desselben Abo-Pakets erscheinen in der Liste (Schritt 2)  
**Ablauf:**

1. Das System ergänzt die Bezeichnung jedes Bestandteils um die bestellte Produktgrösse, sodass etwa die verschiedenen Mehl-, Kartoffel- und Käsegrössen unterscheidbar bleiben.
2. Der Use Case wird bei Schritt 3 fortgesetzt.

### A3: Übernahme der Mitgliedersicht nicht erlaubt

**Auslöser:** Die Administratorin ist nicht berechtigt, eine fremde Sicht zu übernehmen (Schritt 5)  
**Ablauf:**

1. Das System verweigert die Übernahme und belässt die Administratorin in ihrer eigenen Sitzung.
2. Der Use Case wird bei Schritt 8 fortgesetzt.

## Nachbedingungen

### Erfolgsfall

- Die Administratorin kennt die Abo-Bestandteile des Mitglieds einschliesslich der bestellten Produktgrössen.
- Fehlende Aktivierungs- oder Deaktivierungsdaten sind erkannt und bearbeitet.
- Eine übernommene Mitgliedersicht ist wieder beendet.

### Fehlerfall

- Die Daten des Mitglieds bleiben unverändert.
- Eine begonnene Übernahme der Mitgliedersicht wird beendet, ohne Änderungen zu hinterlassen.

## Geschäftsregeln

### GR-001: Bezeichnung der Abo-Bestandteile

Ein Abo-Bestandteil wird mit dem Namen des Abo-Pakets und der bestellten Produktgrösse bezeichnet, damit sich Bestandteile desselben Pakets in Übersichten unterscheiden lassen.

### GR-002: Pendente Abo-Änderungen

Als pendent gilt ein Abo oder Bestandteil, dem das Aktivierungs- oder das Deaktivierungsdatum fehlt. Solche Fälle müssen von der Administration nachgeführt werden.

### GR-003: Sichtbarkeit der Sitzungsübernahme

Während der Übernahme einer Mitgliedersicht ist erkennbar, dass es sich nicht um die eigene Sitzung handelt; die Übernahme beginnt beim Profil des Mitglieds und lässt sich jederzeit beenden.

### GR-004: Auswertungen nur lesend

Ad-hoc-Auswertungen über die Abfragekonsole dienen ausschliesslich dem Lesen von Betriebsdaten. Datenänderungen erfolgen über die regulären Verwaltungsmasken.

### GR-005: Abo-Änderungen zum Geschäftsjahr

Von Mitgliedern selbst ausgelöste Änderungen am Abo — etwa der Wechsel von ganz auf halb — werden auf den Beginn des nächsten Geschäftsjahres wirksam.
