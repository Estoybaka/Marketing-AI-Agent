
from pathlib import Path
from typing import Optional

from lead_database import (
    DEFAULT_DB_PATH,
    calculate_completion,
    get_lead,
)


def prepare_follow_up(
    thread_id: str,
    db_path: Optional[Path] = None,
) -> dict:
    """
    Prepare a follow-up message only when the customer
    has explicitly agreed to be contacted.

    This function does not send messages or change lead status.
    """

    lead = get_lead(
        thread_id,
        db_path or DEFAULT_DB_PATH,
    )

    if lead is None:
        return {
            "success": False,
            "reason": "Lead not found.",
            "message": None,
        }

    # Never contact a customer without explicit permission.
    if lead.get("contact_consent") is not True:
        return {
            "success": False,
            "reason": "Customer has not explicitly agreed to follow-up.",
            "message": None,
        }

    # Do not prepare follow-up for incomplete leads.
    if not calculate_completion(lead):
        return {
            "success": False,
            "reason": "Lead information is incomplete.",
            "message": None,
        }

    name = lead["name"]
    need = lead["need"]

    # Prepare a draft without making promises.
    message = (
        f"Hello {name},\n\n"
        f"Thank you for sharing your requirement regarding "
        f"{need}.\n\n"
        "We would be happy to discuss your requirements "
        "and explain the next steps.\n\n"
        "Please let us know a convenient time to discuss this "
        "further.\n\n"
        "Thank you."
    )

    return {
        "success": True,
        "reason": "Follow-up draft prepared. It has not been sent.",
        "message": message,
        "lead_id": lead["lead_id"],
        "contact": lead.get("email") or lead.get("phone"),
        "status": lead["status"],
        "sent": False,
    }
