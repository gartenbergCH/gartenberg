from playwright.sync_api import Page


class SignupWizardPage:
    def __init__(self, page: Page):
        self.page = page

    def fill_personal_data(self, email: str):
        self.page.goto("/my/signup/")
        self.page.wait_for_load_state("networkidle")
        self.page.get_by_label("Nachname").fill("WizardTest")
        self.page.get_by_label("Vorname").fill("E2E")
        self.page.get_by_label("Strasse/Nr.").fill("Teststrasse 1")
        self.page.get_by_label("PLZ").fill("5000")
        self.page.get_by_label("Ort").fill("Aarau")
        self.page.get_by_label("Telefonnummer").fill("079 000 00 00")
        self.page.get_by_label("E-Mail-Adresse").fill(email)
        self.page.get_by_label("Geburtstag").fill("01.01.1990")
        self.page.locator("input[name='agb']").check(force=True)
        self.page.get_by_role("button", name="Anmelden").click()
        self.page.wait_for_load_state("networkidle")

    def select_first_subscription_type(self):
        self.page.wait_for_url("**/my/create/subscription/")
        self.page.wait_for_load_state("networkidle")
        self.page.locator(".btn-increment").first.click()
        self.page.get_by_role("button", name="Weiter").click()

    def select_first_depot(self):
        self.page.wait_for_url("**/selectdepot/")
        # index=0 works here: the depot field has no blank option (not null=True)
        self.page.locator("select[name='depot']").select_option(index=0)
        self.page.get_by_role("button", name="Weiter").click()
        self.page.wait_for_url("**/start/")
        self.page.wait_for_load_state("networkidle")

    def is_on_start_date_step(self) -> bool:
        return "/start/" in self.page.url

    def abort(self):
        self.page.goto("/my/create/subscription/cancel/")
        self.page.wait_for_load_state("networkidle")
