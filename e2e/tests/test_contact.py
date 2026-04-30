import requests

from conftest import MAILHOG_URL, shot, wait_for_email
from pages.contact_page import ContactPage

_CONTACT_ADDRESS = "info@gartenberg.ch"
_MESSAGE_TEXT = "Dies ist eine automatisierte Testnachricht vom E2E-Test."


def test_send_contact_message(member_page):
    # EX-C01: MailHog-Inbox leeren, damit kein Altbestand die Prüfung verfälscht
    requests.delete(f"{MAILHOG_URL}/api/v1/messages", timeout=5)

    contact = ContactPage(member_page)
    contact.navigate()
    shot(member_page, "contact_01_form")

    # EX-C02: Organisationsadresse ist für Member auf der Kontaktseite sichtbar
    content = contact.content()
    assert "Girixweg" in content, \
        "Strassenname 'Girixweg' fehlt auf der Kontaktseite (als Member)"
    assert "Aarau" in content, \
        "Ort 'Aarau' fehlt auf der Kontaktseite (als Member)"

    contact.send_message(subject="E2E Testanfrage", message=_MESSAGE_TEXT)
    shot(member_page, "contact_02_after_send")

    assert contact.is_sent(), "Success alert should be shown after sending the message"

    # EX-C01: E-Mail ist tatsächlich bei info@gartenberg.ch angekommen
    # formemails.contact() sendet an Config.contacts('general') = "info@gartenberg.ch"
    email_body = wait_for_email(_CONTACT_ADDRESS)
    assert _MESSAGE_TEXT in email_body, \
        f"Nachrichtentext fehlt im empfangenen E-Mail (Empfänger: {_CONTACT_ADDRESS})"
