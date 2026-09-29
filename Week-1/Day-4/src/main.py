from datetime import datetime

from src.agents.lead_capture import lead_capture_node
from src.models import NormalizedMessage
from src.state.graph_state import GraphState
from src.validation.rules import validate_lead


def main() -> None:
    message = NormalizedMessage(
        channel="facebook",
        sender_id="user_101",
        text=(
            "I need caregiver support for my father."
        ),
        timestamp=datetime.now(),
        attachments=[],
    )

    state = GraphState(
        message=message,
    )

    updated_state = lead_capture_node(state)

    print("\n--- NORMALIZED MESSAGE ---")
    print(updated_state.message.model_dump_json(indent=2))

    print("\n--- LEAD RECORD ---")
    print(updated_state.lead.model_dump_json(indent=2))

    if updated_state.lead is None:
        print("\n--- VALIDATION ---")
        print("FAILED")
        print("- Lead Capture did not create a lead.")
        return

    errors = validate_lead(updated_state.lead)

    print("\n--- VALIDATION ---")

    if errors:
        print("FAILED")

        for error in errors:
            print(f"- {error}")
    else:
        print("PASSED")

if __name__ == "__main__":
    main()