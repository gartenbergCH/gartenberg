from playwright.sync_api import Page


class JobsPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        self.page.goto("/my/jobs")
        self.page.wait_for_load_state("networkidle")

    def first_job_name(self) -> str:
        return self.page.locator("#filter-table tbody tr:first-child td:nth-child(2) a").inner_text()

    def click_first_job(self):
        self.page.locator("#filter-table tbody tr:first-child td:nth-child(2) a").click()

    def navigate_member_jobs(self):
        self.page.goto("/my/memberjobs")
        self.page.wait_for_load_state("networkidle")

    def job_in_member_list(self, job_name: str) -> bool:
        return self.page.locator(f"#assignments-table a:has-text('{job_name}')").count() > 0


class JobDetailPage:
    def __init__(self, page: Page):
        self.page = page

    def subscribe(self):
        self.page.wait_for_load_state("networkidle")
        # The slot selector must be set before clicking — choose 1 slot
        slots_select = self.page.locator("#job-subscribe-form select[name='slots']")
        if slots_select.count() > 0:
            slots_select.select_option("1")
        self.page.get_by_role("button", name="Bestätigen").click()
        self.page.wait_for_load_state("networkidle")

    def job_title(self) -> str:
        return self.page.locator("h3").first.inner_text()
