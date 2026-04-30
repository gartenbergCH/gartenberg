from playwright.sync_api import Page


class AdminListPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        self.page.goto("/manage/list")
        self.page.wait_for_load_state("networkidle")

    def generate(self, for_date: str = "2027-01-01"):
        # for_date expects ISO format (YYYY-MM-DD); widget renders as type="date"
        self.page.locator("input[name='for_date']").fill(for_date)
        # crispy Submit renders as <input type="submit">, which has ARIA role "button"
        self.page.get_by_role("button", name="Listen Erzeugen", exact=True).click()
        self.page.wait_for_load_state("networkidle")

    def was_successful(self) -> bool:
        return "Listen erstellt" in (self.page.locator(".alert-success").text_content() or "")
