"""Rules for allowed lead lifecycle transitions."""

from src.models import Lead


ALLOWED_TRANSITIONS = {
    "new": {
        "contacted",
        "consultation_requested",
    },
    "contacted": {
        "needs_information",
        "consultation_requested",
    },
    "needs_information": {
        "contacted",
    },
    "qualified": {
        "consultation_requested",
    },
    "consultation_requested": {
        "booked",
    },
    "booked": {
        "converted",
    },
}


def is_transition_allowed(
    current_status: str,
    next_status: str,
) -> bool:
    """
    Return True when a lifecycle transition is allowed.
    """

    allowed_states = ALLOWED_TRANSITIONS.get(
        current_status,
        set(),
    )

    return next_status in allowed_states


def transition_lead(lead: Lead, new_status: str) -> Lead:
    """
    Move a lead from its current status to a new status.

    The transition is allowed only when the lifecycle rules permit it.
    """

    if not is_transition_allowed(lead.status, new_status):
        raise ValueError(
            f"Invalid lifecycle transition: "
            f"{lead.status} -> {new_status}"
        )

    return lead.model_copy(
        update={
            "status": new_status,
        }
    )