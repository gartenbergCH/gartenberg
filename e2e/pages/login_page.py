from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        self.page.goto("/accounts/login/")

    def login(self, email: str, password: str):
        self.page.locator("#username").fill(email)
        self.page.locator("#password").fill(password)
        self.page.get_by_role("button", name="Anmelden").click()

    def is_logged_in(self) -> bool:
        return self.page.url.rstrip("/").endswith("/") and "login" not in self.page.url
