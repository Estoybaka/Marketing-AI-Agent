from datetime import datetime
from src.models.lead import Lead


# Test case for the Lead model to test the default values and initialization
def test_valid_lead():
    now = datetime(2023, 6, 15, 10, 30)
    
    lead = Lead(
        lead_id="lead_001",
        channel="facebook",
        source="unknown",
        created_at=now,
        updated_at=now,
    )
    
    assert lead.lead_id == "lead_001"
    assert lead.status == "new"
    assert lead.qualification_status == "unknown"
    assert lead.consultation_requested is False
    assert lead.name is None
    assert lead.notes == []