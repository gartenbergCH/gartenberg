from playwright.sync_api import Page


class AdminMailPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        # 2.0 moved the mail form from /my/mails to /email/write/
        self.page.goto("/email/write/")
        self.page.wait_for_load_state("networkidle")
        # The richtext message field switched from the old MAILER_RICHTEXT setup to
        # djrichtextfield, but djrichtextfield still uses TinyMCE under the hood — wait
        # until TinyMCE has attached an editor to the textarea.
        self.page.wait_for_function(
            "() => typeof tinymce !== 'undefined' && tinymce.activeEditor !== null"
        )

    def send_copy_to_self(self, subject: str, body: str):
        # 2.0 dropped the free "single email address" recipient. Recipients are now
        # members / areas / jobs / depots / lists or a copy to oneself ("Kopie an mich").
        # Use the copy checkbox so the sending admin (test@test.ch) receives the mail.
        self.page.locator("input[name='subject']").fill(subject)
        self.page.evaluate(f"tinymce.activeEditor.setContent('<p>{body}</p>')")
        # push the editor content into the underlying textarea so it is part of the POST
        self.page.evaluate("tinymce.triggerSave()")
        # 'copy' renders as a Bootstrap-4 custom checkbox (input visually hidden) -> force
        self.page.locator("input[name='copy']").check(force=True)
        # The submit button label is replaced by an AJAX recipient count (emailForm.js),
        # so target it by id, not by visible name. Wait for the redirect to /email/sent.
        with self.page.expect_response(
            lambda r: "/email/sent" in r.url and r.request.method == "GET" and r.status == 200
        ):
            self.page.locator("#submit-id-submit").click()
        self.page.wait_for_load_state("networkidle")

    def reached_sent_page(self) -> bool:
        return "/email/sent" in self.page.url
