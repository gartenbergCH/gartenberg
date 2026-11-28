from conftest import shot
from pages.membership_cancel_page import MembershipCancelPage


def test_mitgliedschaft_nicht_kuendbar_solange_behaltenes_abo_sie_erfordert(member_page):
    # UC-011 A1 / GR-003: Das E2E-Mitglied hat ein künftiges Abo (Start 2027-01-01) mit einem
    # regulären Abo-Typ, der eine Mitgliedschaft erfordert. Wer die Mitgliedschaft kündigt und
    # das Abo behält, wird zurückgewiesen; es wird nichts gekündigt.
    cancel = MembershipCancelPage(member_page)
    cancel.navigate()
    shot(member_page, "membership_cancel_01_page")

    cancel.keep_subscriptions()
    cancel.cancel_membership()
    cancel.set_shares_to_cancel(0)
    cancel.keep_account()
    # Offizielle Beispiel-IBAN; wird nicht gespeichert, weil die Kündigung abgewiesen wird
    cancel.fill_payment_details("CH9300762011623852957")
    shot(member_page, "membership_cancel_02_filled")
    cancel.submit()
    shot(member_page, "membership_cancel_03_rejected")

    assert member_page.url.rstrip("/").endswith(MembershipCancelPage.URL), \
        f"Kündigung hätte abgewiesen werden müssen, gelandet auf {member_page.url}"
    assert "benötigt" in cancel.errors(), \
        f"Hinweis, dass die Mitgliedschaft noch für das Abo benötigt wird, fehlt: '{cancel.errors()}'"

    # Fehlerfall-Nachbedingung: Mitgliedschaft bleibt ungekündigt
    member_page.goto("/my/profile")
    member_page.wait_for_load_state("networkidle")
    status = member_page.locator(".membership-status").inner_text()
    assert "gekündigt" not in status.lower(), f"Mitgliedschaft darf nicht gekündigt sein: '{status}'"
