import re

from conftest import MEMBER_EMAIL, MEMBER_FIRST, MEMBER_LAST, shot
from pages.admin_job_participants_page import AdminJobParticipantsPage
from pages.jobs_page import JobDetailPage, JobsPage


def _subscribe_member_to_a_job(member_page) -> str:
    """Meldet das Mitglied am frühesten künftigen Einsatz an, der noch Platz hat.

    Nicht einfach der nächste Einsatz: die Job-Liste enthält auch den automatisch
    erzeugten Einsatz einer Einsatzmeldung (test_admin_assignment_request läuft vorher).
    Der ist mit einem einzigen Platz bereits voll, und die Einsatz-Teilnehmerliste blendet
    ihn bewusst aus. Ebenso kann das Mitglied für einen Einsatz schon angemeldet sein
    (test_admin_jobs). In beiden Fällen liefert subscribe() False — dann der nächste.
    """
    jobs = JobsPage(member_page)
    jobs.navigate()
    for href in jobs.future_job_hrefs():
        member_page.goto(href)
        if JobDetailPage(member_page).subscribe():
            match = re.search(r"/my/jobs/(\d+)", href)
            assert match, f"Job-Detail-URL erwartet, war aber {href}"
            return match.group(1)
    raise AssertionError("Kein künftiger Einsatz mit freiem Platz gefunden")


def test_einsatzliste_zeigt_eingeschriebene_und_filtert(member_page, admin_page):
    job_id = _subscribe_member_to_a_job(member_page)
    shot(member_page, "job_participants_01_member_subscribed")

    liste = AdminJobParticipantsPage(admin_page)
    # Über das Adminmenü statt über die URL: prüft die Registrierung des Menüeintrags mit
    liste.open_from_admin_menu()
    shot(admin_page, "job_participants_02_list")
    assert liste.URL in admin_page.url, "Menüeintrag sollte auf die Einsatzliste führen"
    assert liste.row_count() > 0, "Die Liste sollte künftige Einsätze enthalten"

    # EX-JP01: Der Einsatz steht mit Name und Kontaktangaben der eingeschriebenen Person da
    row = liste.row_text(job_id)
    assert row, f"Einsatz {job_id} sollte auf der Liste stehen"
    assert MEMBER_LAST in row and MEMBER_FIRST in row, \
        f"Name der eingeschriebenen Person sollte in der Zeile stehen: {row}"
    assert MEMBER_EMAIL in row, f"E-Mail-Adresse sollte in der Zeile stehen: {row}"

    # EX-JP02: Einsätze ohne Anmeldungen verschwinden nicht, sondern fallen auf
    assert "noch niemand eingeschrieben" in liste.content(), \
        "Einsätze ohne Anmeldungen sollten mit einem Hinweis statt leer erscheinen"

    area = liste.area_of(job_id)
    job_name = liste.job_name_of(job_id)

    # EX-JP03: Einschränkung auf den Tätigkeitsbereich
    liste.filter_by(area)
    shot(admin_page, "job_participants_03_filter_area")
    assert liste.row_count() > 0, f"Bereich '{area}' sollte künftige Einsätze enthalten"
    assert set(liste.areas()) == {area}, \
        f"Nach dem Filter auf '{area}' sollten nur Einsätze dieses Bereichs erscheinen"
    assert liste.row_text(job_id), f"Einsatz {job_id} sollte im Bereich '{area}' bleiben"

    # EX-JP04: Einschränkung auf eine einzelne Einsatzart
    liste.filter_by(f"{area} – {job_name}")
    shot(admin_page, "job_participants_04_filter_type")
    assert liste.row_count() > 0, f"Einsatzart '{job_name}' sollte künftige Einsätze enthalten"
    assert set(liste.job_names()) == {job_name}, \
        f"Nach dem Filter auf '{job_name}' sollten nur Einsätze dieser Art erscheinen"
    assert liste.row_text(job_id), f"Einsatz {job_id} sollte bei der Einsatzart bleiben"
