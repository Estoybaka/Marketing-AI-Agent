"""Lead workflow orchestration."""

from src.agents.lead_capture import lead_capture_node
from src.state.graph_state import GraphState
from src.validation.rules import validate_lead
from src.lifecycle.transitions import transition_lead


def run_lead_workflow(state: GraphState) -> GraphState:
    """
    Run the initial Lead workflow.

    Steps:
    1. Capture the lead from the normalized message.
    2. Validate the captured lead.
    3. Store validation errors in the shared state.
    4. Stop the workflow when validation fails.
    5. Apply the lifecycle transition when validation succeeds.
    
    The workflow operates on GraphState so that individual
    workflow steps can later be connected to an orchestration
    framework such as LangGraph without moving business logic
    into the framework itself.
    """

    state = lead_capture_node(state)

    if state.lead is None:
        return state.model_copy(
            update={
                "errors": ["Lead Capture did not produce a lead."],
            }
        )

    errors = validate_lead(state.lead)

    state = state.model_copy(
        update={
            "errors": errors,
        }
    )

    if errors:
        return state

    state = apply_lifecycle_transition(state)

    return state
    
    
def apply_lifecycle_transition(state: GraphState) -> GraphState:
    """
    Apply the initial lifecycle transition based on extracted lead intent.

    A consultation request moves a new lead into
    the consultation_requested status.
    """

    if state.lead is None:
        return state

    if (
        state.lead.status == "new"
        and state.lead.consultation_requested
    ):
        updated_lead = transition_lead(
            state.lead,
            "consultation_requested",
        )

        return state.model_copy(
            update={
                "lead": updated_lead,
            }
        )

    return state