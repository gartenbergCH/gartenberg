from playwright.sync_api import Page


class ConfigPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate_contact(self):
        self.page.goto("/my/contact")
        self.page.wait_for_load_state("networkidle")

    def navigate_unpaid_shares(self):
        self.page.goto("/my/info/unpaidshares")
        self.page.wait_for_load_state("networkidle")

    def content(self) -> str:
        return self.page.content()
