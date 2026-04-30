from conftest import shot
from pages.jobs_page import JobDetailPage, JobsPage


def test_register_for_job(member_page):
    jobs = JobsPage(member_page)
    jobs.navigate()
    shot(member_page, "jobs_01_job_list")

    job_name = jobs.first_job_name()
    jobs.click_first_job()
    shot(member_page, "jobs_02_job_detail")

    detail = JobDetailPage(member_page)

    # EX-J01: Job-Detail zeigt Titel, Zeitpunkt und Beschreibung
    assert detail.job_title().strip(), "Job-Titel sollte nicht leer sein"
    content = member_page.content()
    assert "Zeitpunkt" in content, "Zeitpunkt-Abschnitt fehlt auf der Job-Detail-Seite"
    assert "Beschreibung" in content, "Beschreibungs-Abschnitt fehlt auf der Job-Detail-Seite"

    # EX-J02: Belegte Slots steigen nach Anmeldung um 1
    # subscribe() gibt False zurück wenn der Member bereits angemeldet ist
    # (z.B. weil test_admin_jobs.py denselben Job bereits gebucht hat).
    slots_before = detail.occupied_slots()

    subscribed = detail.subscribe()
    shot(member_page, "jobs_03_after_subscribe")

    if subscribed and slots_before >= 0:
        slots_after = detail.occupied_slots()
        assert slots_after == slots_before + 1, \
            f"Belegte Slots sollten nach Anmeldung von {slots_before} auf {slots_before + 1} steigen, war {slots_after}"

    jobs.navigate_member_jobs()
    shot(member_page, "jobs_04_member_jobs")
    assert jobs.job_in_member_list(job_name), \
        f"Job '{job_name}' should appear in member job list after registration"
