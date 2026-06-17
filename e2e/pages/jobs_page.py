from datetime import datetime
from zoneinfo import ZoneInfo

from playwright.sync_api import Page

# Dates in the jobs table are rendered by Django using TIME_ZONE = 'Europe/Zurich'.
# Using the same timezone here avoids off-by-one-day mismatches when the test runner
# is in UTC and a job's UTC time falls on "today UTC" but "tomorrow CET".
_DISPLAY_TZ = ZoneInfo('Europe/Zurich')


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
        today = datetime.now(tz=_DISPLAY_TZ).date()
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
        # BusinessYearForm sets self.data['year'] = get_business_year() (e.g. 2026) when
        # no GET param is present, even if 2026 is outside the valid choices (member only
        # has assignments in 2027). An invalid choice makes is_valid() return False and
        # assignments = QuerySet.none() — the table stays empty even though data exists.
        # Fix: always pass the latest available year as an explicit GET parameter.
        year_select = self.page.locator("select[name='year']")
        if year_select.count() > 0:
            options = year_select.evaluate(
                "el => Array.from(el.options).map(o => o.value).filter(v => v)"
            )
            if options:
                self.page.goto(f"/my/memberjobs?year={max(options, key=int)}")
                self.page.wait_for_load_state("networkidle")

    def job_in_member_list(self, job_name: str) -> bool:
        # The page lands while DataTables is still enhancing the server-rendered
        # table. DataTables re-renders <tbody>, briefly detaching the original
        # <a> rows — a plain wait_for(visible) on the link races that redraw and
        # can time out even though the data is present (flaky test_register_for_job).
        # First wait for DataTables to finish (it wraps the table in
        # #assignments-table_wrapper), then assert the row is present.
        try:
            self.page.locator("#assignments-table_wrapper").wait_for(
                state="attached", timeout=15000
            )
        except Exception:
            pass  # tolerate a changed wrapper id; the link wait below still guards us
        # has_text does a case-insensitive substring match (the link text is the
        # job type, e.g. "Ernten - Ernten") and avoids quote-injection from job_name.
        job_link = self.page.locator(
            "#assignments-table tbody a", has_text=job_name
        ).first
        try:
            job_link.wait_for(state="visible", timeout=15000)
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
