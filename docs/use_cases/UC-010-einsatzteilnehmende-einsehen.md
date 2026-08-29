# Use Case: Teilnehmende der Einsätze einsehen

## Übersicht

**Use-Case-ID:** UC-010  
**Use-Case-Name:** Teilnehmende der Einsätze einsehen  
**Primärer Akteur:** Einsatzverantwortliche/r  
**Ziel:** Die für einen Ablauf verantwortliche Person sieht auf einer Seite, welche Einsätze
demnächst stattfinden und wer sich dafür eingeschrieben hat, ohne jeden Einsatz einzeln öffnen zu
müssen.  
**Status:** Implementiert

## Kontext

Die Koordination der Ernteverteilung (Abpacken, Leitung Abpacken, Verteilfahrten) und der
Setzlingsfahrten braucht laufend den Überblick "wer hat wann welchen Einsatz". Weil die Plattform
die Angemeldeten nur im Detail eines einzelnen Einsatzes zeigt, werden diese Angaben heute parallel
in Excel-Listen geführt. Die doppelte Führung ist fehleranfällig: Einträge verschieben sich,
und Mitglieder tragen sich mal nur in die Liste, mal nur in die Plattform ein. Die Plattform soll
alleinige Quelle werden.

## Vorbedingungen

- Die verantwortliche Person ist angemeldet und berechtigt, Einsatzanmeldungen einzusehen.
- Es bestehen ausgeschriebene Einsätze, die heute oder später stattfinden.

## Hauptablauf

1. Die verantwortliche Person ruft im Adminmenü den Eintrag für die Einsatz-Teilnehmerliste auf.
2. Das System zeigt alle künftigen Einsätze chronologisch aufsteigend, je Einsatz eine Zeile mit
   Datum und Wochentag, Zeitfenster, Einsatzart, Ort und Platzbelegung.
3. Das System zeigt zu jedem Einsatz die eingeschriebenen Personen mit Name, Vorname,
   Telefonnummer und E-Mail-Adresse an.
4. Die verantwortliche Person schränkt die Anzeige über die Auswahlliste auf einen
   Tätigkeitsbereich oder eine einzelne Einsatzart ein und bestätigt die Auswahl.
5. Das System zeigt dieselbe Darstellung, beschränkt auf die gewählte Einschränkung.
6. Die verantwortliche Person entnimmt der Liste, wer wann eingeteilt ist, und kontaktiert bei
   Bedarf eine Person direkt über die angezeigte Telefonnummer oder E-Mail-Adresse.

## Alternativabläufe

### A1: Einsatz ohne Anmeldungen

**Auslöser:** Für einen angezeigten Einsatz besteht keine einzige Anmeldung (Schritt 3)  
**Ablauf:**

1. Das System weist den Einsatz mit dem Hinweis aus, dass noch niemand eingeschrieben ist, statt
   die Zeile wegzulassen.
2. Der Use Case wird bei Schritt 4 fortgesetzt.

### A2: Abgesagter Einsatz

**Auslöser:** Ein künftiger Einsatz ist abgesagt (Schritt 2)  
**Ablauf:**

1. Das System zeigt den Einsatz weiterhin an und kennzeichnet ihn als abgesagt.
2. Der Use Case wird bei Schritt 3 fortgesetzt.

### A3: Keine Einsätze im gewählten Ausschnitt

**Auslöser:** Die gewählte Einschränkung enthält keine künftigen Einsätze (Schritt 5)  
**Ablauf:**

1. Das System zeigt eine leere Liste mit einem entsprechenden Hinweis.
2. Der Use Case wird bei Schritt 4 fortgesetzt.

### A4: Liste ausserhalb der Plattform weiterverwenden

**Auslöser:** Die verantwortliche Person will die Angaben ausdrucken oder weitergeben (Schritt 6)  
**Ablauf:**

1. Die verantwortliche Person druckt die Seite aus dem Browser oder kopiert die Tabelle in ein
   Tabellenblatt.
2. Der Use Case endet.

## Nachbedingungen

### Erfolgsfall

- Die verantwortliche Person kennt für den gewählten Ausschnitt zu jedem künftigen Einsatz die
  eingeschriebenen Personen samt Kontaktangaben, ohne einen einzelnen Einsatz geöffnet zu haben.
- Die Daten stammen ausschliesslich aus den Anmeldungen der Plattform; eine parallele Liste ist
  nicht mehr nötig.

### Fehlerfall

- Personen ohne die nötige Berechtigung erhalten keinen Zugriff und sehen insbesondere keine
  Kontaktangaben.

## Geschäftsregeln

### GR-001: Nur künftige Einsätze

Angezeigt werden ausschliesslich Einsätze ab dem heutigen Tag. Massgebend ist der Tagesbeginn und
nicht der Aufrufzeitpunkt, damit ein Einsatz von heute Morgen während des laufenden Tages auf der
Liste bleibt. Die Liste dient der Planung; vergangene Einsätze werden über die bestehenden
Auswertungen nachgeschlagen.

### GR-002: Chronologische Sortierung

Die Einsätze sind aufsteigend nach Zeitpunkt sortiert. Dadurch stehen die Einsätze desselben Tages
— etwa Abpacken, Leitung Abpacken und Verteilfahrt — beieinander und der Ablauf eines Tages ist
auf einen Blick lesbar.

### GR-003: Einschränkung auf Tätigkeitsbereich oder Einsatzart

Die Auswahlliste bietet in einer einzigen Auswahl sowohl die Tätigkeitsbereiche als auch die
einzelnen Einsatzarten an. Ohne Auswahl werden alle künftigen Einsätze gezeigt. Es werden keine
Einsatzarten im Code fest verdrahtet, damit Umbenennungen und neue Einsatzarten die Liste nicht
stillschweigend leeren.

### GR-004: Kontaktangaben nur für Berechtigte

Die Seite zeigt Telefonnummern und E-Mail-Adressen der eingeschriebenen Mitglieder. Sie ist deshalb
denselben Berechtigungen unterstellt wie die Einsicht in Einsatzanmeldungen.

### GR-005: Kein Datumsfilter in der ersten Ausbaustufe

Es gibt keinen Von-Bis-Filter. Die Menge künftiger Einsätze ist überschaubar, und die
Einschränkung auf Tätigkeitsbereich oder Einsatzart genügt für die Koordination. Ein Datumsfilter
wird erst nachgezogen, wenn sich das im Betrieb als nötig erweist.

### GR-006: Kein eigener Export in der ersten Ausbaustufe

Die Liste wird als Bildschirmansicht bereitgestellt. Für Ausdruck und Weitergabe genügen der
Browser-Druck und das Kopieren der Tabelle; es wird kein Excel- oder PDF-Export erzeugt.

### GR-007: Einmalige Einsätze

Einmalige Einsätze führen ihre Angaben selbst und gehören keiner wiederkehrenden Einsatzart an. Sie
erscheinen in der ungefilterten Liste und bei der Einschränkung auf ihren Tätigkeitsbereich, nicht
aber bei der Einschränkung auf eine Einsatzart.

### GR-008: Keine Einsätze aus Einsatzmeldungen

Meldet ein Mitglied einen selbständig geleisteten Einsatz, legt die Plattform dafür im Hintergrund
einen Einsatz an. Dieser ist nicht ausgeschrieben, es meldet sich niemand dafür an, und er gehört
weder in die Liste noch in die Auswahl der Einsatzarten. Er wird deshalb ausgenommen — analog zur
Datenverwaltung, die diese Einsätze ebenfalls ausblendet.
