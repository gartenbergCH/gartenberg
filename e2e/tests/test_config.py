from conftest import shot
from pages.config_page import ConfigPage

_EXPECTED_ADDRESS = [
    "Genossenschaft GartenBerg",
    "c/o Patrick Uhlmann",
    "Girixweg",
    "40",
    "5000",
    "Aarau",
]


def test_organisation_address(admin_page):
    page = ConfigPage(admin_page)
    page.navigate_contact()
    shot(admin_page, "config_01_contact")

    content = page.content()
    for text in _EXPECTED_ADDRESS:
        assert text in content, \
            f"Organisationsadresse: '{text}' fehlt auf /my/contact"
