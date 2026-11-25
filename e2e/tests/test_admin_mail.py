import requests

from conftest import ADMIN_EMAIL, MAILHOG_URL, shot, wait_for_email
from pages.admin_mail_page import AdminMailPage

_SUBJECT = "E2E Testmail Admin"


def test_admin_can_send_email(admin_page):
    requests.delete(f"{MAILHOG_URL}/api/v1/messages", timeout=5)

    page = AdminMailPage(admin_page)
    page.navigate()
    shot(admin_page, "admin_mail_01_form")

    # 2.0 sends a copy to the sender via "Kopie an mich"; the admin (test@test.ch) is
    # both sender and recipient.
    page.send_copy_to_self(_SUBJECT, "E2E Testinhalt")
    shot(admin_page, "admin_mail_02_result")

    assert page.reached_sent_page(), \
        f"Nach dem Senden sollte die /email/sent Seite erreicht werden, URL war: '{admin_page.url}'"

    email_body = wait_for_email(ADMIN_EMAIL)
    assert "E2E Testinhalt" in email_body, \
        "Nachrichtentext 'E2E Testinhalt' sollte im E-Mail-Body enthalten sein"

    # Regressions-Schutz für den gartenberg-eigenen EmailAuditMiddleware: Der reale
    # juntagrico-Versand muss einen EmailAuditLog-Eintrag erzeugen. Dieser Integrations-
    # check (echtes Formular -> Middleware -> Log) erkennt, wenn juntagrico die Mail-
    # URLs/Feldnamen ändert — was die isolierten Unit-Tests (gartenberg/tests/test_email_audit.py) nicht
    # können, da sie gegen hartkodierte POST-Daten prüfen.
    admin_page.goto("/admin/gartenberg/emailauditlog/")
    admin_page.wait_for_load_state("networkidle")
    shot(admin_page, "admin_mail_03_audit_log")
    assert _SUBJECT in admin_page.content(), \
        "EmailAuditLog sollte den Versand aufzeichnen (EmailAuditMiddleware-Regression?)"


def test_admin_can_send_email_to_subscription_category(admin_page):
    """UC-005 GR-007 / FR-057: Empfängerauswahl nach Abokategorie, protokolliert im Audit-Log."""
    subject = "E2E Testmail Kategorie"
    page = AdminMailPage(admin_page)
    page.navigate()
    assert admin_page.locator("#div_id_to_categories").count() == 1, \
        "Das Feld 'Kategorien' sollte im Rundmail-Formular vorhanden sein"

    page.select_first_category()
    shot(admin_page, "admin_mail_04_category_selected")
    page.send(subject, "E2E Kategorie-Inhalt")

    assert page.reached_sent_page(), \
        f"Nach dem Senden sollte die /email/sent Seite erreicht werden, URL war: '{admin_page.url}'"
    admin_page.goto("/admin/gartenberg/emailauditlog/")
    admin_page.wait_for_load_state("networkidle")
    shot(admin_page, "admin_mail_05_category_audit_log")
    assert "Abo-BezieherInnen nach Abokategorie" in admin_page.content(), \
        "EmailAuditLog sollte die Gruppe 'Abo-BezieherInnen nach Abokategorie' enthalten"
