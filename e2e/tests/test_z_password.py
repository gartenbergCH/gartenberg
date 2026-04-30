"""
Runs LAST (filename prefix test_z_) because Juntagrico's change_password view
does not call update_session_auth_hash().  Django therefore invalidates the
member's session on the next request after the password is saved.  Any test
that runs after this one with the shared member_context would find itself
logged out.
"""
from conftest import shot
from pages.password_page import PasswordPage


def test_change_password(member_page):
    pwd = PasswordPage(member_page)
    pwd.navigate()
    shot(member_page, "password_01_form")

    pwd.change_password("neues-passwort-e2e")
    shot(member_page, "password_02_after_change")

    assert pwd.is_changed_successfully(), \
        "Success alert should be shown after changing the password"
