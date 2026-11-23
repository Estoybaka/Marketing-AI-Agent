
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
    "New",
    "Contacted",
    "Booked",
    "Qualified",
    "Follow-up",
    "Converted",
    "Lost",
}

ALLOWED_STATUS_TRANSITIONS = {
    "New": {"Contacted", "Qualified", "Follow-up", "Lost"},
    "Contacted": {"Booked", "Qualified", "Follow-up", "Lost"},
    "Qualified": {"Contacted", "Follow-up", "Lost"},
    "Follow-up": {"Contacted", "Lost"},
    "Booked": {"Converted"},
    "Converted": set(),
    "Lost": set(),
}

ALL_LEAD_FIELDS = (
    "name",
    "email",
    "phone",
    "need",
    "when_needed",
    "urgency",
    "source",
    "status",
    "next_field",
    "lead_complete",
    "contact_consent",
    "contact_consent_asked",
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
    """A complete lead needs name, contact, need, and timing."""
    return (
        bool(normalize_value(lead.get("name")))
        and bool(normalize_value(lead.get("need")))
        and bool(normalize_value(lead.get("when_needed")))
        and any(
            bool(normalize_value(lead.get(field)))
            for field in CONTACT_FIELDS
        )
    )


def calculate_next_field(lead):
    """Ask for name, contact, need, and timing in order."""
    if not normalize_value(lead.get("name")):
        return "name"

    if not any(
        normalize_value(lead.get(field))
        for field in CONTACT_FIELDS
    ):
        return "email_or_phone"

    if not normalize_value(lead.get("need")):
        return "need"

    if not normalize_value(lead.get("when_needed")):
        return "when_needed"

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
                    'New', 'Contacted', 'Booked', 'Qualified', 'Follow-up',
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


def _migrate_legacy_table(connection):
    """Create the schema or migrate the previous database schema."""
    if not _table_exists(connection, "leads"):
        _create_leads_table(connection)
        return

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

    columns = _columns(connection, "leads")

    # Modern database: add new columns without rebuilding the table.
    if required_columns.issubset(columns):

        if "when_needed" not in columns:
            connection.execute(
                """
                ALTER TABLE leads
                ADD COLUMN when_needed TEXT
                """
            )

        if "contact_consent" not in columns:
            connection.execute(
                """
                ALTER TABLE leads
                ADD COLUMN contact_consent INTEGER CHECK (
                    contact_consent IS NULL OR contact_consent IN (0, 1)
                )
                """
            )

        if "contact_consent_asked" not in columns:
            connection.execute(
                """
                ALTER TABLE leads
                ADD COLUMN contact_consent_asked INTEGER NOT NULL DEFAULT 0
                    CHECK (contact_consent_asked IN (0, 1))
                """
            )
            
        # Update the SQLite status constraint if it is outdated.
        _migrate_status_constraint(connection)    

        return

    # Older database structure: rebuild while preserving existing data.
    old_rows = connection.execute("SELECT * FROM leads").fetchall()

    connection.execute(
        "ALTER TABLE leads RENAME TO leads_legacy_migration"
    )

    _create_leads_table(connection)

    for row in old_rows:
        old = dict(row)

        thread_id = (
            normalize_value(old.get("thread_id"))
            or str(uuid.uuid4())
        )

        email = normalize_value(old.get("email"))
        phone = normalize_value(old.get("phone"))

        if not email and not phone:
            email, phone = _split_legacy_contact(
                old.get("contact")
            )

        lead = {
            "name": normalize_value(old.get("name")),
            "email": email,
            "phone": phone,
            "need": normalize_value(old.get("need")),
            "when_needed": normalize_value(old.get("when_needed")),
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

        now = datetime.now().isoformat(
            sep=" ",
            timespec="seconds",
        )

        created_at = (
            normalize_value(old.get("created_at")) or now
        )

        updated_at = (
            normalize_value(old.get("updated_at")) or created_at
        )

        connection.execute(
            """
            INSERT INTO leads (
                lead_id, thread_id, name, email, phone, need,
                when_needed, urgency, source, status,
                created_at, updated_at, next_field, lead_complete,
                contact_consent, contact_consent_asked
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                normalize_value(old.get("lead_id"))
                or str(uuid.uuid4()),
                thread_id,
                lead["name"],
                lead["email"],
                lead["phone"],
                lead["need"],
                lead["when_needed"],
                urgency,
                source,
                status,
                created_at,
                updated_at,
                calculate_next_field(lead),
                int(calculate_completion(lead)),
                old.get("contact_consent"),
                old.get("contact_consent_asked") or 0,
            ),
        )

    connection.execute(
        "DROP TABLE leads_legacy_migration"
    )
    
def _migrate_status_constraint(connection):
    """Rebuild the leads table if its status constraint is outdated."""

    schema = connection.execute(
        """
        SELECT sql
        FROM sqlite_master
        WHERE type = 'table' AND name = 'leads'
        """
    ).fetchone()

    if schema is None:
        return

    schema_sql = schema["sql"] or ""

    # Skip migration if the new statuses are already supported.
    if "'Contacted'" in schema_sql and "'Booked'" in schema_sql:
        return

    old_rows = connection.execute(
        "SELECT * FROM leads"
    ).fetchall()

    connection.execute(
        "ALTER TABLE leads RENAME TO leads_status_migration"
    )

    _create_leads_table(connection)

    fields = (
        "lead_id",
        "thread_id",
        "name",
        "email",
        "phone",
        "need",
        "when_needed",
        "urgency",
        "source",
        "status",
        "created_at",
        "updated_at",
        "next_field",
        "lead_complete",
        "contact_consent",
        "contact_consent_asked",
    )

    placeholders = ", ".join("?" for _ in fields)
    field_names = ", ".join(fields)

    for row in old_rows:
        old = dict(row)

        values = []

        for field in fields:
            value = old.get(field)

            if field == "status" and value not in ALLOWED_STATUSES:
                value = "New"

            if field == "contact_consent_asked" and value is None:
                value = 0

            values.append(value)

        connection.execute(
            f"""
            INSERT INTO leads ({field_names})
            VALUES ({placeholders})
            """,
            values,
        )

    connection.execute(
        "DROP TABLE leads_status_migration"
    )    


def initialize_database(db_path: Optional[Path] = None):
    """Initialize the database and migrate the previous schema."""
    database_file = (
        Path(db_path).resolve()
        if db_path is not None
        else DEFAULT_DB_PATH
    )

    database_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with closing(_connect(database_file)) as connection:
        with connection:
            _migrate_legacy_table(connection)


def save_lead(
    thread_id: str,
    lead: dict,
    db_path: Optional[Path] = None,
):
    """Insert or update a lead while preserving saved values."""
    if not isinstance(thread_id, str) or not thread_id.strip():
        raise ValueError(
            "thread_id must be a non-empty string."
        )

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
        "urgency",
        values["urgency"],
        ALLOWED_URGENCY,
    )

    values["source"] = _validate_controlled_value(
        "source",
        values["source"],
        ALLOWED_SOURCES,
    )

    if values["status"] is not None:
        values["status"] = _validate_controlled_value(
            "status",
            values["status"],
            ALLOWED_STATUSES,
        )
          
    # Consent must be explicitly True, explicitly False, or None.
    consent = values["contact_consent"]

    if consent is not None and not isinstance(consent, bool):
        raise ValueError(
            "contact_consent must be True, False, or None."
        )

    consent_asked = values["contact_consent_asked"]

    if consent_asked is not None and not isinstance(
        consent_asked, bool
    ):
        raise ValueError(
            "contact_consent_asked must be True or False."
        )

    with closing(_connect(database_file)) as connection:
        with connection:
            existing = connection.execute(
                "SELECT * FROM leads WHERE thread_id = ?",
                (thread_id,),
            ).fetchone()

            if existing is None:
                
                if values["status"] == "Booked":
                    raise ValueError(
                        "A lead can only be marked Booked after "
                        "the Scheduling Agent confirms the booking."
                    )
                merged = {
                    field: values[field]
                    for field in (
                        "name",
                        "email",
                        "phone",
                        "need",
                        "when_needed",
                        "urgency",
                        "source",
                    )
                }

                merged["status"] = values["status"] or "New"

                merged["contact_consent"] = (
                    values["contact_consent"]
                )

                merged["contact_consent_asked"] = (
                    values["contact_consent_asked"]
                    if values["contact_consent_asked"] is not None
                    else False
                )

                merged["lead_complete"] = int(
                    calculate_completion(merged)
                )

                merged["next_field"] = calculate_next_field(
                    merged
                )

                now = datetime.now().isoformat(
                    sep=" ",
                    timespec="seconds",
                )

                connection.execute(
                    """
                    INSERT INTO leads (
                        lead_id, thread_id, name, email, phone, need,
                        when_needed, urgency, source, status,
                        created_at, updated_at, next_field, lead_complete,
                        contact_consent, contact_consent_asked
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        str(uuid.uuid4()),
                        thread_id,
                        merged["name"],
                        merged["email"],
                        merged["phone"],
                        merged["need"],
                        merged["when_needed"],
                        merged["urgency"],
                        merged["source"],
                        merged["status"],
                        now,
                        now,
                        merged["next_field"],
                        merged["lead_complete"],
                        merged["contact_consent"],
                        int(merged["contact_consent_asked"]),
                    ),
                )

            else:
                old = dict(existing)
                merged = {}

                for field in (
                    "name",
                    "email",
                    "phone",
                    "need",
                    "when_needed",
                    "urgency",
                    "source",
                ):
                    merged[field] = (
                        values[field] or old[field]
                    )

                old_status = old["status"] or "New"
                new_status = values["status"]
                
                if new_status == "Booked" and old_status != "Booked":
                    raise ValueError(
                        "A lead can only be marked Booked after "
                        "the Scheduling Agent confirms the booking."
                    )
                
                if new_status is not None and new_status != old_status:
                    allowed_next_statuses = ALLOWED_STATUS_TRANSITIONS.get(
                        old_status, set(),  
                    )
                    
                    if new_status not in allowed_next_statuses:
                        raise ValueError(
                            f"Invalid status transition: "
                            f"{old_status} -> {new_status}. "
                        )    
                merged["status"] = new_status or old_status
                merged["contact_consent"] = (
                    values["contact_consent"]
                    if values["contact_consent"] is not None
                    else old["contact_consent"]
                )

                merged["contact_consent_asked"] = (
                    values["contact_consent_asked"]
                    if values["contact_consent_asked"] is not None
                    else bool(old["contact_consent_asked"])
                )

                merged["lead_complete"] = int(
                    calculate_completion(merged)
                )

                merged["next_field"] = calculate_next_field(
                    merged
                )

                connection.execute(
                    """
                    UPDATE leads
                    SET name = ?, email = ?, phone = ?, need = ?,
                        when_needed = ?, urgency = ?, source = ?,
                        status = ?, next_field = ?, lead_complete = ?,
                        contact_consent = ?,
                        contact_consent_asked = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE thread_id = ?
                    """,
                    (
                        merged["name"],
                        merged["email"],
                        merged["phone"],
                        merged["need"],
                        merged["when_needed"],
                        merged["urgency"],
                        merged["source"],
                        merged["status"],
                        merged["next_field"],
                        merged["lead_complete"],
                        merged["contact_consent"],
                        int(merged["contact_consent_asked"]),
                        thread_id,
                    ),
                )


def get_lead(
    thread_id: str,
    db_path: Optional[Path] = None,
):
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

    result["lead_complete"] = bool(
        result["lead_complete"]
    )

    if result["contact_consent"] is not None:
        result["contact_consent"] = bool(
            result["contact_consent"]
        )

    result["contact_consent_asked"] = bool(
        result["contact_consent_asked"]
    )

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

        result["lead_complete"] = bool(
            result["lead_complete"]
        )

        if result["contact_consent"] is not None:
            result["contact_consent"] = bool(
                result["contact_consent"]
            )

        result["contact_consent_asked"] = bool(
            result["contact_consent_asked"]
        )

        results.append(result)

    return results

if __name__ == "__main__":
    initialize_database()

    print("SQLite database initialized successfully.")
    print(f"Database location: {DEFAULT_DB_PATH}")
    print(f"Saved leads: {len(list_leads())}")
