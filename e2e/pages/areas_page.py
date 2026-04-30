from playwright.sync_api import Page


class AreasPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        self.page.goto("/my/areas")
        self.page.wait_for_load_state("networkidle")

    def area_count(self) -> int:
        return self.page.locator(".activity-area-list-element a").count()

    def first_area_name(self) -> str:
        return self.page.locator(".activity-area-list-element a").first.inner_text()

    def click_first_area(self):
        self.page.locator(".activity-area-list-element a").first.click()
        self.page.wait_for_load_state("networkidle")

    def detail_heading(self) -> str:
        return self.page.locator("h3").first.inner_text()
