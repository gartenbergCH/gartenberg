from playwright.sync_api import Page


class AdminJobsPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate_add_recurring_job(self):
        self.page.goto("/admin/juntagrico/recuringjob/add/")
        self.page.wait_for_load_state("networkidle")

    def fill_job_form(self, slots: int, date: str, time: str):
        self.page.locator("select[name='type']").select_option(index=0)
        self.page.locator("input[name='slots']").fill(str(slots))
        self.page.locator("input[name='time_0']").fill(date)
        self.page.locator("input[name='time_1']").fill(time)

    def save(self):
        self.page.get_by_role("button", name="Sichern").click()
        self.page.wait_for_load_state("networkidle")

    def was_saved_successfully(self) -> bool:
        return self.page.locator(".success").count() > 0 or "change" in self.page.url
