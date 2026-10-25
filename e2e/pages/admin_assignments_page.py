from playwright.sync_api import Page


class AdminAssignmentsPage:
    """Einsatzübersicht der Verwaltung mit "E-Mails unter 100 % kopieren" (UC-013)."""

    URL = "/manage/assignments"
    # Spalte "Arbeitseinsätze Status" im juntagrico-Template
    PROGRESS_COLUMN = 5

    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        # Die Zwischenablage ist nur in einem "secure context" (HTTPS/localhost) verfügbar,
        # E2E läuft über http://juntagrico:8000. Deshalb writeText abfangen und merken.
        self.page.add_init_script(
            "Object.defineProperty(navigator, 'clipboard', {value: {"
            "writeText: text => { window.__copied = text; return Promise.resolve() }"
            "}})"
        )
        self.page.goto(self.URL)
        self.page.wait_for_load_state("networkidle")
        self.page.locator("#filter-table tbody tr:has(td:nth-child(2))").first.wait_for(
            state="visible", timeout=10000
        )

    def copy_button(self):
        return self.page.locator(".copy-incomplete-emails")

    def copy_incomplete_emails(self) -> set[str]:
        self.page.evaluate("window.__copied = null")
        self.copy_button().click()
        self.page.wait_for_function("window.__copied !== null")
        return set(self.page.evaluate("window.__copied").split("\n"))

    def show_co_members(self):
        # Bootstrap-Switch: das <input> ist versteckt, das Label lässt sich klicken
        self.page.locator("label[for='show_co_members']").click()

    def search(self, text: str):
        self.page.locator("#filter-table_wrapper input[type='search']").fill(text)

    def rows(self) -> list[tuple[set[str], float]]:
        """Je Abo die angezeigten E-Mail-Adressen (Spalte BezieherInnen) und den Status in %."""
        result = []
        for row in self.page.locator("#filter-table tbody tr:has(td:nth-child(2))").all():
            emails = {e.strip() for e in row.locator("td").first.locator(".email").all_inner_texts()}
            progress = row.locator("td").nth(self.PROGRESS_COLUMN).inner_text().strip()
            result.append((emails, float(progress.rstrip("%").replace(",", "."))))
        return result
