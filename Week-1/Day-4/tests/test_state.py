from datetime import datetime

from src.agents.lead_capture import lead_capture_node
from src.models import NormalizedMessage
from src.state.graph_state import GraphState


def test_graph_state_starts_with_message_and_no_lead():
    message = NormalizedMessage(
        sender_id="user_101",
        channel="facebook",
        text="I need caregiver support.",
        timestamp=datetime.now(),
        attachments=[],
    )

    state = GraphState(
        message=message,
    )

    assert state.message == message
    assert state.lead is None
    assert state.errors == []
    
    
    
def test_lead_capture_node_adds_lead_to_state():
    message = NormalizedMessage(
        sender_id="user_101",
        channel="facebook",
        text="I need caregiver support.",
        timestamp=datetime.now(),
        attachments=[],
    )

    state = GraphState(
        message=message,
    )

    updated_state = lead_capture_node(state)

    assert updated_state.message == message
    assert updated_state.lead is not None
    assert updated_state.lead.service_interest == "caregiver_support"
    assert updated_state.errors == []