# Week 3 — Day 3 Documentation

## Information Extraction, Lead Updating & Multi-Turn Lead Capture

**Project:** Caregiver Service AI Agent
**Week:** 3
**Day:** 3
**Status:** Completed
**Completion:** 100%

---

# 1. Day 3 Objective

The main objective of Day 3 was to teach the lead-capture agent how to understand useful information from a user's natural-language message and store that information inside a structured lead record.

The agent should be able to:

* Read a user's message.
* Extract the customer's name.
* Extract the customer's contact information.
* Extract the customer's care requirement.
* Store the extracted information.
* Preserve information collected in previous messages.
* Detect which required field is still missing.
* Determine which field should be requested next.
* Determine when the lead is complete.
* Handle information arriving in different orders.
* Handle multiple pieces of information in a single message.
* Continue the conversation across multiple turns.

The basic architecture developed during Day 3 was:

```text
USER MESSAGE
     ↓
EXTRACT INFORMATION
     ↓
UPDATE LEAD
     ↓
CHECK REQUIRED FIELDS
     ↓
FIND MISSING FIELD
     ↓
ASK USER
     ↓
REPEAT
     ↓
LEAD COMPLETE
```

---

# 2. What Is Information Extraction?

Information extraction means taking useful information from a normal human message and converting it into structured data.

For example, a customer might say:

```text
My name is Ram and I need care for my elderly mother.
```

The message contains two useful pieces of information:

```text
name = Ram
need = care for my elderly mother
```

The structured lead becomes:

```python
{
    "name": "Ram",
    "contact": None,
    "need": "care for my elderly mother"
}
```

The important idea is that the agent does not need to store the entire message as the lead.

Instead, it extracts the useful information and stores it in the correct fields.

---

# 3. Lead Fields Used in Day 3

The lead model contains three required customer-information fields:

```text
name
contact
need
```

The lead can also have two control fields:

```text
next_field
lead_complete
```

The complete conceptual lead structure is:

```python
{
    "name": None,
    "contact": None,
    "need": None,
    "next_field": None,
    "lead_complete": False
}
```

In the Python prototype, `next_field` and `lead_complete` are calculated from the lead rather than permanently stored in the basic dictionary.

---

# 4. Meaning of Each Field

## 4.1 Name

The customer's name.

Example:

```text
Ram Sharma
```

Stored as:

```python
"name": "Ram Sharma"
```

---

## 4.2 Contact

The customer's phone number or email address.

Example:

```text
ram@example.com
```

Stored as:

```python
"contact": "ram@example.com"
```

A phone number can also be stored.

Example:

```text
9812345678
```

Stored as:

```python
"contact": "9812345678"
```

---

## 4.3 Need

The type of caregiver service the customer needs.

Example:

```text
Care for my elderly mother
```

Stored as:

```python
"need": "Care for my elderly mother"
```

---

## 4.4 next_field

`next_field` tells the agent which required piece of information should be requested next.

The required order is:

```text
name
↓
contact
↓
need
```

For example:

```python
next_field = "contact"
```

means the agent already has the customer's name but still needs contact information.

---

## 4.5 lead_complete

`lead_complete` tells the system whether all required lead information has been collected.

If one or more fields are missing:

```python
lead_complete = False
```

If all required fields are present:

```python
lead_complete = True
```

---

# 5. Why None Is Used

Python uses `None` to represent the absence of a value.

For example:

```python
lead = {
    "name": None,
    "contact": None,
    "need": None
}
```

This means that none of the required information has been collected yet.

If the customer's name is later provided:

```python
lead["name"] = "Anita"
```

the lead becomes:

```python
{
    "name": "Anita",
    "contact": None,
    "need": None
}
```

Therefore:

```python
None
```

means:

> We do not have this information yet.

---

# 6. Missing Field Detection

The agent must know what information is missing.

The required order is:

1. name
2. contact
3. need

The function created for this purpose is:

```python
def find_next_field(lead):
    if lead["name"] is None:
        return "name"

    if lead["contact"] is None:
        return "contact"

    if lead["need"] is None:
        return "need"

    return None
```

---

# 7. Understanding find_next_field()

The function checks the fields one by one.

First:

```python
if lead["name"] is None:
```

If the name is missing, it returns:

```python
"name"
```

If the name exists, it checks the contact:

```python
if lead["contact"] is None:
```

If contact is missing, it returns:

```python
"contact"
```

If both name and contact exist, it checks need:

```python
if lead["need"] is None:
```

If need is missing, it returns:

```python
"need"
```

Finally, if none of the fields are missing:

```python
return None
```

This means:

> There is no next field to collect.

---

# 8. Lead Completion Detection

The next function checks both the next field and whether the lead is complete.

```python
def check_lead(lead):
    next_field = find_next_field(lead)

    if next_field is None:
        lead_complete = True
    else:
        lead_complete = False

    return next_field, lead_complete
```

The logic is:

```text
If there is no missing field
        ↓
lead_complete = True

If there is a missing field
        ↓
lead_complete = False
```

---

# 9. Example of Missing-Field Detection

Suppose the lead is:

```python
lead = {
    "name": None,
    "contact": "anita@example.com",
    "need": "care for father"
}
```

The name is missing.

Therefore:

```python
next_field = "name"
lead_complete = False
```

The agent should ask:

```text
Sure. May I have your name?
```

---

# 10. Another Example

Suppose the lead is:

```python
lead = {
    "name": "Anita",
    "contact": None,
    "need": "care for father"
}
```

The name exists, but contact is missing.

Therefore:

```python
next_field = "contact"
lead_complete = False
```

The agent should ask:

```text
Thanks. What is your phone number or email?
```

---

# 11. Complete Lead Example

Suppose the lead is:

```python
lead = {
    "name": "Anita",
    "contact": "anita@example.com",
    "need": "care for father"
}
```

All required information exists.

Therefore:

```python
next_field = None
lead_complete = True
```

The agent can finish the lead-capture process.

Example response:

```text
Thank you. I have recorded your information.
```

---

# 12. Information Extraction

Day 3 introduced simple rule-based extraction using Python.

The prototype uses regular expressions and keyword-based rules.

The three extraction functions are:

```text
extract_name()
extract_contact()
extract_need()
```

These functions examine the user's message and try to find useful information.

---

# 13. Extracting the Name

The name extraction function is:

```python
def extract_name(message):
    name_match = re.search(
        r"(?:my name is|i am|i'm|name is)\s+([a-zA-Z]+(?:\s+[a-zA-Z]+)*)",
        message,
        re.IGNORECASE
    )

    if name_match:
        return name_match.group(1).strip()

    return None
```

It can recognize patterns such as:

```text
My name is Ram
```

```text
I am Anita
```

```text
I'm Sita
```

The extracted value becomes:

```python
"Ram"
```

or:

```python
"Anita"
```

or:

```python
"Sita"
```

---

# 14. Extracting Contact Information

The contact extraction function looks for either an email address or a 10-digit phone number.

```python
def extract_contact(message):
    email_match = re.search(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        message
    )

    if email_match:
        return email_match.group(0)

    phone_match = re.search(r"\b\d{10}\b", message)

    if phone_match:
        return phone_match.group(0)

    return None
```

Example:

```text
You can email me at ram@example.com.
```

produces:

```python
"ram@example.com"
```

Example:

```text
My number is 9812345678.
```

produces:

```python
"9812345678"
```

---

# 15. Extracting the Need

The need extraction function searches for common caregiver-related phrases.

```python
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
```

---

# 16. Why the Need Extraction Needed Improvement

During testing, an issue was discovered.

For example:

```text
I need home care for my elderly mother. You can reach me at maya@example.com.
```

A basic extraction rule could accidentally include the contact information inside the need.

That would produce something like:

```text
I need home care for my elderly mother. You can reach me at maya@example.com
```

This is incorrect.

The extraction logic was improved so that the need stops when it reaches phrases such as:

```text
you can reach me
reach me at
my email is
my phone is
contact me at
you can contact me
```

The improved result is:

```python
{
    "name": None,
    "contact": "maya@example.com",
    "need": "I need home care for my elderly mother"
}
```

This was an important lesson:

> Extraction rules need to be tested against realistic messages because one field can accidentally capture information belonging to another field.

---

# 17. Extracting All Information

The individual extraction functions are combined into:

```python
def extract_information(message):
    return {
        "name": extract_name(message),
        "contact": extract_contact(message),
        "need": extract_need(message)
    }
```

For example:

```text
Hi, I'm Ram. My email is ram@example.com and I need care for my elderly mother.
```

The extraction result is:

```python
{
    "name": "Ram",
    "contact": "ram@example.com",
    "need": "I need care for my elderly mother"
}
```

One message can therefore provide multiple fields.

---

# 18. Updating the Existing Lead

Extraction alone is not enough.

The extracted information must be added to the existing lead.

The function used is:

```python
def update_lead(lead, extracted_information):
    if extracted_information["name"] is not None:
        lead["name"] = extracted_information["name"]

    if extracted_information["contact"] is not None:
        lead["contact"] = extracted_information["contact"]

    if extracted_information["need"] is not None:
        lead["need"] = extracted_information["need"]
```

The important rule is:

> Only update a field when new information for that field was actually extracted.

---

# 19. Why State Preservation Matters

Consider this conversation:

```text
User: Hi, I'm Anita.
```

The lead becomes:

```python
{
    "name": "Anita",
    "contact": None,
    "need": None
}
```

Then the user says:

```text
anita@gmail.com
```

The new message contains contact information but does not contain the name.

The system must NOT replace the name with `None`.

The correct result is:

```python
{
    "name": "Anita",
    "contact": "anita@gmail.com",
    "need": None
}
```

This is called state preservation.

The agent remembers information from earlier turns.

---

# 20. Multi-Turn Conversation

A lead-capture agent needs to work across multiple messages.

Example:

```text
User: Hi, I'm Anita.
Agent: Thanks. What is your phone number or email?

User: anita@gmail.com
Agent: What kind of care service do you need?

User: Care for my elderly father.
Agent: Thank you. I have recorded your information.
```

Final lead:

```python
{
    "name": "Anita",
    "contact": "anita@gmail.com",
    "need": "Care for my elderly father"
}
```

Final state:

```python
next_field = None
lead_complete = True
```

---

# 21. Creating the Agent Response

The agent needs to convert the lead state into a natural response.

The function used is:

```python
def create_agent_response(lead):
    next_field, lead_complete = check_lead(lead)

    if lead_complete:
        return "Thank you. I have recorded your information."

    if next_field == "name":
        return "Sure. May I have your name?"

    if next_field == "contact":
        return "Thanks. What is your phone number or email?"

    if next_field == "need":
        return "What kind of care service do you need?"

    return "Thank you."
```

This connects the structured lead state to the conversation.

---

# 22. Processing a User Message

The complete processing function is:

```python
def process_message(lead, user_message):
    extracted_information = extract_information(user_message)

    update_lead(lead, extracted_information)

    response = create_agent_response(lead)

    return extracted_information, response
```

The process is:

```text
User message
     ↓
Extract information
     ↓
Update existing lead
     ↓
Check lead
     ↓
Generate response
```

---

# 23. Complete Working Prototype

The complete Day 3 prototype is:

```python
import re


def find_next_field(lead):
    if lead["name"] is None:
        return "name"

    if lead["contact"] is None:
        return "contact"

    if lead["need"] is None:
        return "need"

    return None


def check_lead(lead):
    next_field = find_next_field(lead)

    if next_field is None:
        lead_complete = True
    else:
        lead_complete = False

    return next_field, lead_complete


def extract_name(message):
    name_match = re.search(
        r"(?:my name is|i am|i'm|name is)\s+([a-zA-Z]+(?:\s+[a-zA-Z]+)*)",
        message,
        re.IGNORECASE
    )

    if name_match:
        return name_match.group(1).strip()

    return None


def extract_contact(message):
    email_match = re.search(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        message
    )

    if email_match:
        return email_match.group(0)

    phone_match = re.search(r"\b\d{10}\b", message)

    if phone_match:
        return phone_match.group(0)

    return None


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


def extract_information(message):
    return {
        "name": extract_name(message),
        "contact": extract_contact(message),
        "need": extract_need(message)
    }


def update_lead(lead, extracted_information):
    if extracted_information["name"] is not None:
        lead["name"] = extracted_information["name"]

    if extracted_information["contact"] is not None:
        lead["contact"] = extracted_information["contact"]

    if extracted_information["need"] is not None:
        lead["need"] = extracted_information["need"]


def create_agent_response(lead):
    next_field, lead_complete = check_lead(lead)

    if lead_complete:
        return "Thank you. I have recorded your information."

    if next_field == "name":
        return "Sure. May I have your name?"

    if next_field == "contact":
        return "Thanks. What is your phone number or email?"

    if next_field == "need":
        return "What kind of care service do you need?"

    return "Thank you."


def process_message(lead, user_message):
    extracted_information = extract_information(user_message)

    update_lead(lead, extracted_information)

    response = create_agent_response(lead)

    return extracted_information, response


# Starting lead
lead = {
    "name": None,
    "contact": None,
    "need": None
}


# Multi-turn conversation
messages = [
    "Hi, I'm Anita.",
    "anita@gmail.com",
    "Care for my elderly father."
]


for message in messages:
    extracted_information, response = process_message(
        lead,
        message
    )

    print("User:", message)
    print("Extracted:", extracted_information)
    print("Agent:", response)
    print("Current lead:", lead)
    print("-" * 50)


next_field, lead_complete = check_lead(lead)

print("Final Lead:")
print(lead)

print("next_field:", next_field)
print("lead_complete:", lead_complete)
```

---

# 24. Expected Final Result

After running the complete program, the final lead should be:

```python
{
    "name": "Anita",
    "contact": "anita@gmail.com",
    "need": "Care for my elderly father"
}
```

The final state should be:

```text
next_field: None
lead_complete: True
```

The final agent response should be:

```text
Thank you. I have recorded your information.
```

---

# 25. Test Case 1 — All Information in One Message

Input:

```text
Hi, I'm Ram. My email is ram@example.com and I need care for my elderly mother.
```

Expected extraction:

```python
{
    "name": "Ram",
    "contact": "ram@example.com",
    "need": "I need care for my elderly mother"
}
```

Expected state:

```text
next_field = None
lead_complete = True
```

Result:

```text
PASS
```

---

# 26. Test Case 2 — Information Arrives in Different Order

First message:

```text
I need care for my elderly father.
```

Lead:

```python
{
    "name": None,
    "contact": None,
    "need": "I need care for my elderly father"
}
```

Next field:

```text
name
```

Lead is incomplete.

---

Second message:

```text
You can contact me at sita@example.com.
```

Lead:

```python
{
    "name": None,
    "contact": "sita@example.com",
    "need": "I need care for my elderly father"
}
```

Next field:

```text
name
```

Lead is still incomplete.

---

Third message:

```text
My name is Sita.
```

Final lead:

```python
{
    "name": "Sita",
    "contact": "sita@example.com",
    "need": "I need care for my elderly father"
}
```

Final state:

```text
next_field = None
lead_complete = True
```

Result:

```text
PASS
```

---

# 27. Test Case 3 — One Field Per Message

Conversation:

```text
User: Hi, I'm Anita.
Agent: Thanks. What is your phone number or email?

User: anita@gmail.com
Agent: What kind of care service do you need?

User: Care for my elderly father.
Agent: Thank you. I have recorded your information.
```

Final lead:

```python
{
    "name": "Anita",
    "contact": "anita@gmail.com",
    "need": "Care for my elderly father"
}
```

Result:

```text
PASS
```

---

# 28. Test Case 4 — Information Already Exists

Starting lead:

```python
{
    "name": "Anita",
    "contact": None,
    "need": "care for father"
}
```

User message:

```text
anita@gmail.com
```

The system extracts:

```python
{
    "name": None,
    "contact": "anita@gmail.com",
    "need": None
}
```

After updating:

```python
{
    "name": "Anita",
    "contact": "anita@gmail.com",
    "need": "care for father"
}
```

The existing name and need are preserved.

Result:

```text
PASS
```

---

# 29. Important Rule Learned

The agent must never overwrite useful existing information with `None`.

Incorrect behavior:

```python
lead["name"] = None
```

when the new message did not contain a name.

Correct behavior:

```python
if extracted_information["name"] is not None:
    lead["name"] = extracted_information["name"]
```

This rule is important for maintaining conversation state.

---

# 30. Day 3 Architecture

The complete Day 3 architecture can be represented as:

```text
                    USER MESSAGE
                         │
                         ▼
                EXTRACT INFORMATION
                         │
             ┌───────────┼───────────┐
             ▼           ▼           ▼
           NAME       CONTACT       NEED
             │           │           │
             └───────────┼───────────┘
                         ▼
                    UPDATE LEAD
                         │
                         ▼
                CHECK REQUIRED FIELDS
                         │
                         ▼
                   FIND NEXT FIELD
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
        FIELD MISSING          ALL COMPLETE
              │                     │
              ▼                     ▼
         ASK USER             LEAD COMPLETE
              │
              ▼
        NEXT USER MESSAGE
              │
              └──────────► REPEAT
```

---

# 31. Rule-Based Prototype vs Real AI

The Day 3 implementation is intentionally a simple rule-based prototype.

It uses:

* Python
* dictionaries
* functions
* `if` statements
* regular expressions
* keyword matching

It does NOT yet use a large language model to understand every possible way a customer might express information.

For example, the current system understands certain patterns such as:

```text
My name is Anita.
```

```text
I'm Anita.
```

```text
I need care for my father.
```

```text
anita@example.com
```

But a real customer might say:

```text
You can call me Anita.
```

or:

```text
I'm looking for somebody who can stay with my mother during the day.
```

The current rule-based prototype may not correctly understand every such variation.

That limitation is expected at this stage.

---

# 32. Why We Built the Rule-Based Version First

The purpose of Day 3 was not to build a production-level AI extraction system.

The purpose was to understand the underlying architecture.

Before using an LLM, it is important to understand:

```text
What information do we need?
        ↓
How do we represent it?
        ↓
How do we know what is missing?
        ↓
How do we update existing information?
        ↓
How do we know when the lead is complete?
```

Once these concepts are understood, an LLM can later be introduced to make the extraction much more flexible.

The architecture remains similar.

---

# 33. Day 3 Key Lessons

## Lesson 1 — Natural language must become structured data

Customers speak naturally, but the system needs structured fields.

Example:

```text
"My name is Ram and I need care for my mother."
```

becomes:

```python
{
    "name": "Ram",
    "need": "care for my mother"
}
```

---

## Lesson 2 — Information can arrive in any order

The customer does not necessarily provide information in the expected order.

They might provide:

```text
need → contact → name
```

or:

```text
name → need → contact
```

The lead model must preserve everything that has already been collected.

---

## Lesson 3 — One message can contain multiple fields

A customer might say:

```text
I'm Ram, my email is ram@example.com, and I need care for my mother.
```

The system should extract all three fields.

---

## Lesson 4 — Missing information determines the next question

The system should not ask randomly.

It should inspect the lead and determine the next missing required field.

---

## Lesson 5 — State must be preserved

Information from previous messages must remain available.

A new message should update the lead rather than replace the entire lead.

---

## Lesson 6 — Completion must be explicit

The agent needs a clear condition for knowing when the lead is complete.

In this project:

```text
name exists
AND
contact exists
AND
need exists
```

means:

```text
lead_complete = True
```

---

# 34. Final Day 3 Checklist

The following Day 3 objectives have all been completed:

* [x] Understand information extraction
* [x] Understand structured lead data
* [x] Understand the `name` field
* [x] Understand the `contact` field
* [x] Understand the `need` field
* [x] Understand `None`
* [x] Extract a customer's name
* [x] Extract contact information
* [x] Extract the customer's need
* [x] Combine extraction functions
* [x] Update an existing lead
* [x] Preserve previously collected information
* [x] Detect missing fields
* [x] Determine `next_field`
* [x] Determine `lead_complete`
* [x] Generate the next agent question
* [x] Handle one field per message
* [x] Handle multiple fields in one message
* [x] Handle information arriving in different orders
* [x] Build a multi-turn conversation
* [x] Test a complete lead
* [x] Test an incomplete lead
* [x] Test unusual information order
* [x] Test state preservation
* [x] Fix an extraction problem
* [x] Run the complete working prototype

---

# 35. Day 3 Final Status

```text
WEEK 3 — DAY 3

Information Extraction:       COMPLETE
Lead Updating:                COMPLETE
Missing Field Detection:      COMPLETE
Next Field Logic:             COMPLETE
Lead Completion Logic:        COMPLETE
State Preservation:           COMPLETE
Multi-Turn Conversation:      COMPLETE
Testing:                      COMPLETE
Documentation:                COMPLETE

Overall Status:               100% COMPLETE
```

---

# 36. What Has Been Built So Far

At the end of Day 3, the project has moved from a simple lead model to a basic working lead-capture engine.

The system can now:

```text
Receive a customer message
        ↓
Extract useful information
        ↓
Store information in the lead
        ↓
Keep previously collected information
        ↓
Find missing information
        ↓
Ask for the missing information
        ↓
Repeat across multiple messages
        ↓
Recognize when the lead is complete
```

This is the foundation for the caregiver-service lead-capture agent.

---

# 37. What Comes Next

Day 3 focused primarily on the internal lead-processing logic.

The next stage of the project can build on this foundation by making the agent more conversational and intelligent.

The important point is that the underlying lead structure already exists:

```python
{
    "name": ...,
    "contact": ...,
    "need": ...
}
```

and the system already knows how to determine:

```python
next_field
```

and:

```python
lead_complete
```

Future development can therefore focus on improving how the agent communicates with the customer and eventually replacing simple rule-based extraction with more flexible AI/LLM-based extraction.

---

# Final Conclusion

Week 3 Day 3 successfully established the core information-extraction and lead-update system for the caregiver-service AI agent.

The system can now convert customer messages into structured lead information, preserve state across multiple messages, identify missing required information, ask for the next field, and recognize when a lead is complete.

The Day 3 prototype is intentionally simple and rule-based. It is not yet a production-ready AI system, but it provides the correct foundation for the more advanced agent development that will follow.

**Week 3 Day 3 is fully completed.**
