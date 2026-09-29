# Week 1 Decisions, Assumptions, Unknowns, and Open Items

## 1. Purpose

This document keeps confirmed decisions separate from assumptions and unknowns.

This is important because the project must not turn missing business information into hard-coded rules.

---

# 2. Confirmed Project Agreements

The following agreements were established:

1. Understand before implementing.
2. Use public evidence where internal information is unavailable.
3. Mark unknown information as unknown.
4. Separate current state from target state.
5. Normalize incoming messages.
6. Keep agent scopes separate.
7. Scheduling remains separate.
8. Lead Capture does not qualify.
9. Qualification uses approved rules.
10. Sales Follow-up does not own calendar logic.
11. Do not invent customer information.
12. Do not invent pricing.
13. Do not make medical diagnoses.
14. Validate before lifecycle progression.
15. Control lifecycle transitions.
16. Keep business logic separate from orchestration.

---

# 3. Confirmed Public Business Information

The public investigation established that the website presents:

- professional medical/home care,
- care for parents,
- support for families abroad,
- public services,
- public plans,
- public contact paths.

Public services included:

- Caregiver Support,
- Hospital Escort,
- Chronic Disease Monitoring,
- Doctor Consult,
- Lab Coordination,
- Medication Management,
- Wellness Checks,
- Emergency/on-demand support,
- other healthcare coordination.

Public plans included:

- Care Connect,
- Wellness Plus,
- Chronic Care.

---

# 4. Assumptions

## 4.1 Likely Lead Profile

A likely Lead may be an adult child or family member living away from Nepal looking for care for a parent or loved one.

This is an assumption.

---

## 4.2 Funnel Hypothesis

The working funnel is:

```text
Discovery
 ↓
Inquiry
 ↓
Lead Capture
 ↓
Need Understanding
 ↓
Qualification
 ↓
Consultation
 ↓
Plan Recommendation
 ↓
Enrollment / Booking
 ↓
Care Begins
```

This is a target/assumption model.

---

## 4.3 Channel Direction

The project direction includes:

```text
Facebook → first implementation
WhatsApp → later two-way integration
TikTok → outbound + human monitoring
Viber → later
```

These are directions, not proof of current production state.

---

# 5. Unknown Business Rules

The following remain unresolved:

- actual Lead sources,
- channel ownership,
- current CRM,
- current Lead assignment,
- qualification criteria,
- sales-ready definition,
- human handoff,
- pricing response rules,
- plan recommendation rules,
- exact scheduling handoff,
- booking platform,
- lifecycle ownership.

---

# 6. Unknown Technical Details

The provided context discussed:

- Python,
- LangChain,
- LangGraph,
- FastAPI,
- FastMCP / MCP,
- local development,
- VS Code / Cursor.

Still unknown:

- exact versions,
- database,
- LLM/provider,
- package manager,
- final repository structure,
- deployment,
- testing framework version,
- production environment,
- authentication/security details.

These should be verified from the actual project rather than guessed.

---

# 7. Implemented Technical Decisions

The local implementation established:

```text
NormalizedMessage
        ↓
Lead
        ↓
Validation
        ↓
Lifecycle
        ↓
GraphState
        ↓
Lead Capture Node
        ↓
Workflow
```

---

# 8. Important Technical Decision

Validation must happen before lifecycle progression.

Incorrect:

```text
Lead
 ↓
Lifecycle
 ↓
Validation
```

Correct:

```text
Lead
 ↓
Validation
 ↓
if invalid → STOP
 ↓
if valid → Lifecycle
```

---

# 9. Important Data Decision

Missing data remains missing.

For example:

```text
name = null
contact = null
patient_location = null
```

is valid when the customer has not provided those values.

---

# 10. Important Booking Decision

The following must remain separate:

```text
consultation_requested = true
```

and:

```text
status = booked
```

A request is not proof of a completed booking.

---

# 11. Future Work

The following are not Week 1 completed production features:

- real channel integrations,
- CRM,
- database persistence,
- booking integration,
- human handoff mechanism,
- complete Qualification engine,
- full LangGraph application,
- production deployment.

---

# 12. Decision Rule for Week 2

The recommended decision process is:

```text
UNKNOWN
   ↓
ASK
   ↓
BUSINESS DECISION
   ↓
DOCUMENT
   ↓
IMPLEMENT
   ↓
TEST
```

This prevents the system from silently turning assumptions into business rules.
