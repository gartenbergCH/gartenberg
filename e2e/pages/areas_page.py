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

    def _toggle(self, area_id: str, action: str, checked: bool):
        # Seit juntagrico 2.1 nehmen join/leave nur POST mit CSRF-Token an; deshalb über den
        # Schalter wie ein Mitglied, nicht per goto. Das Input des CSS-Switches liegt verdeckt
        # ausserhalb des Klickbereichs; geklickt wird darum das Label "Mitmachen".
        self.page.goto(f"/my/area/{area_id}/")
        self.page.wait_for_load_state("networkidle")
        assert self.is_member() != checked, f"Bereich {area_id} ist schon im Zustand {checked}"
        with self.page.expect_response(f"**/my/area/{area_id}/{action}") as response:
            self.page.locator(f"label[for='area{area_id}']").click()
        assert response.value.ok, f"{action} fehlgeschlagen: HTTP {response.value.status}"
        self.page.reload()
        self.page.wait_for_load_state("networkidle")

    def join(self, area_id: str):
        self._toggle(area_id, "join", True)

    def leave(self, area_id: str):
        self._toggle(area_id, "leave", False)
