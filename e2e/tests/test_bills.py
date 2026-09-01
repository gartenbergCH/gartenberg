"""UC-012 / FR-051: Mitglieder sehen ihre eigenen Rechnungen."""

from datetime import date

from conftest import shot
from pages.admin_billing_page import AdminBillingPage
from pages.admin_impersonate_page import AdminImpersonatePage
from pages.bills_page import BillsPage

_YEAR = str(date.today().year)
_PAYMENT_TYPE = "E2E Bank"


def _ensure_published_bills(billing: AdminBillingPage):
    """Stellt freigegebene Rechnungen sicher — unabhängig davon, ob der Rechnungslauf
    aus test_admin_billing.py (UC-007) vorher gelaufen ist.

    Alle Schritte sind idempotent: die Stammdaten werden nur angelegt, wenn sie fehlen,
    und erzeugt wird nur, solange die Liste anstehende Rechnungen ausweist."""
    billing.ensure_payment_type(_PAYMENT_TYPE)
    billing.ensure_accounting_settings()
    billing.ensure_business_year(_YEAR, f"01.01.{_YEAR}", f"31.12.{_YEAR}")

    billing.navigate_pending_bills()
    billing.select_year(_YEAR)
    if billing.row_count() > 0:
        billing.generate_all_bills()
        billing.publish_all_bills()


def test_member_sees_bills_entry_in_user_menu(member_page):
    """UC-012 Schritt 1: Der Zugang zu den Rechnungen steht im Menü des Mitglieds."""
    page = BillsPage(member_page)
    page.navigate_profile()
    shot(member_page, "bills_01_usermenu")

    assert page.has_menu_entry(), \
        "Sichtbarer Menüeintrag mit Link auf /jb/user_bills fehlt — ist BILLS_USERMENU gesetzt?"
    assert page.menu_entry_text() == "Rechnungen", \
        f"Menüeintrag sollte 'Rechnungen' heissen, war: '{page.menu_entry_text()}'"


def test_member_opens_bills_page_from_menu(member_page):
    """UC-012 Schritt 1-2: Der Menüeintrag führt auf die eigene Rechnungsliste."""
    page = BillsPage(member_page)
    page.navigate_profile()
    page.click_menu_entry()
    shot(member_page, "bills_02_list")

    assert member_page.url.endswith(BillsPage.URL), \
        f"Nach dem Klick sollte {BillsPage.URL} geöffnet sein, war: '{member_page.url}'"
    assert page.heading() == "Rechnungen", \
        f"Seitentitel sollte 'Rechnungen' sein, war: '{page.heading()}'"
    assert page.is_menu_entry_active(), \
        "Menüeintrag 'Rechnungen' sollte auf der Rechnungsseite als aktiv markiert sein"


def test_bills_page_renders_bill_table(member_page):
    """UC-012 Schritt 2 / A1: Die Rechnungsliste rendert mit ihren Spalten.

    Für das frisch angelegte Testmitglied ist sie leer (das Abo startet erst im nächsten
    Geschäftsjahr, es besteht also keine freigegebene Rechnung — Alternativablauf A1).
    Fehlen die Buchhaltungs-Einstellungen mit Standard-Zahlungsart, antwortet die Seite
    mit HTTP 500 statt der Liste.
    """
    page = BillsPage(member_page)
    status = page.navigate()
    shot(member_page, "bills_03_table")

    assert status == 200, f"/jb/user_bills sollte mit 200 antworten, war: {status}"
    assert page.has_table(), "Rechnungstabelle (#filter-table) fehlt"
    for column in ["Nummer", "Datum", "Art", "Betrag", "Bezahlt"]:
        assert column in page.column_headers(), \
            f"Spalte '{column}' fehlt in der Rechnungstabelle: {page.column_headers()}"


def test_member_sees_own_published_bill(admin_page):
    """UC-012 Hauptablauf: Ein Mitglied mit einer freigegebenen Rechnung sieht sie in
    seiner Rechnungsliste, öffnet sie mit Einzahlungsschein und offenem Betrag und kann
    sie als PDF beziehen.

    Das per Signup angelegte Testmitglied hat noch keine Rechnung (sein Abo startet erst
    im nächsten Geschäftsjahr). Geprüft wird deshalb an einem verrechneten Mitglied aus
    den Testdaten, dessen Sitzung über den Impersonate-Link der Rechnungszeile übernommen
    wird (UC-008 FR-045)."""
    billing = AdminBillingPage(admin_page)
    _ensure_published_bills(billing)

    billing.navigate_open_bills()
    billing.select_year(_YEAR)
    assert billing.row_count() > 0, \
        f"Für {_YEAR} sollte mindestens eine freigegebene, offene Rechnung bestehen"
    bill_id = billing.first_bill_id()
    impersonation_url = billing.first_bill_impersonation_url()
    shot(admin_page, "bills_04_admin_open_bill")

    impersonate = AdminImpersonatePage(admin_page)
    try:
        admin_page.goto(impersonation_url)
        admin_page.wait_for_load_state("networkidle")
        assert impersonate.is_impersonating(), \
            "Sitzungsübernahme des verrechneten Mitglieds sollte aktiv sein"

        bills = BillsPage(admin_page)
        assert bills.has_menu_entry(), \
            "Auch in der übernommenen Mitgliedersicht sollte der Menüeintrag erscheinen"

        status = bills.navigate()
        shot(admin_page, "bills_05_member_bill_list")
        assert status == 200, f"/jb/user_bills sollte mit 200 antworten, war: {status}"
        assert bills.lists_bill(bill_id), \
            f"Die freigegebene Rechnung {bill_id} sollte in der Mitgliedersicht erscheinen"

        bills.open_bill(bill_id)
        shot(admin_page, "bills_06_member_bill_detail")
        assert bills.heading() == f"Rechnung {bill_id}", \
            f"Detailseite sollte 'Rechnung {bill_id}' überschrieben sein, war: '{bills.heading()}'"
        assert bills.shows_open_amount(), \
            "Detailseite sollte den noch offenen Betrag ausweisen"
        assert bills.shows_payment_slip(), \
            "Zur unbezahlten Rechnung sollte der QR-Einzahlungsschein angezeigt werden (GR-003)"

        pdf = bills.pdf_response(bill_id)
        assert pdf.status == 200, f"PDF-Abruf sollte mit 200 antworten, war: {pdf.status}"
        assert pdf.body().startswith(b"%PDF"), \
            "Der PDF-Abruf sollte ein PDF-Dokument liefern"
    finally:
        # admin_context ist session-scoped: die Übernahme immer beenden
        impersonate.stop_impersonation()

    assert not impersonate.is_impersonating(), \
        "Nach dem Stopp sollte die Sitzungsübernahme beendet sein"
