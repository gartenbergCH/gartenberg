from conftest import shot
from pages.admin_jobs_page import AdminJobsPage
from pages.jobs_page import JobsPage


def test_admin_can_create_recurring_job(admin_page, member_page):
    admin = AdminJobsPage(admin_page)
    admin.navigate_add_recurring_job()
    shot(admin_page, "admin_jobs_01_add_form")

    admin.fill_job_form(slots=5, date="2027-06-01", time="09:00:00")
    admin.save()
    shot(admin_page, "admin_jobs_02_after_save")

    assert admin.was_saved_successfully(), "Admin save should succeed"

    # Confirm the new job is visible in the member-facing job list
    jobs = JobsPage(member_page)
    jobs.navigate()
    shot(member_page, "admin_jobs_03_member_job_list")
    assert member_page.locator("#filter-table tbody tr").count() > 0, \
        "Job list should contain at least one job after admin created one"
