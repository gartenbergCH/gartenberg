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

    assert shares.shares_count() == before + 1
