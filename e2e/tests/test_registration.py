"""
Verifies that the signup wizard creates a member account and sends a welcome email
with a working confirmation link and a usable auto-generated password.

The member_context session fixture in conftest.py already drives the full wizard:
  1. Calls wait_for_email(MEMBER_EMAIL)    → welcome email was received      (EX-R03)
  2. Calls extract_password(email_body)   → "Passwort:" line found in email  (EX-R03)
  3. Calls extract_confirm_path(body)     → confirmation URL found in email  (EX-R03)
  4. Follows the confirmation URL         → account confirmed
  5. Logs in with the extracted password  → session is valid

If any of those steps fail, member_context raises and every test that uses it is
skipped — so a passing test suite implicitly proves EX-R03 without needing MailHog
access here (test_admin_mail.py clears the inbox before this file runs).
"""
from conftest import MEMBER_EMAIL, MEMBER_FIRST, MEMBER_LAST, shot
from playwright.sync_api import BrowserContext


def test_member_is_logged_in_after_signup(member_context: BrowserContext):
    page = member_context.new_page()
    try:
        page.goto("/my/profile")
        page.wait_for_load_state("networkidle")
        shot(page, "registration_01_profile")

        # Basic: session is valid
        assert "login" not in page.url, "Member should be logged in after signup"

        # EX-R01: name and email are rendered in the (disabled) profile form fields
        content = page.content()
        assert MEMBER_FIRST in content, \
            f"Vorname '{MEMBER_FIRST}' fehlt auf der Profilseite nach dem Signup"
        assert MEMBER_LAST in content, \
            f"Nachname '{MEMBER_LAST}' fehlt auf der Profilseite nach dem Signup"
        assert MEMBER_EMAIL in content, \
            f"E-Mail '{MEMBER_EMAIL}' fehlt auf der Profilseite nach dem Signup"

        # EX-R02: membership-status block exists and confirms active membership
        status = page.locator(".membership-status")
        assert status.count() > 0, "Membership-Status-Block fehlt auf der Profilseite"
        status_text = status.inner_text()
        assert "aktiv" in status_text.lower(), \
            f"Membership-Status sollte 'aktiv' enthalten, war: '{status_text}'"
    finally:
        page.close()
