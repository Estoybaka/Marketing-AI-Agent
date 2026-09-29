from datetime import datetime

from src.models import NormalizedMessage
from src.state.graph_state import GraphState
from src.workflow.lead_workflow import run_lead_workflow


def test_lead_workflow_captures_and_validates_lead(caregiver_message):
    state = GraphState(
        message=caregiver_message,
    )

    result = run_lead_workflow(state)

    assert result.lead is not None
    assert result.lead.service_interest == "caregiver_support"
    assert result.errors == []
    
    
    
def test_consultation_request_moves_lead_to_consultation_requested():
    message = NormalizedMessage(
        sender_id="user_102",
        channel="facebook",
        text="I would like to schedule a consultation.",
        timestamp=datetime.now(),
        attachments=[],
    )

    state = GraphState(
        message=message,
    )

    result = run_lead_workflow(state)

    assert result.lead is not None
    assert result.lead.consultation_requested is True
    assert result.lead.status == "consultation_requested"
    assert result.errors == []
    
    
    
def test_general_service_inquiry_does_not_request_consultation():
    message = NormalizedMessage(
        sender_id="user_103",
        channel="facebook",
        text="I want to know more about caregiver support.",
        timestamp=datetime.now(),
        attachments=[],
    )

    state = GraphState(
        message=message,
    )

    result = run_lead_workflow(state)

    assert result.lead is not None
    assert result.lead.service_interest == "caregiver_support"
    assert result.lead.consultation_requested is False
    assert result.lead.status == "new"
    assert result.errors == []
    
    
def test_invalid_lead_does_not_move_through_lifecycle():
    message = NormalizedMessage(
        sender_id="user_104",
        channel="",
        text="I would like to schedule a consultation.",
        timestamp=datetime.now(),
        attachments=[],
    )

    state = GraphState(
        message=message,
    )

    result = run_lead_workflow(state)

    assert result.lead is not None
    assert result.errors == ["Channel is required."]
    assert result.lead.consultation_requested is True
    assert result.lead.status == "new"