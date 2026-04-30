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


def test_admin_can_view_recent_subscription_changes(admin_page, member_context):
    page = AdminSubscriptionRecentPage(admin_page)
    page.navigate()
    shot(admin_page, "admin_sub_recent_01_page")

    assert page.change_row_count() > 0, \
        "Letzte Änderungen sollte nach der Registrierung mindestens einen Eintrag enthalten"
    assert page.has_change_type("Bestellung"), \
        "Bestellung des Test-Members sollte in den letzten Änderungen erscheinen"


def test_admin_can_view_pending_subscription_changes(admin_page, member_context):
    page = AdminSubscriptionPendingPage(admin_page)
    page.navigate()
    shot(admin_page, "admin_sub_pending_01_page")

    assert page.pending_row_count() > 0, \
        "Pendende Änderungen sollte das noch nicht aktivierte Abo des Test-Members enthalten"
