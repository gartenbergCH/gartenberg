from conftest import shot
from pages.profile_page import ProfilePage


def test_change_phone_number(member_page):
    profile = ProfilePage(member_page)
    profile.navigate()
    shot(member_page, "profile_01_profile")

    new_phone = "079 999 88 77"
    profile.change_phone(new_phone)
    profile.save()
    shot(member_page, "profile_02_after_save")

    profile.assert_success()
    assert profile.get_phone_value() == new_phone
