from playwright.sync_api import Page


class PasswordPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        self.page.goto("/my/password")
        self.page.wait_for_load_state("networkidle")

    def change_password(self, new_password: str):
        # The POST returns HTTP 200 (not a redirect) — the view re-renders
        # the same template with success=True, so a plain networkidle wait suffices.
        self.page.locator("input[name='password']").fill(new_password)
        self.page.locator("input[name='passwordRepeat']").fill(new_password)
        self.page.get_by_role("button", name="Passwort ändern").click()
        self.page.wait_for_load_state("networkidle")

    def is_changed_successfully(self) -> bool:
        return self.page.locator(".alert-success").count() > 0
