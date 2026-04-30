from conftest import MEMBER_EMAIL, MEMBER_FIRST, MEMBER_LAST, shot
from pages.profile_page import ProfilePage


def test_change_phone_number(member_page):
    profile = ProfilePage(member_page)
    profile.navigate()
    shot(member_page, "profile_01_profile")

    # EX-P01: Name und E-Mail sind als (disabled) Formularfelder im HTML vorhanden
    content = profile.content()
    assert MEMBER_FIRST in content, \
        f"Vorname '{MEMBER_FIRST}' fehlt auf der Profilseite"
    assert MEMBER_LAST in content, \
        f"Nachname '{MEMBER_LAST}' fehlt auf der Profilseite"
    assert MEMBER_EMAIL in content, \
        f"E-Mail '{MEMBER_EMAIL}' fehlt auf der Profilseite"

    new_phone = "079 999 88 77"
    profile.change_phone(new_phone)
    profile.save()
    shot(member_page, "profile_02_after_save")

    profile.assert_success()
    assert profile.get_phone_value() == new_phone

    # EX-P02: Änderung überlebt Seitenreload (Wert ist in der DB gespeichert, nicht nur im DOM)
    profile.navigate()
    shot(member_page, "profile_03_after_reload")
    assert profile.get_phone_value() == new_phone, \
        f"Telefonnummer sollte nach Reload noch '{new_phone}' sein"
