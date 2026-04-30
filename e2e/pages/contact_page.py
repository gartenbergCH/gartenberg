from playwright.sync_api import Page


class ContactPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        self.page.goto("/my/contact")
        self.page.wait_for_load_state("networkidle")

    def send_message(self, subject: str, message: str):
        self.page.locator("input[name='subject']").fill(subject)
        self.page.locator("textarea[name='message']").fill(message)
        self.page.get_by_role("button", name="Nachricht verschicken").click()
        self.page.wait_for_load_state("networkidle")

    def is_sent(self) -> bool:
        return self.page.locator(".alert-success").count() > 0

    def content(self) -> str:
        return self.page.content()
