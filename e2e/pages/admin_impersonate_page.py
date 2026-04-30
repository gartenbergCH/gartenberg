from playwright.sync_api import Page


class AdminImpersonatePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate_search(self, query: str):
        # Juntagrico generates auth.User.username as '{slugify(first)}_{slugify(last)}_{seed}'
        # — the email is NOT stored on auth.User. Search by the slugified last name instead.
        self.page.goto(f"/impersonate/search/?q={query}")
        self.page.wait_for_load_state("networkidle")

    def impersonate_first_result(self):
        # Stock Django impersonate template renders <ul><li><a href="/impersonate/{pk}/">...</a></li></ul>
        self.page.locator("ul li a").first.click()
        self.page.wait_for_load_state("networkidle")

    def is_impersonating(self) -> bool:
        return self.page.locator(".impersonate-row").count() > 0

    def banner_text(self) -> str:
        return self.page.locator(".impersonate-row .alert").text_content() or ""

    def stop_impersonation(self):
        self.page.goto("/impersonate/stop/")
        self.page.wait_for_load_state("networkidle")
