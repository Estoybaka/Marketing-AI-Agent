# Week 3 - Day 3
# Part 4: Multi-Turn Lead Capture
#
# This program:
# 1. Receives a user message
# 2. Extracts information
# 3. Updates the existing lead
# 4. Checks missing fields
# 5. Decides what the agent should ask next
# 6. Continues until the lead is complete


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

    # Look for an email
    email_match = re.search(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        message
    )

    if email_match:
        return email_match.group(0)

    # Look for a 10-digit phone number
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
    """

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

    # Contact-related phrases tell us where the need ends
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
    Update only fields that contain new information.

    Existing information is preserved.
    """

    if extracted_information["name"] is not None:
        lead["name"] = extracted_information["name"]

    if extracted_information["contact"] is not None:
        lead["contact"] = extracted_information["contact"]

    if extracted_information["need"] is not None:
        lead["need"] = extracted_information["need"]


# --------------------------------------------------
# FUNCTION 8: CREATE THE AGENT RESPONSE
# --------------------------------------------------

def create_agent_response(lead):
    """
    Decide what the agent should say next.
    """

    next_field, lead_complete = check_lead(lead)

    if lead_complete:
        return (
            "Thank you. I have recorded your information."
        )

    if next_field == "name":
        return "Sure. May I have your name?"

    if next_field == "contact":
        return "Thanks. What is your phone number or email?"

    if next_field == "need":
        return "What kind of care service do you need?"

    return "Thank you."


# --------------------------------------------------
# FUNCTION 9: PROCESS ONE USER MESSAGE
# --------------------------------------------------

def process_message(lead, user_message):
    """
    Process one user message.

    Steps:
    1. Extract information
    2. Update the lead
    3. Check whether the lead is complete
    4. Generate the agent's response
    """

    extracted_information = extract_information(user_message)

    update_lead(lead, extracted_information)

    response = create_agent_response(lead)

    return extracted_information, response


# ==================================================
# START THE CONVERSATION
# ==================================================

print("=" * 60)
print("CAREGIVER LEAD CAPTURE AGENT")
print("=" * 60)

# This is the lead's memory
lead = {
    "name": None,
    "contact": None,
    "need": None
}


# --------------------------------------------------
# MESSAGE 1
# --------------------------------------------------

user_message = "Hi, I'm Anita."

print("\nUSER:")
print(user_message)

extracted, response = process_message(lead, user_message)

print("\nEXTRACTED:")
print(extracted)

print("\nCURRENT LEAD:")
print(lead)

print("\nAGENT:")
print(response)


# --------------------------------------------------
# MESSAGE 2
# --------------------------------------------------

user_message = "anita@gmail.com"

print("\nUSER:")
print(user_message)

extracted, response = process_message(lead, user_message)

print("\nEXTRACTED:")
print(extracted)

print("\nCURRENT LEAD:")
print(lead)

print("\nAGENT:")
print(response)


# --------------------------------------------------
# MESSAGE 3
# --------------------------------------------------

user_message = "Care for my elderly father."

print("\nUSER:")
print(user_message)

extracted, response = process_message(lead, user_message)

print("\nEXTRACTED:")
print(extracted)

print("\nCURRENT LEAD:")
print(lead)

print("\nAGENT:")
print(response)


# --------------------------------------------------
# FINAL RESULT
# --------------------------------------------------

next_field, lead_complete = check_lead(lead)

print("\n" + "=" * 60)
print("FINAL LEAD")
print("=" * 60)

print(lead)

print("\nNext field:")
print(next_field)

print("\nLead complete:")
print(lead_complete)