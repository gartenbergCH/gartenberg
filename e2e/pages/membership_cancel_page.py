from playwright.sync_api import Page


class MembershipCancelPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        self.page.goto("/my/cancel/membership")
        self.page.wait_for_load_state("networkidle")

    def can_cancel(self) -> bool:
        return self.page.locator(".alert-danger").count() == 0

    def cancel_blocked_reason(self) -> str:
        return self.page.locator(".alert-danger").inner_text()
