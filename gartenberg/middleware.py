EMAIL_SEND_PATHS = {
    '/my/mails/send',
    '/my/mails/send/depot',
    '/my/mails/send/area',
    '/my/mails/send/job',
}


class EmailAuditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' and request.path in EMAIL_SEND_PATHS:
            sender = request.POST.get('sender', '–')
            subject = request.POST.get('subject', '–')
            groups = []
            if request.POST.get('allsubscription') == 'on':
                groups.append('Abo-BezieherInnen')
            if request.POST.get('allshares') == 'on':
                groups.append('Anteilsschein-BesitzerInnen')
            if request.POST.get('all') == 'on':
                groups.append('Alle Mitglieder')
            if request.POST.get('allsingleemail') == 'on':
                groups.append('Einzeladressen')
            if request.POST.get('recipients'):
                groups.append('Vorausgefüllte Adressen')
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
