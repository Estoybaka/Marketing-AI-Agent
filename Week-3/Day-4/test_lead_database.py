import sqlite3
from pathlib import Path

from lead_database import (
    initialize_database,
    save_lead,
    get_lead,
    list_leads,
)


TEST_DB_PATH = Path(__file__).resolve().with_name("test_leads.db")


def reset_database():
    """Create the test database and clear its records."""

    initialize_database(TEST_DB_PATH)

    with sqlite3.connect(str(TEST_DB_PATH)) as connection:
        connection.execute("DELETE FROM leads")


def test_database_initializes():
    reset_database()

    assert TEST_DB_PATH.exists()
    assert TEST_DB_PATH.is_file()


def test_new_lead_can_be_saved_and_retrieved():
    reset_database()

    save_lead(
        "conversation-1",
        {
            "name": "Ram Sharma",
            "email": "ram@example.com",
            "need": "Care for elderly mother",
            "urgency": "Medium",
            "source": "Website",
        },
        TEST_DB_PATH,
    )

    lead = get_lead("conversation-1", TEST_DB_PATH)

    assert lead is not None
    assert lead["name"] == "Ram Sharma"
    assert lead["email"] == "ram@example.com"
    assert lead["phone"] is None
    assert lead["need"] == "Care for elderly mother"
    assert lead["urgency"] == "Medium"
    assert lead["source"] == "Website"
    assert lead["status"] == "New"
    assert lead["lead_complete"] is True
    assert lead["next_field"] is None
    assert lead["lead_id"]
    assert lead["created_at"]
    assert lead["updated_at"]


def test_missing_values_do_not_erase_saved_information():
    reset_database()

    save_lead(
        "conversation-1",
        {
            "name": "Ram Sharma",
            "email": "ram@example.com",
            "need": "Care for elderly mother",
        },
        TEST_DB_PATH,
    )

    save_lead(
        "conversation-1",
        {
            "name": None,
            "email": "",
            "phone": None,
            "need": None,
        },
        TEST_DB_PATH,
    )

    lead = get_lead("conversation-1", TEST_DB_PATH)

    assert lead["name"] == "Ram Sharma"
    assert lead["email"] == "ram@example.com"
    assert lead["need"] == "Care for elderly mother"
    assert lead["lead_complete"] is True


def test_existing_email_can_be_corrected():
    reset_database()

    save_lead(
        "conversation-1",
        {
            "name": "Ram Sharma",
            "email": "old@example.com",
            "need": "Care for elderly mother",
        },
        TEST_DB_PATH,
    )

    save_lead(
        "conversation-1",
        {"email": "ram@example.com"},
        TEST_DB_PATH,
    )

    lead = get_lead("conversation-1", TEST_DB_PATH)

    assert lead["email"] == "ram@example.com"
    assert lead["name"] == "Ram Sharma"
    assert lead["need"] == "Care for elderly mother"


def test_phone_can_satisfy_contact_requirement():
    reset_database()

    save_lead(
        "conversation-phone-only",
        {
            "name": "Anita Sharma",
            "phone": "+977 9800000000",
            "need": "Care for elderly father",
        },
        TEST_DB_PATH,
    )

    lead = get_lead("conversation-phone-only", TEST_DB_PATH)

    assert lead is not None
    assert lead["email"] is None
    assert lead["phone"] == "+977 9800000000"
    assert lead["lead_complete"] is True
    assert lead["next_field"] is None


def test_missing_contact_keeps_lead_incomplete():
    reset_database()

    save_lead(
        "conversation-no-contact",
        {
            "name": "Ram Sharma",
            "need": "Care for elderly mother",
        },
        TEST_DB_PATH,
    )

    lead = get_lead("conversation-no-contact", TEST_DB_PATH)

    assert lead is not None
    assert lead["lead_complete"] is False
    assert lead["next_field"] == "email_or_phone"


def test_conversations_have_separate_leads():
    reset_database()

    save_lead(
        "conversation-1",
        {"name": "Ram Sharma", "email": "ram@example.com"},
        TEST_DB_PATH,
    )
    save_lead(
        "conversation-2",
        {"name": "Anita Sharma", "email": "anita@example.com"},
        TEST_DB_PATH,
    )

    first = get_lead("conversation-1", TEST_DB_PATH)
    second = get_lead("conversation-2", TEST_DB_PATH)

    assert first["name"] == "Ram Sharma"
    assert second["name"] == "Anita Sharma"
    assert first["lead_id"] != second["lead_id"]


def test_lead_can_be_found_in_list():
    reset_database()

    save_lead(
        "conversation-1",
        {"name": "Ram Sharma", "email": "ram@example.com"},
        TEST_DB_PATH,
    )

    leads = list_leads(TEST_DB_PATH)

    assert len(leads) == 1
    assert leads[0]["thread_id"] == "conversation-1"
    assert leads[0]["email"] == "ram@example.com"


def test_unknown_conversation_returns_none():
    reset_database()

    assert get_lead("unknown-conversation", TEST_DB_PATH) is None


if __name__ == "__main__":
    tests = [
        test_database_initializes,
        test_new_lead_can_be_saved_and_retrieved,
        test_missing_values_do_not_erase_saved_information,
        test_existing_email_can_be_corrected,
        test_phone_can_satisfy_contact_requirement,
        test_missing_contact_keeps_lead_incomplete,
        test_conversations_have_separate_leads,
        test_lead_can_be_found_in_list,
        test_unknown_conversation_returns_none,
    ]

    print("\nRunning SQLite database tests...\n")

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print(f"\nAll {len(tests)} SQLite database tests passed!")
