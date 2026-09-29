from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, Field


class Lead(BaseModel):
    """
    Target Lead Structure for the Local Lead Capture Prototype.
    
    """
    lead_id: str
    name: Optional[str] = None
    contact: Optional[str] = None
    channel: str
    source: str = "unknown"
    need: Optional[str] = None
    service_interest: Optional[str] = None
    patient_location: Optional[str] = None
    urgency: Optional[str] = None
    preferred_contact_time: Optional[str] = None
    plan_interest: Optional[str] = None
    status: str = "new"
    qualification_status: str = "unknown"
    consultation_requested: bool = False
    notes: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    
# leads = {
#     "lead_id" : "lead_001",
#     "name" : null,
#     "contact" : null,
#     "channel" : "facebook",
#     "source" :"unknown",
#     "need" : null,
#     "service_interest" : "carregiver_support",
#     "patient_location" : null,
#     "urgency" : null,
#     "preferred_contact_time" : null,
#     "plan_interest" : null,
#     "status" : "new",
#     "qualification_status" : "unknown",
#     "consultation_requested" : False,
#     "notes" : [],
#     "created_at" : "...",
#     "updated_at" : "...",
# }