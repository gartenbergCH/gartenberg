from contextlib import contextmanager
from urllib.parse import urlparse

from playwright.sync_api import Page, Playwright

from conftest import BASE_URL, shot
from pages.admin_subscription_page import AdminMemberPage
from pages.config_page import ConfigPage

_COOKIE_CONSENT = {
    "name": "cookieconsent_status",
    "value": "dismiss",
    "domain": urlparse(BASE_URL).hostname,
    "path": "/",
}


@contextmanager
def _anon_page(playwright: Playwright) -> Page:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(base_url=BASE_URL)
    context.add_cookies([_COOKIE_CONSENT])
    page = context.new_page()
    try:
        yield page
    finally:
        page.close()
        context.close()
        browser.close()


def test_statistics_template(admin_page):
    # Any page using base.html includes the statistics snippet via
    # SCRIPTS = {'template': 'js/statistics.html'} — use a stable admin page.
    AdminMemberPage(admin_page).navigate()
    shot(admin_page, "template_02_statistics")

    source = admin_page.content()
    assert "statistics.gartenberg.ch" in source, \
        "Plausible-Domain 'statistics.gartenberg.ch' fehlt im HTML (SCRIPTS-Template nicht eingebunden?)"
    assert "script.js" in source, \
        "Plausible-Script-Tag fehlt im HTML"
    assert "pixel.gif" in source, \
        "Plausible-Noscript-Pixel fehlt im HTML"


def test_signup_template(playwright: Playwright):
    with _anon_page(playwright) as anon:
        page = ConfigPage(anon)
        page.navigate_signup()
        shot(anon, "template_01_signup")

        content = page.content()

        # Probe-Mitgliedschaft-Box mit blauem Header
        assert "Probe Mitgliedschaft" in content, \
            "Probe-Mitgliedschaft-Box fehlt im signup-Template"

        # Preise für die drei Probe-Abo-Typen (Fliesstext im Template)
        for price in ["366 CHF", "233 CHF", "162 CHF"]:
            assert price in content, \
                f"Probe-Abo-Preis '{price}' fehlt im signup-Template"

        # Statuten-Link
        assert anon.locator("a[href*='statuten']").count() > 0, \
            "Link zu den Statuten fehlt im signup-Template"

        # Betriebsreglement-Link
        assert anon.locator("a[href*='betriebsreglement']").count() > 0, \
            "Link zum Betriebsreglement fehlt im signup-Template"
