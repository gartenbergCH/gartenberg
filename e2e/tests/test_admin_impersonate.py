from conftest import MEMBER_FIRST, MEMBER_LAST, shot
from pages.admin_impersonate_page import AdminImpersonatePage


def test_admin_can_impersonate_member(admin_page, member_context):
    page = AdminImpersonatePage(admin_page)
    try:
        # Juntagrico sets auth.User.username = '{slugify(first)}_{slugify(last)}_{seed}'.
        # The auth.User.email field stays empty, so searching by MEMBER_EMAIL finds nothing.
        # The slugified last name is reliably part of the generated username.
        page.navigate_search(MEMBER_LAST.lower())
        shot(admin_page, "admin_impersonate_01_search")

        page.impersonate_first_result()
        shot(admin_page, "admin_impersonate_02_as_member")

        assert page.is_impersonating(), \
            "Impersonate-Banner (.impersonate-row) sollte nach dem Start sichtbar sein"
        banner = page.banner_text()
        assert MEMBER_FIRST in banner and MEMBER_LAST in banner, \
            f"Banner sollte '{MEMBER_FIRST} {MEMBER_LAST}' enthalten, war: '{banner}'"

        # Auf Mitglieder-Profil zugreifen während Impersonation aktiv ist
        admin_page.goto("/my/profile")
        admin_page.wait_for_load_state("networkidle")
        shot(admin_page, "admin_impersonate_03_member_profile")
        assert MEMBER_LAST in admin_page.content(), \
            f"Profil-Seite sollte '{MEMBER_LAST}' enthalten"
    finally:
        # Immer stoppen — admin_context ist session-scoped und würde sonst
        # alle nachfolgenden Admin-Tests beeinflussen
        page.stop_impersonation()

    shot(admin_page, "admin_impersonate_04_after_stop")
    assert not page.is_impersonating(), \
        "Impersonate-Banner sollte nach dem Stopp nicht mehr sichtbar sein"
