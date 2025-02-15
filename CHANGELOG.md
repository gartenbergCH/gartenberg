# Changelog

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
