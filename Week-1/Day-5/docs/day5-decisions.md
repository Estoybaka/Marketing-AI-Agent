# Day 5 — Decisions and Unknowns

## 1. Purpose

Day 5 focused on moving the Lead Capture prototype from a collection of
functions toward a workflow-oriented architecture.

The main areas introduced or clarified were:

- explicit extraction thinking
- lead lifecycle/status transitions
- shared workflow state
- node-like Lead Capture behavior
- workflow validation
- negative testing
- reusable test fixtures
- preparation for a future workflow orchestration framework

---

## 2. Lead Capture Responsibility

Lead Capture is responsible for extracting supported information from an
incoming normalized message.

Lead Capture currently:

- preserves the communication channel
- preserves the source
- detects supported service interest
- detects explicit consultation intent
- detects potential urgency
- preserves certain explicitly stated needs
- detects explicitly named plan interest
- records pricing inquiry notes

Lead Capture does not:

- qualify the lead
- diagnose a patient
- invent pricing
- book an appointment
- make a final sales decision

This separation keeps Lead Capture focused on extraction rather than
downstream decision-making.

---

## 3. Lifecycle Decision

Lead lifecycle states are represented explicitly.

The lifecycle transition rules are stored separately from Lead Capture.

Allowed transitions are defined in:

`src/lifecycle/transitions.py`

The `transition_lead()` function is responsible for applying an allowed
transition.

An invalid lifecycle transition raises an error rather than silently
changing the Lead status.

---

## 4. Shared State Decision

A shared `GraphState` model was introduced.

It currently contains:

- `message`
- `lead`
- `errors`

The purpose of shared state is to provide a consistent structure that can
be passed between workflow steps.

This separates workflow state from individual agent implementation details.

---

## 5. Lead Capture Node Decision

Lead Capture was separated into two levels:

### Business logic

`capture_lead()`

This function receives a `NormalizedMessage` and creates a `Lead`.

### Workflow node

`lead_capture_node()`

This function receives `GraphState`, runs Lead Capture, and returns an
updated `GraphState`.

This separation creates a clean boundary between business logic and
workflow orchestration.

---

## 6. Validation Decision

The workflow validates the captured Lead before applying lifecycle
transitions.

If validation produces errors, the workflow stops before applying a
lifecycle transition.

This prevents an invalid Lead from moving forward in the lifecycle.

---

## 7. Test Fixture Decision

Reusable test setup was introduced through:

`tests/conftest.py`

The `caregiver_message` fixture provides a reusable
`NormalizedMessage` for workflow tests.

This reduces repeated test setup and keeps individual tests focused on
the behavior being tested.

---

## 8. Workflow Architecture Decision

The current workflow is intentionally implemented using ordinary Python
functions and `GraphState`.

The current conceptual flow is:

NormalizedMessage
    ↓
GraphState
    ↓
Lead Capture Node
    ↓
Validation
    ↓
Lifecycle Transition
    ↓
Updated GraphState

The architecture is prepared for future integration with a workflow
orchestration framework such as LangGraph.

LangGraph has not been introduced into the current implementation.

The business logic should remain independent of the orchestration
framework.

---

# 9. Testing

The Day 5 implementation was verified using the existing test suite.

Final observed result:

`29 passed`

Negative testing was also used to verify that an invalid Lead does not
move through the lifecycle.

---

# 10. Important Unknowns

The following areas remain intentionally unresolved:

### 10.1 Qualification logic

The exact business rules for determining whether a Lead is qualified,
not qualified, or still unknown have not been fully implemented.

### 10.2 Real external channels

The prototype currently works with normalized messages.

Real Facebook, WhatsApp, or other channel integrations have not been
implemented.

### 10.3 Database persistence

Lead records currently exist in the application workflow.

A production database/persistence layer has not been implemented.

### 10.4 CRM integration

No CRM integration has been implemented.

### 10.5 Appointment booking

The prototype does not book real appointments.

### 10.6 Human handoff implementation

The lifecycle contains a `human_handoff` status, but a real human
handoff mechanism has not been implemented.

### 10.7 Production orchestration

The current workflow is local Python orchestration.

A production workflow framework has not yet been introduced.

---

# 11. Day 5 Architectural Principle

The main architectural principle established during Day 5 is:

> Keep business logic independent from workflow orchestration.

Lead Capture should know how to extract Lead information.

Lifecycle logic should know which transitions are allowed.

Validation should know how to validate a Lead.

Shared state should carry information between workflow steps.

The workflow should coordinate these responsibilities.

A future orchestration framework should coordinate the workflow without
requiring the underlying business logic to be rewritten.