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
