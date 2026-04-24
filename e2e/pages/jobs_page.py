from datetime import date, datetime

from playwright.sync_api import Page


class JobsPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        self.page.goto("/my/jobs")
        self.page.wait_for_load_state("networkidle")

    def _nearest_future_job_href(self) -> str:
        """Return the href of the job with the nearest future date (date > today).

        DataTables sorts the table alphabetically by the "D d.m.Y" string, which
        is NOT chronological order — e.g. "Di 01.06.2027" (Tuesday) sorts before
        "Do 07.05.2026" (Thursday) because "Di" < "Do" lexicographically.  Picking
        the *first* DOM row therefore picks the wrong job when the day-of-week prefix
        differs.  Scanning all rows and picking the minimum future date is robust
        against any DataTables sort order.
        """
        today = date.today()
        rows = self.page.locator("#filter-table tbody tr")
        best_date = None
        best_href = None
        for i in range(rows.count()):
            row = rows.nth(i)
            cell_text = row.locator("td:first-child").inner_text().strip()
            for part in cell_text.split():
                try:
                    row_date = datetime.strptime(part, "%d.%m.%Y").date()
                    if row_date > today and (best_date is None or row_date < best_date):
                        best_date = row_date
                        best_href = row.locator("td:nth-child(2) a").get_attribute("href")
                    break
                except ValueError:
                    continue
        return best_href or ""

    def first_job_name(self) -> str:
        href = self._nearest_future_job_href()
        return self.page.locator(f"#filter-table a[href='{href}']").inner_text()

    def click_first_job(self):
        href = self._nearest_future_job_href()
        self.page.locator(f"#filter-table a[href='{href}']").click()

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
        # Wait for the GET response of the redirect target (not the POST's 302).
        # After a successful POST the server redirects back to the same job URL.
        # Waiting for the POST 302 leaves a brief networkidle gap before the
        # follow-up GET starts — on slow CI runners wait_for_load_state("networkidle")
        # can fire during that gap and return too early.  Waiting for the GET 200
        # ensures the full POST→redirect→page-load cycle has completed.
        with self.page.expect_response(
            lambda resp: "/my/jobs/" in resp.url and resp.request.method == "GET" and resp.status == 200
        ):
            self.page.get_by_role("button", name="Bestätigen").click()
        self.page.wait_for_load_state("networkidle")

    def job_title(self) -> str:
        return self.page.locator("h3").first.inner_text()
