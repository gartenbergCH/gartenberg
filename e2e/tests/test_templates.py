from contextlib import contextmanager
from urllib.parse import urlparse

from playwright.sync_api import Page, Playwright

from conftest import BASE_URL, shot
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
