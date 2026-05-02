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
        # Use wait_for so DataTables has time to finish its client-side initialisation
        # (networkidle fires before DataTables re-renders tbody rows on slow CI runners).
        try:
            self.page.locator(f"#assignments-table a:has-text('{job_name}')").wait_for(
                state="visible", timeout=10000
            )
            return True
        except Exception:
            return False


class JobDetailPage:
    def __init__(self, page: Page):
        self.page = page

    def subscribe(self) -> bool:
        """Subscribe to the job. Returns False when the form is unavailable
        (already subscribed, job full, or past) so callers can skip assertions."""
        self.page.wait_for_load_state("networkidle")
        slots_select = self.page.locator("#job-subscribe-form select[name='slots']")
        if slots_select.count() > 0:
            slots_select.select_option("1")
        confirm_button = self.page.get_by_role("button", name="Bestätigen")
        if confirm_button.count() == 0:
            return False
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
            confirm_button.click()
        self.page.wait_for_load_state("networkidle")
        return True

    def job_title(self) -> str:
        return self.page.locator("h3").first.inner_text()

    def occupied_slots(self) -> int:
        # Status div title attribute: "X von Y gebucht" — absent for infinite-slot jobs
        loc = self.page.locator("[title*='von'][title*='gebucht']")
        if loc.count() == 0:
            return -1  # infinite-slot job; caller should skip slot assertions
        title = loc.first.get_attribute("title") or ""
        try:
            return int(title.split()[0])
        except (ValueError, IndexError):
            return -1
