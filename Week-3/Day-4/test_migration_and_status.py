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
    assert migrated["when_needed"] is None
    assert migrated["lead_complete"] is False
    assert migrated["next_field"] == "when_needed"
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
            "when_needed": "next week",
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
    assert updated["when_needed"] == "next week"
    assert updated["name"] == "Anita"
    assert updated["email"] == "anita@example.com"
    assert updated["status"] == "Qualified"

    print("PASS: Existing lead details are preserved on update.")
    print("PASS: Qualified status remains Qualified.")

def test_new_statuses_are_accepted(tmp_path):
    """Verify Contacted is accepted and Booked requires confirmation."""

    database_path = tmp_path / "new_statuses.db"
    initialize_database(database_path)

    save_lead(
        "status-contacted",
        {
            "name": "Test Customer",
            "email": "test@example.com",
            "need": "Care for elderly parent",
            "when_needed": "next week",
            "status": "Contacted",
        },
        database_path,
    )

    saved = get_lead("status-contacted", database_path)
    assert saved["status"] == "Contacted"

    try:
        save_lead(
            "status-booked",
            {
                "name": "Test Customer",
                "email": "test@example.com",
                "need": "Care for elderly parent",
                "when_needed": "next week",
                "status": "Booked",
            },
            database_path,
        )
    except ValueError as error:
        assert "Scheduling Agent confirms" in str(error)
    else:
        raise AssertionError(
            "Booked must require Scheduling Agent confirmation."
        )
    
def test_existing_modern_database_status_migration(tmp_path):
    """Verify that an existing modern database gets the new statuses."""

    database_path = tmp_path / "old_modern_status.db"

    # Create a modern database using the OLD status constraint.
    with closing(sqlite3.connect(database_path)) as connection:
        connection.execute(
            """
            CREATE TABLE leads (
                lead_id TEXT PRIMARY KEY,
                thread_id TEXT NOT NULL UNIQUE,
                name TEXT,
                email TEXT,
                phone TEXT,
                need TEXT,
                when_needed TEXT,
                urgency TEXT CHECK (
                    urgency IS NULL OR
                    urgency IN ('Low', 'Medium', 'High')
                ),
                source TEXT CHECK (
                    source IS NULL OR
                    source IN (
                        'Website', 'Facebook', 'WhatsApp',
                        'Referral', 'Other'
                    )
                ),
                status TEXT NOT NULL DEFAULT 'New' CHECK (
                    status IN (
                        'New', 'Qualified', 'Follow-up',
                        'Converted', 'Lost'
                    )
                ),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                next_field TEXT,
                lead_complete INTEGER NOT NULL DEFAULT 0 CHECK (
                    lead_complete IN (0, 1)
                ),
                contact_consent INTEGER CHECK (
                    contact_consent IS NULL OR contact_consent IN (0, 1)
                ),
                contact_consent_asked INTEGER NOT NULL DEFAULT 0
                    CHECK (contact_consent_asked IN (0, 1))
            )
            """
        )

        connection.execute(
            """
            INSERT INTO leads (
                lead_id, thread_id, name, email, need,
                when_needed, status, contact_consent,
                contact_consent_asked
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "old-001",
                "old-thread-001",
                "Sita",
                "sita@example.com",
                "Care for elderly mother",
                "next week",
                "Qualified",
                1,
                1,
            ),
        )
        connection.commit()

    # Migrate the existing database.
    initialize_database(database_path)

    migrated = get_lead("old-thread-001", database_path)

    assert migrated is not None
    assert migrated["lead_id"] == "old-001"
    assert migrated["name"] == "Sita"
    assert migrated["email"] == "sita@example.com"
    assert migrated["need"] == "Care for elderly mother"
    assert migrated["when_needed"] == "next week"
    assert migrated["status"] == "Qualified"
    assert migrated["contact_consent"] is True
    assert migrated["contact_consent_asked"] is True

    # Verify Contacted is accepted through the application.
    save_lead(
            "migrated-contacted",
            {
                "name": "Test Customer",
                "email": "test@example.com",
                "need": "Care for elderly parent",
                "when_needed": "next week",
                "status": "Contacted",
            },
            database_path,
        )

    saved = get_lead("migrated-contacted", database_path)
    assert saved["status"] == "Contacted"
        
        #Verify the database constraint accepts Booked as a valid status.
        #Normal application updates still require scheduling confirmation.
    with closing(sqlite3.connect(database_path)) as connection:
            connection.execute(
                """
                
                INSERT INTO leads (
                    lead_id, thread_id, name, status
                )
                VALUES (?, ?, ?, ?) 
              """,
                (
                    "history-booked-001",
                    "history-booked-thread",    
                    "History Customer",
                    "Booked"
                )
            )
            connection.commit()
            
    historical = get_lead("history-booked-thread", database_path)
    assert historical["status"] == "Booked"    

    # Running migration again must not damage existing records.
    initialize_database(database_path)

    final_record = get_lead("old-thread-001", database_path)

    assert final_record["name"] == "Sita"
    assert final_record["status"] == "Qualified"
    assert final_record["contact_consent"] is True

    print("PASS: Existing modern database migrated successfully.")
    print("PASS: Existing lead data and consent were preserved.")
    print("PASS: New statuses work after migration.")
    print("PASS: Repeated migration preserves existing records.")    

def test_valid_status_transitions(tmp_path):
    """Verify that valid status transitions are accepted."""

    database_path = tmp_path / "valid_transitions.db"
    initialize_database(database_path)

    save_lead("transition-001", {"name": "Test Customer"}, database_path)

    save_lead(
        "transition-001",
        {"status": "Contacted"},
        database_path,
    )

    contacted = get_lead("transition-001", database_path)
    assert contacted["status"] == "Contacted"

    save_lead(
        "transition-001",
        {"status": "Qualified"},
        database_path,
    )

    qualified = get_lead("transition-001", database_path)
    assert qualified["status"] == "Qualified"


def test_invalid_status_transition_is_rejected(tmp_path):
    """Verify that booking requires Scheduling Agent confirmation."""

    database_path = tmp_path / "invalid_transitions.db"
    initialize_database(database_path)

    save_lead("transition-002", {"name": "Test Customer"}, database_path)

    try:
        save_lead(
            "transition-002",
            {"status": "Booked"},
            database_path,
        )
    except ValueError as error:
        assert "Scheduling Agent confirms" in str(error)
    else:
        raise AssertionError("New -> Booked should have been rejected.")

    unchanged = get_lead("transition-002", database_path)
    assert unchanged["status"] == "New"

if __name__ == "__main__":
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = __import__("pathlib").Path(temp_dir)

        test_legacy_migration(temp_path)
        test_status_preservation(temp_path)

    print("\nAll migration and status tests passed!")
