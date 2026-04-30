from playwright.sync_api import Page


class AdminJobsPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate_add_recurring_job(self):
        self.page.goto("/admin/juntagrico/recuringjob/add/")
        self.page.wait_for_load_state("networkidle")

    def fill_job_form(self, slots: int, date: str, time: str):
        # The 'type' field is a Django admin autocomplete (Select2).
        # The underlying <select> is aria-hidden; click the visible Select2 trigger instead.
        self.page.locator(".field-type .select2-selection--single").click()
        first_option = self.page.locator(".select2-results__option:not(.select2-results__option--disabled)").first
        first_option.wait_for(state="visible", timeout=10000)
        first_option.click()
        self.page.locator("input[name='slots']").fill(str(slots))
        self.page.locator("input[name='time_0']").fill(date)
        self.page.locator("input[name='time_1']").fill(time)

    def save(self):
        self.page.get_by_role("button", name="Sichern", exact=True).click()
        self.page.wait_for_load_state("networkidle")

    def was_saved_successfully(self) -> bool:
        return self.page.locator(".success").count() > 0 or "change" in self.page.url

    def list_content(self) -> str:
        """Return page content of the changelist shown after a successful save."""
        return self.page.content()
