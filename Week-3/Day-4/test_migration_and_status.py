import sqlite3
from contextlib import closing

from lead_database import initialize_database, save_lead, get_lead


def test_legacy_migration(tmp_path):
    """Verify that an old database migrates to the new lead schema."""

    database_path = tmp_path / "migration_test.db"

    # Create a database using the old schema.
    with closing(sqlite3.connect(database_path)) as connection:
        connection.execute(
            """
            CREATE TABLE leads (
                thread_id TEXT PRIMARY KEY,
                name TEXT,
                contact TEXT,
                need TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        connection.execute(
            """
            INSERT INTO leads (thread_id, name, contact, need)
            VALUES (?, ?, ?, ?)
            """,
            (
                "legacy-001",
                "Ram Sharma",
                "ram@example.com",
                "Care for elderly mother",
            ),
        )
        connection.commit()

    # Upgrade the old schema.
    initialize_database(database_path)

    migrated = get_lead("legacy-001", database_path)

    assert migrated is not None, "Legacy lead was lost."
    assert migrated["name"] == "Ram Sharma"
    assert migrated["email"] == "ram@example.com"
    assert migrated["phone"] is None
    assert migrated["need"] == "Care for elderly mother"
    assert migrated["lead_complete"] is True
    assert migrated["next_field"] is None
    assert migrated["lead_id"], "Migration did not assign a lead_id."
    assert migrated["created_at"] != "CURRENT_TIMESTAMP"
    assert migrated["updated_at"] != "CURRENT_TIMESTAMP"

    print("PASS: Legacy contact record migrated successfully.")
    print("PASS: Migrated timestamps and completion fields are valid.")


def test_status_preservation(tmp_path):
    """Verify that updating a lead does not reset its status."""

    database_path = tmp_path / "status_test.db"
    initialize_database(database_path)

    save_lead(
        "status-test-001",
        {
            "name": "Anita",
            "email": "anita@example.com",
            "need": "Care for elderly father",
            "status": "Qualified",
        },
        database_path,
    )

    first = get_lead("status-test-001", database_path)
    assert first["status"] == "Qualified"

    # Update the care need without supplying a new status.
    save_lead(
        "status-test-001",
        {
            "need": "Daily care for elderly father",
        },
        database_path,
    )

    updated = get_lead("status-test-001", database_path)

    assert updated["need"] == "Daily care for elderly father"
    assert updated["name"] == "Anita"
    assert updated["email"] == "anita@example.com"
    assert updated["status"] == "Qualified"

    print("PASS: Existing lead details are preserved on update.")
    print("PASS: Qualified status remains Qualified.")


if __name__ == "__main__":
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = __import__("pathlib").Path(temp_dir)

        test_legacy_migration(temp_path)
        test_status_preservation(temp_path)

    print("\nAll migration and status tests passed!")
