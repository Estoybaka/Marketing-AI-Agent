import sqlite3
import tempfile
from contextlib import closing
from pathlib import Path

from lead_database import initialize_database, save_lead, get_lead


def main():
    with tempfile.TemporaryDirectory() as temp_dir:
        test_db = Path(temp_dir) / "schema_test.db"

        initialize_database(test_db)

        # Inspect the schema and always close the SQLite connection.
        with closing(sqlite3.connect(test_db)) as connection:
            columns = {
                row[1]
                for row in connection.execute(
                    "PRAGMA table_info(leads)"
                ).fetchall()
            }

        required_columns = {
            "lead_id",
            "thread_id",
            "name",
            "email",
            "phone",
            "need",
            "urgency",
            "source",
            "status",
            "created_at",
            "updated_at",
            "next_field",
            "lead_complete",
        }

        missing = required_columns - columns
        assert not missing, f"Missing columns: {sorted(missing)}"
        print("PASS: Full lead schema exists.")

        save_lead(
            "schema-test-001",
            {
                "name": "Anita",
                "email": "anita@example.com",
                "phone": None,
                "need": "Care for elderly father",
                "urgency": "Medium",
                "source": "Website",
                "status": "New",
            },
            test_db,
        )

        lead = get_lead("schema-test-001", test_db)

        assert lead is not None
        assert lead["name"] == "Anita"
        assert lead["email"] == "anita@example.com"
        assert lead["phone"] is None
        assert lead["need"] == "Care for elderly father"
        assert lead["urgency"] == "Medium"
        assert lead["source"] == "Website"
        assert lead["status"] == "New"
        assert lead["lead_complete"] is True
        assert lead["next_field"] is None
        assert lead["lead_id"]
        print("PASS: Full lead record saves and retrieves correctly.")

        save_lead(
            "schema-test-002",
            {
                "name": "Sarah",
                "email": None,
                "phone": None,
                "need": "Care for grandfather",
            },
            test_db,
        )

        incomplete = get_lead("schema-test-002", test_db)

        assert incomplete["lead_complete"] is False
        assert incomplete["next_field"] == "email_or_phone"
        print("PASS: Missing contact is detected correctly.")

        try:
            save_lead(
                "schema-test-invalid",
                {
                    "name": "Test",
                    "email": "test@example.com",
                    "need": "Care",
                    "urgency": "Urgent",
                },
                test_db,
            )
        except ValueError:
            print("PASS: Invalid urgency is rejected.")
        else:
            raise AssertionError("Invalid urgency was not rejected.")

    # The temporary directory is cleaned up after all connections close.
    print("\nAll full-schema tests passed!")


if __name__ == "__main__":
    main()