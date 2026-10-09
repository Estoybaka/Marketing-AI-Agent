
"""
Local tests for lead-management logic.

These tests do not call Gemini or use API quota.
Run with: python test_lead_logic.py
"""

from typing import Optional


# --------------------------------------------------
# 1. Update a lead with extracted information
# --------------------------------------------------

def update_lead(lead: dict, extracted: dict) -> None:
    """Update supplied fields without erasing missing values."""

    for field in ["name", "contact", "need"]:
        new_value = extracted.get(field)

        if new_value is not None and str(new_value).strip():
            lead[field] = str(new_value).strip()


# --------------------------------------------------
# 2. Find the next missing field
# --------------------------------------------------

def find_next_field(lead: dict) -> Optional[str]:
    """Return the first missing required field."""

    if not lead.get("name"):
        return "name"

    if not lead.get("contact"):
        return "contact"

    if not lead.get("need"):
        return "need"

    return None


# --------------------------------------------------
# 3. Determine whether a lead is complete
# --------------------------------------------------

def is_lead_complete(lead: dict) -> bool:
    return find_next_field(lead) is None


# --------------------------------------------------
# 4. Local tests
# --------------------------------------------------

def test_information_is_merged():
    lead = {
        "name": None,
        "contact": "anita@example.com",
        "need": None
    }

    update_lead(
        lead,
        {
            "name": "Anita Sharma",
            "contact": None,
            "need": "Care for her elderly father"
        }
    )

    assert lead["name"] == "Anita Sharma"
    assert lead["contact"] == "anita@example.com"
    assert lead["need"] == "Care for her elderly father"

    print("PASS: Existing information is preserved.")


def test_missing_fields_are_detected():
    lead = {
        "name": None,
        "contact": "anita@example.com",
        "need": "Care for her elderly father"
    }

    assert find_next_field(lead) == "name"

    lead["name"] = "Anita Sharma"

    assert find_next_field(lead) is None

    print("PASS: Missing fields are detected correctly.")


def test_empty_values_do_not_erase_information():
    lead = {
        "name": "Anita Sharma",
        "contact": "anita@example.com",
        "need": "Care for her elderly father"
    }

    update_lead(
        lead,
        {
            "name": None,
            "contact": " ",
            "need": None
        }
    )

    assert lead["name"] == "Anita Sharma"
    assert lead["contact"] == "anita@example.com"
    assert lead["need"] == "Care for her elderly father"

    print("PASS: Empty values do not erase saved information.")


def test_incomplete_lead_is_not_complete():
    lead = {
        "name": "Anita Sharma",
        "contact": None,
        "need": "Care for her elderly father"
    }

    assert is_lead_complete(lead) is False
    assert find_next_field(lead) == "contact"

    print("PASS: Incomplete leads are not marked complete.")


def test_complete_lead_is_recognized():
    lead = {
        "name": "Anita Sharma",
        "contact": "anita@example.com",
        "need": "Care for her elderly father"
    }

    assert is_lead_complete(lead) is True

    print("PASS: Complete leads are recognized.")


# --------------------------------------------------
# 5. Run all tests
# --------------------------------------------------

if __name__ == "__main__":
    tests = [
        test_information_is_merged,
        test_missing_fields_are_detected,
        test_empty_values_do_not_erase_information,
        test_incomplete_lead_is_not_complete,
        test_complete_lead_is_recognized
    ]

    failures = 0

    print("\nRunning local lead-logic tests...\n")

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

    print("\nAll local lead-logic tests passed!")