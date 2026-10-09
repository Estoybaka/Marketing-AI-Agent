import re
import sqlite3
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

import lead_graph
from lead_database import initialize_database, get_lead


TEST_DB_PATH = Path(__file__).resolve().with_name(
    "test_graph_leads.db"
)


def reset_test_database():
    """Initialize the test database and clear existing test records."""

    initialize_database(TEST_DB_PATH)

    with closing(sqlite3.connect(str(TEST_DB_PATH))) as connection:
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

    if "care" in lowered_message:
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


def invoke_graph(thread_id: str, message: str) -> dict:
    """Invoke the real graph using mocked extraction and test storage."""

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
        patch.object(lead_graph, "DB_PATH", TEST_DB_PATH),
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


def test_incomplete_lead_is_saved():
    reset_test_database()

    result = invoke_graph(
        "integration-partial-1",
        "My email is ram@example.com.",
    )

    saved = get_lead(
        "integration-partial-1",
        TEST_DB_PATH,
    )

    assert saved is not None
    assert saved["email"] == "ram@example.com"
    assert saved["phone"] is None
    assert saved["name"] is None
    assert result["next_field"] == "name"
    assert result["lead_complete"] is False


def test_complete_lead_is_saved():
    reset_test_database()

    result = invoke_graph(
        "integration-complete-1",
        (
            "My name is Ram Sharma. My email is ram@example.com. "
            "I need care for my elderly mother."
        ),
    )

    saved = get_lead(
        "integration-complete-1",
        TEST_DB_PATH,
    )

    assert saved is not None
    assert saved["name"] == "Ram Sharma"
    assert saved["email"] == "ram@example.com"
    assert saved["need"] is not None
    assert saved["lead_complete"] is True
    assert saved["next_field"] is None
    assert saved["lead_id"]


def test_corrected_email_is_saved():
    reset_test_database()

    thread_id = "integration-correction-1"

    invoke_graph(
        thread_id,
        (
            "My name is Anita Sharma. My email is "
            "wrong@example.com. I need care for my father."
        ),
    )

    result = invoke_graph(
        thread_id,
        "Correction: my email is anita@example.com.",
    )

    saved = get_lead(thread_id, TEST_DB_PATH)

    assert saved is not None
    assert saved["email"] == "anita@example.com"
    assert saved["name"] == "Anita Sharma"
    assert saved["need"] is not None
    assert saved["lead_complete"] is True


def test_conversations_have_separate_saved_leads():
    reset_test_database()

    invoke_graph(
        "integration-customer-1",
        "My name is Ram Sharma. My email is ram@example.com.",
    )

    invoke_graph(
        "integration-customer-2",
        "My name is Anita Sharma. My email is anita@example.com.",
    )

    first = get_lead(
        "integration-customer-1",
        TEST_DB_PATH,
    )
    second = get_lead(
        "integration-customer-2",
        TEST_DB_PATH,
    )

    assert first is not None
    assert second is not None
    assert first["name"] == "Ram Sharma"
    assert second["name"] == "Anita Sharma"
    assert first["email"] == "ram@example.com"
    assert second["email"] == "anita@example.com"
    assert first["lead_id"] != second["lead_id"]


if __name__ == "__main__":
    tests = [
        test_incomplete_lead_is_saved,
        test_complete_lead_is_saved,
        test_corrected_email_is_saved,
        test_conversations_have_separate_saved_leads,
    ]

    print("\nRunning LangGraph + SQLite integration tests...\n")

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print("\nAll LangGraph + SQLite integration tests passed!")
