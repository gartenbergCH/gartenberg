from conftest import shot
from pages.admin_assignments_page import AdminAssignmentsPage


def _expected(rows) -> set[str]:
    return set().union(*(emails for emails, progress in rows if progress < 100))


def test_kopiert_e_mails_der_abos_unter_100_prozent(admin_page):
    page = AdminAssignmentsPage(admin_page)
    page.navigate()
    shot(admin_page, "admin_assignments_01_list")

    rows = page.rows()
    expected = _expected(rows)
    assert expected, f"Die Testdaten sollten Abos unter 100 % enthalten: {rows}"

    # EX-AA01: Kopiert genau die Adressen der Abos unter 100 % (UC-013 Hauptablauf)
    copied = page.copy_incomplete_emails()
    shot(admin_page, "admin_assignments_02_copied")
    assert copied == expected, f"Kopiert: {copied}, erwartet: {expected}"
    complete = set().union(*(emails for emails, progress in rows if progress >= 100))
    assert not (copied & (complete - expected)), "Abos mit 100 % oder mehr dürfen nicht dabei sein"

    # EX-AA02: Mit eingeschaltetem Schalter kommen die Mitbezüger/innen dazu (GR-002)
    page.show_co_members()
    with_co_members = _expected(page.rows())
    assert with_co_members >= expected
    assert page.copy_incomplete_emails() == with_co_members
    shot(admin_page, "admin_assignments_03_co_members")

    # EX-AA03: Ohne berücksichtigte Abos unter 100 % ist die Schaltfläche deaktiviert (A2)
    page.search("keine-treffer-e2e")
    shot(admin_page, "admin_assignments_04_no_rows")
    assert page.copy_button().is_disabled(), "Ohne Treffer sollte die Schaltfläche deaktiviert sein"
