# Use Case: Rechnungen bearbeiten

## Übersicht

**Use-Case-ID:** UC-007  
**Use-Case-Name:** Rechnungen bearbeiten  
**Primärer Akteur:** Administrator/in  
**Ziel:** Die Koordination stellt den Mitgliedern die Beiträge für ein Geschäftsjahr in Rechnung, verbucht die Zahlungseingänge und bringt Differenzen zum Ausgleich.  
**Status:** Implementiert

## Vorbedingungen

- Die Administratorin ist angemeldet und berechtigt, Rechnungen zu bearbeiten.
- Für das betroffene Geschäftsjahr ist ein Geschäftsjahr mit Start- und Enddatum erfasst.
- Die zu verrechnenden Abos und ihre Bestandteile sind aktiviert.

## Hauptablauf

1. Die Administratorin ruft die Übersicht der anstehenden Rechnungen auf und wählt das Geschäftsjahr.
2. Das System listet die Mitglieder mit den in diesem Geschäftsjahr verrechenbaren Abo-Bestandteilen und dem daraus errechneten Betrag auf.
3. Die Administratorin erstellt die Rechnungen für die gewählten Mitglieder.
4. Das System legt je Mitglied eine Rechnung mit den einzelnen Positionen, dem Gesamtbetrag und einer Referenznummer für die Zahlungszuordnung an.
5. Die Administratorin gibt die Rechnungen frei und lässt sie den Mitgliedern zustellen.
6. Das System stellt den Mitgliedern die Rechnung mit Einzahlungsschein zu und vermerkt die erfolgte Benachrichtigung.
7. Die Administratorin erfasst die eingegangenen Zahlungen mit Datum, Betrag und Zahlungsart.
8. Das System verbucht die Zahlung auf der Rechnung und weist den noch offenen Betrag aus.
9. Das System markiert die Rechnung als bezahlt, sobald der offene Betrag ausgeglichen ist.

## Alternativabläufe

### A1: Zahlung weicht vom Rechnungsbetrag ab

**Auslöser:** Der einbezahlte Betrag deckt die Rechnung nicht oder übersteigt sie (Schritt 8)  
**Ablauf:**

1. Das System weist den verbleibenden offenen Betrag beziehungsweise die Überzahlung aus.
2. Die Administratorin erfasst eine Ausgleichsposition, um die Differenz zu bereinigen.
3. Der Use Case wird bei Schritt 8 fortgesetzt.

### A2: Mehrwertsteuersatz muss angepasst werden

**Auslöser:** Für eine bereits erstellte Rechnung gilt ein anderer Mehrwertsteuersatz (Schritt 5)  
**Ablauf:**

1. Die Administratorin setzt den Mehrwertsteuersatz der Rechnung neu.
2. Das System berechnet den Steueranteil der Positionen neu.
3. Der Use Case wird bei Schritt 5 fortgesetzt.

### A3: Zusätzliche Position ohne Abo-Bezug

**Auslöser:** Es ist ein Betrag zu verrechnen, der sich nicht aus einem Abo-Bestandteil ergibt (Schritt 4)  
**Ablauf:**

1. Die Administratorin ergänzt die Rechnung um eine Position eines eigens definierten Positionstyps mit Betrag und Beschreibung.
2. Der Use Case wird bei Schritt 4 fortgesetzt.

## Nachbedingungen

### Erfolgsfall

- Für die betroffenen Mitglieder bestehen freigegebene Rechnungen des gewählten Geschäftsjahres mit ihren Positionen.
- Die Mitglieder wurden über ihre Rechnung benachrichtigt.
- Eingegangene Zahlungen sind der jeweiligen Rechnung zugeordnet und der offene Betrag stimmt.

### Fehlerfall

- Es wird keine Rechnung erstellt, freigegeben oder als bezahlt markiert.
- Bereits bestehende Rechnungen und verbuchte Zahlungen bleiben unverändert.

## Geschäftsregeln

### GR-001: Geschäftsjahr als Abrechnungsperiode

Jede Rechnung gehört zu genau einem Geschäftsjahr. Das Geschäftsjahr von GartenBerg beginnt am 1. Januar; sein Enddatum muss nach dem Startdatum liegen.

### GR-002: Rechnungspositionen aus Abo-Bestandteilen

Eine Rechnungsposition bezieht sich entweder auf einen Abo-Bestandteil oder auf einen eigens definierten Positionstyp, nie auf beides.

### GR-003: Verrechnungszeitraum

Der verrechnete Zeitraum ergibt sich aus dem Geschäftsjahr, begrenzt durch das Aktivierungs- und das Enddatum des zugrunde liegenden Abos.

### GR-004: Mehrwertsteuer nur auf Abo-Positionen

Der Steueranteil wird ausschliesslich für Positionen mit Abo-Bezug aus dem Steuersatz der Rechnung berechnet. Positionen ohne Abo-Bezug tragen keinen Steueranteil.

### GR-005: Referenznummer zur Zahlungszuordnung

Jede Rechnung erhält eine 27-stellige Referenznummer, die Mitglied und Rechnung eindeutig bezeichnet und die automatische Zuordnung von Zahlungen ermöglicht.

### GR-006: Offener Betrag

Der offene Betrag einer Rechnung ist der Rechnungsbetrag abzüglich aller darauf verbuchten Zahlungen.
