from src.models import Lead

VALID_STATUSES = {
    "new", 
    "contacted",
    "needs_information",
    "qualified", 
    "consultation_requested",
    "booked",
    "converted",
    "not_qualified",
    "inactive", 
    "human_handoff",
}

VALID_QUALIFICATION_STATUSES = {
    "unknown",
    "qualified",
    "not_qualified",
}

def validate_lead(lead: Lead) -> list[str]:
    """
    Validate a lead record.
    Args:
        lead: The lead record to validate.
    Returns:
    A list of validation errors
    An empty list indicates that the lead is valid.
    """
    errors: list[str] = []
    
    if not lead.channel.strip():
        errors.append("Channel is required.")
        
    if not lead.source.strip():
        errors.append("Source is required.")
        
    if not lead.lead_id.strip():
        errors.append("Lead ID is required.")
        
    if lead.status not in VALID_STATUSES:
        errors.append(f"Invalid status: {lead.status}")
    
    if lead.qualification_status not in VALID_QUALIFICATION_STATUSES:
        errors.append(f"Invalid qualification status: {lead.qualification_status}")
    
    # if lead.consultation_requested and lead.status != "booked":
    #     errors.append("Lead Capture must not mark consultation_requested as True if status is not booked.")
    return errors