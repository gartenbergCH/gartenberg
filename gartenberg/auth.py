def client_ip(request):
    """
    Client-IP für django-axes (AXES_CLIENT_IP_CALLABLE).

    In Produktion steht genau ein nginx vor gunicorn. nginx hängt die IP, von der die Anfrage kommt, hinten an
    X-Forwarded-For an. Nur dieser letzte Eintrag ist vertrauenswürdig, alles davor kann der Client selbst
    mitschicken. Würde man den ersten Eintrag nehmen, könnte ein Angreifer pro Versuch eine andere IP vortäuschen
    und die Sperre umgehen. Ohne Proxy (lokal, Tests) fehlt der Header und REMOTE_ADDR wird verwendet.
    """
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
    last_hop = forwarded_for.rsplit(',', 1)[-1].strip()
    return last_hop or request.META.get('REMOTE_ADDR')
