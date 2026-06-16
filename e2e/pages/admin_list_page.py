from playwright.sync_api import Page


class AdminListPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        # 2.0 moved the depot list page from /manage/list to /list
        self.page.goto("/list")
        self.page.wait_for_load_state("networkidle")

    def generate(self, for_date: str = "2027-01-01"):
        # for_date expects ISO format (YYYY-MM-DD); widget renders as type="date"
        self.page.locator("input[name='for_date']").fill(for_date)
        # crispy Submit renders as <input type="submit">, which has ARIA role "button"
        self.page.get_by_role("button", name="Listen Erzeugen", exact=True).click()
        # juntagrico redirects to '' (empty Location) after generation; Chromium does
        # not follow that, leaving a blank page. Re-navigate to /list explicitly so the
        # generated lists (and their download links) are visible.
        self.page.wait_for_load_state("networkidle")
        self.page.goto("/list")
        self.page.wait_for_load_state("networkidle")

    def _generated_links(self):
        # In 2.0 generated lists render as download links (/list/<name>) in the
        # depot_lists section; not-yet-generated lists render as plain text.
        return self.page.locator("a[href*='/list/']")

    def was_successful(self) -> bool:
        return self._generated_links().count() > 0

    def open_first_generated_link(self):
        self._generated_links().first.click()
        self.page.wait_for_load_state("networkidle")

    def is_accessible(self) -> bool:
        return self.page.locator("body").is_visible() and "404" not in self.page.title()
