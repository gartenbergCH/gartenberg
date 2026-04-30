from playwright.sync_api import Page


class AdminBillingPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate_pending_bills(self):
        self.page.goto("/jb/pending_bills")
        self.page.wait_for_load_state("networkidle")

    def heading(self) -> str:
        return self.page.locator("h3").first.inner_text().strip()

    def has_year_selector(self) -> bool:
        return self.page.locator("select#year").count() > 0

    def has_table(self) -> bool:
        return self.page.locator("#filter-table").count() > 0
