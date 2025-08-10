# Changelog

## 4.0.0 - 10.08.2025

* Bump Juntagrico to 1.7.0
* Bump juntagrico-billing to 1.7.1
* Bump juntagrico-pg to 1.7.0
* Bump juntagrico-assignment-request to 1.7.0
* Der Organisationsname GartenBerg wird neu überall als GartenBerg geschrieben (vorher teilweise Gartenberg)

Rechnungen
* Erlaubt bei Rechnungen dem Admin die MWST zu aktualisieren oder die Rechnung mit einer Ausgleichszahlung auszugleichen

Arbeitseinsätze
* Es kann konfiguriert werden ob zukünftige Einsätze schon zählen oder nicht: https://juntagrico.readthedocs.io/en/latest/reference/templates.html#juntagrico-widgets-assignment-progress-html-progress
* Darstellung der meine Einsätze Seite verbessert. Es wird nun eine Tabelle verwendet wie auch auf anderen Einsatzseiten. Dadurch sind mehr Informationen sichtbar und es kann auch sortiert und gefiltert werden. Zudem gibt es neu eine Jahresauswahl wodurch eine Kontrolle einfacher ist und es gibt einen Hinweis auf Mitbezüger und einen Link auf die Seite wo auch deren Einsätze sichtbar sind.
* (deaktiviert, Entscheid Koordi vom 08.08.2025): Mitglieder können sich neu selber von angemeldeten Einsätzen wieder abmelden und die Anzahl Teilnehmer ändern. Der Arbeitseinsatzkontakt erhält eine Benachrichtigung darüber per Email (sofern mit der Einstellung DISABLE_NOTIFICATIONS nicht deaktiviert). Die Funktion kann mit der Einstellung ALLOW_JOB_UNSUBSCRIBE global deaktiviert werden.
* Verbesserung der Performanz der Job Tabelle falls es sehr viele Jobs gibt. Diese werden neu schneller geladen/angezeigt
* Neu können die Gärtner/Koordis direkt auf dem Arbeitseinsatz in der "Dabei sind" Liste Anpassungen vornehmen. D. h. abmelden oder mehr Teilnehmer eintragen.
* Die Erfassung von neuen Einsätzen wurde verbessert: Felder sinnvoller angeordnet. Zeigt die Standardwerte und Beschreibung der Jobart an.
* Auf der Arbeitseinsatzübersicht kann neu mit von/bis Datum oder dem Jahr gefiltert werden.

Abos
* Es gibt die neue Seite "Letze Änderungen", wo aufgelistet wird welche Änderungen an Abos es in einem wählbaren Datumsbereich gegeben hat
* Es gibt eine Seite "Pendente Änderungen" wo aufgelistet wird was noch bearbeitet werden muss (fehlendes Aktivierungs- oder Deaktivierungsdatum)
* Auf der Aboseite des Benutzers werden Links auf die Dokumente (FAQ, Betriebsreglement, AGB) angezeigt

Sicherheit
* Deaktivierte Benutzer können ihr Passwort nicht mehr zurücksetzen lassen

Export
* Datum und Zahlen werden neu nicht mehr als Zeichenfolgen, sondern in ihrem richtigen Format exportiert. Dadurch kann beispielsweise nach Datum sortiert werden in Excel oder Formeln verwendet werden)

Mitgliedschaftseite
* Zeigt Links auf die Dokumente (FAQ, Betriebsreglement, AGB) an.
* Zeigt eine klarere Beschreibung an falls die Mitgliedschaft nicht gekündet werden kann (weil der Anteilschein noch für ein Abo benötigt wird)
* Die Admins können neue eine Mitgliedernummer vergeben, welche auf der Mitgliedschaftseite angezeigt wird.

Änderungen Anteilscheine
* Unbezahlte Anteilscheine die nicht für ein Abo benötigt werden können neu gekündigt werden. Nützlich falls man bspw. aus Versehen einen Anteilschein zuviel bestellt.
* Die Koordis erhalten eine Meldung über gekündigte Anteilscheine

Anmeldeprozess
* Mit der Option REQUIRED_SHARES kann neu definiert werden wieviele Anteilscheine bei der Registrierung mindestens bestellt werden müssen. Dadurch ist es möglich für Probeabos keine Anteilscheine mehr zu benötigen (Minimum 0)
* Der eingegebene Kommentar wurde früher nur per E-Mail versendet. Neu wird er auch auf dem Mitglied gespeichert und bleibt somit erhalten/einsehbar
* Falls es für ein Depot Zusatzkosten (= Lieferkosten) gibt wird dies neu während dem Anmeldeprozess angezeigt.

Depot
* Die Depotbeschreibung kann bei der Anmeldung gelesen werden (= öffentlich). Alle "sensitiven" Informationen müssen im Feld "Zugriffsbeschreibung" enthalten sein
* Für die Depots können Abholzeiten angegeben werden. Diese werden auch bei der Anmeldung angezeigt.

Technisch
* Python 3.8 wird nicht mehr unterstützt

## 3.0.10 - 13.06.2025

* Bump Juntagrico to 1.6.10

## 3.0.9 - 15.02.2025

* [juntagrico-pg](https://github.com/juntagrico/juntagrico-pg) installieren

## 3.0.8 - 10.02.2025

* Bump whitenoise from 6.8.2 to 6.9.0

## 3.0.7 - 24.01.2025

Update auf Juntagrico 1.6.9
* Bugfix: Im Email über den Abowechsel wird neu der richtige Abotyp angezeigt
* Bugfix: Depots mit Koordinaten werden neu auf der Karte angezeigt auch wenn einzelne Depots keine Koordinaten haben
* Bugfix: Zeigt Links um Jobs zu erstellen auch für nicht Admins an (sofern diese über die Berechtigung dafür verfügen)
* Bugfix: Bei der Erstellung eines neuen Abos wurde auch bei Probeabos jeweils der Zusatz pro Jahr angezeigt. Dies ist neu nicht mehr der Fall.

## 3.0.6 - 22.12.2024

* bug beheben (Server Error 500) bei Neuregistrierungen mit Mitbezügern
* Genossenschaftsadresse von Kathrin auf Patrick wechseln
* Webseitenadresse korrekt setzen

## 3.0.5 - 22.12.2024

* Bump juntagrico-billing from 1.6.3 to 1.6.4
* Bump whitenoise from 6.6.0 to 6.8.2
* Bump juntagrico-assignment-request from 1.6.3 to 1.6.4
* Update juntagrico requirement from ~=1.6.5 to ~=1.6.8

## 3.0.4 - 03.10.2024

* Aktualisierung auf [Juntagrico 1.6.5](https://github.com/juntagrico/juntagrico/releases/tag/1.6.5)

## 3.0.3 - 15.09.2024

* Automatische Generierung der Depotliste deaktiviert. Diese kann seit Juntagrico 1.6 per Knopfdruck generiert werden.

## 3.0.2 - 14.09.2024

* Die Arbeitseinsatz Balken für den Kernbereich waren rot. Das hat zu Verwirrung geführt da es wie fehlende Einsätze aussieht. Nun gibt es nur noch grüne und graue Balken.

## 3.0.1 - 09.09.2024

* use patched version of juntagrico that corrects the sorting of the members in the depotlist

## 3.0.0 - 02.09.2024

* Updated link to statuten and betriebsreglement
* Updated link to FAQ
* bump to juntagrico v1.6

Relevante Änderungen
* Information bei Depotänderungen
* Depotlisten per Knopfdruck erstellen unter Angabe eines Stichtages
* Benutzer können ihr Abo selber anpassen (z. B. von ganz auf halb wechseln). Die Änderung erfolgt dann jeweils zum neuen Geschäftsjahr
* Es gibt keine Textlängenbeschränkung mehr für fast alles (z. B. Jobbeschreibung, Depotbeschreibung etc.)
* Arbeitseinsätze können neu beliebige Gleitkommazahlen sein. So können beispielsweise auch halbe Arbeitseinsätze etc. ausgeschrieben werden
* Depots können in Touren organisiert werden. So könnten wir die Aarauer und Fricker Tour abbilden.
* Diverse neue Ansichten und Listen, z. B. unbezahlte Anteilscheine
* Beim Aboexport kann ein Start- und Enddatum für die Einsatzzählung angegeben werden. So wäre es bspw. auch möglich das jahresübergreifend anzuschauen
* Einige Performanzverbesserungen, z. B. bei der Mitgliederliste
* Einige Fehlerbehebungen. Unter anderem auch bei den Einsatzzahlen (Doppelzählung wenn Mitabonnenten zu anderen Abos gewechselt haben).
* Layoutverbesserungen, z. B. auf dem Mobiltelefon

## 2.0.1 - 01.04.2024

* Hinweis falls unbezahlte Anteilscheine bestehen das man diese für das Probeabo ignorieren kann

## 2.0.0 - 01.04.2024

* bump to juntagrico-billing 1.5.6: show swiss QR payslip
* change the genossenschaft adress to the official adress

## 1.5.8 - 21.01.2024

* bump to juntagrico 1.5.8

## 1.5.7 - 13.05.2023

* bump to juntagrico 1.5.7
