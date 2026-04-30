from conftest import shot
from pages.admin_billing_page import AdminBillingPage


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
