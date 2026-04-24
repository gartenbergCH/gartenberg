from playwright.sync_api import Page


class ProfilePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        self.page.goto("/my/profile")
        self.page.wait_for_load_state("networkidle")

    def change_phone(self, new_phone: str):
        self.page.get_by_label("Telefonnummer").fill(new_phone)

    def save(self):
        self.page.get_by_role("button", name="Speichern").click()

    def assert_success(self):
        self.page.get_by_text("Personalien erfolgreich geändert").wait_for()

    def get_phone_value(self) -> str:
        return self.page.get_by_label("Telefonnummer").input_value()
