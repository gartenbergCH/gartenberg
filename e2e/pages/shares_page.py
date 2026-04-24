from playwright.sync_api import Page


class SharesPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        self.page.goto("/my/share/manage/")
        self.page.wait_for_load_state("networkidle")

    def order_shares(self, count: int):
        # bootstrap-input-spinner wraps the input; use the + button to increment
        for _ in range(count):
            self.page.locator(".btn-increment").first.click()
        self.page.get_by_role("button", name="Bestellen").click()

    def shares_count(self) -> int:
        return self.page.locator("#filter-table tbody tr").count()
