from playwright.sync_api import Page


class MembershipCancelPage:
    """Gemeinsame Kündigungsseite für Abo, Mitgliedschaft und Anteilscheine (UC-011, seit juntagrico 2.1)."""

    URL = "/my/cancellation"

    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        self.page.goto(self.URL)
        self.page.wait_for_load_state("networkidle")

    def _choose(self, selector: str):
        # Bootstrap-Custom-Radios sind visuell versteckt (wie die Checkboxen im Signup)
        self.page.locator(selector).first.check(force=True)

    def keep_subscriptions(self):
        for radio in self.page.locator("input[name^='primary_subscription_'][value='keep']").all():
            radio.check(force=True)

    def cancel_membership(self):
        self._choose("input[name='membership'][value='False']")

    def keep_account(self):
        # Vorauswahl ist "Mitglied nach der Kündigung löschen"
        self._choose("input[name='account'][value='True']")

    def set_shares_to_cancel(self, count: int):
        # bootstrap-input-spinner ignoriert direkt gesetzte Werte; über die -/+ Knöpfe bedienen
        shares = self.page.locator("input[name='shares']")
        if not shares.count():
            return
        decrement = self.page.locator(".btn-decrement").first
        increment = self.page.locator(".btn-increment").first
        for _ in range(50):
            current = int(shares.input_value() or 0)
            if current == count:
                return
            (decrement if current > count else increment).click()
        raise AssertionError(f"Anteilscheine liessen sich nicht auf {count} stellen")

    def fill_payment_details(self, iban: str):
        # IBAN ist im Formular als required markiert, sonst blockiert der Browser den Submit
        iban_field = self.page.locator("input[name='iban']")
        if not iban_field.input_value():
            iban_field.fill(iban)

    def submit(self):
        self.page.locator("input[type='submit'][name='submit']").click()
        self.page.wait_for_load_state("networkidle")

    def errors(self) -> str:
        return " ".join(self.page.locator(".alert-danger, .invalid-feedback, .errorlist").all_inner_texts())
