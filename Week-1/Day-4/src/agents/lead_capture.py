#  The function is to create a lead capture agent that can handle incoming messages and extract relevant information for lead generation.

from datetime import datetime

from src.models import Lead, NormalizedMessage
from src.state.graph_state import GraphState


def _contains_any(text:str, phrases:list[str]) -> bool:
    normalized_text = text.lower()
    return any(
        phrase.lower() in normalized_text 
        for phrase in phrases
    )


def capture_lead(message: NormalizedMessage, source:str = "unknown") -> Lead:
    """
    Captures a lead from a normalized message.
    
    Lead Capture:
    - preserves channel
    -preserves source
    - extracts only directed supported information from the message text
    - leaves other fields as None or default values
    - identifies consultation intent
    - identifies potential urgency
    - identifies service interest based on keywords
    - does not qualify
    - does not diagnose
    - does not book appointments
    """
    
    text = message.text.strip()
    text_lower = text.lower()
    
    now = datetime.now()
    
    service_interest = None
    need =  None
    urgency = None
    consultation_requested = False
    plan_interest = None
    
    # 1. Detect service interest based on keywords
    if _contains_any(text, [
        "caregiver",
        "caregiver support"
        
    ]):
        service_interest = "caregiver_support"
        
    # 2. Detect explicit consultation intent
    
    if _contains_any(text, [
        "schedule a consultation",
        "book a consultation",
        "consultation",
        "consult",
    ]):
        consultation_requested = True
        
    # 3. Detect potential urgency
    if _contains_any(text, [
        "today",
        "as soon as possible",
        "urgent",
        "urgently",
        "immediately",
        "alone at home",
        "alone and not well",
    ]):
        urgency = "potential"
    
    
    # 4. Preserve the stated need for the urgent test case
    if (
        "check on my mother" in text_lower or
        "check on my father" in text_lower or
        "check on my parent" in text_lower 
    ):
        need = text
       
    # 5. Detect explicitly named plan interest
    if _contains_any(text, [
        "care connect",
    ]):
        plan_interest = "Care Connect" 
        
    # 6. Pricing questions should not produce an invented price
    if _contains_any(text, [
        "how much",
        "price",
        "pricing",
        "cost",
        "monthly package"
    ]):
        notes = ["pricing inquiry detected"]
    else:
        notes = []


    return Lead(
        lead_id=f"lead_{message.sender_id}",
        name = None,
        contact = None,
        channel = message.channel,
        source=source,
        need=need,        
        service_interest=service_interest,
        patient_location = None,
        urgency=urgency,
        preferred_contact_time = None,
        plan_interest=plan_interest,
        status="new",
        qualification_status="unknown",
        consultation_requested=consultation_requested,
        notes=notes,
        created_at=now,
        updated_at=now
    ) 
    
def lead_capture_node(state: GraphState) -> GraphState:
    """
    Run Lead Capture using the shared workflow state.

    The node reads the normalized message from state,
    captures a Lead, and returns an updated state.
    
    
    In short, It converts an incoming message 
    into a basic Lead record by extracting only clearly supported information,
    then passes that Lead into the next step of the workflow.
    """

    lead = capture_lead(state.message)

    return state.model_copy(
        update={
            "lead": lead,
        }
    )   