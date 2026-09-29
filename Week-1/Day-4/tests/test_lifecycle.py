from src.lifecycle.transitions import is_transition_allowed


def test_new_can_become_contacted():
    assert is_transition_allowed(
        "new",
        "contacted",
    )


def test_new_can_become_consultation_requested():
    assert is_transition_allowed(
        "new",
        "consultation_requested",
    )


def test_new_cannot_become_booked_directly():
    assert not is_transition_allowed(
        "new",
        "booked",
    )


def test_consultation_requested_can_become_booked():
    assert is_transition_allowed(
        "consultation_requested",
        "booked",
    )


def test_unknown_status_cannot_transition():
    assert not is_transition_allowed(
        "unknown",
        "contacted",
    )