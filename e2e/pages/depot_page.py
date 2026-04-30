from playwright.sync_api import Page


class DepotPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        self.page.goto("/my/depot/")
        self.page.wait_for_load_state("networkidle")

    def is_on_depot_page(self) -> bool:
        return "/my/depot/" in self.page.url

    def heading(self) -> str:
        return self.page.locator("h3").first.inner_text()
