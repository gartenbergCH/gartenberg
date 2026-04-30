from conftest import shot
from pages.jobs_page import JobsPage, JobDetailPage


def test_register_for_job(member_page):
    jobs = JobsPage(member_page)
    jobs.navigate()
    shot(member_page, "jobs_01_job_list")

    job_name = jobs.first_job_name()
    jobs.click_first_job()
    shot(member_page, "jobs_02_job_detail")

    detail = JobDetailPage(member_page)
    detail.subscribe()
    shot(member_page, "jobs_03_after_subscribe")

    jobs.navigate_member_jobs()
    shot(member_page, "jobs_04_member_jobs")
    assert jobs.job_in_member_list(job_name), f"Job '{job_name}' should appear in member job list after registration"
