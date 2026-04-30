from conftest import shot
from pages.shares_page import SharesPage


def test_order_additional_share(member_page):
    shares = SharesPage(member_page)
    shares.navigate()
    shot(member_page, "shares_01_before_order")

    before = shares.shares_count()
    shares.order_shares(1)
    shares.navigate()  # reload to see updated list
    shot(member_page, "shares_02_after_order")

    assert shares.shares_count() == before + 1, \
        f"Anteilsschein-Anzahl sollte von {before} auf {before + 1} gestiegen sein"

    # EX-S01: Neu bestellter Anteil hat Status "unbezahlt"
    # state_text = 0 (paid=0, cancelled=0, payback=0) → "unbezahlt"
    status = shares.last_row_status()
    assert "unbezahlt" in status.lower(), \
        f"Neu bestellter Anteil sollte Status 'unbezahlt' haben, war: '{status}'"

    # EX-S02 (angepasst): manage_shares.html zeigt den Preis nicht direkt —
    # "750" ist nur auf /my/signup/ sichtbar (TC-S03 in test_config.py abgedeckt).
    # Stattdessen: Die drei Pflicht-Abschnitte der Seite sind vorhanden.
    content = shares.content()
    for section in ["Bescheinigung", "Übersicht", "bestellen"]:
        assert section.lower() in content.lower(), \
            f"Pflichtabschnitt '{section}' fehlt auf der Anteilsschein-Verwaltungsseite"
