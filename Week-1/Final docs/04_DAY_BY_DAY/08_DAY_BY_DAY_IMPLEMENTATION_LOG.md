# Day-by-Day Week 1 Implementation Log

## Purpose

This document records the actual learning and implementation progression from Day 1 through Day 6.

It is not only a list of tasks. It explains why each day existed and how the work led to the next day.

---

# DAY 1 - UNDERSTANDING

## 1. Main Goal

Day 1 was intentionally about understanding rather than coding.

The purpose was to establish:

- what the project is,
- which track is being handled,
- what the wider architecture looks like,
- what evidence can be trusted,
- where agent boundaries should exist.

---

## 2. Main Agreements

The Day 1 agreements were:

1. Start from zero.
2. Documentation before implementation.
3. Day 1 is understanding, not coding.
4. Never guess the current business process.
5. Use `UNKNOWN` when evidence is unavailable.
6. Separate `CURRENT` from `TARGET`.
7. Facebook is the first implementation target.
8. Normalize messages before downstream agents.
9. Keep agent scopes separate.
10. Scheduling is separate.
11. Content starts from an approved source brief.
12. Lead Capture should not qualify.
13. Qualification should not invent rules.
14. Sales Follow-up should not own calendar logic.
15. Agents must not invent customer data, prices, or medical claims.

---

## 3. Main Day 1 Lesson

The architecture should not start with:

```text
Write code
   ↓
Connect APIs
   ↓
Hope the workflow matches the business
```

Instead:

```text
Understand
   ↓
Evidence
   ↓
Boundaries
   ↓
Data / Interface Design
   ↓
Local Implementation
   ↓
Testing
   ↓
Integration
```

This became the foundation for the following days.

---


# DAY 2 - PUBLIC BUSINESS INVESTIGATION

## 1. Main Goal

Day 2 focused on the publicly visible business.

The Week 1 evidence constraint was:

> Work from assumptions and public information only: website + social profiles.

Therefore Day 2 was not treated as an internal process audit.

---

## 2. Website

The public website investigated was:

```text
https://www.saathisnehacare.com/
```

The public site presents professional medical/home care in Nepal.

It emphasizes:

- care for parents,
- families abroad,
- professional home care,
- updates about parents' health,
- care services and plans.

---

## 3. Public Customer Journey

The public customer journey was:

```text
Free Consultation
      ↓
Personalized Plan
      ↓
Care Begins
      ↓
Stay Connected
```

This was documented as public-facing information.

It was not automatically converted into the internal technical lifecycle.

---

## 4. Public Customer / Market Understanding

Public positioning included:

- parents living in Nepal,
- families abroad,
- people needing professional home care,
- families wanting health updates.

Working assumption:

> A likely Lead may be an adult child or family member living away from Nepal who is looking for care/support for a parent or loved one in Nepal.

This was marked as an assumption.

---

## 5. Public Contact Entry Points

Identified public entry points included:

- WhatsApp
- Messenger
- Instagram
- Phone
- Website/contact journey

The website stated:

- care team contact within 24 hours,
- emergency line available 24/7.

---

## 6. Public Services

The investigation recorded:

- Caregiver Support
- Hospital Escort
- Chronic Disease Monitoring
- Doctor Consult
- Lab Coordination
- Medication Management
- Wellness Checks
- Emergency/on-demand support
- Other healthcare coordination

---

## 7. Public Plans

The investigation recorded:

- Care Connect
- Wellness Plus
- Chronic Care

Public features included:

- wellness checks,
- family dashboard/app access,
- dedicated care manager,
- vitals,
- family health reports,
- medicine coordination/refills,
- monthly doctor review.

The public existence of these services/plans was treated as confirmed.

The internal plan recommendation rules remained unknown.

---

## 8. Channel Direction

The project direction established:

```text
Facebook → first implementation target
WhatsApp → later two-way integration
TikTok → outbound content + human monitoring
Viber → later / nice-to-have
```

These are directions, not proof of current integrations.

---

## 9. Source vs Channel

A key Day 2/3 lesson was:

```text
source  = where the Lead came from
channel = where the conversation is happening
```

Example:

```text
source  = facebook_ad
channel = whatsapp
```

This distinction later became part of the Lead data model.

---

# DAY 3 - DATA AND INTERFACE DESIGN

## 1. Main Goal

Day 3 connected the business understanding to technical design.

The bridge was:

```text
Business Understanding
        ↓
Data / Interface Design
        ↓
Later Implementation
```

---

## 2. NormalizedMessage

The common message contract was defined as:

```text
sender_id
channel
text
timestamp
attachments
```

The conceptual JSON structure was:

```json
{
  "channel": "...",
  "sender_id": "...",
  "text": "...",
  "timestamp": "...",
  "attachments": []
}
```

The reason for normalization was to keep platform-specific logic outside downstream agents.

---

## 3. Lead Schema

The target Lead structure included:

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

Not all fields are required at initial capture.

---

## 4. Data Rule

If the customer does not provide information:

```text
keep it null/unknown
```

Do not invent:

- name,
- contact,
- location,
- service,
- plan,
- price,
- qualification,
- medical information.

---

## 5. Agent Contracts

The design established:

| Agent | Input | Output |
|---|---|---|
| Lead Capture | Normalized Message | Lead Record |
| Lead Qualification | Lead + Rules | Qualification Result |
| Sales Follow-up | Lead + Conversation | Response + Updated Lead |
| Scheduling | Consultation Request | Booking Result |
| Content | Source Brief | Platform Content |

These are design contracts, not confirmed production APIs.

---

## 6. Lifecycle

The initial idea was:

```text
new
 ↓
contacted
 ↓
booked
```

It was then expanded conceptually:

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

Possible branches:

```text
not_qualified
inactive
human_handoff
```

---

## 7. Five Core Test Cases

The five core cases became the bridge into Day 4.

### Case 1

General service inquiry.

Expected:

- no invented service,
- no invented need.

### Case 2

Specific caregiver-support inquiry.

Expected:

```text
service_interest = caregiver_support
```

### Case 3

Potential urgent request.

Expected:

- preserve need,
- flag potential urgency,
- no diagnosis,
- no unsupported emergency classification.

### Case 4

Pricing inquiry.

Expected:

- detect pricing intent,
- no invented price.

### Case 5

Consultation request.

Expected:

```text
consultation_requested = true
```

Not:

```text
booked
```

---

# DAY 4 - LOCAL LEAD CAPTURE PROTOTYPE

## 1. Main Goal

Day 4 turned the Day 3 design into a small local and testable implementation.

The pipeline was:

```text
Sample Channel Message
        ↓
Normalized Message
        ↓
Lead Capture
        ↓
Lead Record
        ↓
Validation
        ↓
Expected Test Result
```

---

## 2. Day 4 Goals

1. Set up local Python project.
2. Create clean project structure.
3. Represent normalized message in code.
4. Represent Lead in code.
5. Implement simple Lead Capture.
6. Run five Day 3 test cases.
7. Validate outputs.
8. Add automated tests.
9. Document decisions and unknowns.
10. Prepare Lead Capture for later LangGraph integration.

---

## 3. Local Technical Direction

The Day 4 prototype used:

- Python,
- Pydantic data models,
- NormalizedMessage,
- Lead,
- deterministic Lead Capture,
- validation rules,
- automated tests,
- a simple main entry point,
- Day 4 decision/unknown documentation.

---

## 4. Project Structure

The recommended starter structure was:

```text
week1/day4/
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── message.py
│   │   └── lead.py
│   ├── agents/
│   │   ├── __init__.py
│   │   └── lead_capture.py
│   ├── validation/
│   │   ├── __init__.py
│   │   └── rules.py
│   └── main.py
├── tests/
│   ├── test_message.py
│   ├── test_lead.py
│   └── test_lead_capture.py
├── day4-test-results.md
├── day4-decisions-and-unknowns.md
└── day4-summary.md
```

This was a recommended starter structure, not a confirmed production repository structure.

---

## 5. Why Deterministic Logic Was Used First

The purpose was to prove the data flow before adding LLM behavior.

The desired first flow was:

```text
input
  ↓
known transformation
  ↓
structured output
  ↓
validation
```

This made the system easier to understand and test.

---

## 6. Day 4 Lead Capture Boundaries

Lead Capture:

- reads normalized message,
- preserves channel,
- preserves source when known,
- extracts supported information,
- leaves missing information unknown/null,
- sets initial target status,
- avoids qualification,
- avoids pricing decisions,
- avoids medical decisions.

It must not:

- invent customer data,
- diagnose,
- invent qualification criteria,
- own calendar logic,
- invent prices,
- claim booking.

---

## 7. Day 4 Learning Order

```text
Python dictionaries / JSON
        ↓
Data models
        ↓
Functions
        ↓
Validation
        ↓
Lead Capture
        ↓
Test cases
        ↓
Automated tests
        ↓
LangGraph node concept
```

The main lesson was:

> Understand the data flow before copying an orchestration framework tutorial.

---

## 8. What Day 4 Proved

The implementation demonstrated:

```text
Sample Message
      ↓
Normalized Message Object
      ↓
Lead Capture
      ↓
Lead Record
      ↓
Validation
      ↓
Expected Test Result
```

The system could be explained in terms of:

- why messages are normalized,
- how a Lead is created,
- what came from the customer,
- what was extracted,
- what remained unknown,
- why Lead Capture does not qualify,
- why pricing is not invented,
- why medical decisions are not invented,
- how the function can later become a workflow node.

---

# DAY 5 - LIFECYCLE, STATE, WORKFLOW, AND TESTING

## 1. Main Goal

Day 5 moved from a set of functions to workflow thinking.

---

## 2. Day 5 Tasks

The agreed plan was:

1. Review Day 4 implementation.
2. Verify existing tests.
3. Add explicit extraction thinking.
4. Introduce lifecycle/status-transition thinking.
5. Create lifecycle module.
6. Introduce minimal shared state.
7. Convert Lead Capture into a node-like function.
8. Add expanded tests.
9. Add negative tests.
10. Create test fixtures.
11. Prepare LangGraph boundary.
12. Document Day 5 decisions and unknowns.

All agreed tasks were completed.

---

## 3. Lifecycle Module

The lifecycle module introduced:

```text
ALLOWED_TRANSITIONS
is_transition_allowed()
transition_lead()
```

The principle became:

```text
A Lead cannot jump arbitrarily between states.
```

---

## 4. GraphState

Shared state was introduced:

```python
class GraphState(BaseModel):
    message: NormalizedMessage
    lead: Lead | None = None
    errors: list[str] = Field(default_factory=list)
```

This allowed the workflow to pass:

```text
message
lead
errors
```

through its steps.

---

## 5. Lead Capture Node

The business function:

```text
capture_lead()
```

was separated from the workflow node:

```text
lead_capture_node()
```

The relationship is:

```text
GraphState
   ↓
lead_capture_node()
   ↓
capture_lead()
   ↓
Lead
   ↓
GraphState
```

---

## 6. Validation-Gate Bug

A negative test revealed an important workflow issue.

Input included:

- empty channel,
- consultation intent.

Validation correctly found:

```text
Channel is required.
```

But the initial workflow still allowed:

```text
new
 ↓
consultation_requested
```

The workflow was corrected.

Final behavior:

```text
Invalid Lead
     ↓
Validation Error
     ↓
STOP
```

This is one of the most important implementation lessons from Week 1.

---

## 7. Testing

The Day 5 final test state was:

```text
29 passed
```

The suite covered:

- Lead model,
- Lead Capture,
- lifecycle,
- NormalizedMessage,
- GraphState,
- workflow,
- negative behavior.

---

## 8. Fixtures

Reusable fixtures were introduced through:

```text
tests/conftest.py
```

A `caregiver_message` fixture was used.

The full suite remained:

```text
29 passed
```

---

## 9. LangGraph Boundary

The project did not force the business logic into LangGraph during Day 5.

The intended separation is:

```text
Business logic:
capture_lead()
validate_lead()
transition_lead()

Workflow:
run_lead_workflow()

State:
GraphState

Future orchestration:
LangGraph
```

---

# DAY 6 - FINALIZATION

## 1. Main Goal


The focus is:

```text
Business discovery
+
Technical foundation
+
Evidence
+
Final documentation
+
Kickoff preparation
```

---

## 2. Task 1 - Finish Funnel Audit

Complete the Week 1 audit for:

- website,
- ads,
- social,
- inbound Lead handling.

Separate:

- confirmed information,
- assumptions,
- unknowns,
- target behavior.

---

## 3. Task 2 - Finalize Agent Scope

Finalize boundaries for:

- Lead Capture,
- Lead Qualification,
- Content,
- Sales Follow-up.

The goal is to prevent overlap.

---

## 4. Task 3 - Finalize Lead Data Dictionary

For each Lead field, document:

- name,
- meaning,
- type,
- required/optional,
- owner,
- population timing,
- allowed values,
- example,
- implementation status.

---

## 5. Task 4 - Verify Development Environment

The environment must be documented from actual project setup.

The provided context confirms the technical direction but does not provide exact versions.

Therefore exact versions must not be invented.

---

## 6. Task 5 - Run All Tests

The command defined in the Day 6 plan is:

```powershell
pytest
```

The Day 5 baseline was:

```text
29 passed
```

Day 6 should verify that the current repository remains passing after final changes.

---

## 7. Task 6 - Create Week 1 Evidence

Evidence categories include:

- repository structure,
- models,
- Lead Capture,
- lifecycle,
- GraphState,
- workflow,
- tests,
- test output,
- fixtures,
- documentation,
- funnel audit,
- agent scope,
- data dictionary,
- environment verification.

---

## 8. Task 7 - Create Final Report

The final report should contain:

1. Week 1 objectives
2. Work completed
3. Technical implementation
4. Funnel audit findings
5. Agent scope
6. Lead data dictionary
7. Development environment
8. Testing results
9. Evidence
10. Known gaps
11. Unknowns
12. Follow-up questions

---

## 9. Task 8 - Prepare Kickoff Questions

Questions should target unresolved decisions.

Business:

- actual Lead sources,
- qualified Lead definition,
- sales-ready definition,
- human handoff.

Data:

- mandatory fields,
- customer-provided vs internal fields,
- lifecycle values.

Integrations:

- first channels,
- CRM,
- booking system.

Agent responsibility:

- where Lead Capture stops,
- where Qualification begins,
- when Sales Follow-up takes over.

---

# Final Week 1 State

The final intended Week 1 structure is:

```text
BUSINESS DISCOVERY
        |
        +-- Funnel Audit
        +-- Agent Scope
        +-- Data Dictionary

TECHNICAL FOUNDATION
        |
        +-- Lead Models
        +-- Lead Capture
        +-- Validation
        +-- Lifecycle
        +-- GraphState
        +-- Workflow
        +-- Tests

        ↓
        
WEEK 1 EVIDENCE

        ↓

FINAL REPORT

        ↓

KICKOFF QUESTIONS
```
