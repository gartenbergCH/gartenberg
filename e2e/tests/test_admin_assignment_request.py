import uuid
from datetime import date, timedelta

from conftest import shot
from pages.admin_assignment_request_page import AdminAssignmentRequestPage
from pages.assignment_request_page import AssignmentRequestPage

# Im laufenden Geschäftsjahr, damit die beurteilte Anfrage auf der Mitgliederliste
# sichtbar bleibt (dort werden neben offenen nur Anfragen dieser Saison angezeigt).
_JOB_TIME = (date.today() + timedelta(days=3)).strftime("%Y-%m-%dT14:00")


def _report_assignment(member_page, description: str) -> AssignmentRequestPage:
    """Das Mitglied meldet einen selbständig geleisteten Einsatz (UC-003)."""
    page = AssignmentRequestPage(member_page)
    page.navigate()
    page.submit_request(job_time=_JOB_TIME, description=description)
    assert page.is_submitted_successfully(), \
        "Die Meldung des Mitglieds sollte erfolgreich abgesetzt werden"
    return page


def test_approver_confirms_reported_assignment(member_page, admin_page):
    """UC-009: Verantwortliche Person bestätigt eine gemeldete Arbeit; daraus entsteht
    die Anrechnung, und das Mitglied sieht Entscheid samt Rückmeldung."""
    description = f"E2E UC009 Bestaetigung {uuid.uuid4().hex[:8]}"
    response_text = "Danke, der Einsatz wird dir angerechnet."

    member = _report_assignment(member_page, description)
    shot(member_page, "approver_01_member_reported")

    approver = AdminAssignmentRequestPage(admin_page)
    approver.navigate_open_requests()
    shot(admin_page, "approver_02_open_requests")
    assert approver.lists_request(description), \
        "Die Meldung ohne genannte Ansprechperson sollte bei der verantwortlichen Person erscheinen"

    approver.open_response_form(description)
    shot(admin_page, "approver_03_respond_form")
    approver.respond(response_text, "Bestätigen")
    shot(admin_page, "approver_04_after_confirm")

    assert not approver.lists_request(description), \
        "Nach dem Entscheid sollte die Anfrage nicht mehr unter den offenen Anfragen stehen"

    approver.navigate_archive()
    shot(admin_page, "approver_05_archive_confirmed")
    assert approver.status_of(description) == "Bestätigt", \
        f"Im Archiv sollte die Anfrage als 'Bestätigt' geführt werden, war: '{approver.status_of(description)}'"
    # Der Status verlinkt auf den automatisch erzeugten Einsatz -> die Anrechnung ist entstanden
    assert approver.has_assignment_link(description), \
        "Eine bestätigte Anfrage sollte auf den Einsatz verlinken, über den sie angerechnet wird"

    member.navigate()
    shot(member_page, "approver_06_member_sees_confirmation")
    assert member.status_of(description) == "Bestätigt", \
        f"Das Mitglied sollte den Stand 'Bestätigt' sehen, war: '{member.status_of(description)}'"
    assert member.response_shown(description, response_text), \
        "Die Rückmeldung der verantwortlichen Person sollte beim Mitglied sichtbar sein"


def test_approver_rejects_reported_assignment(member_page, admin_page):
    """UC-009 A1: Verantwortliche Person lehnt eine gemeldete Arbeit ab — es entsteht
    keine Anrechnung, das Mitglied sieht die Begründung."""
    description = f"E2E UC009 Ablehnung {uuid.uuid4().hex[:8]}"
    response_text = "Diese Arbeit war nicht abgesprochen."

    member = _report_assignment(member_page, description)

    approver = AdminAssignmentRequestPage(admin_page)
    approver.navigate_open_requests()
    assert approver.lists_request(description), \
        "Die Meldung sollte vor dem Entscheid unter den offenen Anfragen stehen"

    approver.open_response_form(description)
    approver.respond(response_text, "Ablehnen")
    shot(admin_page, "approver_07_after_reject")

    approver.navigate_archive()
    shot(admin_page, "approver_08_archive_rejected")
    assert approver.status_of(description) == "Abgelehnt", \
        f"Im Archiv sollte die Anfrage als 'Abgelehnt' geführt werden, war: '{approver.status_of(description)}'"
    assert not approver.has_assignment_link(description), \
        "Eine abgelehnte Anfrage darf keinen Einsatz verlinken — es entsteht keine Anrechnung"

    member.navigate()
    shot(member_page, "approver_09_member_sees_rejection")
    assert member.status_of(description) == "Abgelehnt", \
        f"Das Mitglied sollte den Stand 'Abgelehnt' sehen, war: '{member.status_of(description)}'"
    assert member.response_shown(description, response_text), \
        "Die Begründung der verantwortlichen Person sollte beim Mitglied sichtbar sein"
