from conftest import shot
from pages.config_page import ConfigPage

_EXPECTED_BANK = [
    "CH02 8080 8004 4102 8510 0",
    "Genossenschaft GartenBerg c/o Patrick Uhlmann, Girixweg 40, CH-5000 Aarau",
]

_EXPECTED_ADDRESS = [
    "Genossenschaft GartenBerg",
    "c/o Patrick Uhlmann",
    "Girixweg",
    "40",
    "5000",
    "Aarau",
]


def test_organisation_bank_connection(member_page):
    page = ConfigPage(member_page)
    page.navigate_unpaid_shares()
    shot(member_page, "config_02_unpaid_shares")

    content = page.content()
    for text in _EXPECTED_BANK:
        assert text in content, \
            f"Bankverbindung: '{text}' fehlt auf /my/info/unpaidshares"


def test_organisation_address(admin_page):
    page = ConfigPage(admin_page)
    page.navigate_contact()
    shot(admin_page, "config_01_contact")

    content = page.content()
    for text in _EXPECTED_ADDRESS:
        assert text in content, \
            f"Organisationsadresse: '{text}' fehlt auf /my/contact"
