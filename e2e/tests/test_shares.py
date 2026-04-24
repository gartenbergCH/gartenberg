from pages.shares_page import SharesPage


def test_order_additional_share(member_page):
    shares = SharesPage(member_page)
    shares.navigate()

    before = shares.shares_count()
    shares.order_shares(1)
    shares.navigate()  # reload to see updated list

    assert shares.shares_count() == before + 1
