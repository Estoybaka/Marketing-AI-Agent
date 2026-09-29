# Models for the NormalizedMessage and Lead classes in the Local Lead Capture Prototype.

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

# BaseModel is a class from the Pydantic library that provides data validation and settings management using Python type annotations.
class NormalizedMessage(BaseModel):
    """
    Message Structure passed from channel adapter to downstream  agents for processing.
    Structure we finalized for follwing fields:
    - sender_id: Unique identifier for the sender of the message.
    - channel: The communication channel through which the message was received (e.g., "facebook", "whatsapp").
    - text: The textual content of the message.
    - timestamp: The date and time when the message was sent.
    - attachments: A list of any attachments included with the message (e.g., images, documents).
    """
    sender_id: str
    channel: str
    text: str = Field(min_length=1)
    timestamp: datetime
    attachments: list[Any] = Field(default_factory=list)

# message = {
#     "sender_id": 123,
#     "channel": "facebook",
#     "text": "Do you provide caregiver support for elderly parents?",
#     "timestamp": "2023-06-15T10:30:00Z",
#     "attachments": []
# }