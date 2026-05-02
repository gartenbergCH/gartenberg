"""
Runs LAST (filename prefix test_z_) because Juntagrico's change_password view
does not call update_session_auth_hash().  Django therefore invalidates the
member's session on the next request after the password is saved.  Any test
that runs after this one with the shared member_context would find itself
logged out.
"""
from conftest import BASE_URL, MEMBER_EMAIL, _COOKIE_CONSENT_COOKIE, shot
from pages.password_page import PasswordPage


def test_change_password(member_page):
    pwd = PasswordPage(member_page)
    pwd.navigate()
    shot(member_page, "password_01_form")

    pwd.change_password("neues-passwort-e2e")
    shot(member_page, "password_02_after_change")

    assert pwd.is_changed_successfully(), \
        "Success alert should be shown after changing the password"


def test_login_with_new_password(member_context, playwright):
    """EX-PW01: Neues Passwort funktioniert in einem frischen Browser-Kontext."""
    browser2 = playwright.chromium.launch(headless=True)
    ctx2 = browser2.new_context(base_url=BASE_URL)
    ctx2.add_cookies([_COOKIE_CONSENT_COOKIE])
    p2 = ctx2.new_page()
    try:
        p2.goto("/accounts/login/")
        p2.locator("#username").fill(MEMBER_EMAIL)
        p2.locator("#password").fill("neues-passwort-e2e")
        p2.get_by_role("button", name="Anmelden").click()
        p2.wait_for_url("**/")
        shot(p2, "password_03_new_login")
        assert "login" not in p2.url, \
            "Login mit neuem Passwort sollte erfolgreich sein und nicht auf /login/ bleiben"
    finally:
        p2.close()
        ctx2.close()
        browser2.close()
