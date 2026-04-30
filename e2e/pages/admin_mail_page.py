import re

from playwright.sync_api import Page


class AdminMailPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        self.page.goto("/my/mails")
        self.page.wait_for_load_state("networkidle")
        # Wait until TinyMCE has fully initialised and attached an editor to the textarea
        self.page.wait_for_function(
            "() => typeof tinymce !== 'undefined' && tinymce.activeEditor !== null"
        )

    def send_to_single(self, recipient: str, subject: str, body: str):
        # jQuery trigger fires the change-handler that toggles #singleemail visibility;
        # force-checking the Bootstrap-Switch input alone does not dispatch change events
        self.page.evaluate("$('#allsingleemail').prop('checked', true).trigger('change')")
        self.page.locator("input#singleemail").wait_for(state="visible")
        self.page.locator("input#singleemail").fill(recipient)
        self.page.locator("input#subject").fill(subject)
        self.page.evaluate(f"tinymce.activeEditor.setContent('<p>{body}</p>')")
        # The #sendmail click-handler copies TinyMCE content → #textMessage before submit
        with self.page.expect_response(
            lambda r: "/mails/send/result/" in r.url and r.status == 200
        ):
            self.page.locator("#sendmail").click()
        self.page.wait_for_load_state("networkidle")

    def sent_count_from_url(self) -> int:
        m = re.search(r"/result/(\d+)/", self.page.url)
        return int(m.group(1)) if m else 0
