from conftest import MEMBER_LAST, shot
from pages.admin_subscription_page import AdminMemberPage


def test_admin_can_view_member_list(admin_page, member_context):
    page = AdminMemberPage(admin_page)
    page.navigate()
    shot(admin_page, "admin_member_01_list")

    assert page.member_row_count() > 0, "Mitgliederliste sollte mindestens einen Eintrag enthalten"
    assert page.contains_member(MEMBER_LAST), \
        f"Mitglied '{MEMBER_LAST}' sollte in der aktiven Mitgliederliste erscheinen"
