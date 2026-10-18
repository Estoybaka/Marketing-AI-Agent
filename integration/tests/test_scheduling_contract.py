
import pytest

from integration.scheduling_contract import prepare_scheduling_request


@pytest.fixture
def complete_lead():
    return {
        "lead_id": "lead-test-001",
        "name": "Maya Sharma",
        "email": "maya@example.com",
        "phone": None,
        "need": "Daily care for her father",
    }


def test_complete_ready_lead_produces_handoff_request(complete_lead):
    result = prepare_scheduling_request(
        lead=complete_lead,
        requested_date="2026-10-20",
        requested_time="10:00",
        customer_ready=True,
    )

    assert result["status"] == "ready_for_handoff"
    assert result["missing_fields"] == []
    assert result["request"] == {
        "lead_id": "lead-test-001",
        "name": "Maya Sharma",
        "email": "maya@example.com",
        "phone": None,
        "need": "Daily care for her father",
        "requested_date": "2026-10-20",
        "requested_time": "10:00",
    }


def test_missing_contact_prevents_handoff(complete_lead):
    complete_lead["email"] = None

    result = prepare_scheduling_request(
        lead=complete_lead,
        requested_date="2026-10-20",
        requested_time="10:00",
        customer_ready=True,
    )

    assert result["status"] == "not_ready"
    assert "email_or_phone" in result["missing_fields"]
    assert result["request"] is None


def test_missing_date_and_time_prevent_handoff(complete_lead):
    result = prepare_scheduling_request(
        lead=complete_lead,
        requested_date=None,
        requested_time="",
        customer_ready=True,
    )

    assert result["status"] == "not_ready"
    assert "requested_date" in result["missing_fields"]
    assert "requested_time" in result["missing_fields"]
    assert result["request"] is None


def test_customer_not_ready_prevents_handoff(complete_lead):
    result = prepare_scheduling_request(
        lead=complete_lead,
        requested_date="2026-10-20",
        requested_time="10:00",
        customer_ready=False,
    )

    assert result["status"] == "not_ready"
    assert result["request"] is None


def test_missing_name_or_need_prevents_handoff(complete_lead):
    complete_lead["name"] = " "
    complete_lead["need"] = None

    result = prepare_scheduling_request(
        lead=complete_lead,
        requested_date="2026-10-20",
        requested_time="10:00",
        customer_ready=True,
    )

    assert result["status"] == "not_ready"
    assert "name" in result["missing_fields"]
    assert "need" in result["missing_fields"]
    assert result["request"] is None


def test_invalid_lead_type_is_rejected():
    with pytest.raises(ValueError, match="lead must be a dictionary"):
        prepare_scheduling_request(
            lead=None,
            requested_date="2026-10-20",
            requested_time="10:00",
            customer_ready=True,
        )


def test_handoff_never_claims_booking_confirmation(complete_lead):
    result = prepare_scheduling_request(
        lead=complete_lead,
        requested_date="2026-10-20",
        requested_time="10:00",
        customer_ready=True,
    )

    assert result["status"] == "ready_for_handoff"
    assert "booking_confirmed" not in result
