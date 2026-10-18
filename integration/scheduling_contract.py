
"""Scheduling handoff contract.

This module prepares a request for an external Scheduling Agent.
It does not book appointments or confirm availability.
"""


def prepare_scheduling_request(
    lead: dict,
    requested_date: str | None,
    requested_time: str | None,
    customer_ready: bool,
) -> dict:
    """Validate the information needed before scheduling handoff."""

    if not isinstance(lead, dict):
        raise ValueError("lead must be a dictionary.")

    required_fields = ("name", "need")
    missing_fields = [
        field
        for field in required_fields
        if not str(lead.get(field) or "").strip()
    ]

    if not any(
        str(lead.get(field) or "").strip()
        for field in ("email", "phone")
    ):
        missing_fields.append("email_or_phone")

    if not requested_date or not requested_date.strip():
        missing_fields.append("requested_date")

    if not requested_time or not requested_time.strip():
        missing_fields.append("requested_time")

    if missing_fields:
        return {
            "status": "not_ready",
            "missing_fields": missing_fields,
            "request": None,
        }

    if customer_ready is not True:
        return {
            "status": "not_ready",
            "missing_fields": [],
            "request": None,
        }

    return {
        "status": "ready_for_handoff",
        "missing_fields": [],
        "request": {
            "lead_id": lead.get("lead_id"),
            "name": lead["name"].strip(),
            "email": (lead.get("email") or "").strip() or None,
            "phone": (lead.get("phone") or "").strip() or None,
            "need": lead["need"].strip(),
            "requested_date": requested_date.strip(),
            "requested_time": requested_time.strip(),
        },
    }
