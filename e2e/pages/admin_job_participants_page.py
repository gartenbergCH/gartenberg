from playwright.sync_api import Page


class AdminJobParticipantsPage:
    """Einsatz-Teilnehmerliste (UC-010): künftige Einsätze mit den Eingeschriebenen."""

    URL = "/einsatzliste/"

    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        self.page.goto(self.URL)
        self.page.wait_for_load_state("networkidle")

    def open_from_admin_menu(self):
        """Ruft die Seite über den Adminmenü-Eintrag auf.

        Prüft damit gleichzeitig, dass die Registrierung über den juntagrico-Addon-Hook
        greift — ohne sie wäre die Seite nur über die URL erreichbar.
        """
        self.page.goto("/")
        self.page.wait_for_load_state("networkidle")
        # base.html rendert das Menü zweimal: eingeklappt in der Navbar (d-md-none) und in
        # der Sidebar (d-none d-md-block). Nur der sichtbare Treffer ist anklickbar.
        self.page.locator(".menu-job-participants:visible").first.click()
        self.page.wait_for_load_state("networkidle")

    def filter_by(self, label: str):
        self.page.locator("#scope").select_option(label=label)
        self.page.locator("#job-participants-filter-submit").click()
        self.page.wait_for_load_state("networkidle")

    def _rows(self):
        return self.page.locator("#job-participants-table tbody tr[data-job-id]")

    def row_count(self) -> int:
        return self._rows().count()

    def is_empty(self) -> bool:
        return self.page.locator("#job-participants-empty").count() > 0

    def areas(self) -> list[str]:
        return [text.strip() for text in self.page.locator("#job-participants-table .job-area").all_text_contents()]

    def job_names(self) -> list[str]:
        return [text.strip() for text in self.page.locator("#job-participants-table .job-name").all_text_contents()]

    def row_text(self, job_id: str) -> str:
        row = self.page.locator(f"#job-participants-table tbody tr[data-job-id='{job_id}']")
        if row.count() == 0:
            return ""
        return row.first.inner_text()

    def content(self) -> str:
        return self.page.locator("#job-participants-table").inner_text()

    def area_of(self, job_id: str) -> str:
        return self.page.locator(
            f"#job-participants-table tbody tr[data-job-id='{job_id}'] .job-area"
        ).first.inner_text().strip()

    def job_name_of(self, job_id: str) -> str:
        return self.page.locator(
            f"#job-participants-table tbody tr[data-job-id='{job_id}'] .job-name"
        ).first.inner_text().strip()
