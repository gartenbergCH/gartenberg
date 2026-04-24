from pathlib import Path

from pages.jobs_page import JobsPage, JobDetailPage

_SHOT_DIR = Path("/e2e/screenshots")


def _shot(page, name: str) -> None:
    _SHOT_DIR.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(_SHOT_DIR / f"{name}.png"), full_page=True)


def test_register_for_job(member_page):
    jobs = JobsPage(member_page)
    jobs.navigate()
    _shot(member_page, "jobs_01_job_list")

    job_name = jobs.first_job_name()
    jobs.click_first_job()
    _shot(member_page, "jobs_02_job_detail")

    detail = JobDetailPage(member_page)
    detail.subscribe()
    _shot(member_page, "jobs_03_after_subscribe")

    jobs.navigate_member_jobs()
    _shot(member_page, "jobs_04_member_jobs")
    assert jobs.job_in_member_list(job_name), f"Job '{job_name}' should appear in member job list after registration"
