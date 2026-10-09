import tempfile
from pathlib import Path
from unittest.mock import patch

import lead_graph
from lead_database import get_lead


def test_conversation_collects_required_fields():
    with tempfile.TemporaryDirectory() as temp_dir:
        test_db = Path(temp_dir) / "graph_test.db"
        thread_id = "offline-schema-test-001"

        # Simulate Gemini extraction without making an API call.
        simulated_extractions = [
            {
                "name": "Ram Sharma",
                "email": None,
                "phone": None,
                "need": None,
                "urgency": None,
                "source": None,
            },
            {
                "name": None,
                "email": "ram@example.com",
                "phone": None,
                "need": None,
                "urgency": "Medium",
                "source": "Website",
            },
            {
                "name": None,
                "email": None,
                "phone": None,
                "need": "Care for elderly mother",
                "urgency": None,
                "source": None,
            },
        ]

        messages = [
            "My name is Ram Sharma.",
            "My email is ram@example.com.",
            "I need care for my elderly mother.",
        ]

        config = {"configurable": {"thread_id": thread_id}}

        with (
            patch.object(lead_graph, "DB_PATH", test_db),
            patch.object(
                lead_graph,
                "extract_information",
                side_effect=simulated_extractions,
            ),
        ):
            results = []

            for message in messages:
                result = lead_graph.graph.invoke(
                    {"user_message": message},
                    config=config,
                )
                results.append(result)

            # Turn 1: name is saved; contact is requested.
            assert results[0]["name"] == "Ram Sharma"
            assert results[0]["next_field"] == "email_or_phone"
            assert results[0]["lead_complete"] is False
            assert results[0]["response"] == (
                "What is your phone number or email address?"
            )

            # Turn 2: email is saved; care need is requested.
            assert results[1]["email"] == "ram@example.com"
            assert results[1]["urgency"] == "Medium"
            assert results[1]["source"] == "Website"
            assert results[1]["next_field"] == "need"
            assert results[1]["lead_complete"] is False

            # Turn 3: all required information is now present.
            final_result = results[2]
            assert final_result["name"] == "Ram Sharma"
            assert final_result["email"] == "ram@example.com"
            assert final_result["phone"] is None
            assert final_result["need"] == "Care for elderly mother"
            assert final_result["next_field"] is None
            assert final_result["lead_complete"] is True
            assert final_result["status"] == "New"
            assert final_result["lead_id"]

            saved = get_lead(thread_id, test_db)
            assert saved is not None
            assert saved["name"] == "Ram Sharma"
            assert saved["email"] == "ram@example.com"
            assert saved["need"] == "Care for elderly mother"
            assert saved["urgency"] == "Medium"
            assert saved["source"] == "Website"
            assert saved["status"] == "New"
            assert saved["lead_complete"] is True

        print("PASS: Conversation asks for missing fields in order.")
        print("PASS: Separate email and phone fields work.")
        print("PASS: Optional urgency and source are saved.")
        print("PASS: Lead becomes complete when required fields exist.")
        print("PASS: Final lead is persisted in SQLite.")


def test_phone_also_completes_contact_requirement():
    with tempfile.TemporaryDirectory() as temp_dir:
        test_db = Path(temp_dir) / "phone_test.db"
        thread_id = "offline-phone-test-001"

        with (
            patch.object(lead_graph, "DB_PATH", test_db),
            patch.object(
                lead_graph,
                "extract_information",
                return_value={
                    "name": "Anita Sharma",
                    "email": None,
                    "phone": "+977 9800000000",
                    "need": "Care for elderly father",
                    "urgency": None,
                    "source": None,
                },
            ),
        ):
            result = lead_graph.graph.invoke(
                {
                    "user_message": (
                        "My name is Anita Sharma. My phone is "
                        "+977 9800000000. I need care for my father."
                    )
                },
                config={
                    "configurable": {
                        "thread_id": thread_id,
                    }
                },
            )

            assert result["email"] is None
            assert result["phone"] == "+977 9800000000"
            assert result["lead_complete"] is True
            assert result["next_field"] is None

        print("PASS: Phone number alone satisfies the contact requirement.")


def main():
    test_conversation_collects_required_fields()
    test_phone_also_completes_contact_requirement()
    print("\nAll offline graph tests passed!")


if __name__ == "__main__":
    main()
