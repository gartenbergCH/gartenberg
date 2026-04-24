from datetime import date

from playwright.sync_api import Page


class JobsPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        self.page.goto("/my/jobs")
        self.page.wait_for_load_state("networkidle")

    def _first_future_job_row(self):
        # generate_testdata creates type_2 jobs with time=build_time (in the past by test run).
        # Those appear first (sorted ascending) but have can_interact=False.
        # Skip rows whose date matches today and return the first future one.
        today_str = date.today().strftime("%d.%m.%Y")
        rows = self.page.locator("#filter-table tbody tr")
        for i in range(rows.count()):
            row = rows.nth(i)
            if today_str not in row.locator("td:first-child").inner_text():
                return row
        return rows.first

    def first_job_name(self) -> str:
        return self._first_future_job_row().locator("td:nth-child(2) a").inner_text()

    def click_first_job(self):
        self._first_future_job_row().locator("td:nth-child(2) a").click()

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
        slots_select = self.page.locator("#job-subscribe-form select[name='slots']")
        if slots_select.count() > 0:
            slots_select.select_option("1")
        # Override window.confirm so initJob.js's confirmation dialog auto-accepts
        self.page.evaluate("window.confirm = () => true")
        # Wait for the POST response explicitly: expect_navigation() is deprecated
        # in Playwright 1.44+ and may be a no-op; expect_response() reliably waits
        # for the actual network round-trip (POST → 302) before we navigate away.
        with self.page.expect_response(
            lambda resp: "/my/jobs/" in resp.url and resp.request.method == "POST"
        ):
            self.page.get_by_role("button", name="Bestätigen").click()
        self.page.wait_for_load_state("networkidle")

    def job_title(self) -> str:
        return self.page.locator("h3").first.inner_text()
