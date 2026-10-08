# Week 3 - Day 3
# Part 3: Improved Information Extraction
#
# This program:
# 1. Reads a customer message
# 2. Extracts name, contact, and need
# 3. Keeps the extracted fields separate
# 4. Updates the lead
# 5. Detects missing fields
# 6. Checks whether the lead is complete


import re


# --------------------------------------------------
# FUNCTION 1: FIND THE NEXT MISSING FIELD
# --------------------------------------------------

def find_next_field(lead):
    """
    Return the first required field that is missing.
    """

    if lead["name"] is None:
        return "name"

    if lead["contact"] is None:
        return "contact"

    if lead["need"] is None:
        return "need"

    return None


# --------------------------------------------------
# FUNCTION 2: CHECK THE LEAD
# --------------------------------------------------

def check_lead(lead):
    """
    Check whether the lead is complete.
    """

    next_field = find_next_field(lead)

    if next_field is None:
        lead_complete = True
    else:
        lead_complete = False

    return next_field, lead_complete


# --------------------------------------------------
# FUNCTION 3: EXTRACT NAME
# --------------------------------------------------

def extract_name(message):
    """
    Try to find the customer's name.
    """

    name_match = re.search(
        r"(?:my name is|i am|i'm|name is)\s+([a-zA-Z]+(?:\s+[a-zA-Z]+)*)",
        message,
        re.IGNORECASE
    )

    if name_match:
        return name_match.group(1).strip()

    return None


# --------------------------------------------------
# FUNCTION 4: EXTRACT CONTACT
# --------------------------------------------------

def extract_contact(message):
    """
    Try to find an email address or phone number.
    """

    # Try email first
    email_match = re.search(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        message
    )

    if email_match:
        return email_match.group(0)

    # Try 10-digit phone number
    phone_match = re.search(
        r"\b\d{10}\b",
        message
    )

    if phone_match:
        return phone_match.group(0)

    return None


# --------------------------------------------------
# FUNCTION 5: EXTRACT NEED
# --------------------------------------------------

def extract_need(message):
    """
    Try to identify the customer's care requirement.

    The extraction stops before contact information
    begins.
    """

    lower_message = message.lower()

    # Possible phrases that indicate a care need
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

    # Find the earliest matching need phrase
    for phrase in need_phrases:

        position = lower_message.find(phrase)

        if position != -1:

            if start_position is None or position < start_position:
                start_position = position

    # If no need phrase was found
    if start_position is None:
        return None

    # Start extracting from the need phrase
    need_text = message[start_position:].strip()

    # --------------------------------------------------
    # Remove contact-related information
    # --------------------------------------------------

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

    # Cut the need before contact information
    if stop_position is not None:
        need_text = need_text[:stop_position].strip()

    # Remove unnecessary punctuation
    need_text = need_text.rstrip(".,!?")

    return need_text


# --------------------------------------------------
# FUNCTION 6: EXTRACT ALL INFORMATION
# --------------------------------------------------

def extract_information(message):
    """
    Extract name, contact, and need.
    """

    extracted = {
        "name": extract_name(message),
        "contact": extract_contact(message),
        "need": extract_need(message)
    }

    return extracted


# --------------------------------------------------
# FUNCTION 7: UPDATE THE LEAD
# --------------------------------------------------

def update_lead(lead, extracted_information):
    """
    Update only the fields that contain new information.

    Existing information is preserved.
    """

    if extracted_information["name"] is not None:
        lead["name"] = extracted_information["name"]

    if extracted_information["contact"] is not None:
        lead["contact"] = extracted_information["contact"]

    if extracted_information["need"] is not None:
        lead["need"] = extracted_information["need"]


# --------------------------------------------------
# TEST 1
# --------------------------------------------------

print("=" * 60)
print("TEST 1")
print("=" * 60)

message_1 = "Hi, I'm Anita. My father needs someone to care for him."

lead_1 = {
    "name": None,
    "contact": None,
    "need": None
}

print("Customer message:")
print(message_1)

extracted_1 = extract_information(message_1)

print("\nExtracted information:")
print(extracted_1)

update_lead(lead_1, extracted_1)

next_field, lead_complete = check_lead(lead_1)

print("\nUpdated lead:")
print(lead_1)

print("\nNext field:")
print(next_field)

print("Lead complete:")
print(lead_complete)


# --------------------------------------------------
# TEST 2
# --------------------------------------------------

print("\n" + "=" * 60)
print("TEST 2")
print("=" * 60)

message_2 = "My name is Ram. My email is ram@example.com."

lead_2 = {
    "name": None,
    "contact": None,
    "need": None
}

print("Customer message:")
print(message_2)

extracted_2 = extract_information(message_2)

print("\nExtracted information:")
print(extracted_2)

update_lead(lead_2, extracted_2)

next_field, lead_complete = check_lead(lead_2)

print("\nUpdated lead:")
print(lead_2)

print("\nNext field:")
print(next_field)

print("Lead complete:")
print(lead_complete)


# --------------------------------------------------
# TEST 3
# --------------------------------------------------

print("\n" + "=" * 60)
print("TEST 3")
print("=" * 60)

message_3 = (
    "I need home care for my elderly mother. "
    "You can reach me at maya@example.com."
)

lead_3 = {
    "name": None,
    "contact": None,
    "need": None
}

print("Customer message:")
print(message_3)

extracted_3 = extract_information(message_3)

print("\nExtracted information:")
print(extracted_3)

update_lead(lead_3, extracted_3)

next_field, lead_complete = check_lead(lead_3)

print("\nUpdated lead:")
print(lead_3)

print("\nNext field:")
print(next_field)

print("Lead complete:")
print(lead_complete)


# --------------------------------------------------
# TEST 4
# --------------------------------------------------

print("\n" + "=" * 60)
print("TEST 4")
print("=" * 60)

message_4 = (
    "My name is Sarah. "
    "I need someone to care for my elderly father. "
    "My phone is 9876543210."
)

lead_4 = {
    "name": None,
    "contact": None,
    "need": None
}

print("Customer message:")
print(message_4)

extracted_4 = extract_information(message_4)

print("\nExtracted information:")
print(extracted_4)

update_lead(lead_4, extracted_4)

next_field, lead_complete = check_lead(lead_4)

print("\nUpdated lead:")
print(lead_4)

print("\nNext field:")
print(next_field)

print("Lead complete:")
print(lead_complete)