# Week 3 — Day 1

## Lead Capture & Conversational Lead Collection Specification

**Project:** Saathi Sneha Care
**Week:** 3
**Day:** 1
**Focus:** Design and specification of interactive Lead Capture
**Status:** Day 1 design completed

---

# 1. Purpose of Day 1

The purpose of Day 1 is to define exactly how the Week 3 Lead Capture system should behave before implementing the database, extraction logic, and LangGraph workflow.

The Week 3 mentor requirement is:

> The agent should be able to collect a lead's name, contact information, and need when someone shows interest, and save that information.

The important part of this requirement is that the agent must not only extract information that happens to be present in a customer's first message.

The agent must also be able to **communicate with the customer and collect missing information through follow-up questions**.

Therefore, Week 3 Lead Capture is designed as an **interactive, multi-turn lead collection process**.

---

# 2. Week 3 Core Objective

By the end of Week 3, the system should be able to perform the following process:

```text
Customer shows interest
        ↓
Agent detects potential lead
        ↓
Agent extracts available information
        ↓
Agent checks what information is missing
        ↓
Agent asks for the missing information
        ↓
Customer responds
        ↓
Agent extracts the new information
        ↓
Agent updates the existing lead state
        ↓
Agent checks again for missing information
        ↓
Repeat until minimum information is complete
        ↓
Validate the collected information
        ↓
Save the lead
        ↓
Confirm that the information was recorded
```

This is the central behavior that Week 3 will implement.

---

# 3. Relationship to Week 1

Week 1 established the business and lead-capture foundation.

The original Lead Capture responsibility was to capture information such as:

* name
* contact
* need
* source
* urgency
* service interest
* other relevant lead information

Week 1 also established that the Lead Capture component should:

* preserve the source and channel when available
* extract explicit customer information
* identify need and service interest
* identify urgency signals
* identify consultation intent
* create or update a lead
* leave unavailable information unknown
* avoid inventing customer information

Lead Capture should not:

* qualify the lead
* diagnose medical conditions
* make sales decisions
* book appointments
* invent prices
* invent customer information
* make downstream qualification decisions
* own calendar logic

Therefore, Week 3 does **not** replace the Week 1 Lead Capture design.

Instead, Week 3 makes Lead Capture more interactive.

---

# 4. Relationship to Week 2

Week 2 introduced the LangGraph-based FAQ workflow.

The Week 2 FAQ workflow follows the basic pattern:

```text
START
  ↓
FAQ selection
  ↓
Answer
  ↓
END
```

The FAQ system is primarily a question → answer workflow.

Week 3 introduces a different type of workflow.

The Lead Capture workflow needs to maintain information across multiple customer messages.

For example:

```text
Customer:
"I am interested in caregiver service."

Agent:
"Sure. May I have your name?"

Customer:
"Ram Sharma"

Agent:
"What is your phone number or email?"

Customer:
"ram@example.com"

Agent:
"What kind of care do you need?"

Customer:
"Care for my elderly mother."

Agent:
"Thank you. I have recorded your information."
```

This means the Week 3 workflow requires **state**.

The system must remember:

```text
name = Ram Sharma
contact = ram@example.com
need = care for my elderly mother
```

while the conversation is still continuing.

---

# 5. Week 3 Design Principle

The most important design principle is:

## Extract first, ask second.

When a customer sends a message, the system should first determine what information is already available.

It should **not immediately ask every question**.

For example:

Customer:

> "My name is Anita and I need someone to care for my father."

The system should extract:

```text
name = Anita
need = someone to care for my father
contact = missing
```

Therefore, it should ask only:

> "Thank you, Anita. May I have your phone number or email address?"

It should not ask:

> "What is your name?"

because the customer already provided their name.

---

# 6. Minimum Required Lead Information

For the Week 3 mentor requirement, the minimum information that must be collected is:

| Field     | Required for Week 3 | Purpose                                                    |
| --------- | ------------------- | ---------------------------------------------------------- |
| `name`    | Yes                 | Identify the potential customer                            |
| `contact` | Yes                 | Provide a way to contact the customer                      |
| `need`    | Yes                 | Understand what care/service the customer is interested in |

A lead becomes **complete for Week 3** when all three fields contain usable information.

```text
name != missing
AND
contact != missing
AND
need != missing
```

Then:

```text
lead_complete = true
```

---

# 7. Important Meaning of "Complete"

`lead_complete = true` does **not** mean:

* the lead is qualified
* the customer has purchased
* a consultation is booked
* payment has been made
* the service has been confirmed
* the lead is high quality
* the customer is medically suitable

It means only:

> The minimum information required by the Week 3 Lead Capture process has been collected.

This distinction is important because Lead Capture and Lead Qualification are different responsibilities.

---

# 8. Additional Lead Information

Week 1 identified additional useful Lead fields, including:

```text
lead_id
name
contact
channel
source
need
service_interest
patient_location
urgency
preferred_contact_time
plan_interest
status
qualification_status
consultation_requested
notes
created_at
updated_at
```

These remain part of the broader Lead model.

However, they are **not all mandatory during the initial Week 3 conversational collection**.

The Week 3 minimum collection requirement is:

```text
name
contact
need
```

Other fields should be captured when they are naturally available, but the agent should not unnecessarily interrogate the customer for every possible field during the initial lead-capture conversation.

---

# 9. Information Should Not Be Invented

The system must never guess missing customer information.

For example:

Customer:

> "I need someone to care for my father."

The system knows:

```text
need = care for my father
```

But it does not know:

```text
name
contact
```

Therefore:

```text
name = None
contact = None
need = "care for my father"
```

The system must not generate:

```text
name = Unknown Customer
contact = 9800000000
```

or any other fabricated value.

Unknown information remains unknown until the customer provides it.

---

# 10. Information Can Arrive in Any Order

The customer does not have to answer questions in the exact order the agent asks them.

For example:

Agent:

> "May I have your name?"

Customer:

> "My email is [anita@gmail.com](mailto:anita@gmail.com)."

The system should recognize:

```text
contact = anita@gmail.com
```

The name is still missing.

Therefore:

```text
name = None
contact = anita@gmail.com
need = None
```

The workflow should continue by requesting the next missing field.

The system should not discard the information simply because it arrived earlier or later than expected.

---

# 11. Example: Name First

Customer:

> "I am Anita. I need someone to care for my father."

Extracted state:

```text
name = Anita
contact = None
need = someone to care for my father
```

Missing:

```text
contact
```

Agent response:

> "Thank you, Anita. May I have your phone number or email address?"

---

# 12. Example: Contact First

Customer:

> "You can reach me at [anita@gmail.com](mailto:anita@gmail.com). I am looking for care for my elderly father."

Extracted state:

```text
name = None
contact = anita@gmail.com
need = care for my elderly father
```

Missing:

```text
name
```

Agent response:

> "Thank you. May I have your name?"

The order does not matter.

---

# 13. Example: Everything Provided Immediately

Customer:

> "Hi, I'm Raj. My number is 9812345678 and I need care for my mother."

The system extracts:

```text
name = Raj
contact = 9812345678
need = care for my mother
```

All required fields are available.

Therefore:

```text
lead_complete = true
next_field = None
```

The agent should **not ask unnecessary follow-up questions**.

The workflow can move to:

```text
Validation
    ↓
Save Lead
    ↓
Confirmation
```

---

# 14. Example: Nothing Useful Provided

Customer:

> "I am interested in your service."

The system recognizes that the customer is showing interest, but no minimum lead fields have yet been provided.

State:

```text
name = None
contact = None
need = None
```

The next field should be:

```text
name
```

Agent:

> "Absolutely. May I have your name?"

After the customer answers, the state is updated rather than replaced.

---

# 15. Example: Multi-Turn Conversation

Conversation:

### Turn 1

Customer:

> "I am interested in caregiver service."

State:

```text
name = None
contact = None
need = caregiver service
next_field = name
lead_complete = false
```

Agent:

> "Sure. May I have your name?"

---

### Turn 2

Customer:

> "Ram Sharma"

Updated state:

```text
name = Ram Sharma
contact = None
need = caregiver service
next_field = contact
lead_complete = false
```

Agent:

> "Thank you, Ram. May I have your phone number or email address?"

---

### Turn 3

Customer:

> "[ram@example.com](mailto:ram@example.com)"

Updated state:

```text
name = Ram Sharma
contact = ram@example.com
need = caregiver service
next_field = None
lead_complete = true
```

The workflow can now validate and save the lead.

---

# 16. Lead State

The conversational system requires state so that information from previous messages is not lost.

The conceptual Week 3 state is:

```text
LeadState
│
├── user_message
├── name
├── contact
├── need
├── next_field
├── lead_complete
└── response
```

### `user_message`

Contains the latest customer message being processed.

Example:

```text
"Ram Sharma"
```

### `name`

Stores the customer's name when known.

Example:

```text
"Ram Sharma"
```

### `contact`

Stores the customer's phone number or email when known.

Example:

```text
"ram@example.com"
```

### `need`

Stores what the customer needs or is interested in.

Example:

```text
"care for my elderly mother"
```

### `next_field`

Identifies the next missing minimum field.

Possible values:

```text
"name"
"contact"
"need"
None
```

### `lead_complete`

Indicates whether all three minimum fields have been collected.

Possible values:

```text
True
False
```

### `response`

Contains the response the agent should send to the customer.

---

# 17. Why State Is Necessary

Without state, the agent could lose previously collected information.

Example:

Turn 1:

```text
Customer:
"My name is Ram."

State:
name = Ram
```

Turn 2:

```text
Customer:
"ram@gmail.com"
```

If the system treats Turn 2 as a completely new request, it might forget:

```text
name = Ram
```

and incorrectly conclude:

```text
name = missing
contact = ram@gmail.com
```

A stateful workflow instead produces:

```text
name = Ram
contact = ram@gmail.com
```

This is one of the main reasons LangGraph is useful for Week 3.

---

# 18. Missing-Field Detection

After every customer message, the workflow should check which required fields are still missing.

Conceptually:

```text
If name is missing:
    next_field = name

Else if contact is missing:
    next_field = contact

Else if need is missing:
    next_field = need

Else:
    next_field = None
    lead_complete = true
```

The exact implementation will be written during the implementation days.

The important Day 1 decision is the behavior.

---

# 19. Follow-Up Question Behavior

When information is missing, the agent should ask for it.

The agent should ask **one clear question at a time**.

Examples:

### Missing name

> "May I have your name?"

### Missing contact

> "May I have your phone number or email address?"

### Missing need

> "Could you tell me what kind of care or service you need?"

The questions should be:

* clear
* short
* polite
* directly related to the missing information
* free of unnecessary questions

---

# 20. The Agent Must Remember Previous Information

Suppose the customer says:

> "My name is Anita."

The agent asks:

> "What is your phone number or email?"

Customer says:

> "[anita@gmail.com](mailto:anita@gmail.com)"

The agent should understand that:

```text
name = Anita
contact = anita@gmail.com
```

It should not ask for the name again.

This is called **state accumulation**.

Each new turn adds or updates information while preserving already collected information.

---

# 21. Lead Collection Loop

The core Week 3 loop is:

```text
                 ┌─────────────────────┐
                 │ Customer Message    │
                 └──────────┬──────────┘
                            ↓
                 ┌─────────────────────┐
                 │ Extract Information │
                 └──────────┬──────────┘
                            ↓
                 ┌─────────────────────┐
                 │ Update Lead State   │
                 └──────────┬──────────┘
                            ↓
                 ┌─────────────────────┐
                 │ Check Missing       │
                 │ Fields              │
                 └──────────┬──────────┘
                            ↓
                  Are fields missing?
                       /          \
                     Yes           No
                      ↓             ↓
              Ask for next       Validate
              missing field         ↓
                      ↓           Save
              Customer replies      ↓
                      ↓          Confirm
              Update state
                      ↓
                 Check again
```

This loop is the heart of Week 3.

---

# 22. Save Condition

The target Week 3 behavior is:

```text
Do not save the final lead until:
name + contact + need
are available and usable.
```

Once the minimum information is complete:

```text
Validate
   ↓
Save
```

The database will be introduced on Day 2.

Therefore, Day 1 defines the **save condition**, but does not implement database persistence yet.

---

# 23. Validation Concept

Validation will happen after the necessary information has been collected.

Examples of things validation should eventually check:

### Name

The name should contain meaningful customer-provided information.

### Contact

The contact should look like a usable phone number or email address.

### Need

The need should contain meaningful information about what service/care the customer is seeking.

Validation should not invent or repair information in a way that changes what the customer actually said.

If validation fails, the agent should ask the customer for the information again.

---

# 24. Example of Invalid Contact

Customer:

> "My name is Ram."

Agent:

> "May I have your phone number or email address?"

Customer:

> "hello"

The system should not automatically assume:

```text
contact = hello
```

Instead, validation should identify that the contact information may not be usable.

The agent can ask:

> "Could you please provide a valid phone number or email address?"

The exact validation rules will be implemented later.

---

# 25. Privacy Boundary

The Week 3 Lead Capture process should collect only information necessary for initial lead capture.

The minimum required information is:

```text
name
contact
need
```

The agent should not unnecessarily request:

* detailed medical history
* diagnosis information
* payment information
* highly sensitive personal information
* unrelated personal information

The purpose of this workflow is **lead capture**, not medical assessment or full customer onboarding.

---

# 26. Lead Capture vs Lead Qualification

These responsibilities must remain separate.

### Lead Capture

Answers:

> "What information has the customer provided?"

It collects:

```text
name
contact
need
```

and other relevant information when available.

### Lead Qualification

Answers:

> "Does this lead meet our qualification criteria?"

Qualification may involve:

* urgency
* service fit
* location
* plan interest
* consultation intent
* other business criteria

Lead Qualification is not the main Week 3 task.

---

# 27. Lead Capture vs FAQ Agent

The existing Week 2 FAQ agent answers customer questions.

For example:

```text
Customer:
"What services do you provide?"

FAQ Agent:
"Approved FAQ answer..."
```

The Week 3 Lead Capture agent has a different purpose.

For example:

```text
Customer:
"I am interested in caregiver service."

Lead Capture:
"Sure. May I have your name?"
```

The two capabilities may eventually work together, but Week 3 should not become a large FAQ + sales + qualification system.

The primary objective remains:

```text
Interest
→ collect information
→ save lead
```

---

# 28. LangGraph's Role

LangGraph will be responsible for orchestrating the process.

Conceptually, the workflow will contain steps such as:

```text
START
  ↓
Process Customer Message
  ↓
Extract Lead Information
  ↓
Update Lead State
  ↓
Check Required Fields
  ↓
 ┌───────────────────────┐
 │ Missing information?  │
 └───────────┬───────────┘
             │
       Yes   │   No
        ↓    │    ↓
 Ask Question│ Validate
        ↓    │    ↓
 Wait/Process│ Save
 Next Message│
             ↓
           END
```

The exact node names and graph structure will be finalized during the implementation days.

---

# 29. Database's Role

The database has a separate responsibility.

LangGraph manages the workflow and state during the conversation.

The database provides persistent storage.

Conceptually:

```text
LangGraph
    ↓
Completed Lead
    ↓
Validation
    ↓
Database
```

The database should ultimately contain the collected lead information.

For Week 3, Supabase/PostgreSQL is the planned database direction.

Database setup belongs primarily to Day 2.

---

# 30. One Conversation Should Represent One Lead Collection Process

A major design consideration is avoiding this problem:

```text
Customer message 1
→ create database row

Customer message 2
→ create another database row

Customer message 3
→ create another database row
```

That would incorrectly create multiple leads for the same conversation.

Instead, the target behavior is:

```text
Conversation
   ↓
One evolving lead state
   ↓
Complete lead
   ↓
Save/update the appropriate lead record
```

The exact mechanism for identifying the same ongoing conversation and lead record will be finalized during the database and LangGraph implementation work.

---

# 31. Handling Information Provided Out of Order

The workflow must support any order.

Example:

```text
Customer:
"ram@example.com"

State:
contact = ram@example.com
name = missing
need = missing
```

Then:

```text
Customer:
"My name is Ram Sharma."

State:
contact = ram@example.com
name = Ram Sharma
need = missing
```

Then:

```text
Customer:
"I need care for my mother."

State:
contact = ram@example.com
name = Ram Sharma
need = care for my mother
```

Final:

```text
lead_complete = true
```

The workflow should not depend on a rigid sequence of customer answers.

---

# 32. Handling a Customer Who Provides Everything

Customer:

> "Hi, I'm Ram Sharma. My email is [ram@example.com](mailto:ram@example.com) and I'm looking for care for my elderly mother."

System:

```text
name = Ram Sharma
contact = ram@example.com
need = care for my elderly mother
```

No additional collection questions are necessary.

The system moves toward:

```text
Validation
→ Save
→ Confirmation
```

This is important because a good lead-capture agent should not create unnecessary friction.

---

# 33. Handling a Customer Who Refuses

Suppose:

Agent:

> "May I have your phone number or email address?"

Customer:

> "I don't want to share my number."

The system must not invent a contact.

Instead:

```text
contact = missing
```

The workflow can politely explain that contact information is needed to follow up, or allow another supported contact method such as email.

The exact refusal-handling behavior can be expanded during implementation/testing.

The fundamental rule is:

> Never fabricate information just to make `lead_complete` become true.

---

# 34. Handling Unrelated Questions

A customer may say:

> "I am interested in care for my mother. Also, what services do you provide?"

This creates two intents:

```text
Lead Capture
+
FAQ
```

This is a real integration consideration because Week 2 already contains an FAQ agent.

However, complex intent routing is **not required to complete the core Day 1 design**.

The Week 3 priority remains:

```text
Collect minimum lead information
```

FAQ/lead-routing integration can be handled later without expanding the Week 3 core unnecessarily.

---

# 35. Handling Existing Information

The system should not overwrite good existing information with empty values.

Example:

Current state:

```text
name = Ram
contact = ram@example.com
need = care for mother
```

New message:

> "I don't have anything else to add."

The system should retain:

```text
name = Ram
contact = ram@example.com
need = care for mother
```

It should not change them to `None`.

---

# 36. Handling New Information

If a customer provides a better or corrected value, the system should update the state.

Example:

Customer initially provides:

```text
contact = 9812345678
```

Later:

> "Actually, please use [ram@example.com](mailto:ram@example.com) instead."

The state can become:

```text
contact = ram@example.com
```

The implementation should preserve the latest customer-provided value when a clear correction is made.

---

# 37. Week 3 Scope

## Included

The Week 3 implementation should include:

1. Detecting potential lead interest.
2. Extracting name.
3. Extracting contact.
4. Extracting need.
5. Detecting missing required fields.
6. Asking for missing fields.
7. Receiving customer responses.
8. Maintaining state across turns.
9. Updating the lead as new information arrives.
10. Determining when the minimum lead is complete.
11. Validating collected information.
12. Saving the completed lead.
13. Confirming successful collection.
14. Testing complete conversations.
15. Testing incomplete conversations.
16. Testing multi-turn conversations.
17. Testing non-invention behavior.
18. Testing database persistence.

---

# 38. Explicitly Out of Scope

The following are not required for the core Week 3 task:

* advanced lead scoring
* complex qualification rules
* medical diagnosis
* medical recommendations
* appointment booking
* calendar integration
* payment processing
* production WhatsApp integration
* production SMS integration
* production CRM integration
* complex analytics
* automated sales closing
* advanced personalization

These may become future tasks, but they should not distract from the Week 3 mentor requirement.

---

# 39. Day-by-Day Implementation Relationship

## Day 1 — Design

Define:

```text
Lead Capture behavior
State
Required fields
Missing-field behavior
Conversation flow
Save condition
Validation concept
Edge cases
```

No database implementation is required yet.

---

## Day 2 — Database

Implement:

```text
Supabase/PostgreSQL
        ↓
Lead table
        ↓
Database connection
        ↓
Environment configuration
        ↓
Test insert
```

---

## Day 3 — Extraction

Implement:

```text
Customer message
        ↓
Information extraction
        ↓
name/contact/need
        ↓
Missing-field detection
        ↓
Validation
```

---

## Day 4 — LangGraph Integration

Connect:

```text
State
↓
Extraction
↓
Missing-field detection
↓
Question generation
↓
State update
↓
Validation
↓
Save
```

Then test multi-turn conversations.

---

## Day 5 — Verification and Evidence

Run:

```text
Existing Week 2 tests
        +
Week 3 extraction tests
        +
Lead collection tests
        +
Database tests
        +
Multi-turn tests
        +
Failure cases
```

Then prepare:

```text
Week 3 evidence
Week 3 report
README updates
Mentor requirement verification
```

---

# 40. Day 1 Final Architecture

The complete conceptual architecture for Day 1 is:

```text
                    CUSTOMER
                       │
                       ▼
              Customer Message
                       │
                       ▼
               ┌───────────────┐
               │ Lead Capture  │
               └───────┬───────┘
                       │
                       ▼
              Extract available
                 information
                       │
                       ▼
              ┌────────────────┐
              │ Update State   │
              └───────┬────────┘
                      │
                      ▼
             Check required fields
                      │
              ┌───────┴────────┐
              │                │
           Missing          Complete
              │                │
              ▼                ▼
       Ask next question    Validate
              │                │
              ▼                ▼
       Customer replies      Save
              │                │
              └───────┐        ▼
                      │     Database
                      │
                      ▼
                Update State
                      │
                      ▼
                Check Again
```

---

# 41. Day 1 Definition of Done

Day 1 is considered complete when the following have been defined:

| Requirement                                   | Status   |
| --------------------------------------------- | -------- |
| Mentor requirement understood                 | COMPLETE |
| Interactive collection requirement understood | COMPLETE |
| Lead Capture responsibility defined           | COMPLETE |
| Lead Capture boundaries defined               | COMPLETE |
| Minimum required fields defined               | COMPLETE |
| Optional/additional fields identified         | COMPLETE |
| Extraction behavior defined                   | COMPLETE |
| Missing-field behavior defined                | COMPLETE |
| Follow-up question behavior defined           | COMPLETE |
| Multi-turn state defined                      | COMPLETE |
| Information accumulation defined              | COMPLETE |
| Lead completeness rule defined                | COMPLETE |
| Save condition defined                        | COMPLETE |
| Validation concept defined                    | COMPLETE |
| LangGraph role defined                        | COMPLETE |
| Database role defined                         | COMPLETE |
| Privacy boundary defined                      | COMPLETE |
| Edge cases documented                         | COMPLETE |
| Complete conversation example documented      | COMPLETE |
| Incomplete conversation example documented    | COMPLETE |
| Out-of-order information documented           | COMPLETE |
| Non-invention rule documented                 | COMPLETE |
| Week 3 scope defined                          | COMPLETE |
| Out-of-scope items defined                    | COMPLETE |

---

# 42. Day 1 Final Decision

The Week 3 Lead Capture agent will **not** be designed as a simple one-shot extractor.

Instead, it will be designed as a:

> **Stateful conversational Lead Capture workflow that extracts information from customer messages, identifies missing required fields, asks targeted follow-up questions, accumulates information across turns, validates the completed lead, and saves it to a database.**

The minimum lead information required for completion is:

```text
name
contact
need
```

The central workflow is:

```text
Extract
   ↓
Update State
   ↓
Check Missing Fields
   ↓
Ask
   ↓
Receive Response
   ↓
Update State
   ↓
Repeat
   ↓
Validate
   ↓
Save
```

This is the foundation for the actual Week 3 implementation.

---

# 43. Final Mentor Requirement Mapping

The mentor requirement:

> "Agent can collect a lead's name/contact/need when someone shows interest, and save it."

will be satisfied as follows:

### "Agent can collect"

The agent actively asks for information that is missing.

### "a lead's name"

The workflow extracts or asks for the customer's name.

### "contact"

The workflow extracts or asks for a phone number or email.

### "need"

The workflow extracts or asks what care/service the customer needs.

### "when someone shows interest"

The workflow starts lead collection when the customer expresses interest in the service or communicates a relevant care/service need.

### "and save it"

Once the minimum information is complete and validated, the lead is persisted in the database.

Therefore:

```text
Interest
   ↓
Lead Capture
   ↓
Name
Contact
Need
   ↓
Validation
   ↓
Database
```

is the exact Week 3 target.

---

# 44. Day 1 Evidence to Preserve

The following should be kept as Week 3 Day 1 evidence:

1. This Lead Capture specification.
2. The LeadState design.
3. The conversational workflow.
4. The required-field definition.
5. The example conversations.
6. The scope and boundary definition.
7. The Week 3 implementation plan.
8. The Day 1 completion checklist.

These documents demonstrate that the implementation was designed before coding rather than being built without a defined behavior.

---

# 45. Status at the End of Day 1

## Completed

```text
Business requirement understood
        ↓
Lead Capture scope understood
        ↓
Interactive collection requirement identified
        ↓
Required fields defined
        ↓
State defined
        ↓
Missing-field behavior defined
        ↓
Conversation loop defined
        ↓
Save condition defined
        ↓
Validation concept defined
        ↓
Database role defined
        ↓
LangGraph role defined
        ↓
Edge cases defined
        ↓
Implementation boundaries defined
```

## Not Yet Implemented

```text
Database
Supabase connection
Lead table
Extraction code
Validation code
LangGraph Lead Capture graph
Interactive runtime
Database persistence
Automated tests
```

Those belong to Days 2–5.

---

# 46. Day 1 Conclusion

The key lesson from Day 1 is that **lead capture is not simply extracting three fields from one message**.

A real lead may provide information gradually.

For example:

```text
Message 1:
"I need care for my mother."

Message 2:
"My name is Ram."

Message 3:
"ram@example.com"
```

The system must combine all three messages into one lead:

```text
name = Ram
contact = ram@example.com
need = care for my mother
```

Only after the required information has been collected should the workflow proceed to validation and saving.

This stateful conversational behavior is the main new capability being introduced in Week 3.
