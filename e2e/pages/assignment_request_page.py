from playwright.sync_api import Page


class AssignmentRequestPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        self.page.goto("/ar/assignment/request")
        self.page.wait_for_load_state("networkidle")

    def submit_request(self, job_time: str, description: str):
        """
        job_time: datetime-local string, e.g. "2026-05-07T09:00"
        """
        self.page.locator("input[name='job_time']").fill(job_time)
        # index 0 is the empty "--------" option; index 1 is the first real area
        self.page.locator("select[name='activityarea']").select_option(index=1)
        self.page.locator("textarea[name='description']").fill(description)
        # Wait for the GET 200 of the redirect target, not the POST 302 (same
        # networkidle-gap issue as in JobDetailPage.subscribe)
        with self.page.expect_response(
            lambda r: "/ar/assignment/request" in r.url and r.request.method == "GET" and r.status == 200
        ):
            self.page.get_by_role("button", name="Absenden").click()
        self.page.wait_for_load_state("networkidle")

    def is_submitted_successfully(self) -> bool:
        return self.page.locator(".alert-success").count() > 0

    def has_pending_requests(self) -> bool:
        return self.page.locator("#filter-table tbody tr").count() > 0

    def _rows_for(self, description: str):
        """Pro Anfrage rendert die Liste zwei <tr>: die Datenzeile und darunter eine Zeile
        mit Beschreibung und (nach dem Entscheid) der Antwort. CSS kennt keinen
        Vorgänger-Selektor, deshalb per XPath über die eindeutige Beschreibung."""
        description_row = self.page.locator(
            "xpath=//tr[contains(@class, 'ar-assignment-request-description')]"
            f'[contains(., "{description}")]'
        )
        return description_row.locator("xpath=preceding-sibling::tr[1]"), description_row

    def status_of(self, description: str) -> str:
        # Spalten: Einsatz vom | Abgesprochen mit | Status
        data_row, _ = self._rows_for(description)
        return data_row.locator("td").nth(2).inner_text().strip()

    def response_shown(self, description: str, response_text: str) -> bool:
        _, description_row = self._rows_for(description)
        return response_text in description_row.inner_text()
