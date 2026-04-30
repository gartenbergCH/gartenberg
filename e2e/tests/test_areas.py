from conftest import shot
from pages.areas_page import AreasPage


def test_areas_list_and_detail(member_page):
    areas = AreasPage(member_page)
    areas.navigate()
    shot(member_page, "areas_01_list")

    assert areas.area_count() > 0, "Areas list should contain at least one area"

    area_name = areas.first_area_name()
    areas.click_first_area()
    shot(member_page, "areas_02_detail")

    assert area_name in areas.detail_heading(), \
        f"Area detail heading should contain '{area_name}'"

    # EX-A01: Detail-Seite zeigt Beschreibungs- und Kontaktperson-Abschnitt
    content = areas.content()
    assert "Beschreibung" in content, \
        "Beschreibungs-Abschnitt fehlt auf der Bereich-Detail-Seite"
    assert "Kontaktperson" in content, \
        "Kontaktperson-Abschnitt fehlt auf der Bereich-Detail-Seite"

    # EX-A02: Bereich beitreten und wieder verlassen
    area_id = areas.area_id()
    assert area_id, "Bereich-ID konnte nicht aus der Seite gelesen werden"

    # Sicherstellen, dass der Member noch nicht Mitglied ist (frischer member_context)
    if areas.is_member():
        # Bereits Mitglied — zuerst verlassen, dann erst testen
        areas.leave(area_id)
        shot(member_page, "areas_03_before_join")
        assert not areas.is_member(), \
            "Member sollte nach dem Verlassen nicht mehr Mitglied des Bereichs sein"

    areas.join(area_id)
    shot(member_page, "areas_03_after_join")
    assert areas.is_member(), \
        f"Member sollte nach dem Beitreten Mitglied des Bereichs '{area_name}' sein"

    areas.leave(area_id)
    shot(member_page, "areas_04_after_leave")
    assert not areas.is_member(), \
        f"Member sollte nach dem Verlassen kein Mitglied des Bereichs '{area_name}' mehr sein"
