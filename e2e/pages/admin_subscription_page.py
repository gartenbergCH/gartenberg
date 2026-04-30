from playwright.sync_api import Page


class AdminMemberPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        self.page.goto("/manage/member/active")
        self.page.wait_for_load_state("networkidle")

    def member_row_count(self) -> int:
        return self.page.locator("#filter-table tbody tr").count()

    def contains_member(self, name: str) -> bool:
        return self.page.locator("#filter-table tbody").get_by_text(name).count() > 0


class AdminSubscriptionRecentPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        self.page.goto("/manage/subscription/recent")
        self.page.wait_for_load_state("networkidle")

    def change_row_count(self) -> int:
        return self.page.locator("#filter-table tbody tr").count()

    def has_change_type(self, change_type: str) -> bool:
        return self.page.locator("#filter-table tbody").get_by_text(change_type).count() > 0


class AdminSubscriptionPendingPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        self.page.goto("/manage/subscription/pending")
        self.page.wait_for_load_state("networkidle")

    def pending_row_count(self) -> int:
        return self.page.locator("#filter-table tbody tr").count()
