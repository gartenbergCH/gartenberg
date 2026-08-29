# Use Case: Mitgliedschaft beantragen

## Übersicht

**Use-Case-ID:** UC-001  
**Use-Case-Name:** Mitgliedschaft beantragen  
**Primärer Akteur:** Interessent/in  
**Ziel:** Eine interessierte Person meldet sich mit einem passenden Abo bei der Genossenschaft GartenBerg an und weiss dabei, ob sie eine Probe-Mitgliedschaft oder eine volle Mitgliedschaft mit Anteilscheinen eingeht.  
**Status:** Implementiert

## Vorbedingungen

- Die Person ist nicht angemeldet; eine bestehende Sitzung wird zu Beginn beendet.
- Für die gewünschten Produkte sind bestellbare Abo-Pakete und mindestens ein sichtbares Depot erfasst.
- Statuten und Betriebsreglement der Genossenschaft sind hinterlegt und öffentlich abrufbar.

## Hauptablauf

1. Die Interessentin ruft die Anmeldeseite der Genossenschaft auf.
2. Das System zeigt die Einstiegsinformationen von GartenBerg an: einen hervorgehobenen Hinweis auf die auf drei Monate befristete Probe-Mitgliedschaft mit den Preisen der drei Probe-Varianten, den Anteilscheinpreis für die volle Mitgliedschaft sowie Verweise auf Statuten und Betriebsreglement.
3. Die Interessentin erfasst ihre Personendaten und bestätigt, die Bedingungen gelesen zu haben.
4. Das System prüft die Angaben und führt sie zur Auswahl der Abo-Bestandteile.
5. Die Interessentin wählt die gewünschten Abo-Bestandteile und deren Anzahl.
6. Die Interessentin wählt ein Depot; das System weist auf allfällige Zusatzkosten des Depots hin.
7. Das System zeigt das reguläre Startdatum zum nächsten Geschäftsjahr an und erläutert, dass wegen freier Plätze auch ein Start auf den nächsten Monatsbeginn möglich ist.
8. Die Interessentin trägt das gewünschte Startdatum ein.
9. Die Interessentin erfasst optional Mitbezüger/innen oder fährt ohne solche fort.
10. Die Interessentin bestellt die für ihre Abo-Bestandteile benötigten Anteilscheine; bei einer Probe-Mitgliedschaft bleibt die Anzahl bei null.
11. Das System zeigt eine Zusammenfassung der Bestellung.
12. Die Interessentin bestätigt die Bestellung verbindlich.
13. Das System legt Mitgliedschaft, Abo und allfällige Anteilscheine an, versendet die Begrüssungsnachricht mit Zugangsdaten und Bestätigungslink und zeigt die Willkommensseite.
14. Die Interessentin bestätigt ihre E-Mail-Adresse über den Bestätigungslink und meldet sich an.

## Alternativabläufe

### A1: Angaben zur Person unvollständig oder ungültig

**Auslöser:** Pflichtfelder fehlen, das Geburtsdatum ist unlesbar oder die Bedingungen wurden nicht bestätigt (Schritt 4)  
**Ablauf:**

1. Das System zeigt die Anmeldeseite erneut mit den beanstandeten Feldern an.
2. Die Interessentin korrigiert die Angaben.
3. Der Use Case wird bei Schritt 4 fortgesetzt.

### A2: Zu wenige Anteilscheine bestellt

**Auslöser:** Die bestellte Anzahl Anteilscheine unterschreitet die für die gewählten Abo-Bestandteile nötige Anzahl (Schritt 10)  
**Ablauf:**

1. Das System weist auf die fehlenden Anteilscheine hin und lässt die Bestellung nicht zu.
2. Die Interessentin erhöht die Anzahl oder wechselt zu einer Probe-Variante.
3. Der Use Case wird bei Schritt 10 fortgesetzt.

### A3: Gewünschtes Startdatum nicht zulässig

**Auslöser:** Das eingetragene Startdatum liegt ausserhalb des zulässigen Bereichs (Schritt 8)  
**Ablauf:**

1. Das System meldet, dass das gewählte Startdatum nicht gültig ist.
2. Die Interessentin trägt ein anderes Datum ein.
3. Der Use Case wird bei Schritt 8 fortgesetzt.

### A4: Anmeldung abgebrochen

**Auslöser:** Die Interessentin bricht den Anmeldeprozess ab (Schritt 5 bis 11)  
**Ablauf:**

1. Das System verwirft die begonnene Anmeldung.
2. Der Use Case endet.

## Nachbedingungen

### Erfolgsfall

- Mitglied, Abo mit den gewählten Bestandteilen und gewünschtem Startdatum sowie die bestellten Anteilscheine sind erfasst.
- Das Mitglied hat Zugangsdaten erhalten und seine E-Mail-Adresse bestätigt.
- Die Koordination ist über die neue Anmeldung und allfällige neue Anteilscheine informiert.
- Ein bei der Anmeldung hinterlassener Kommentar ist am Mitglied gespeichert.

### Fehlerfall

- Es werden weder Mitglied noch Abo noch Anteilscheine angelegt.
- Die Person bleibt nicht angemeldet und kann die Anmeldung erneut starten.

## Geschäftsregeln

### GR-001: Preis eines Anteilscheins

Ein Anteilschein von GartenBerg kostet CHF 750. Dieser Betrag wird im Anmeldeprozess ausgewiesen und beim Austritt zurückerstattet.

### GR-002: Keine Pflicht-Anteilscheine bei der Anmeldung

Unabhängig vom gewählten Abo verlangt GartenBerg bei der Anmeldung keine Mindestanzahl Anteilscheine. Dadurch ist eine Probe-Mitgliedschaft ohne Anteilschein möglich.

### GR-003: Anteilscheine nach Abo-Bestandteilen

Die zu bestellende Anzahl Anteilscheine ergibt sich aus den gewählten Abo-Bestandteilen. Sie kann nicht unterschritten werden.

### GR-004: Probe-Mitgliedschaft

Die Probe-Mitgliedschaft ist zeitlich auf drei Monate befristet, erfordert keinen Anteilschein und wird in drei Grössen angeboten (ganz, halb, mini). Sie verlängert sich nicht automatisch.

### GR-005: Startdatum ausserhalb des Geschäftsjahresbeginns

Reguläres Startdatum ist der Beginn des nächsten Geschäftsjahres, das bei GartenBerg am 1. Januar beginnt. Solange freie Plätze bestehen, ist ein Start auch auf den nächsten Monatsbeginn möglich; die Zusage gilt nur, sofern zum gewünschten Datum ein Abo frei ist.

### GR-006: Zustimmung zu Statuten und Betriebsreglement

Vor dem Absenden der Personendaten müssen Statuten und Betriebsreglement zur Kenntnis genommen und die Bedingungen bestätigt werden. Beide Dokumente sind von der Anmeldeseite aus verlinkt.
