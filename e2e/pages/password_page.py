from playwright.sync_api import Page


class PasswordPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        self.page.goto("/my/password")
        self.page.wait_for_load_state("networkidle")

    def change_password(self, old_password: str, new_password: str):
        # Der POST leitet auf /my/password/done weiter, das den Erfolgshinweis rendert.
        # Seit juntagrico 2.0.11 ein Django-PasswordChangeForm (mit Altem Passwort)
        self.page.locator("input[name='old_password']").fill(old_password)
        self.page.locator("input[name='new_password1']").fill(new_password)
        self.page.locator("input[name='new_password2']").fill(new_password)
        self.page.get_by_role("button", name="Passwort ändern").click()
        self.page.wait_for_load_state("networkidle")

    def is_changed_successfully(self) -> bool:
        return self.page.locator(".alert-success").count() > 0
