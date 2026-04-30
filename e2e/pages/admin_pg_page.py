from playwright.sync_api import Page


class AdminPgPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        self.page.goto("/jpg/home")
        self.page.wait_for_load_state("networkidle")

    def execute_sql(self, sql: str) -> str:
        self.page.locator("input#sql").fill(sql)
        with self.page.expect_response(
            lambda r: "/jpg/sql" in r.url and r.status == 200
        ):
            self.page.locator("input#execute").click()
        return self.page.locator("textarea#textarea_id").input_value()
