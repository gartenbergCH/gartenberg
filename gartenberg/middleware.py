import re

# Mail-Versand-Endpunkte ab juntagrico 2.0 (POST). Die Zähl-Endpunkte
# (.../recipients/count) und die Ergebnisseite (/email/sent) sind bewusst
# nicht enthalten. In 1.7 waren dies /my/mails/send[/depot|/area|/job].
EMAIL_SEND_PATH_RE = re.compile(r'^/email/(write|to/\d+|depot/\d+|area/\d+|job/\d+)/$')


class EmailAuditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Nur echte Sende-Versuche auditieren: die Form trägt den Submit-Button
        # 'submit'. Ein POST mit 'members' ohne 'submit' ist nur ein Vorbefüllen des
        # Formulars (juntagrico.views.email.write behandelt es wie ein GET).
        if (request.method == 'POST'
                and EMAIL_SEND_PATH_RE.match(request.path)
                and 'submit' in request.POST):
            sender = request.POST.get('from_email', '–')
            subject = request.POST.get('subject', '–')
            groups = []
            to_list = request.POST.getlist('to_list')
            if 'all_subscriptions' in to_list:
                groups.append('Abo-BezieherInnen')
            if 'all_shares' in to_list:
                groups.append('Anteilsschein-BesitzerInnen')
            if request.POST.getlist('to_members'):
                groups.append('Einzelne Mitglieder')
            if request.POST.getlist('to_areas'):
                groups.append('Tätigkeitsbereiche')
            if request.POST.getlist('to_jobs'):
                groups.append('Einsätze')
            if request.POST.getlist('to_depots'):
                groups.append('Depots')
            if request.POST.get('copy') == 'on':
                groups.append('Kopie an Absender')
            try:
                from gartenberg.models import EmailAuditLog
                EmailAuditLog.objects.create(
                    sender=sender,
                    subject=subject,
                    recipient_groups=', '.join(groups) or '–',
                    url=request.path,
                )
            except Exception:
                pass
        return self.get_response(request)
