import base64
import os
import quopri
import re
import time
import uuid
from pathlib import Path
from urllib.parse import urlparse

import pytest
import requests
from playwright.sync_api import BrowserContext, Page, Playwright

_SCREENSHOT_DIR = Path("/e2e/screenshots")

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000")
MAILHOG_URL = os.environ.get("MAILHOG_URL", "http://localhost:8025")

_COOKIE_CONSENT_COOKIE = {
    "name": "cookieconsent_status",
    "value": "dismiss",
    "domain": urlparse(BASE_URL).hostname,
    "path": "/",
}

ADMIN_EMAIL = "test@test.ch"
ADMIN_PASSWORD = "test"

# Unique per test-run so re-using an old container doesn't cause "email already exists" errors
MEMBER_EMAIL = f"e2e.{uuid.uuid4().hex[:8]}@gartenberg-e2e.local"
MEMBER_FIRST = "E2E"
MEMBER_LAST = "Testperson"


def _decode_body(part: dict) -> str:
    body = part.get("Body", "")
    headers = part.get("Headers", {})
    encoding = headers.get("Content-Transfer-Encoding", [""])[0].lower().strip()
    if encoding == "base64":
        return base64.b64decode(body).decode("utf-8", errors="replace")
    if encoding == "quoted-printable":
        return quopri.decodestring(body.encode()).decode("utf-8", errors="replace")
    return body


def wait_for_email(recipient: str, timeout: int = 60) -> str:
    deadline = time.time() + timeout
    while time.time() < deadline:
        resp = requests.get(f"{MAILHOG_URL}/api/v2/messages", timeout=5)
        resp.raise_for_status()
        for msg in resp.json().get("items", []):
            if any(recipient.lower() in to.lower() for to in msg["Raw"]["To"]):
                # MIME can be null when the email is not multipart
                mime = msg.get("MIME") or {}
                parts = mime.get("Parts") or []
                for part in parts:
                    ct = (part.get("Headers") or {}).get("Content-Type", [""])[0]
                    if "text/plain" in ct:
                        return _decode_body(part)
                if parts:
                    return _decode_body(parts[0])
                # Fallback: plain-text email, body is in Content.Body
                content = msg.get("Content") or {}
                return content.get("Body", "")
        time.sleep(2)
    raise TimeoutError(f"No email for {recipient} found within {timeout}s")


def extract_password(email_body: str) -> str:
    match = re.search(r"Passwort:\s*(\S+)", email_body)
    if not match:
        raise ValueError(f"No password found in email body:\n{email_body[:600]}")
    return match.group(1)


def extract_confirm_path(email_body: str) -> str:
    match = re.search(r"(https?://[^\s]*confirm[^\s]*)", email_body)
    if not match:
        raise ValueError(f"No confirmation URL found in email body:\n{email_body[:600]}")
    url = match.group(1).rstrip(".")
    for prefix in [BASE_URL, "http://juntagrico:8000", "http://localhost:8000", "http://testserver"]:
        if url.startswith(prefix):
            return url[len(prefix):]
    return urlparse(url).path


@pytest.fixture(scope="session")
def admin_context(playwright: Playwright) -> BrowserContext:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(base_url=BASE_URL)
    context.add_cookies([_COOKIE_CONSENT_COOKIE])
    page = context.new_page()
    page.goto("/accounts/login/")
    page.locator("#username").fill(ADMIN_EMAIL)
    page.locator("#password").fill(ADMIN_PASSWORD)
    page.get_by_role("button", name="Anmelden").click()
    page.wait_for_url("**/")
    page.close()
    yield context
    context.close()
    browser.close()


@pytest.fixture(scope="session")
def member_context(playwright: Playwright) -> BrowserContext:
    """Goes through the full signup wizard and returns a logged-in browser context."""
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(base_url=BASE_URL)
    # Pre-accept cookie consent so the banner never blocks interactions
    context.add_cookies([_COOKIE_CONSENT_COOKIE])
    page = context.new_page()

    requests.delete(f"{MAILHOG_URL}/api/v1/messages", timeout=5)

    # Step 1: Personal data
    page.goto("/my/signup/")
    page.get_by_label("Nachname").fill(MEMBER_LAST)
    page.get_by_label("Vorname").fill(MEMBER_FIRST)
    page.get_by_label("Strasse/Nr.").fill("Teststrasse 42")
    page.get_by_label("PLZ").fill("5000")
    page.get_by_label("Ort").fill("Aarau")
    page.get_by_label("Telefonnummer").fill("079 123 99 00")
    page.get_by_label("E-Mail-Adresse").fill(MEMBER_EMAIL)
    page.get_by_label("Geburtstag").fill("15.06.1990")
    # Bootstrap 4 custom checkbox: input is visually hidden (opacity: 0);
    # force=True bypasses actionability checks and directly dispatches the click
    page.locator("input[name='agb']").check(force=True)
    page.get_by_role("button", name="Anmelden").click()
    page.wait_for_load_state("networkidle")

    # If form validation failed, the page stays on /my/signup/ — fail with a clear message
    if "/my/signup/" in page.url:
        errors = page.locator(".alert-danger, .invalid-feedback, .errorlist").all_text_contents()
        raise AssertionError(f"Signup form validation failed. URL: {page.url}\nErrors: {errors}")

    # Step 2: Subscription type
    # bootstrap-input-spinner hides the number input and shows +/- buttons;
    # click the + button once to set the first type's quantity from 0 to 1
    page.wait_for_url("**/my/create/subscription/")
    page.wait_for_load_state("networkidle")
    page.locator(".btn-increment").first.click()
    page.get_by_role("button", name="Weiter").click()

    # Step 3: Depot
    page.wait_for_url("**/selectdepot/")
    page.locator("select[name='depot']").select_option(index=0)
    page.get_by_role("button", name="Weiter").click()

    # Step 4: Start date
    page.wait_for_url("**/start/")
    page.locator("input[name='start_date']").fill("01.01.2027")
    page.get_by_role("button", name="Weiter").click()

    # Step 5: Co-members — skip
    page.wait_for_url("**/addmembers/")
    page.get_by_role("link", name="Überspringen").click()

    # Step 6: Shares — the spinner is pre-set to the required minimum; just continue
    page.wait_for_url("**/shares/")
    page.wait_for_load_state("networkidle")
    page.get_by_role("button", name="Weiter").click()

    # Step 7: Summary — confirm
    page.wait_for_url("**/summary/")
    page.get_by_role("button", name="Verbindlich bestellen").click()
    page.wait_for_url("**/my/welcome**")

    # Retrieve auto-generated password and confirmation link from welcome email
    email_body = wait_for_email(MEMBER_EMAIL)
    password = extract_password(email_body)
    confirm_path = extract_confirm_path(email_body)

    page.goto(confirm_path)
    page.wait_for_url("**/")

    # Login
    page.goto("/accounts/login/")
    page.locator("#username").fill(MEMBER_EMAIL)
    page.locator("#password").fill(password)
    page.get_by_role("button", name="Anmelden").click()
    page.wait_for_url("**/")
    page.close()

    yield context
    context.close()
    browser.close()


@pytest.fixture
def admin_page(admin_context: BrowserContext) -> Page:
    page = admin_context.new_page()
    yield page
    page.close()


@pytest.fixture
def member_page(member_context: BrowserContext) -> Page:
    page = member_context.new_page()
    yield page
    page.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        for fixture_name in ("member_page", "admin_page"):
            page = item.funcargs.get(fixture_name)
            if page is not None:
                try:
                    if not page.is_closed():
                        _SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
                        safe_name = item.nodeid.replace("/", "_").replace("::", "__")
                        page.screenshot(
                            path=str(_SCREENSHOT_DIR / f"FAILED__{safe_name}.png"),
                            full_page=True,
                        )
                except Exception:
                    pass
