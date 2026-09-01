from playwright.sync_api import Page


class BillsPage:
    """
    Mitglieder-Sicht auf die eigenen Rechnungen (UC-012).

    Der Menüeintrag wird nur gerendert, wenn BILLS_USERMENU = True gesetzt ist.
    """

    URL = "/jb/user_bills"

    def __init__(self, page: Page):
        self.page = page

    # --- Benutzermenü ---------------------------------------------------

    def navigate_profile(self):
        """Beliebige Mitgliederseite öffnen, auf der das Benutzermenü gerendert wird."""
        self.page.goto("/my/profile")
        self.page.wait_for_load_state("networkidle")

    def menu_entry(self):
        """Der sichtbare Menüeintrag.

        base.html bindet das Menü zweimal ein: einmal für kleine Bildschirme in der
        zugeklappten Navbar (d-md-none) und einmal in der Seitenleiste (d-none d-md-block).
        Ohne ':visible' trifft '.first' den ausgeblendeten Eintrag und jeder Klick läuft
        in einen Timeout.
        """
        return self.page.locator(f".main-menu a[href='{self.URL}']:visible")

    def has_menu_entry(self) -> bool:
        return self.menu_entry().count() > 0

    def menu_entry_text(self) -> str:
        return self.menu_entry().first.inner_text().strip()

    def is_menu_entry_active(self) -> bool:
        classes = self.menu_entry().first.get_attribute("class") or ""
        return "active" in classes.split()

    def click_menu_entry(self):
        self.menu_entry().first.click()
        self.page.wait_for_url(f"**{self.URL}")
        self.page.wait_for_load_state("networkidle")

    # --- Rechnungsliste -------------------------------------------------

    def navigate(self) -> int:
        """Direktaufruf der Rechnungsliste, gibt den HTTP-Status zurück."""
        response = self.page.goto(self.URL)
        self.page.wait_for_load_state("networkidle")
        return response.status

    def heading(self) -> str:
        return self.page.locator("h3").first.inner_text().strip()

    def has_table(self) -> bool:
        return self.page.locator("#filter-table").count() > 0

    def column_headers(self) -> list[str]:
        headers = self.page.locator("#filter-table thead th").all_inner_texts()
        return [h.strip() for h in headers if h.strip()]

    def bill_link(self, bill_id: str):
        return self.page.locator(f"#filter-table tbody a[href='/jb/user_bill/{bill_id}']")

    def lists_bill(self, bill_id: str) -> bool:
        return self.bill_link(bill_id).count() > 0

    def open_bill(self, bill_id: str):
        self.bill_link(bill_id).first.click()
        self.page.wait_for_url(f"**/jb/user_bill/{bill_id}")
        self.page.wait_for_load_state("networkidle")

    # --- Rechnungsdetail ------------------------------------------------

    def shows_payment_slip(self) -> bool:
        """Der Einzahlungsschein wird als eingebettetes SVG ausgeliefert; 'Zahlteil' ist
        die Überschrift des Zahlteils im deutschsprachigen Schweizer QR-Einzahlungsschein."""
        return "Zahlteil" in self.page.content()

    def shows_open_amount(self) -> bool:
        return "Betrag noch offen" in self.page.content()

    def pdf_response(self, bill_id: str):
        """Lädt das Rechnungs-PDF über den Request-Kontext der Seite (gleiche Session).

        Der PDF-Link liefert Content-Disposition: attachment und würde im Browser einen
        Download statt einer Navigation auslösen."""
        return self.page.request.get(f"/jb/user_bill_pdf/{bill_id}")
