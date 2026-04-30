from urllib.parse import urlparse

from playwright.sync_api import Playwright

from conftest import BASE_URL, shot
from pages.config_page import ConfigPage

_COOKIE_CONSENT = {
    "name": "cookieconsent_status",
    "value": "dismiss",
    "domain": urlparse(BASE_URL).hostname,
    "path": "/",
}

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


def test_share_price(playwright: Playwright):
    # SignupView calls logout() for authenticated users, so never use a shared
    # admin/member context here — create a one-off anonymous page instead.
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(base_url=BASE_URL)
    context.add_cookies([_COOKIE_CONSENT])
    anon_page = context.new_page()
    try:
        page = ConfigPage(anon_page)
        page.navigate_signup()
        shot(anon_page, "config_03_signup_share_price")
        assert "750" in page.content(), \
            "Anteilsscheinpreis '750' (CHF) fehlt auf /my/signup/"
    finally:
        anon_page.close()
        context.close()
        browser.close()


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
