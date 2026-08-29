from datetime import date

from conftest import shot
from pages.admin_billing_page import AdminBillingPage

# Die Testdaten (generate_testdata) enthalten zwei seit 2017 aktivierte Abos ohne
# Deaktivierungsdatum. Für das laufende Geschäftsjahr sind sie damit verrechenbar.
_YEAR = str(date.today().year)
_PAYMENT_TYPE = "E2E Bank"


def test_admin_can_view_pending_bills(admin_page):
    page = AdminBillingPage(admin_page)
    page.navigate_pending_bills()
    shot(admin_page, "admin_billing_01_pending")

    assert page.heading() == "Anstehende Rechnungen", \
        f"Seitentitel sollte 'Anstehende Rechnungen' sein, war: '{page.heading()}'"
    assert page.has_year_selector(), \
        "Geschäftsjahres-Auswahl (select#year) sollte vorhanden sein"
    assert page.has_table(), \
        "Tabelle (#filter-table) sollte vorhanden sein"


def test_admin_can_bill_and_collect_payment(admin_page):
    """UC-007: Geschäftsjahr anlegen, Rechnungen erzeugen, freigeben und eine
    Zahlung verbuchen — der Rechnungslauf von der Pendenz bis zur bezahlten Rechnung."""
    page = AdminBillingPage(admin_page)

    # --- Stammdaten: Zahlungsart, Buchhaltungs-Einstellungen, Geschäftsjahr
    # Reihenfolge zwingend: die Einstellungen verlangen eine bestehende Zahlungsart.
    page.ensure_payment_type(_PAYMENT_TYPE)
    page.ensure_accounting_settings()
    page.ensure_business_year(_YEAR, f"01.01.{_YEAR}", f"31.12.{_YEAR}")
    shot(admin_page, "admin_billing_02_business_year")

    # --- Anstehende Rechnungen für das Geschäftsjahr
    page.navigate_pending_bills()
    page.select_year(_YEAR)
    shot(admin_page, "admin_billing_03_pending_for_year")
    assert page.row_count() > 0, \
        f"Für {_YEAR} sollten verrechenbare Abo-Bestandteile aufgelistet werden"

    # --- Rechnungen erzeugen -> landen unveröffentlicht
    page.generate_all_bills()
    shot(admin_page, "admin_billing_04_unpublished")
    assert "unpublished_bills" in admin_page.url, \
        f"Nach dem Erzeugen sollte die Liste der unveröffentlichten Rechnungen erscheinen, URL war: '{admin_page.url}'"
    assert page.row_count() > 0, \
        "Nach dem Erzeugen sollte mindestens eine unveröffentlichte Rechnung vorhanden sein"

    # --- Freigeben: danach sind keine unveröffentlichten Rechnungen mehr offen
    page.publish_all_bills()
    shot(admin_page, "admin_billing_05_after_publish")
    assert page.row_count() == 0, \
        "Nach dem Veröffentlichen sollte die Liste der unveröffentlichten Rechnungen leer sein"

    # --- Offene Rechnungen: die freigegebene Rechnung ist jetzt sichtbar
    page.navigate_open_bills()
    page.select_year(_YEAR)
    shot(admin_page, "admin_billing_06_open")
    assert page.row_count() > 0, \
        "Die freigegebenen Rechnungen sollten als offene Rechnungen erscheinen"
    bill_id = page.first_bill_id()

    # --- Zahlungseingang über den vollen Betrag verbuchen
    amount = page.record_full_payment(bill_id)
    shot(admin_page, "admin_billing_07_after_payment")
    assert float(amount) > 0, \
        f"Die Rechnung sollte einen Betrag > 0 aufweisen, war: '{amount}'"

    # --- Ausgeglichene Rechnung verschwindet aus den offenen Rechnungen
    page.navigate_open_bills()
    page.select_year(_YEAR)
    shot(admin_page, "admin_billing_08_after_payment_open")
    assert not page.lists_bill(bill_id), \
        f"Rechnung {bill_id} sollte nach dem vollen Zahlungseingang nicht mehr offen sein"
