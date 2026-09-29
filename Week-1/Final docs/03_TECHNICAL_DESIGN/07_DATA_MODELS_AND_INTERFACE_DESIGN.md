# Data Models, Interfaces, Validation, Lifecycle, State, and Workflow Design

## 1. Purpose

This document explains the technical design developed from Day 3 through Day 5.

It is intentionally detailed because the project is being learned step by step.

---

# 2. NormalizedMessage

## 2.1 Structure

The common message structure contains:

```text
sender_id
channel
text
timestamp
attachments
```

Conceptual JSON:

```json
{
  "channel": "...",
  "sender_id": "...",
  "text": "...",
  "timestamp": "...",
  "attachments": []
}
```

---

# 3. Why Normalization Exists

Different platforms can send different payloads.

For example:

```text
Facebook payload
WhatsApp payload
Website payload
TikTok payload
```

If Lead Capture understands each raw platform format, the Lead Capture logic becomes tied to every platform.

Instead:

```text
Facebook
WhatsApp
Website
TikTok
   ↓
Channel Adapter
   ↓
NormalizedMessage
   ↓
Lead Capture
```

Now Lead Capture can work with one common structure.

---

# 4. Possible Future Message Metadata

During Day 3, additional fields were considered:

- `message_id`
- `conversation_id`
- sender name
- metadata
- attachment structure
- empty-message handling

These were not all confirmed as final fields.

They remain design considerations rather than production requirements.

---

# 5. Lead Model

The target Lead model is:

```json
{
  "lead_id": "...",
  "name": null,
  "contact": null,
  "channel": "...",
  "source": "...",
  "need": null,
  "service_interest": null,
  "patient_location": null,
  "urgency": null,
  "preferred_contact_time": null,
  "plan_interest": null,
  "status": "new",
  "qualification_status": "unknown",
  "consultation_requested": false,
  "notes": [],
  "created_at": "...",
  "updated_at": "..."
}
```

This is a target technical design, not a confirmed CRM schema.

---

# 6. Data Rule: Do Not Invent

A central design rule is:

If the customer does not provide a value:

```text
keep it unknown/null
```

Do not invent:

- name,
- phone number,
- location,
- service,
- plan,
- price,
- qualification,
- medical information.

This rule appears throughout Lead Capture, validation, and testing.

---

# 7. Lead Capture Function

The business logic is represented by:

```text
capture_lead()
```

Input:

```text
NormalizedMessage
```

Output:

```text
Lead
```

The function extracts supported information and creates a structured Lead.

---

# 8. Deterministic First Implementation

Day 4 intentionally used deterministic extraction logic first.

The reason was to prove:

```text
Input
  ↓
Known transformation
  ↓
Structured output
  ↓
Validation
```

before introducing LLM uncertainty.

This made the early system easier to understand and test.

---

# 9. Validation

Validation was kept separate from Lead Capture.

The validation layer checks:

- channel,
- source,
- Lead ID,
- lifecycle status,
- qualification status.

The architecture is:

```text
Lead Capture
     ↓
Lead
     ↓
Validation
```

Validation does not fill missing information.

---

# 10. Validation Rules

The agreed rules include:

1. `channel` must not be empty.
2. `sender_id` should exist for channel conversations.
3. `text` may be empty only for supported attachment-only messages.
4. Never infer missing customer information.
5. Never assign qualification status without approved rules.
6. Do not classify emergencies solely from a keyword without escalation rules.
7. Do not invent prices.
8. Do not provide medical diagnosis.
9. Invalid status values should be flagged.
10. Unsupported qualification values should be flagged.

---

# 11. Lifecycle Thinking

Before Day 5, status could be thought of as a simple field.

Day 5 introduced a stronger model:

> Status is a lifecycle state, and movement between states must be controlled.

The initial concept was:

```text
new
 ↓
contacted
 ↓
booked
```

It was expanded into:

```text
new
 ↓
contacted
 ↓
needs_information
 ↓
qualified
 ↓
consultation_requested
 ↓
booked
 ↓
converted
```

Possible branches include:

```text
not_qualified
inactive
human_handoff
```

These are target/proposed workflow states.

---

# 12. Lifecycle Module

The lifecycle rules are stored in the lifecycle module.

Important components:

```text
ALLOWED_TRANSITIONS
is_transition_allowed()
transition_lead()
```

The transition process is:

```text
Current Status
      +
Requested Status
      ↓
Lifecycle Rules
      ↓
Allowed?
   /       \
 Yes       No
  |         |
  ↓         ↓
Update    Reject
```

An invalid transition raises an error rather than silently changing the status.

---

# 13. Shared Workflow State

Day 5 introduced:

```text
GraphState
```

Conceptually:

```python
class GraphState(BaseModel):
    message: NormalizedMessage
    lead: Lead | None = None
    errors: list[str] = Field(default_factory=list)
```

The state contains:

```text
message
lead
errors
```

The purpose is to provide a consistent structure between workflow steps.

---

# 14. Lead Capture Node

Day 5 separated business logic from workflow-node behavior.

## Business function

```text
capture_lead()
```

Input:

```text
NormalizedMessage
```

Output:

```text
Lead
```

## Workflow node

```text
lead_capture_node()
```

Input:

```text
GraphState
```

Output:

```text
GraphState
```

The flow is:

```text
GraphState
   ↓
lead_capture_node()
   ↓
capture_lead()
   ↓
Lead
   ↓
Updated GraphState
```

---

# 15. Workflow Runner

The workflow was introduced as:

```text
run_lead_workflow(state)
```

The current flow is:

```text
GraphState
     ↓
Lead Capture Node
     ↓
Validate Lead
     ↓
If invalid → STOP
     ↓
If valid → lifecycle transition
     ↓
Updated GraphState
```

The workflow coordinates responsibilities.

It should not become the place where every business rule is written.

---

# 16. Important Validation-Gate Bug

A key learning moment happened during negative testing.

The test used:

- empty channel,
- explicit consultation intent.

Validation correctly returned:

```text
Channel is required.
```

However, the first workflow behavior still allowed:

```text
new
 ↓
consultation_requested
```

even though the Lead was invalid.

That was incorrect.

The workflow was changed to:

```text
Invalid Lead
     ↓
Validation Error
     ↓
STOP
```

This established an important rule:

> An invalid Lead must not move forward through the lifecycle.

---

# 17. Five Core Behavioral Tests

## Test 1 - General inquiry

Input:

```text
I would like to know more about your services.
```

Expected:

- no specific service invented,
- no specific need invented,
- missing information remains unknown.

---

## Test 2 - Specific service inquiry

Input:

```text
Do you provide caregiver support for elderly parents?
```

Expected:

```text
service_interest = caregiver_support
```

because the customer explicitly stated the service interest.

---

## Test 3 - Potential urgent request

Input:

```text
I need someone to check on my mother today.
She is alone and not well.
```

Expected:

- preserve stated need,
- flag potential urgency,
- do not diagnose,
- do not automatically declare an emergency,
- use approved escalation rules when known.

Internal escalation rules are still unknown.

---

## Test 4 - Pricing inquiry

Input:

```text
How much does your monthly home care package cost?
```

Expected:

- detect pricing intent,
- keep `plan_interest` null if no plan was named,
- do not invent a price.

---

## Test 5 - Consultation request

Input:

```text
I would like to schedule a consultation to discuss care options for my father.
```

Expected:

```json
{
  "consultation_requested": true
}
```

It must not automatically become:

```text
status = booked
```

---

# 18. Important Information Distinctions

For every test and future implementation, separate:

1. Customer-provided information.
2. Extracted information.
3. Missing information.
4. Unknown business rules.

Example:

Customer asks for a consultation.

Supported:

```text
consultation_requested = true
```

Not supported:

```text
status = booked
```

because no actual booking has occurred.

---

# 19. LangGraph Boundary

LangGraph is treated as a future orchestration layer.

The Week 1 separation is:

### Business logic

```text
capture_lead()
validate_lead()
transition_lead()
```

### Workflow

```text
run_lead_workflow()
lead_capture_node()
```

### State

```text
GraphState
```

### Future orchestration

```text
LangGraph
```

The purpose is to make the local logic understandable and testable before introducing the orchestration framework.

---

# 20. Current Technical Architecture

```text
INCOMING MESSAGE
        |
        v
NormalizedMessage
        |
        v
GraphState
        |
        v
Lead Capture Node
        |
        v
capture_lead()
        |
        v
Lead
        |
        v
validate_lead()
        |
    +---+---+
    |       |
 invalid   valid
    |       |
    v       v
  STOP   lifecycle rules
            |
            v
    transition_lead()
            |
            v
      Updated Lead
            |
            v
       GraphState
```

---

# 21. Testing Baseline

At the end of Day 5:

```text
29 passed
```

This was the recorded baseline after:

- model tests,
- Lead Capture tests,
- lifecycle tests,
- NormalizedMessage tests,
- GraphState tests,
- workflow tests,
- negative tests,
- fixture-based tests.

Day 6 is expected to verify the current project still passes after any final changes.

---

# 22. Test Fixtures

Reusable test fixture support was introduced through:

```text
tests/conftest.py
```

A reusable `caregiver_message` fixture was used.

The benefit is:

```text
Reusable fixture
      ↓
Test
      ↓
Workflow
      ↓
Assertions
```

rather than constructing identical test input repeatedly.

---

# 23. What the Technical Foundation Proves

The Week 1 prototype demonstrates that the project can:

1. represent an incoming message,
2. normalize it,
3. extract supported Lead information,
4. create a Lead,
5. validate the Lead,
6. reject invalid data,
7. apply controlled lifecycle transitions,
8. pass data through shared state,
9. execute a workflow-shaped sequence,
10. test both positive and negative behavior.

---

# 24. What It Does Not Prove

It does not prove that the project already has:

- real Facebook integration,
- real WhatsApp integration,
- real website integration,
- production CRM,
- production database,
- real appointment booking,
- real human handoff,
- complete Lead Qualification,
- full LangGraph application,
- production deployment.

These remain future work or unknowns.
