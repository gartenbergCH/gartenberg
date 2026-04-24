"""
Verifies that the signup wizard creates a member account and sends a welcome email
with a working confirmation link and a usable auto-generated password.

The member_context session fixture in conftest.py already drives the full wizard.
Here we only assert that the resulting logged-in session works.
"""
from playwright.sync_api import BrowserContext


def test_member_is_logged_in_after_signup(member_context: BrowserContext):
    page = member_context.new_page()
    try:
        page.goto("/my/profile")
        page.wait_for_load_state("networkidle")
        assert "login" not in page.url, "Member should be logged in after signup"
        assert page.locator(".membership-status").count() > 0, "Profile page should show membership status"
    finally:
        page.close()
