import pytest

from lead_database import get_lead, save_lead
from sales_follow_up import prepare_follow_up


def create_test_lead(db_path, thread_id, consent, need="elder care support"):
    lead = {
        "name": "Asha",
        "email": "asha@example.com",
        "phone": None,
        "need": need,
        "when_needed": "next week",
        "urgency": "Medium",
        "source": "Website",
        "status": "New",
        "contact_consent": consent,
        "contact_consent_asked": True,
    }

    save_lead(thread_id, lead, db_path)


def test_missing_lead_is_blocked(tmp_path):
    db_path = tmp_path / "test_leads.db"

    result = prepare_follow_up("unknown-thread", db_path)

    assert result["success"] is False
    assert result["message"] is None
    assert result["reason"] == "Lead not found."


@pytest.mark.parametrize("consent", [None, False])
def test_follow_up_without_consent_is_blocked(tmp_path, consent):
    db_path = tmp_path / "test_leads.db"
    create_test_lead(db_path, "thread-1", consent)

    result = prepare_follow_up("thread-1", db_path)

    assert result["success"] is False
    assert result["message"] is None
    assert "not explicitly agreed" in result["reason"]


def test_incomplete_lead_is_blocked(tmp_path):
    db_path = tmp_path / "test_leads.db"
    create_test_lead(
        db_path,
        "thread-2",
        True,
        need=None,
    )

    result = prepare_follow_up("thread-2", db_path)

    assert result["success"] is False
    assert result["message"] is None
    assert result["reason"] == "Lead information is incomplete."


def test_follow_up_draft_is_prepared_with_consent(tmp_path):
    db_path = tmp_path / "test_leads.db"
    create_test_lead(db_path, "thread-3", True)

    result = prepare_follow_up("thread-3", db_path)

    assert result["success"] is True
    assert result["sent"] is False
    assert result["contact"] == "asha@example.com"
    assert "Hello Asha" in result["message"]
    assert "elder care support" in result["message"]
    assert "has not been sent" in result["reason"]


def test_follow_up_does_not_change_lead_status(tmp_path):
    db_path = tmp_path / "test_leads.db"
    create_test_lead(db_path, "thread-4", True)

    before = get_lead("thread-4", db_path)

    prepare_follow_up("thread-4", db_path)

    after = get_lead("thread-4", db_path)

    assert after["status"] == before["status"]
    assert after["contact_consent"] is True


def test_phone_only_lead_can_receive_follow_up_draft(tmp_path):
    db_path = tmp_path / "test_leads.db"

    save_lead(
        "thread-5",
        {
            "name": "Ravi",
            "email": None,
            "phone": "9800000000",
            "need": "home care support",
            "when_needed": "next week",
            "urgency": "Medium",
            "source": "Website",
            "status": "New",
            "contact_consent": True,
            "contact_consent_asked": True,
        },
        db_path,
    )

    result = prepare_follow_up("thread-5", db_path)

    assert result["success"] is True
    assert result["contact"] == "9800000000"
    assert result["sent"] is False