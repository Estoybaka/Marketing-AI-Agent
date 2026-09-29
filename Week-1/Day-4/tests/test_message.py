from datetime import datetime
import pytest
from pydantic import ValidationError
from src.models.message import NormalizedMessage

print(NormalizedMessage.model_json_schema())

def test_valid_normalized_message():
    message = NormalizedMessage(
            sender_id="user_123",
            channel="facebook",
            text="Do you provide caregiver support for elderly parents?",
            timestamp=datetime(2023, 6, 15, 10, 30),
            attachments=[]
    )
    
    assert message.sender_id == "user_123"
    assert message.channel == "facebook"
    assert message.text == "Do you provide caregiver support for elderly parents?"
    assert message.timestamp == datetime(2023, 6, 15, 10, 30)
    assert message.attachments == []


def test_missing_required_fields():
    with pytest.raises(ValidationError):
        NormalizedMessage(
            sender_id=123,
            text="Do you provide caregiver support for elderly parents?",
            timestamp=datetime(2023, 6, 15, 10, 30),
        )
        

def test_missing_sender_id():
    with pytest.raises(ValidationError):
        NormalizedMessage(
            channel="facebook",
            text="Do you provide caregiver support for elderly parents?",
            timestamp=datetime(2023, 6, 15, 10, 30),
        )
        
        
def test_empty_message_is_invalid():
    with pytest.raises(ValidationError):
        NormalizedMessage(
            channel="facebook",
            sender_id="user_001",
            text="",
            timestamp=datetime(2023, 6, 15, 10, 30)
        )

