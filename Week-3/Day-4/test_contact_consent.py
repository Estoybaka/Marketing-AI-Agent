
import pytest

from lead_database import save_lead, get_lead
from unittest.mock import patch

import lead_graph
from lead_graph import check_missing_fields


def test_customer_consent_can_be_saved_as_true(tmp_path):
    db_path = tmp_path / "leads.db"

    save_lead(
        "thread-1",
        {
            "name": "Alex",
            "email": "alex@example.com",
            "need": "Elderly care",
            "contact_consent": True,
        },
        db_path,
    )

    lead = get_lead("thread-1", db_path)

    assert lead["contact_consent"] is True


def test_customer_declining_consent_can_be_saved(tmp_path):
    db_path = tmp_path / "leads.db"

    save_lead(
        "thread-2",
        {
            "name": "Sam",
            "phone": "9800000000",
            "need": "Home care",
            "contact_consent": False,
        },
        db_path,
    )

    lead = get_lead("thread-2", db_path)

    assert lead["contact_consent"] is False


def test_omitted_consent_preserves_existing_answer(tmp_path):
    db_path = tmp_path / "leads.db"

    save_lead(
        "thread-3",
        {
            "name": "Jordan",
            "email": "jordan@example.com",
            "need": "Care service",
            "contact_consent": True,
        },
        db_path,
    )

    # Update another field without providing consent.
    save_lead(
        "thread-3",
        {
            "need": "Elderly home care",
        },
        db_path,
    )

    lead = get_lead("thread-3", db_path)

    assert lead["contact_consent"] is True
    assert lead["need"] == "Elderly home care"


def test_invalid_consent_value_is_rejected(tmp_path):
    db_path = tmp_path / "leads.db"

    with pytest.raises(ValueError):
        save_lead(
            "thread-4",
            {
                "name": "Taylor",
                "contact_consent": "yes",
            },
            db_path,
        )


def test_consent_defaults_to_none(tmp_path):
    db_path = tmp_path / "leads.db"

    save_lead(
        "thread-5",
        {
            "name": "Morgan",
            "email": "morgan@example.com",
            "need": "Personal care",
        },
        db_path,
    )

    lead = get_lead("thread-5", db_path)

    assert lead["contact_consent"] is None


def test_consent_question_status_is_saved(tmp_path):
    db_path = tmp_path / "consent_asked.db"

    save_lead(
        "consent-asked-1",
        {
            "name": "Ram Sharma",
            "email": "ram@example.com",
            "need": "Care for elderly mother",
            "contact_consent_asked": True,
        },
        db_path,
    )

    saved = get_lead("consent-asked-1", db_path)

    assert saved is not None
    assert saved["contact_consent_asked"] is True
    assert saved["contact_consent"] is None


def test_consent_question_status_is_preserved_on_update(tmp_path):
    db_path = tmp_path / "consent_asked_update.db"

    save_lead(
        "consent-asked-2",
        {
            "name": "Anita Sharma",
            "email": "anita@example.com",
            "need": "Care for elderly father",
            "contact_consent_asked": True,
        },
        db_path,
    )

    save_lead(
        "consent-asked-2",
        {"urgency": "Medium"},
        db_path,
    )

    saved = get_lead("consent-asked-2", db_path)

    assert saved is not None
    assert saved["contact_consent_asked"] is True



def test_complete_lead_asks_for_contact_consent(tmp_path):
    db_path = tmp_path / "graph_consent.db"

    with (
        patch.object(lead_graph, "DB_PATH", db_path),
        patch.object(
            lead_graph,
            "extract_information",
            return_value={
                "name": "Ram Sharma",
                "email": "ram@example.com",
                "phone": None,
                "need": "Care for elderly mother",
                "when_needed": "next week",
                "need_is_vague": False,
                "need_is_correction": False,
                "urgency": None,
                "source": None,
            },
        ),
    ):
        result = check_missing_fields(
            {"user_message": "My name is Ram Sharma."},
            {"configurable": {"thread_id": "consent-graph-1"}},
        )

    assert result["lead_complete"] is True
    assert result["contact_consent"] is None
    assert result["contact_consent_asked"] is True
    assert "Please reply yes or no" in result["response"]

    saved = get_lead("consent-graph-1", db_path)
    assert saved["contact_consent"] is None
    assert saved["contact_consent_asked"] is True


def test_customer_yes_grants_consent(tmp_path):
    db_path = tmp_path / "graph_yes.db"

    with (
        patch.object(lead_graph, "DB_PATH", db_path),
        patch.object(
            lead_graph,
            "extract_information",
            return_value={
                "name": None,
                "email": None,
                "phone": None,
                "need": None,
                "need_is_vague": False,
                "need_is_correction": False,
                "urgency": None,
                "source": None,
            },
        ),
    ):
        save_lead(
            "consent-graph-2",
            {
                "name": "Ram Sharma",
                "email": "ram@example.com",
                "need": "Care for elderly mother",
                "when_needed": "next week",
                "contact_consent_asked": True,
            },
            db_path,
        )

        result = check_missing_fields(
            {"user_message": "Yes, please."},
            {"configurable": {"thread_id": "consent-graph-2"}},
        )

    assert result["contact_consent"] is True
    assert "agreed" in result["response"].lower()


def test_customer_no_declines_consent(tmp_path):
    db_path = tmp_path / "graph_no.db"

    with (
        patch.object(lead_graph, "DB_PATH", db_path),
        patch.object(
            lead_graph,
            "extract_information",
            return_value={
                "name": None,
                "email": None,
                "phone": None,
                "need": None,
                "need_is_vague": False,
                "need_is_correction": False,
                "urgency": None,
                "source": None,
            },
        ),
    ):
        save_lead(
            "consent-graph-3",
            {
                "name": "Ram Sharma",
                "email": "ram@example.com",
                "need": "Care for elderly mother",
                "when_needed": "next week",
                "contact_consent_asked": True,
            },
            db_path,
        )

        result = check_missing_fields(
            {"user_message": "No, thank you."},
            {"configurable": {"thread_id": "consent-graph-3"}},
        )

    assert result["contact_consent"] is False
    assert "will not" in result["response"].lower()


def test_ambiguous_answer_does_not_grant_consent(tmp_path):
    db_path = tmp_path / "graph_ambiguous.db"

    with (
        patch.object(lead_graph, "DB_PATH", db_path),
        patch.object(
            lead_graph,
            "extract_information",
            return_value={
                "name": None,
                "email": None,
                "phone": None,
                "need": None,
                "need_is_vague": False,
                "need_is_correction": False,
                "urgency": None,
                "source": None,
            },
        ),
    ):
        save_lead(
            "consent-graph-4",
            {
                "name": "Ram Sharma",
                "email": "ram@example.com",
                "need": "Care for elderly mother",
                "when_needed": "next week",
                "contact_consent_asked": True,
            },
            db_path,
        )

        result = check_missing_fields(
            {"user_message": "Maybe later."},
            {"configurable": {"thread_id": "consent-graph-4"}},
        )

    assert result["contact_consent"] is None
    assert result["contact_consent_asked"] is True
    assert "Please reply yes or no" in result["response"]
    
    
def test_customer_can_revoke_previously_granted_consent(tmp_path):
    db_path = tmp_path / "graph_revoke.db"

    with (
        patch.object(lead_graph, "DB_PATH", db_path),
        patch.object(
            lead_graph,
            "extract_information",
            return_value={
                "name": None,
                "email": None,
                "phone": None,
                "need": None,
                "when_needed": None,
                "need_is_vague": False,
                "need_is_correction": False,
                "urgency": None,
                "source": None,
            },
        ),
    ):
        save_lead(
            "consent-graph-5",
            {
                "name": "Ram Sharma",
                "email": "ram@example.com",
                "need": "Care for elderly mother",
                "when_needed": "next week",
                "contact_consent": True,
                "contact_consent_asked": True,
            },
            db_path,
        )

        result = check_missing_fields(
            {"user_message": "No, please don't contact me."},
            {"configurable": {"thread_id": "consent-graph-5"}},
        )

    assert result["contact_consent"] is False
    assert "will not" in result["response"].lower()

    saved = get_lead("consent-graph-5", db_path)
    assert saved["contact_consent"] is False

    print("PASS: Customer can revoke previously granted consent.")    