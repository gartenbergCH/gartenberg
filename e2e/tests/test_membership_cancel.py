from conftest import shot
from pages.membership_cancel_page import MembershipCancelPage


def test_membership_cancel_blocked_by_active_subscription(member_page):
    cancel = MembershipCancelPage(member_page)
    cancel.navigate()
    shot(member_page, "membership_cancel_01_page")

    # The E2E member has a future subscription (start 2027-01-01), so
    # cancellation is blocked and the danger alert is shown instead of the form.
    assert not cancel.can_cancel(), \
        "Cancellation should be blocked for a member with an active subscription"
    assert "Abo" in cancel.cancel_blocked_reason(), \
        "Block reason should mention an active subscription or required shares"
