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

    def content(self) -> str:
        return self.page.content()

    def area_id(self) -> str:
        """Return the area ID from the switch checkbox on the current detail page."""
        return self.page.locator("input.switch").first.get_attribute("value") or ""

    def is_member(self) -> bool:
        """True when the current member belongs to the currently shown area."""
        return self.page.locator("input.switch").first.is_checked()

    def join(self, area_id: str):
        self.page.goto(f"/my/area/{area_id}/join")
        self.page.goto(f"/my/area/{area_id}/")
        self.page.wait_for_load_state("networkidle")

    def leave(self, area_id: str):
        self.page.goto(f"/my/area/{area_id}/leave")
        self.page.goto(f"/my/area/{area_id}/")
        self.page.wait_for_load_state("networkidle")
