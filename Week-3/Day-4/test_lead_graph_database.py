import re
import sqlite3
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

import lead_graph
from lead_database import initialize_database, get_lead


def reset_test_database(db_path: Path) -> None:
    """Initialize an isolated test database and clear its records."""

    initialize_database(db_path)

    with closing(sqlite3.connect(str(db_path))) as connection:
        with connection:
            connection.execute("DELETE FROM leads")


def fake_extract_information(message: str) -> dict:
    """
    Provide predictable information extraction for tests.
    This function does not call Gemini.
    """

    result = {
        "name": None,
        "email": None,
        "phone": None,
        "need": None,
        "need_is_correction": False,
        "need_is_vague": False,
        "urgency": None,
        "source": None,
    }

    name_match = re.search(
        r"\bmy name is ([A-Za-z]+(?:\s+[A-Za-z]+)*)",
        message,
        re.IGNORECASE,
    )
    if name_match:
        result["name"] = name_match.group(1).strip()

    email_match = re.search(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        message,
        re.IGNORECASE,
    )
    if email_match:
        result["email"] = email_match.group(0)

    phone_match = re.search(
        r"\b(?:\+?\d[\d ()-]{7,}\d)\b",
        message,
    )
    if phone_match:
        result["phone"] = phone_match.group(0).strip()

    lowered_message = message.lower()

    vague_phrases = (
        "some help for my mom",
        "some help for my mother",
        "some help for my dad",
        "some help for my father",
        "book a service",
    )

    if any(phrase in lowered_message for phrase in vague_phrases):
        result["need_is_vague"] = True
    elif "care" in lowered_message:
        result["need"] = message.strip()

    if "urgency is high" in lowered_message:
        result["urgency"] = "High"
    elif "urgency is medium" in lowered_message:
        result["urgency"] = "Medium"
    elif "urgency is low" in lowered_message:
        result["urgency"] = "Low"

    if "website" in lowered_message:
        result["source"] = "Website"
    elif "facebook" in lowered_message:
        result["source"] = "Facebook"
    elif "whatsapp" in lowered_message:
        result["source"] = "WhatsApp"
    elif "referral" in lowered_message:
        result["source"] = "Referral"

    return result


def invoke_graph(
    thread_id: str,
    message: str,
    db_path: Path,
) -> dict:
    """Invoke the real graph using mocked extraction and isolated storage."""

    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    initial_state = {
        "name": None,
        "email": None,
        "phone": None,
        "need": None,
        "urgency": None,
        "source": None,
        "status": None,
        "lead_id": None,
        "user_message": message,
        "next_field": None,
        "lead_complete": False,
        "response": "",
        "changed_fields": [],
    }

    with (
        patch.object(lead_graph, "DB_PATH", db_path),
        patch.object(
            lead_graph,
            "extract_information",
            side_effect=fake_extract_information,
        ),
    ):
        return lead_graph.graph.invoke(
            initial_state,
            config=config,
        )


def test_incomplete_lead_is_saved(tmp_path):
    db_path = tmp_path / "test_graph_leads.db"
    reset_test_database(db_path)

    result = invoke_graph(
        "integration-partial-1",
        "My email is ram@example.com.",
        db_path,
    )

    saved = get_lead("integration-partial-1", db_path)

    assert saved is not None
    assert saved["email"] == "ram@example.com"
    assert saved["phone"] is None
    assert saved["name"] is None
    assert result["next_field"] == "name"
    assert result["lead_complete"] is False


def test_complete_lead_is_saved(tmp_path):
    db_path = tmp_path / "test_graph_leads.db"
    reset_test_database(db_path)

    result = invoke_graph(
        "integration-complete-1",
        (
            "My name is Ram Sharma. My email is ram@example.com. "
            "I need care for my elderly mother."
        ),
        db_path,
    )

    saved = get_lead("integration-complete-1", db_path)

    assert saved is not None
    assert saved["name"] == "Ram Sharma"
    assert saved["email"] == "ram@example.com"
    assert saved["need"] is not None
    assert saved["lead_complete"] is True
    assert saved["next_field"] is None
    assert saved["lead_id"]


def test_corrected_email_is_saved(tmp_path):
    db_path = tmp_path / "test_graph_leads.db"
    reset_test_database(db_path)

    thread_id = "integration-correction-1"

    invoke_graph(
        thread_id,
        (
            "My name is Anita Sharma. My email is "
            "wrong@example.com. I need care for my father."
        ),
        db_path,
    )

    result = invoke_graph(
        thread_id,
        "Correction: my email is anita@example.com.",
        db_path,
    )

    saved = get_lead(thread_id, db_path)

    assert saved is not None
    assert saved["email"] == "anita@example.com"
    assert saved["name"] == "Anita Sharma"
    assert saved["need"] is not None
    assert saved["lead_complete"] is True


def test_conversations_have_separate_saved_leads(tmp_path):
    db_path = tmp_path / "test_graph_leads.db"
    reset_test_database(db_path)

    invoke_graph(
        "integration-customer-1",
        "My name is Ram Sharma. My email is ram@example.com.",
        db_path,
    )

    invoke_graph(
        "integration-customer-2",
        "My name is Anita Sharma. My email is anita@example.com.",
        db_path,
    )

    first = get_lead("integration-customer-1", db_path)
    second = get_lead("integration-customer-2", db_path)

    assert first is not None
    assert second is not None
    assert first["name"] == "Ram Sharma"
    assert second["name"] == "Anita Sharma"
    assert first["email"] == "ram@example.com"
    assert second["email"] == "anita@example.com"
    assert first["lead_id"] != second["lead_id"]


def test_vague_request_asks_for_clarification_without_guessing_need(
    tmp_path,
):
    db_path = tmp_path / "test_graph_leads.db"
    reset_test_database(db_path)

    thread_id = "vague-request-mom-1"

    result = invoke_graph(
        thread_id,
        "I need some help for my mom.",
        db_path,
    )

    saved = get_lead(thread_id, db_path)

    assert saved is not None
    assert saved["need"] is None
    assert result["response"]
    assert "what kind of care or help do you need" in (
        result["response"].lower()
    )
    assert "personal care" in result["response"].lower()
    assert "your mom need" not in result["response"].lower()


def test_generic_booking_request_does_not_assume_family_member(
    tmp_path,
):
    db_path = tmp_path / "test_graph_leads.db"
    reset_test_database(db_path)

    thread_id = "vague-booking-request-1"

    result = invoke_graph(
        thread_id,
        "I want to book a service.",
        db_path,
    )

    saved = get_lead(thread_id, db_path)

    assert saved is not None
    assert saved["need"] is None
    assert result["response"]
    assert "what kind of care or help do you need" in (
        result["response"].lower()
    )
    assert "mom" not in result["response"].lower()
    assert "father" not in result["response"].lower()


def test_update_lead_preserves_additional_care_needs():
    lead = {
        "name": "Ram Sharma",
        "email": "ram@example.com",
        "phone": None,
        "need": "Care for elderly mother",
        "urgency": None,
        "source": None,
    }

    lead_graph.update_lead(
        lead,
        {"need": "Help with medication reminders"},
    )

    assert "Care for elderly mother" in lead["need"]
    assert "Help with medication reminders" in lead["need"]

    updated_need = lead["need"]

    lead_graph.update_lead(
        lead,
        {"need": "Help with medication reminders"},
    )

    assert lead["need"] == updated_need


def test_update_lead_replaces_care_need_when_explicitly_corrected():
    lead = {
        "name": "Ram Sharma",
        "email": "ram@example.com",
        "phone": None,
        "need": "Overnight care for elderly mother",
        "urgency": None,
        "source": None,
    }

    lead_graph.update_lead(
        lead,
        {
            "need": "Daytime care for elderly mother",
            "need_is_correction": True,
        },
    )

    assert lead["need"] == "Daytime care for elderly mother"
    assert "Overnight care" not in lead["need"]
