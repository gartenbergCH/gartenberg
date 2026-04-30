from conftest import shot
from pages.admin_jobs_page import AdminJobsPage
from pages.jobs_page import JobDetailPage, JobsPage

_JOB_SLOTS = 5
_JOB_DATE = "2027-06-01"


def test_admin_can_create_recurring_job(admin_page, member_page):
    admin = AdminJobsPage(admin_page)
    admin.navigate_add_recurring_job()
    shot(admin_page, "admin_jobs_01_add_form")

    admin.fill_job_form(slots=_JOB_SLOTS, date=_JOB_DATE, time="09:00:00")
    admin.save()
    shot(admin_page, "admin_jobs_02_after_save")

    assert admin.was_saved_successfully(), "Admin save should succeed"

    # EX-AJ01: Changelist zeigt den erstellten Job mit korrekten Werten
    # "Sichern" leitet auf die Changelist zurück — Change-Formular ist nicht mehr aktiv.
    content = admin.list_content()
    assert str(_JOB_SLOTS) in content, \
        f"Slot-Anzahl '{_JOB_SLOTS}' sollte in der Job-Changelist sichtbar sein"
    assert "2027" in content, \
        "Jahr '2027' des erstellten Jobs sollte in der Job-Changelist sichtbar sein"

    # EX-AJ02: Member findet den Job und kann sich anmelden
    jobs = JobsPage(member_page)
    jobs.navigate()
    shot(member_page, "admin_jobs_03_member_job_list")
    assert member_page.locator("#filter-table tbody tr").count() > 0, \
        "Job list should contain at least one job after admin created one"

    job_name = jobs.first_job_name()
    jobs.click_first_job()
    shot(member_page, "admin_jobs_04_job_detail")

    detail = JobDetailPage(member_page)
    detail.subscribe()
    shot(member_page, "admin_jobs_05_after_subscribe")

    jobs.navigate_member_jobs()
    shot(member_page, "admin_jobs_06_member_jobs")
    assert jobs.job_in_member_list(job_name), \
        f"Job '{job_name}' sollte nach der Anmeldung in der Member-Jobliste erscheinen"
