# Use Case: Depotlisten erstellen

## Übersicht

**Use-Case-ID:** UC-004  
**Use-Case-Name:** Depotlisten erstellen  
**Primärer Akteur:** Administrator/in  
**Ziel:** Die Koordination erzeugt zu einem frei gewählten Stichtag die Verteillisten, mit denen im Depot ersichtlich ist, welches Mitglied welche Produkte in welcher Grösse bezieht.  
**Status:** Implementiert

## Vorbedingungen

- Die Administratorin ist angemeldet und berechtigt, Listen zu erzeugen.
- Es bestehen Depots, die für die Depotliste sichtbar geschaltet sind.
- Die Produkte und Produktgrössen sind erfasst und in der gewünschten Reihenfolge sortiert.

## Hauptablauf

1. Die Administratorin ruft die Seite zur Listenerzeugung auf.
2. Das System zeigt die verfügbaren Listen an: die Hauptliste, die Depot- und die Mengenübersicht sowie je eine eigene Liste für Kartoffeln, Mehl und Glarner Alpkäse.
3. Die Administratorin trägt den Stichtag ein, für den die Listen gelten sollen.
4. Die Administratorin löst die Erzeugung aus.
5. Das System ermittelt je Liste die am Stichtag aktiven Abos, die einen Bestandteil des jeweiligen Produkts enthalten, und beschränkt die Spalten auf die Produktgrössen dieses Produkts.
6. Das System erzeugt die Listen als druckfertige Dokumente, gruppiert nach Depot mit Abholtag, Adresse, Kontakt und Abholzeitfenster, und weist je Produktgrösse die Bezugsmenge pro Abo sowie eine Gesamtsumme aus.
7. Das System meldet die erfolgreiche Erzeugung und stellt die Listen zum Abruf bereit.
8. Die Administratorin ruft die gewünschte Liste ab und druckt sie für die Verteilung aus.

## Alternativabläufe

### A1: Produkt ohne Bestellungen

**Auslöser:** Für ein Produkt bestehen am Stichtag keine aktiven Abo-Bestandteile (Schritt 5)  
**Ablauf:**

1. Das System erzeugt die betreffende Liste ohne Einträge, statt die Erzeugung abzubrechen.
2. Der Use Case wird bei Schritt 6 fortgesetzt.

### A2: Produkt mit vielen Produktgrössen

**Auslöser:** Die zu druckende Liste betrifft Mehl oder Glarner Alpkäse (Schritt 6)  
**Ablauf:**

1. Das System erzeugt die Liste im Querformat und ohne die Kontrollspalten für Abholung und Taschenrückgabe, damit alle Produktgrössen auf die Seite passen.
2. Der Use Case wird bei Schritt 7 fortgesetzt.

### A3: Neue Listen vor Ablauf des Stichtags nötig

**Auslöser:** Die Administratorin benötigt Listen zu einem anderen Stichtag (Schritt 8)  
**Ablauf:**

1. Die Administratorin trägt einen neuen Stichtag ein und erzwingt die erneute Erzeugung.
2. Das System überschreibt die bestehenden Listen.
3. Der Use Case wird bei Schritt 7 fortgesetzt.

## Nachbedingungen

### Erfolgsfall

- Für jede definierte Liste liegt ein druckfertiges Dokument zum gewählten Stichtag vor und ist abrufbar.
- Die Hauptliste sowie die Depot- und Mengenübersicht enthalten ausschliesslich Gemüse; die Hofprodukte sind auf ihre eigenen Listen verteilt.

### Fehlerfall

- Es werden keine neuen Listen bereitgestellt; die zuletzt erzeugten Listen bleiben unverändert abrufbar.

## Geschäftsregeln

### GR-001: Listenerzeugung nur auf Anforderung

Depotlisten werden nicht automatisch an festen Wochentagen erzeugt, sondern ausschliesslich auf Knopfdruck unter Angabe eines Stichtags.

### GR-002: Hauptlisten nur mit Gemüse

Hauptliste, Depotübersicht und Mengenübersicht enthalten nur das Produkt Gemüse. Ohne diese Einschränkung würden die Hofprodukte-Kategorien die Übersichten unlesbar machen.

### GR-003: Eigene Liste je Hofprodukt

Für Kartoffeln, Mehl und Glarner Alpkäse wird je eine eigene Liste geführt, die ausschliesslich die Bestellungen dieses Produkts ausweist.

### GR-004: Kompaktes Layout für breite Sortimente

Mehl und Glarner Alpkäse werden im Querformat ohne die Kontrollspalten für Abholung und Taschenrückgabe gedruckt, weil ihre Produktgrössen die Hochformat-Tabelle sprengen. Gemüse und Kartoffeln behalten das reguläre Layout mit diesen Spalten.

### GR-005: Sichtbarkeit und Reihenfolge der Produktgrössen

Auf den Listen erscheinen nur Produktgrössen, die für die Depotliste freigegeben sind. Ihre Reihenfolge folgt der von der Administration festgelegten Sortierung, nicht der Menge je Grösse.

### GR-006: Stichtagsbezug

Auf einer Liste erscheint ein Abo nur, wenn es am gewählten Stichtag aktiv ist. Das Erstellungsdatum und der Stichtag werden auf jeder Liste ausgewiesen.
