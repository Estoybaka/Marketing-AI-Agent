
"""
Tests for customer messages after lead completion.

These tests do not call Gemini or use API quota.
Run with: python test_completed_lead.py
"""

from copy import deepcopy
from typing import Optional


REQUIRED_FIELDS = ["name", "contact", "need"]


def update_lead(lead: dict, extracted: dict) -> None:
    """Apply non-empty extracted values to a lead."""

    for field in REQUIRED_FIELDS:
        value = extracted.get(field)

        if value is not None and str(value).strip():
            lead[field] = str(value).strip()


def find_next_field(lead: dict) -> Optional[str]:
    """Find the first missing required field."""

    for field in REQUIRED_FIELDS:
        if not lead.get(field):
            return field

    return None


def process_customer_message(
    lead: dict,
    extracted: dict
) -> dict:
    """
    Simulate lead updates without calling an AI model.

    This is a local test helper, not yet the production
    LangGraph conversation handler.
    """

    old_lead = deepcopy(lead)

    update_lead(lead, extracted)

    next_field = find_next_field(lead)
    lead_complete = next_field is None

    changed = lead != old_lead

    questions = {
        "name": "Sure. May I have your name?",
        "contact": "What is your phone number or email?",
        "need": "What kind of care service do you need?"
    }

    if not lead_complete:
        response = questions[next_field]
    elif changed and not all(old_lead.values()):
        response = "Thank you. I have recorded your information."
    elif changed:
        response = (
            "Thank you. I have updated your information."
        )
    else:
        response = (
            "Thank you. I still have your information recorded. "
            "Is there anything else I can help you with?"
        )

    return {
        "lead": lead,
        "next_field": next_field,
        "lead_complete": lead_complete,
        "changed": changed,
        "response": response
    }


# --------------------------------------------------
# TEST 1: Add information to a completed lead
# --------------------------------------------------

def test_add_information_after_completion():
    lead = {
        "name": "Anita Sharma",
        "contact": "anita@example.com",
        "need": "Care for her elderly father"
    }

    result = process_customer_message(
        lead,
        {
            "name": None,
            "contact": None,
            "need": (
                "Care for her elderly father, "
                "including daily activities"
            )
        }
    )

    assert result["lead_complete"] is True
    assert result["changed"] is True
    assert "daily activities" in result["lead"]["need"]
    assert "updated" in result["response"].lower()

    print("PASS: Additional care details update a completed lead.")


# --------------------------------------------------
# TEST 2: No new information
# --------------------------------------------------

def test_no_information_change():
    lead = {
        "name": "Anita Sharma",
        "contact": "anita@example.com",
        "need": "Care for her elderly father"
    }

    original_lead = deepcopy(lead)

    result = process_customer_message(
        lead,
        {
            "name": None,
            "contact": None,
            "need": None
        }
    )

    assert result["lead_complete"] is True
    assert result["changed"] is False
    assert result["lead"] == original_lead
    assert "anything else" in result["response"].lower()

    print("PASS: Unchanged leads are not falsely reported as updated.")


# --------------------------------------------------
# TEST 3: Correct an existing contact
# --------------------------------------------------

def test_correct_existing_contact():
    lead = {
        "name": "Anita Sharma",
        "contact": "wrong@example.com",
        "need": "Care for her elderly father"
    }

    result = process_customer_message(
        lead,
        {
            "name": None,
            "contact": "anita@example.com",
            "need": None
        }
    )

    assert result["lead"]["contact"] == "anita@example.com"
    assert result["lead_complete"] is True
    assert result["changed"] is True
    assert "updated" in result["response"].lower()

    print("PASS: A corrected contact replaces the previous contact.")


# --------------------------------------------------
# TEST 4: Missing fields still need to be collected
# --------------------------------------------------

def test_incomplete_lead_stays_incomplete():
    lead = {
        "name": "Anita Sharma",
        "contact": None,
        "need": "Care for her elderly father"
    }

    result = process_customer_message(
        lead,
        {
            "name": None,
            "contact": None,
            "need": None
        }
    )

    assert result["lead_complete"] is False
    assert result["next_field"] == "contact"
    assert "phone number or email" in result["response"].lower()

    print("PASS: Incomplete leads still prompt for missing information.")


# --------------------------------------------------
# RUN ALL TESTS
# --------------------------------------------------

if __name__ == "__main__":
    tests = [
        test_add_information_after_completion,
        test_no_information_change,
        test_correct_existing_contact,
        test_incomplete_lead_stays_incomplete
    ]

    failures = 0

    print("\nRunning completed-lead tests...\n")

    for test in tests:
        try:
            test()
        except AssertionError:
            failures += 1
            print(f"FAIL: {test.__name__}")
        except Exception as error:
            failures += 1
            print(f"ERROR: {test.__name__}: {error}")

    print("\n" + "=" * 45)
    print(f"Tests run: {len(tests)}")
    print(f"Passed: {len(tests) - failures}")
    print(f"Failed: {failures}")
    print("=" * 45)

    if failures:
        raise SystemExit(1)

    print("\nAll completed-lead tests passed!")