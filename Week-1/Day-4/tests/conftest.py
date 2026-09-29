from datetime import datetime

import pytest

from src.models import NormalizedMessage


@pytest.fixture
def caregiver_message():
    return NormalizedMessage(
        sender_id="user_101",
        channel="facebook",
        text="I need caregiver support.",
        timestamp=datetime.now(),
        attachments=[],
    )