from datetime import date

from conftest import shot
from pages.assignment_request_page import AssignmentRequestPage


def test_report_assignment(member_page):
    request_page = AssignmentRequestPage(member_page)
    request_page.navigate()
    shot(member_page, "assignment_request_01_form")

    # Gemeldet wird geleistete Arbeit: das Formular lehnt Daten in der Zukunft ab
    today = date.today().strftime("%Y-%m-%dT00:00")
    request_page.submit_request(
        job_time=today,
        description="E2E Testeinsatz: selbständige Gartenarbeit",
    )
    shot(member_page, "assignment_request_02_after_submit")

    assert request_page.is_submitted_successfully(), \
        "Success alert should be shown after submitting the request"
    assert request_page.has_pending_requests(), \
        "Submitted request should appear in the pending requests table"
