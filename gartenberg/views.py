"""Einsatzliste mit den eingeschriebenen Personen (UC-010).

juntagrico zeigt die Angemeldeten eines Einsatzes nur im Detail dieses einen Einsatzes.
Für die Koordination der Ernteverteilung (Abpacken, Leitung Abpacken, Verteilfahrten) und
der Setzlingsfahrten braucht es den Überblick über mehrere Einsätze hinweg — ohne ihn
werden diese Angaben parallel in Excel geführt.
"""
from django.shortcuts import render
from django.utils import timezone

from juntagrico.entity.jobs import ActivityArea, Job, JobType
from juntagrico.view_decorators import any_permission_required
from juntagrico_assignment_request.models import AssignmentRequest

# Präfixe der Filterwerte im Auswahlfeld. Tätigkeitsbereiche und Einsatzarten teilen sich
# ein einziges Feld (GR-003), deshalb muss der Wert seine Art mittragen.
AREA_SCOPE = 'area'
TYPE_SCOPE = 'type'


def _parse_scope(raw):
    """Zerlegt einen Filterwert 'area:<id>' bzw. 'type:<id>' in (Art, Id).

    Unbrauchbare Werte gelten als "kein Filter". So quittiert weder ein Tippfehler in der
    URL noch ein Lesezeichen auf einen inzwischen gelöschten Bereich die Seite mit einem
    Fehler; die Nutzerin sieht stattdessen wieder alle Einsätze.
    """
    scope, _, raw_id = (raw or '').partition(':')
    if scope in (AREA_SCOPE, TYPE_SCOPE) and raw_id.isdigit():
        return scope, int(raw_id)
    return None, None


def _participants(job):
    """Eingeschriebene Personen eines Einsatzes, je Mitglied genau ein Eintrag.

    Wer mehrere Plätze belegt, hat dafür mehrere Assignments und würde sonst mehrfach
    in der Liste stehen.
    """
    by_member = {}
    for assignment in job.assignment_set.all():
        entry = by_member.setdefault(assignment.member_id, {'member': assignment.member, 'slots': 0})
        entry['slots'] += 1
    return sorted(by_member.values(), key=lambda e: (e['member'].last_name, e['member'].first_name))


def _scope_choices():
    """Auswahl für das Filterfeld: erst die Tätigkeitsbereiche, dann die Einsatzarten.

    Die Einträge stammen aus der Datenbank statt aus einer Liste im Code, damit eine
    umbenannte oder neue Einsatzart die Liste nicht stillschweigend leert (GR-003).
    """
    areas = ActivityArea.objects.order_by('sort_order', 'name')
    job_types = (
        JobType.objects.exclude(name__startswith=AssignmentRequest.JOB_NAME_PREFIX)
        .select_related('activityarea')
        .order_by('activityarea__sort_order', 'name')
    )
    return [
        ('Tätigkeitsbereiche', [
            {'value': f'{AREA_SCOPE}:{area.id}', 'label': area.name}
            for area in areas
        ]),
        ('Einsatzarten', [
            {'value': f'{TYPE_SCOPE}:{job_type.id}',
             'label': f'{job_type.activityarea.name} – {job_type.get_name}'}
            for job_type in job_types
        ]),
    ]


@any_permission_required('juntagrico.view_assignment', 'juntagrico.change_assignment')
def job_participants(request):
    scope, scope_id = _parse_scope(request.GET.get('scope'))

    # Ab Tagesbeginn statt ab "jetzt": ein Einsatz von heute Morgen gehört noch auf die
    # Liste, solange der Tag läuft.
    since = timezone.localtime().replace(hour=0, minute=0, second=0, microsecond=0)
    jobs = (
        Job.objects.filter(time__gte=since)
        # Einsatzmeldungen (juntagrico-assignment-request) erzeugen im Hintergrund je einen
        # Einsatz. Sie sind nicht ausgeschrieben, es meldet sich niemand dafür an — auf der
        # Koordinationsliste wären sie nur Rauschen. juntagrico-assignment-request blendet
        # sie im Django-Admin über dieselbe Beziehung aus.
        .exclude(assignment__assignmentrequest__isnull=False)
        .order_by('time')
        .prefetch_related('assignment_set__member')
    )
    if scope == AREA_SCOPE:
        jobs = jobs.in_areas([scope_id])
    elif scope == TYPE_SCOPE:
        jobs = jobs.filter(RecuringJob___type=scope_id)

    return render(request, 'gartenberg/job_participants.html', {
        'rows': [{'job': job, 'participants': _participants(job)} for job in jobs],
        'scope_choices': _scope_choices(),
        'selected_scope': f'{scope}:{scope_id}' if scope else '',
    })
