from datetime import datetime

from src.agents.lead_capture import capture_lead
from src.models.message import NormalizedMessage
from src.validation.rules import validate_lead


def make_message(text: str) -> NormalizedMessage:
    return NormalizedMessage(
        channel="facebook",
        sender_id="user_101",
        text=text,
        timestamp=datetime(2026, 9, 24, 10, 0, 0),
        attachments=[],
    )


def test_general_inquiry_does_not_invent_service():
    message = make_message(
        "I would like to know more about your services."
    )

    lead = capture_lead(message)

    assert lead.service_interest is None
    assert lead.need is None
    assert lead.consultation_requested is False
    assert lead.status == "new"
    assert lead.qualification_status == "unknown"


def test_specific_service_is_extracted():
    message = make_message(
        "Do you provide caregiver support for elderly parents?"
    )

    lead = capture_lead(message)

    assert lead.service_interest == "caregiver_support"
    assert lead.status == "new"


def test_potential_urgent_request():
    message = make_message(
        "I need someone to check on my mother today. "
        "She is alone and not well."
    )

    lead = capture_lead(message)

    assert lead.urgency == "potential"
    assert lead.need == message.text
    assert lead.consultation_requested is False


def test_pricing_request_does_not_invent_price():
    message = make_message(
        "How much does your monthly home care package cost?"
    )

    lead = capture_lead(message)

    assert lead.plan_interest is None
    assert "pricing inquiry detected" in lead.notes


def test_consultation_request():
    message = make_message(
        "I would like to schedule a consultation "
        "to discuss care options for my father."
    )

    lead = capture_lead(message)

    assert lead.consultation_requested is True
    assert lead.status == "new"


def test_channel_and_source_are_preserved():
    message = NormalizedMessage(
        channel="whatsapp",
        sender_id="user_202",
        text="I need caregiver support.",
        timestamp=datetime(2026, 9, 24, 10, 0, 0),
        attachments=[],
    )

    lead = capture_lead(
        message,
        source="facebook_ad",
    )

    assert lead.channel == "whatsapp"
    assert lead.source == "facebook_ad"


def test_generated_lead_passes_validation():
    message = make_message(
        "Do you provide caregiver support?"
    )

    lead = capture_lead(message)

    errors = validate_lead(lead)

    assert errors == []  # Expecting no validation errors for a valid lead
    

def test_customer_statement_does_not_create_diagnosis():
    message = make_message(
        "I think my mother has dementia."
    )
    
    lead = capture_lead(message)
    
    assert not hasattr(lead, "diagnosis")
    
    
def test_caregiver_service_is_detected():
    message = NormalizedMessage(
        sender_id="user_101",
        channel="facebook",
        text="Do you provide caregiver support?",
        timestamp=datetime.now(),
        attachments=[],
    )

    lead = capture_lead(message)

    assert lead.service_interest == "caregiver_support"
    
    
def test_vague_request_does_not_guess_service():
    message = NormalizedMessage(
        sender_id="user_101",
        channel="facebook",
        text="I need help for my father.",
        timestamp=datetime.now(),
        attachments=[],
    )

    lead = capture_lead(message)

    assert lead.service_interest is None
    
    
    
def test_consultation_request_is_not_booking():
    message = NormalizedMessage(
        sender_id="user_101",
        channel="facebook",
        text="I want to schedule a consultation.",
        timestamp=datetime.now(),
        attachments=[],
    )

    lead = capture_lead(message)

    assert lead.consultation_requested is True
    assert lead.status == "new"
    
    
def test_urgent_message_is_marked_potential():
    message = NormalizedMessage(
        sender_id="user_101",
        channel="facebook",
        text="My mother is alone and not well.",
        timestamp=datetime.now(),
        attachments=[],
    )

    lead = capture_lead(message)

    assert lead.urgency == "potential"
    
    
    
    
def test_pricing_question_does_not_invent_price():
    message = NormalizedMessage(
        sender_id="user_101",
        channel="facebook",
        text="How much does the monthly package cost?",
        timestamp=datetime.now(),
        attachments=[],
    )

    lead = capture_lead(message)

    assert "pricing inquiry detected" in lead.notes
    
    
    
    
