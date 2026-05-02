from conftest import shot
from pages.admin_list_page import AdminListPage


def test_admin_can_generate_depot_list(admin_page):
    page = AdminListPage(admin_page)
    page.navigate()
    shot(admin_page, "admin_list_01_form")

    page.generate("2027-01-01")
    shot(admin_page, "admin_list_02_result")

    assert page.was_successful(), \
        "Nach der Listenerzeugung sollte die Erfolgsmeldung 'Listen erstellt' erscheinen"

    # EX-AL01: Erste generierte Liste ist abrufbar (kein 404/500)
    page.open_first_generated_link()
    shot(admin_page, "admin_list_03_generated_file")
    assert page.is_accessible(), \
        "Generierte Depotliste sollte abrufbar sein (kein 404)"
