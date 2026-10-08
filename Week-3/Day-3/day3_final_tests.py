# Week 3 - Day 3
# Final Robustness Tests
#
# Tests:
# 1. All information provided in one message
# 2. Information provided in an unusual order
#
# The goal is to make sure our lead model:
# - extracts multiple fields
# - preserves previous information
# - handles any order
# - correctly detects completion


import re


# --------------------------------------------------
# FIND NEXT MISSING FIELD
# --------------------------------------------------

def find_next_field(lead):

    if lead["name"] is None:
        return "name"

    if lead["contact"] is None:
        return "contact"

    if lead["need"] is None:
        return "need"

    return None


# --------------------------------------------------
# CHECK LEAD
# --------------------------------------------------

def check_lead(lead):

    next_field = find_next_field(lead)

    if next_field is None:
        lead_complete = True
    else:
        lead_complete = False

    return next_field, lead_complete


# --------------------------------------------------
# EXTRACT NAME
# --------------------------------------------------

def extract_name(message):

    name_match = re.search(
        r"(?:my name is|i am|i'm|name is)\s+([a-zA-Z]+(?:\s+[a-zA-Z]+)*)",
        message,
        re.IGNORECASE
    )

    if name_match:
        return name_match.group(1).strip()

    return None


# --------------------------------------------------
# EXTRACT CONTACT
# --------------------------------------------------

def extract_contact(message):

    email_match = re.search(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        message
    )

    if email_match:
        return email_match.group(0)

    phone_match = re.search(
        r"\b\d{10}\b",
        message
    )

    if phone_match:
        return phone_match.group(0)

    return None


# --------------------------------------------------
# EXTRACT NEED
# --------------------------------------------------

def extract_need(message):

    lower_message = message.lower()

    need_phrases = [
        "i need",
        "need care",
        "need someone to care",
        "care for",
        "caregiver",
        "elderly care",
        "home care"
    ]

    start_position = None

    for phrase in need_phrases:

        position = lower_message.find(phrase)

        if position != -1:

            if start_position is None or position < start_position:
                start_position = position

    if start_position is None:
        return None

    need_text = message[start_position:].strip()

    stop_phrases = [
        "you can reach me",
        "reach me at",
        "my email is",
        "my phone is",
        "contact me at",
        "you can contact me"
    ]

    lower_need_text = need_text.lower()

    stop_position = None

    for phrase in stop_phrases:

        position = lower_need_text.find(phrase)

        if position != -1:

            if stop_position is None or position < stop_position:
                stop_position = position

    if stop_position is not None:
        need_text = need_text[:stop_position].strip()

    need_text = need_text.rstrip(".,!?")

    return need_text


# --------------------------------------------------
# EXTRACT ALL INFORMATION
# --------------------------------------------------

def extract_information(message):

    extracted = {
        "name": extract_name(message),
        "contact": extract_contact(message),
        "need": extract_need(message)
    }

    return extracted


# --------------------------------------------------
# UPDATE LEAD
# --------------------------------------------------

def update_lead(lead, extracted_information):

    if extracted_information["name"] is not None:
        lead["name"] = extracted_information["name"]

    if extracted_information["contact"] is not None:
        lead["contact"] = extracted_information["contact"]

    if extracted_information["need"] is not None:
        lead["need"] = extracted_information["need"]


# ==================================================
# TEST A
# ALL INFORMATION IN ONE MESSAGE
# ==================================================

print("=" * 60)
print("TEST A - ALL INFORMATION IN ONE MESSAGE")
print("=" * 60)


lead_a = {
    "name": None,
    "contact": None,
    "need": None
}


message_a = (
    "Hi, I'm Ram. "
    "My email is ram@example.com "
    "and I need care for my elderly mother."
)


print("\nUSER:")
print(message_a)


extracted_a = extract_information(message_a)

print("\nEXTRACTED:")
print(extracted_a)


update_lead(lead_a, extracted_a)

print("\nUPDATED LEAD:")
print(lead_a)


next_field_a, complete_a = check_lead(lead_a)

print("\nNEXT FIELD:")
print(next_field_a)

print("\nLEAD COMPLETE:")
print(complete_a)


# ==================================================
# TEST B
# INFORMATION IN UNUSUAL ORDER
# ==================================================

print("\n\n" + "=" * 60)
print("TEST B - INFORMATION IN UNUSUAL ORDER")
print("=" * 60)


lead_b = {
    "name": None,
    "contact": None,
    "need": None
}


# --------------------------------------------------
# MESSAGE 1
# --------------------------------------------------

message_b1 = "I need care for my elderly father."

print("\nUSER:")
print(message_b1)


extracted_b1 = extract_information(message_b1)

print("\nEXTRACTED:")
print(extracted_b1)


update_lead(lead_b, extracted_b1)

print("\nUPDATED LEAD:")
print(lead_b)


next_field_b1, complete_b1 = check_lead(lead_b)

print("\nNEXT FIELD:")
print(next_field_b1)

print("\nLEAD COMPLETE:")
print(complete_b1)


# --------------------------------------------------
# MESSAGE 2
# --------------------------------------------------

message_b2 = "You can contact me at sita@example.com."

print("\nUSER:")
print(message_b2)


extracted_b2 = extract_information(message_b2)

print("\nEXTRACTED:")
print(extracted_b2)


update_lead(lead_b, extracted_b2)

print("\nUPDATED LEAD:")
print(lead_b)


next_field_b2, complete_b2 = check_lead(lead_b)

print("\nNEXT FIELD:")
print(next_field_b2)

print("\nLEAD COMPLETE:")
print(complete_b2)


# --------------------------------------------------
# MESSAGE 3
# --------------------------------------------------

message_b3 = "My name is Sita."

print("\nUSER:")
print(message_b3)


extracted_b3 = extract_information(message_b3)

print("\nEXTRACTED:")
print(extracted_b3)


update_lead(lead_b, extracted_b3)

print("\nUPDATED LEAD:")
print(lead_b)


next_field_b3, complete_b3 = check_lead(lead_b)

print("\nNEXT FIELD:")
print(next_field_b3)

print("\nLEAD COMPLETE:")
print(complete_b3)


# ==================================================
# FINAL SUMMARY
# ==================================================

print("\n\n" + "=" * 60)
print("FINAL TEST SUMMARY")
print("=" * 60)


print("\nTEST A:")
print("Lead:", lead_a)
print("Complete:", complete_a)


print("\nTEST B:")
print("Lead:", lead_b)
print("Complete:", complete_b3)