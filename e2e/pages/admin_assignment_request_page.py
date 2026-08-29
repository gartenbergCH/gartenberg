from playwright.sync_api import Page


class AdminAssignmentRequestPage:
    """Sicht der/des Einsatzverantwortlichen auf gemeldete Einsätze (UC-009)."""

    def __init__(self, page: Page):
        self.page = page

    def navigate_open_requests(self):
        self.page.goto("/ar/assignment/list")
        self.page.wait_for_load_state("networkidle")

    def navigate_archive(self):
        self.page.goto("/ar/assignment/archive")
        self.page.wait_for_load_state("networkidle")

    def _data_row(self, description: str):
        """Pro Anfrage rendert die Liste zwei <tr>: die Datenzeile und darunter eine Zeile
        mit der Beschreibung. CSS kennt keinen Vorgänger-Selektor, deshalb per XPath von
        der (eindeutigen) Beschreibung auf die zugehörige Datenzeile zurückgehen."""
        return self.page.locator(
            "xpath=//tr[contains(@class, 'ar-assignment-request-description')]"
            f'[contains(., "{description}")]/preceding-sibling::tr[1]'
        )

    def lists_request(self, description: str) -> bool:
        return self._data_row(description).count() > 0

    def open_response_form(self, description: str):
        link = self._data_row(description).locator("a[href*='/ar/assignment/respond/']")
        link.wait_for(state="visible", timeout=10000)
        link.click()
        self.page.wait_for_load_state("networkidle")

    def respond(self, response_text: str, decision: str):
        """decision ist die Beschriftung des Submit-Buttons: 'Bestätigen', 'Ablehnen'
        oder 'Nur Antwort senden'."""
        self.page.locator("textarea[name='response']").fill(response_text)
        # Auf das GET 200 des Redirect-Ziels warten, nicht auf den POST 302
        with self.page.expect_response(
            lambda r: "/ar/assignment/list" in r.url
            and r.request.method == "GET"
            and r.status == 200
        ):
            self.page.get_by_role("button", name=decision, exact=True).click()
        self.page.wait_for_load_state("networkidle")

    def status_of(self, description: str) -> str:
        # Spalten: Einsatz vom | Von | Abgesprochen mit | Status
        return self._data_row(description).locator("td").nth(3).inner_text().strip()

    def has_assignment_link(self, description: str) -> bool:
        """Bei einer bestätigten Anfrage verlinkt der Status auf den Einsatz, über den die
        Anrechnung läuft — der Beleg dafür, dass die Anrechnung tatsächlich entstanden ist."""
        return self._data_row(description).locator("td a[href*='/my/jobs/']").count() > 0
