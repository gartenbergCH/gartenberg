from conftest import shot
from pages.depot_page import DepotPage


def test_depot_details(member_page):
    depot = DepotPage(member_page)
    depot.navigate()
    shot(member_page, "depot_01_details")

    assert depot.is_on_depot_page(), \
        f"Should have been redirected to a depot detail page, got: {depot.heading()}"
    assert depot.heading(), "Depot heading should not be empty"
