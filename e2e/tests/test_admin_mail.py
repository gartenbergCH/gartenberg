import requests

from conftest import ADMIN_EMAIL, MAILHOG_URL, shot, wait_for_email
from pages.admin_mail_page import AdminMailPage

_SUBJECT = "E2E Testmail Admin"


def test_admin_can_send_email(admin_page):
    requests.delete(f"{MAILHOG_URL}/api/v1/messages", timeout=5)

    page = AdminMailPage(admin_page)
    page.navigate()
    shot(admin_page, "admin_mail_01_form")

    page.send_to_single(ADMIN_EMAIL, _SUBJECT, "E2E Testinhalt")
    shot(admin_page, "admin_mail_02_result")

    assert page.sent_count_from_url() == 1, \
        f"Result-URL sollte 1 gesendete Mail anzeigen, URL war: '{admin_page.url}'"

    email_body = wait_for_email(ADMIN_EMAIL)
    assert "E2E Testinhalt" in email_body, \
        f"Nachrichtentext 'E2E Testinhalt' sollte im E-Mail-Body enthalten sein"
