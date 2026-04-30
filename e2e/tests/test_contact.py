from conftest import shot
from pages.contact_page import ContactPage


def test_send_contact_message(member_page):
    contact = ContactPage(member_page)
    contact.navigate()
    shot(member_page, "contact_01_form")

    contact.send_message(
        subject="E2E Testanfrage",
        message="Dies ist eine automatisierte Testnachricht vom E2E-Test.",
    )
    shot(member_page, "contact_02_after_send")

    assert contact.is_sent(), "Success alert should be shown after sending the message"
