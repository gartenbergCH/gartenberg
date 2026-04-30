from conftest import shot
from pages.depot_page import DepotPage


def test_depot_details(member_page):
    depot = DepotPage(member_page)
    depot.navigate()
    shot(member_page, "depot_01_details")

    assert depot.is_on_depot_page(), \
        f"Should have been redirected to a depot detail page, got: {depot.heading()}"

    heading = depot.heading()
    assert heading.strip(), "Depot heading should not be empty"

    # EX-D01: Die Seite enthält die drei festen Abschnittslabels aus depot.html
    content = depot.content()
    for section in ["Adresse", "Abholung", "Kontaktperson"]:
        assert section in content, \
            f"Pflichtabschnitt '{section}' fehlt auf der Depot-Detailseite"

    # EX-D02: Heading enthält einen konkreten Depot-Namen (nicht nur das Vocabulary-Wort)
    # Das Heading-Template ist: "{% vocabulary 'depot' %} {{ depot.name }}"
    # → mind. zwei Tokens; das zweite ist der eigentliche Name
    heading_parts = heading.strip().split()
    assert len(heading_parts) >= 2, \
        f"Depot-Heading sollte Vocabulary-Wort + Name enthalten, war: '{heading}'"
    depot_name = " ".join(heading_parts[1:])
    assert depot_name.strip(), \
        f"Depot-Name (nach Vocabulary-Wort) sollte nicht leer sein, war: '{heading}'"
