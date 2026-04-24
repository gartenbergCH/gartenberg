from pages.profile_page import ProfilePage


def test_change_phone_number(member_page):
    profile = ProfilePage(member_page)
    profile.navigate()

    new_phone = "079 999 88 77"
    profile.change_phone(new_phone)
    profile.save()

    profile.assert_success()
    assert profile.get_phone_value() == new_phone
