"""Registriert die GartenBerg-Erweiterungen bei juntagrico.

Wird von juntagrico.util.addons.load_addons() automatisch geladen (autodiscover auf
Modulen namens 'juntagricoapp' in allen installierten Apps).
"""
from juntagrico.util import addons

# Eintrag im Adminmenü für die Einsatz-Teilnehmerliste (UC-010). Der Addon-Hook wird dem
# Überschreiben von juntagrico/menu/admin.html vorgezogen: dieses Template wird bereits
# von juntagrico-billing überschrieben, ein zweites Override wäre von der Reihenfolge in
# INSTALLED_APPS abhängig.
addons.config.register_admin_menu('gartenberg/menu/admin/job_participants.html')
