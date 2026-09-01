from datetime import date

from playwright.sync_api import Page


class AdminBillingPage:
    def __init__(self, page: Page):
        self.page = page

    # ------------------------------------------------------------------ Navigation

    def navigate_pending_bills(self):
        self.page.goto("/jb/pending_bills")
        self.page.wait_for_load_state("networkidle")

    def navigate_unpublished_bills(self):
        self.page.goto("/jb/unpublished_bills")
        self.page.wait_for_load_state("networkidle")

    def navigate_open_bills(self):
        self.page.goto("/jb/open_bills")
        self.page.wait_for_load_state("networkidle")

    def heading(self) -> str:
        return self.page.locator("h3").first.inner_text().strip()

    def has_year_selector(self) -> bool:
        return self.page.locator("select#year").count() > 0

    def has_table(self) -> bool:
        return self.page.locator("#filter-table").count() > 0

    # ------------------------------------------------------- Stammdaten (Django-Admin)

    def _admin_save(self):
        # exact=True: der Admin hat mehrere Submit-Buttons, die "Sichern" enthalten
        self.page.get_by_role("button", name="Sichern", exact=True).click()
        self.page.wait_for_load_state("networkidle")

    def _changelist_rows(self, model_path: str) -> int:
        self.page.goto(f"/admin/{model_path}/")
        self.page.wait_for_load_state("networkidle")
        return self.page.locator("#result_list tbody tr").count()

    def ensure_accounting_settings(self, debtor_account: str = "1100", vat_percent: str = "0"):
        """Ohne den Buchhaltungs-Einstellungs-Singleton bricht die Rechnungserzeugung mit
        HTTP 500 ab: create_bills_for_items() liest den MwSt-Satz über
        Settings.objects.first().

        Setzt eine bestehende Zahlungsart voraus: default_paymenttype und
        balancing_paymenttype sind zwar null=True, aber nicht blank=True und damit im
        Admin-Formular Pflichtfelder."""
        if self._changelist_rows("juntagrico_billing/settings") > 0:
            return
        self.page.goto("/admin/juntagrico_billing/settings/add/")
        self.page.wait_for_load_state("networkidle")
        self.page.locator("input[name='debtor_account']").fill(debtor_account)
        self.page.locator("input[name='vat_percent']").fill(vat_percent)
        # Index 0 ist die Leer-Option des Django-ForeignKey-Selects
        self.page.locator("select[name='default_paymenttype']").select_option(index=1)
        self.page.locator("select[name='balancing_paymenttype']").select_option(index=1)
        self._admin_save()

    def ensure_payment_type(self, name: str, booking_account: str = "1020"):
        if self._changelist_rows("juntagrico_billing/paymenttype") > 0:
            return
        self.page.goto("/admin/juntagrico_billing/paymenttype/add/")
        self.page.wait_for_load_state("networkidle")
        self.page.locator("input[name='name']").fill(name)
        self.page.locator("input[name='booking_account']").fill(booking_account)
        self._admin_save()

    def ensure_business_year(self, name: str, start: str, end: str):
        """start/end im Schweizer Eingabeformat (TT.MM.JJJJ), passend zu DATE_INPUT_FORMATS."""
        if self._changelist_rows("juntagrico_billing/businessyear") > 0:
            return
        self.page.goto("/admin/juntagrico_billing/businessyear/add/")
        self.page.wait_for_load_state("networkidle")
        self.page.locator("input[name='name']").fill(name)
        self.page.locator("input[name='start_date']").fill(start)
        self.page.locator("input[name='end_date']").fill(end)
        self._admin_save()

    # ------------------------------------------------------------------ Rechnungslauf

    def select_year(self, name: str):
        self.page.locator("select#year").select_option(label=name)
        self.page.get_by_role("button", name="Ändern").click()
        self.page.wait_for_load_state("networkidle")

    def row_count(self) -> int:
        """Anzahl echter Datenzeilen.

        Zwei Fallstricke: DataTables rendert das tbody erst nach 'networkidle' neu
        (siehe docs/e2e-reference.md), und bei leerer Tabelle steht dort eine
        Platzhalterzeile ("Keine Daten vorhanden") mit einer einzigen colspan-Zelle.
        Deshalb nur Zeilen mit mehr als einer Zelle zählen."""
        try:
            self.page.locator("#filter-table tbody tr").first.wait_for(
                state="visible", timeout=10000
            )
        except Exception:
            return 0
        return self.page.locator("#filter-table tbody tr:has(td:nth-child(2))").count()

    def generate_all_bills(self):
        # Auf das GET 200 des Redirect-Ziels warten, nicht auf den POST 302
        with self.page.expect_response(
            lambda r: "/jb/unpublished_bills" in r.url and r.request.method == "GET" and r.status == 200
        ):
            self.page.get_by_role("button", name="Alle generieren").click()
        self.page.wait_for_load_state("networkidle")

    def publish_all_bills(self):
        """Der Veröffentlichen-Button ist ein DataTables-Action-Button. Ohne Zeilenauswahl
        wirkt er über get_selected_or_all() auf alle Zeilen der Tabelle."""
        self.page.locator("#filter-table tbody a.bill-id").first.wait_for(
            state="visible", timeout=10000
        )
        with self.page.expect_response(
            lambda r: "/jb/unpublished_bills" in r.url and r.request.method == "GET" and r.status == 200
        ):
            self.page.get_by_role("button", name="Veröffentlichen").click()
        self.page.wait_for_load_state("networkidle")

    def first_bill_id(self) -> str:
        """Rechnungsnummer aus der ersten Tabellenzeile (Link auf das Admin-Change-Formular)."""
        link = self.page.locator(
            "#filter-table tbody a[href*='/admin/juntagrico_billing/bill/']"
        ).first
        link.wait_for(state="visible", timeout=10000)
        # /admin/juntagrico_billing/bill/<id>/change/
        return link.get_attribute("href").rstrip("/").split("/")[-2]

    def first_bill_impersonation_url(self) -> str:
        """Adresse des Impersonate-Links aus derselben Zeile wie first_bill_id().

        Die Mitglieder-Spalte rendert über display_linked.html einen Link zur
        Sitzungsübernahme. Er trägt target="_blank"; statt ihn zu klicken (und einen
        zweiten Tab zu erhalten) wird die Adresse ausgelesen und im selben Tab aufgerufen."""
        link = self.page.locator("#filter-table tbody tr").first.locator("a.impersonate-action")
        link.wait_for(state="attached", timeout=10000)
        return link.get_attribute("href")

    def lists_bill(self, bill_id: str) -> bool:
        return self.page.locator(
            f"#filter-table tbody a[href*='/admin/juntagrico_billing/bill/{bill_id}/']"
        ).count() > 0

    # ------------------------------------------------------------------ Zahlungseingang

    def record_full_payment(self, bill_id: str) -> str:
        """Erfasst über das Payment-Inline des Rechnungsformulars eine Zahlung über den
        vollen Rechnungsbetrag. Gibt den einbezahlten Betrag zurück."""
        self.page.goto(f"/admin/juntagrico_billing/bill/{bill_id}/change/")
        self.page.wait_for_load_state("networkidle")

        amount = self.page.locator("input[name='amount']").input_value()

        # Das Formular hat zwei Inlines (Positionen und Zahlungen) mit gleichnamigen
        # Feldern. 'paid_date' gibt es nur bei den Zahlungen -> daraus das Inline-Präfix
        # der leeren Zusatzzeile ableiten ('__prefix__' ist die Vorlagenzeile).
        paid_date = self.page.locator(
            "input[name$='-paid_date']:not([name*='__prefix__'])"
        ).last
        prefix = paid_date.get_attribute("name").rsplit("-", 1)[0]

        paid_date.fill(date.today().strftime("%d.%m.%Y"))
        # Index 0 ist die Leer-Option des Django-ForeignKey-Selects
        self.page.locator(f"select[name='{prefix}-type']").select_option(index=1)
        self.page.locator(f"input[name='{prefix}-amount']").fill(amount)
        self._admin_save()
        return amount
