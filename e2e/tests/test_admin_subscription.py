from conftest import MEMBER_LAST, shot
from pages.admin_subscription_page import (
    AdminMemberPage,
    AdminSubscriptionRecentPage,
    AdminSubscriptionPendingPage,
)


def test_admin_can_view_member_list(admin_page, member_context):
    page = AdminMemberPage(admin_page)
    page.navigate()
    shot(admin_page, "admin_member_01_list")

    assert page.member_row_count() > 0, "Mitgliederliste sollte mindestens einen Eintrag enthalten"
    assert page.contains_member(MEMBER_LAST), \
        f"Mitglied '{MEMBER_LAST}' sollte in der aktiven Mitgliederliste erscheinen"

    # EX-AS01: Jede Zeile hat einen Link zum Django-Admin-Editformular
    assert page.has_admin_edit_links(), \
        "Mitgliederliste sollte Links zu Django-Admin-Editformularen (/admin/juntagrico/member/) enthalten"


def test_admin_can_view_recent_subscription_changes(admin_page, member_context):
    page = AdminSubscriptionRecentPage(admin_page)
    page.navigate()
    shot(admin_page, "admin_sub_recent_01_page")

    assert page.change_row_count() > 0, \
        "Letzte Änderungen sollte nach der Registrierung mindestens einen Eintrag enthalten"
    assert page.has_change_type("Bestellung"), \
        "Bestellung des Test-Members sollte in den letzten Änderungen erscheinen"

    # EX-AS02: Member-Name des Test-Members erscheint in einer Tabellenzeile
    assert MEMBER_LAST in page.tbody_text(), \
        f"Member-Name '{MEMBER_LAST}' sollte in den letzten Abo-Änderungen sichtbar sein"


def test_admin_can_view_pending_subscription_changes(admin_page, member_context):
    page = AdminSubscriptionPendingPage(admin_page)
    page.navigate()
    shot(admin_page, "admin_sub_pending_01_page")

    assert page.pending_row_count() > 0, \
        "Pendende Änderungen sollte das noch nicht aktivierte Abo des Test-Members enthalten"

    # EX-AS03: Startdatum des bestellten Abos (2027) ist in der Tabelle sichtbar
    assert "2027" in page.tbody_text(), \
        "Startdatum '2027' des bestellten Abos sollte in den pendenden Änderungen erscheinen"
