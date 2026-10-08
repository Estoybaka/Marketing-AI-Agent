# Week 3 - Day 3
# Information Extraction + Missing-Field Detection
# Part 1: Checking which lead fields are missing


def find_next_field(lead):
    """
    Check the lead information and return
    the next required field that is missing.
    """

    if lead["name"] is None:
        return "name"

    if lead["contact"] is None:
        return "contact"

    if lead["need"] is None:
        return "need"

    # If nothing is missing
    return None


def check_lead(lead):
    """
    Check the lead and determine:
    - which field should be collected next
    - whether the lead is complete
    """

    next_field = find_next_field(lead)

    if next_field is None:
        lead_complete = True
    else:
        lead_complete = False

    return next_field, lead_complete


# --------------------------------------------------
# TEST 1
# --------------------------------------------------

lead_1 = {
    "name": "Maya",
    "contact": "maya@example.com",
    "need": "care for elderly mother"
}

next_field, lead_complete = check_lead(lead_1)

print("TEST 1")
print("Lead:", lead_1)
print("Next field:", next_field)
print("Lead complete:", lead_complete)

print("-" * 50)


# --------------------------------------------------
# TEST 2
# --------------------------------------------------

lead_2 = {
    "name": "Anita",
    "contact": None,
    "need": "care for elderly father"
}

next_field, lead_complete = check_lead(lead_2)

print("TEST 2")
print("Lead:", lead_2)
print("Next field:", next_field)
print("Lead complete:", lead_complete)

print("-" * 50)


# --------------------------------------------------
# TEST 3
# --------------------------------------------------

lead_3 = {
    "name": "Ram",
    "contact": "ram@example.com",
    "need": "care for elderly mother"
}

next_field, lead_complete = check_lead(lead_3)

print("TEST 3")
print("Lead:", lead_3)
print("Next field:", next_field)
print("Lead complete:", lead_complete)

print("-" * 50)


# --------------------------------------------------
# TEST 4
# --------------------------------------------------

lead_4 = {
    "name": None,
    "contact": "sita@example.com",
    "need": "care for father"
}

next_field, lead_complete = check_lead(lead_4)

print("TEST 4")
print("Lead:", lead_4)
print("Next field:", next_field)
print("Lead complete:", lead_complete)

print("-" * 50)


# --------------------------------------------------
# TEST 5
# --------------------------------------------------

lead_5 = {
    "name": "Sarah",
    "contact": None,
    "need": None
}

next_field, lead_complete = check_lead(lead_5)

print("TEST 5")
print("Lead:", lead_5)
print("Next field:", next_field)
print("Lead complete:", lead_complete)

print("-" * 50)