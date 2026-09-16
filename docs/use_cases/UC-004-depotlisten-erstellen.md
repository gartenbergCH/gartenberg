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
- Abo-Typen, deren Abo-Paket mehrere Grössen desselben Produkts enthält, ist die bezogene Produktgrösse zugeordnet (GR-009).

## Hauptablauf

1. Die Administratorin ruft die Seite zur Listenerzeugung auf.
2. Das System zeigt die verfügbaren Listen an: die Hauptliste, die Depot- und die Mengenübersicht sowie je eine eigene Liste für Kartoffeln, Mehl und Glarner Alpkäse.
3. Die Administratorin trägt den Stichtag ein, für den die Listen gelten sollen.
4. Die Administratorin löst die Erzeugung aus.
5. Das System ermittelt je Liste die Abos, die am Stichtag einen aktiven Bestandteil des jeweiligen Produkts enthalten, und beschränkt die Spalten auf die Produktgrössen dieses Produkts.
6. Das System erzeugt die Listen als druckfertige Dokumente, gruppiert nach Depot mit Abholtag, Adresse, Kontakt und Abholzeitfenster, listet die Abos innerhalb eines Depots alphabetisch auf und weist je Produktgrösse die Anzahl der am Stichtag aktiven Bestandteile dieser Grösse pro Abo sowie eine Gesamtsumme aus.
7. Das System meldet die erfolgreiche Erzeugung und stellt die Listen zum Abruf bereit.
8. Die Administratorin ruft die gewünschte Liste ab und druckt sie für die Verteilung aus.

## Alternativabläufe

### A1: Produkt ohne Bestellungen

**Auslöser:** Für ein Produkt bestehen am Stichtag keine aktiven Abo-Bestandteile, z.B. weil sie erst bestellt oder bereits deaktiviert sind (Schritt 5)  
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

### A4: Abo-Typ ohne zugeordnete Produktgrösse

**Auslöser:** Ein am Stichtag aktiver Bestandteil gehört zu einem Abo-Typ, dessen Abo-Paket mehrere Grössen des Produkts enthält und dem keine Produktgrösse zugeordnet ist (Schritt 6)  
**Ablauf:**

1. Das System zählt diesen Bestandteil in keiner Grössen-Spalte, statt ihn in allen Grössen des Pakets zu zählen.
2. Das System weist auf der betroffenen Liste einen Hinweis mit dem Namen des Abo-Typs aus.
3. Die Administratorin ordnet dem Abo-Typ im Admin die Produktgrösse zu und erzeugt die Listen neu (A3).

## Nachbedingungen

### Erfolgsfall

- Für jede definierte Liste liegt ein druckfertiges Dokument zum gewählten Stichtag vor und ist abrufbar.
- Die Hauptliste sowie die Depot- und Mengenübersicht enthalten ausschliesslich Gemüse; die Hofprodukte sind auf ihre eigenen Listen verteilt.
- Innerhalb jedes Depots sind die Bezüger/innen alphabetisch aufgeführt.

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

Auf einer Liste erscheint ein Abo nur, wenn es am gewählten Stichtag einen aktiven Bestandteil des Produkts der Liste enthält. Massgebend ist der Bestandteil, nicht das Abo: Ein aktives Gemüse-Abo mit bloss bestelltem Mehl erscheint nicht auf der Mehl-Liste. Ein Bestandteil ist am Stichtag aktiv, wenn er spätestens am Stichtag aktiviert und nicht vor dem Stichtag deaktiviert wurde:

| Zustand des Bestandteils                               | Erscheint / wird gezählt |
|--------------------------------------------------------|--------------------------|
| Bestellt, noch nicht aktiviert                         | Nein                     |
| Aktiviert erst nach dem Stichtag                       | Nein                     |
| Aktiv                                                  | Ja                       |
| Gekündigt, noch nicht deaktiviert                      | Ja                       |
| Gekündigt, Deaktivierung am oder nach dem Stichtag     | Ja                       |
| Deaktiviert vor dem Stichtag                           | Nein                     |

Das Erstellungsdatum und der Stichtag werden auf jeder Liste ausgewiesen.

### GR-007: Alphabetische Reihenfolge der Bezüger/innen

Innerhalb eines Depots sind die Abos alphabetisch nach der Hauptbezügerin sortiert, gross-/kleinschreibungsunabhängig zuerst nach Vor-, dann nach Nachname. Beim Verteilen wird die Liste als Nachschlagewerk für einen einzelnen Namen benutzt; ohne festgelegte Reihenfolge erscheinen die Zeilen in beliebiger Datenbankreihenfolge und der Name lässt sich nur durch Absuchen der ganzen Seite finden. Die Regel gilt für alle Listen aus GR-002 und GR-003. Sie ergänzt GR-005, die nur die Reihenfolge der Spalten festlegt.

### GR-008: Menge je Produktgrösse

In der Spalte einer Produktgrösse steht pro Abo die Anzahl der gemäss GR-006 aktiven Bestandteile, die genau diese Grösse beziehen. Ein Bestandteil zählt nur in der Spalte seiner eigenen Grösse, nicht in den Spalten der übrigen Grössen desselben Produkts. Beispiel: Wer 2× Weizenmehl Halbweiss 3kg, 1× Weizenmehl Ruch 1kg und 1× Dinkelmehl Halbweiss 1kg bezieht, hat in diesen Spalten 2, 1 und 1 und in allen übrigen Mehl-Spalten keinen Eintrag. Die Gesamtsumme je Depot folgt derselben Regel; sie gilt auch für die Depot- und Mengenübersicht.

Massgebend für die Grösse eines Bestandteils ist sein Abo-Typ:

- Ist dem Abo-Typ eine Produktgrösse zugeordnet (GR-009), zählt der Bestandteil nur in dieser Grösse.
- Sonst zählt er in jeder Grösse seines Abo-Pakets. Das ist richtig, solange das Paket höchstens eine Grösse des Produkts enthält (z.B. die Gemüse-Pakete).
- Enthält das Paket mehrere Grössen des Produkts und fehlt die Zuordnung, ist die Grösse unbekannt: Der Bestandteil wird nicht gezählt und die Liste weist einen Hinweis aus (A4).

### GR-009: Zuordnung der Produktgrösse zum Abo-Typ

Bei GartenBerg enthalten die Abo-Pakete „Mehl“ und „Glarner Alpkäse“ alle Grössen ihres Produkts; die bestellte Sorte ist ein eigener Abo-Typ. Die Pakete werden bewusst nicht je Grösse aufgeteilt, weil das Bestellformular sonst die Überschriften „Mehl“ und „Glarner Alpkäse“ ausblendet. Stattdessen legt die Administration beim Abo-Typ fest, welche Produktgrösse er auf den Depotlisten bezieht. Die Grösse muss im Abo-Paket des Typs enthalten sein. Neue oder umbenannte Typen solcher Pakete sind bei der Erfassung zuzuordnen.
