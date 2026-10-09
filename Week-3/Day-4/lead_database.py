import re
import sqlite3
import uuid
from contextlib import closing
from datetime import datetime
from pathlib import Path
from typing import Optional

DEFAULT_DB_PATH = Path(__file__).resolve().with_name("leads.db")

CONTACT_FIELDS = ("email", "phone")

ALLOWED_URGENCY = {"Low", "Medium", "High"}
ALLOWED_SOURCES = {
    "Website", "Facebook", "WhatsApp", "Referral", "Other"
}
ALLOWED_STATUSES = {
    "New", "Qualified", "Follow-up", "Converted", "Lost"
}

ALL_LEAD_FIELDS = (
    "name", "email", "phone", "need",
    "urgency", "source", "status",
    "next_field", "lead_complete",
)


def normalize_value(value):
    """Trim text and convert empty strings to None."""
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip()
        return value or None
    return value


def calculate_completion(lead):
    """A complete lead needs a name, a need, and email or phone."""
    return (
        bool(normalize_value(lead.get("name")))
        and bool(normalize_value(lead.get("need")))
        and any(
            bool(normalize_value(lead.get(field)))
            for field in CONTACT_FIELDS
        )
    )


def calculate_next_field(lead):
    """Follow the Day 2 priority: name, contact, then need."""
    if not normalize_value(lead.get("name")):
        return "name"

    if not any(
        normalize_value(lead.get(field))
        for field in CONTACT_FIELDS
    ):
        return "email_or_phone"

    if not normalize_value(lead.get("need")):
        return "need"

    return None


def _validate_controlled_value(field, value, allowed_values):
    value = normalize_value(value)
    if value is not None and value not in allowed_values:
        choices = ", ".join(sorted(allowed_values))
        raise ValueError(
            f"Invalid {field}: {value!r}. Allowed values: {choices}"
        )
    return value


def _connect(database_file):
    connection = sqlite3.connect(str(database_file))
    connection.row_factory = sqlite3.Row
    return connection


def _split_legacy_contact(contact):
    """Best-effort conversion from the old combined contact field."""
    contact = normalize_value(contact)
    if not contact:
        return None, None

    if re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", contact):
        return contact, None

    digits = re.sub(r"\D", "", contact)
    if len(digits) >= 7 and re.fullmatch(r"[+\d()\-\s.]+", contact):
        return None, contact

    # Keep ambiguous legacy contact data rather than discard it.
    return contact, None


def _table_exists(connection, table_name):
    return connection.execute(
        """
        SELECT 1 FROM sqlite_master
        WHERE type = 'table' AND name = ?
        """,
        (table_name,),
    ).fetchone() is not None


def _columns(connection, table_name):
    return {
        row["name"]
        for row in connection.execute(
            f"PRAGMA table_info({table_name})"
        ).fetchall()
    }


def _create_leads_table(connection):
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS leads (
            lead_id TEXT PRIMARY KEY,
            thread_id TEXT NOT NULL UNIQUE,
            name TEXT,
            email TEXT,
            phone TEXT,
            need TEXT,
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
            )
        )
        """
    )


def _migrate_legacy_table(connection):
    """Create the schema or migrate the previous combined-contact table."""
    if not _table_exists(connection, "leads"):
        _create_leads_table(connection)
        return

    required_columns = {
        "lead_id", "thread_id", "name", "email", "phone", "need",
        "urgency", "source", "status", "created_at", "updated_at",
        "next_field", "lead_complete",
    }
    columns = _columns(connection, "leads")

    if required_columns.issubset(columns):
        return

    old_rows = connection.execute("SELECT * FROM leads").fetchall()

    connection.execute("ALTER TABLE leads RENAME TO leads_legacy_migration")
    _create_leads_table(connection)

    for row in old_rows:
        old = dict(row)
        thread_id = normalize_value(old.get("thread_id")) or str(uuid.uuid4())

        email = normalize_value(old.get("email"))
        phone = normalize_value(old.get("phone"))

        if not email and not phone:
            email, phone = _split_legacy_contact(old.get("contact"))

        lead = {
            "name": normalize_value(old.get("name")),
            "email": email,
            "phone": phone,
            "need": normalize_value(old.get("need")),
        }

        urgency = old.get("urgency")
        if urgency not in ALLOWED_URGENCY:
            urgency = None

        source = old.get("source")
        if source not in ALLOWED_SOURCES:
            source = None

        status = old.get("status")
        if status not in ALLOWED_STATUSES:
            status = "New"

        now = datetime.now().isoformat(sep=" ", timespec="seconds")
        created_at = normalize_value(old.get("created_at")) or now
        updated_at = normalize_value(old.get("updated_at")) or created_at

        connection.execute(
            """
            INSERT INTO leads (
                lead_id, thread_id, name, email, phone, need,
                urgency, source, status, created_at, updated_at,
                next_field, lead_complete
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                normalize_value(old.get("lead_id")) or str(uuid.uuid4()),
                thread_id,
                lead["name"],
                lead["email"],
                lead["phone"],
                lead["need"],
                urgency,
                source,
                status,
                created_at,
                updated_at,
                calculate_next_field(lead),
                int(calculate_completion(lead)),
            ),
        )

    connection.execute("DROP TABLE leads_legacy_migration")


def initialize_database(db_path: Optional[Path] = None):
    """Initialize the database and migrate the previous schema if needed."""
    database_file = (
        Path(db_path).resolve()
        if db_path is not None
        else DEFAULT_DB_PATH
    )
    database_file.parent.mkdir(parents=True, exist_ok=True)

    with closing(_connect(database_file)) as connection:
        with connection:
            _migrate_legacy_table(connection)


def save_lead(
    thread_id: str,
    lead: dict,
    db_path: Optional[Path] = None,
):
    """Insert or update a lead while preserving saved values on blank input."""
    if not isinstance(thread_id, str) or not thread_id.strip():
        raise ValueError("thread_id must be a non-empty string.")

    database_file = (
        Path(db_path).resolve()
        if db_path is not None
        else DEFAULT_DB_PATH
    )
    initialize_database(database_file)

    values = {
        field: normalize_value(lead.get(field))
        for field in ALL_LEAD_FIELDS
    }

    # Backward compatibility with callers that still send contact.
    if not values["email"] and not values["phone"]:
        values["email"], values["phone"] = _split_legacy_contact(
            lead.get("contact")
        )

    values["urgency"] = _validate_controlled_value(
        "urgency", values["urgency"], ALLOWED_URGENCY
    )
    values["source"] = _validate_controlled_value(
        "source", values["source"], ALLOWED_SOURCES
    )

    # Validate status only when the caller actually supplies it.
    if values["status"] is not None:
        values["status"] = _validate_controlled_value(
            "status", values["status"], ALLOWED_STATUSES
        )

    with closing(_connect(database_file)) as connection:
        with connection:
            existing = connection.execute(
                "SELECT * FROM leads WHERE thread_id = ?",
                (thread_id,),
            ).fetchone()

            if existing is None:
                merged = {
                    field: values[field]
                    for field in (
                        "name", "email", "phone", "need",
                        "urgency", "source",
                    )
                }
                status = values["status"] or "New"
                merged["status"] = status
                merged["lead_complete"] = int(
                    calculate_completion(merged)
                )
                merged["next_field"] = calculate_next_field(merged)

                connection.execute(
                    """
                    INSERT INTO leads (
                        lead_id, thread_id, name, email, phone, need,
                        urgency, source, status, next_field, lead_complete
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        str(uuid.uuid4()),
                        thread_id,
                        merged["name"],
                        merged["email"],
                        merged["phone"],
                        merged["need"],
                        merged["urgency"],
                        merged["source"],
                        merged["status"],
                        merged["next_field"],
                        merged["lead_complete"],
                    ),
                )
            else:
                old = dict(existing)
                merged = {}

                for field in (
                    "name", "email", "phone", "need",
                    "urgency", "source",
                ):
                    merged[field] = values[field] or old[field]

                # An omitted status must not reset the saved status.
                merged["status"] = (
                    values["status"] or old["status"] or "New"
                )
                merged["lead_complete"] = int(
                    calculate_completion(merged)
                )
                merged["next_field"] = calculate_next_field(merged)

                connection.execute(
                    """
                    UPDATE leads
                    SET name = ?, email = ?, phone = ?, need = ?,
                        urgency = ?, source = ?, status = ?,
                        next_field = ?, lead_complete = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE thread_id = ?
                    """,
                    (
                        merged["name"],
                        merged["email"],
                        merged["phone"],
                        merged["need"],
                        merged["urgency"],
                        merged["source"],
                        merged["status"],
                        merged["next_field"],
                        merged["lead_complete"],
                        thread_id,
                    ),
                )


def get_lead(thread_id: str, db_path: Optional[Path] = None):
    """Retrieve a saved lead by its conversation thread ID."""
    database_file = (
        Path(db_path).resolve()
        if db_path is not None
        else DEFAULT_DB_PATH
    )
    initialize_database(database_file)

    with closing(_connect(database_file)) as connection:
        row = connection.execute(
            "SELECT * FROM leads WHERE thread_id = ?",
            (thread_id,),
        ).fetchone()

    if row is None:
        return None

    result = dict(row)
    result["lead_complete"] = bool(result["lead_complete"])
    return result


def list_leads(db_path: Optional[Path] = None):
    """Retrieve all saved leads, newest first."""
    database_file = (
        Path(db_path).resolve()
        if db_path is not None
        else DEFAULT_DB_PATH
    )
    initialize_database(database_file)

    with closing(_connect(database_file)) as connection:
        rows = connection.execute(
            """
            SELECT * FROM leads
            ORDER BY created_at DESC, lead_id
            """
        ).fetchall()

    results = []
    for row in rows:
        result = dict(row)
        result["lead_complete"] = bool(result["lead_complete"])
        results.append(result)

    return results


if __name__ == "__main__":
    initialize_database()
    print("SQLite database initialized successfully.")
    print(f"Database location: {DEFAULT_DB_PATH}")
    print(f"Saved leads: {len(list_leads())}")
