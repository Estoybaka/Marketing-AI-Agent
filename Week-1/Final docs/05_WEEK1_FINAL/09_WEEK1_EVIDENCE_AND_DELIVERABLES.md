# Week 1 Evidence and Deliverables

## 1. Purpose

This document explains what evidence exists for Week 1 and what each evidence item proves.

Evidence should be tied to actual work rather than general statements.

---

# 2. Business Evidence

## 2.1 Funnel Audit

The funnel audit documents:

- public website,
- public customer journey,
- public services,
- public plans,
- public contact entry points,
- social/channel directions,
- source vs channel,
- unknown internal processes.

It proves that the public-facing business understanding was documented.

It does not prove internal CRM or Lead handling.

---

## 2.2 Agent Scope

The scope document records:

- Lead Capture responsibility,
- Lead Qualification responsibility,
- Content responsibility,
- Sales Follow-up responsibility,
- Scheduling boundary,
- prohibited overlap.

It provides a design contract for later implementation.

---

## 2.3 Lead Data Dictionary

The dictionary connects:

```text
Original Week 1 fields
        ↓
Expanded Lead model
        ↓
Workflow ownership
```

It documents:

- field meaning,
- type,
- ownership,
- missing-data behavior,
- examples,
- implementation status.

---

# 3. Technical Evidence

## 3.1 NormalizedMessage

Evidence category:

```text
Message model
```

What it demonstrates:

- common input contract,
- channel normalization,
- separation from raw channel payloads.

---

## 3.2 Lead Model

Evidence demonstrates that the project has a structured Lead representation.

Fields include:

- Lead ID,
- name,
- contact,
- channel,
- source,
- need,
- service interest,
- patient location,
- urgency,
- preferred contact time,
- plan interest,
- status,
- qualification status,
- consultation requested,
- notes,
- timestamps.

---

## 3.3 Lead Capture

Evidence demonstrates:

```text
NormalizedMessage
      ↓
capture_lead()
      ↓
Lead
```

The implementation is deterministic.

---

## 3.4 Validation

Evidence demonstrates validation rules such as:

- required channel,
- required source,
- valid Lead ID,
- valid lifecycle state,
- valid qualification state.

---

## 3.5 Lifecycle

Evidence demonstrates controlled status transitions.

The lifecycle module contains:

```text
ALLOWED_TRANSITIONS
is_transition_allowed()
transition_lead()
```

---

## 3.6 GraphState

Evidence demonstrates shared workflow state:

```text
message
lead
errors
```

---

## 3.7 Workflow

Evidence demonstrates:

```text
GraphState
      ↓
Lead Capture Node
      ↓
Validation
      ↓
Invalid → STOP
      ↓
Valid → Lifecycle
```

---

# 4. Testing Evidence

The recorded Day 5 result was:

```text
29 passed
```

The test coverage included:

- message model,
- Lead model,
- Lead Capture,
- lifecycle,
- GraphState,
- workflow,
- negative cases,
- reusable fixture behavior.

Day 6 should verify the final repository state again.

---

# 5. Negative Test Evidence

The most important negative test demonstrated:

```text
empty channel
+
consultation intent
```

Validation produced:

```text
Channel is required.
```

The workflow was then corrected so that the invalid Lead did not proceed.

This is evidence of a workflow safety rule, not merely a validation rule.

---

# 6. Fixture Evidence

Reusable fixture support was introduced through:

```text
tests/conftest.py
```

The `caregiver_message` fixture was used in workflow testing.

---

# 7. What Week 1 Evidence Does Not Prove

The evidence does not prove production availability of:

- Facebook integration,
- WhatsApp integration,
- CRM,
- database,
- booking,
- human handoff,
- complete Qualification,
- full LangGraph deployment,
- production hosting.

These are not claimed as completed.

---

# 8. Evidence Completion Table

| Evidence | Week 1 Status |
|---|---|
| Project context | Completed |
| Funnel audit | Completed as public/assumption audit |
| Agent scope | Completed |
| Lead data dictionary | Completed |
| NormalizedMessage design | Completed |
| Lead model | Implemented |
| Lead Capture | Implemented locally |
| Validation | Implemented |
| Lifecycle | Implemented |
| GraphState | Implemented |
| Workflow | Implemented |
| Negative tests | Implemented |
| Fixtures | Implemented |
| Test baseline | 29 passed at Day 5 |
| Production integrations | Not implemented |
| Full qualification rules | Unknown / not implemented |
| Production CRM | Not implemented |
| Real booking | Not implemented |

---

# 9. Evidence Principle

A good Week 1 evidence set should allow another person to answer:

1. What did we investigate?
2. What did we design?
3. What did we implement?
4. What did we test?
5. What passed?
6. What remains unknown?
7. What must be decided next?

That is the purpose of this evidence pack.
