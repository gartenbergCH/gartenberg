from pages.admin_jobs_page import AdminJobsPage
from pages.jobs_page import JobsPage


def test_admin_can_create_recurring_job(admin_page, member_page):
    admin = AdminJobsPage(admin_page)
    admin.navigate_add_recurring_job()
    admin.fill_job_form(slots=5, date="2027-06-01", time="09:00:00")
    admin.save()

    assert admin.was_saved_successfully(), "Admin save should succeed"

    # Confirm the new job is visible in the member-facing job list
    jobs = JobsPage(member_page)
    jobs.navigate()
    assert member_page.locator("#filter-table tbody tr").count() > 0, \
        "Job list should contain at least one job after admin created one"
