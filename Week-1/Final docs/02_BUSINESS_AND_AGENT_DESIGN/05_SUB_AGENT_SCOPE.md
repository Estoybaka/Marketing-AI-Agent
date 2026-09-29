# Sub-Agent Scope - Detailed Responsibility and Boundary

## 1. Purpose

This document defines the scope of the four sub-agents in the assigned Marketing, Sales & Lead-Generation track.

The four agents are:

1. Lead Capture
2. Lead Qualification
3. Content
4. Sales Follow-up

Scheduling remains separate.

The main purpose of the scope document is to stop responsibilities from becoming mixed together.

---

# 2. Scope Design Principle

The basic separation is:

```text
Lead Capture
    ↓
Capture what the customer said

Lead Qualification
    ↓
Apply approved business rules

Content
    ↓
Create approved content

Sales Follow-up
    ↓
Continue the customer conversation

Scheduling
    ↓
Handle real booking
```

Each agent should do its own job.

---

# 3. Lead Capture Agent

## 3.1 Purpose

The Lead Capture Agent turns an incoming normalized customer message into structured Lead information.

The core question is:

> What supported Lead information can be extracted from this message?

---

## 3.2 Input

```text
NormalizedMessage
```

The message contains:

- `sender_id`
- `channel`
- `text`
- `timestamp`
- `attachments`

---

## 3.3 Output

```text
Lead
```

The Lead may contain:

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
- lifecycle status,
- qualification status,
- consultation intent,
- notes,
- timestamps.

Not all fields must be populated.

---

## 3.4 Responsibilities

Lead Capture may:

- preserve the source when known,
- preserve the channel,
- extract explicit customer information,
- identify stated need,
- identify explicit service interest,
- identify explicit plan interest,
- identify supported urgency signals,
- detect consultation intent,
- create or update the Lead,
- leave missing information unknown.

---

## 3.5 Current Extraction Examples

### Caregiver support

If the customer says:

```text
Do you provide caregiver support for elderly parents?
```

the supported extraction is:

```text
service_interest = caregiver_support
```

---

### Consultation

If the customer says:

```text
I would like to schedule a consultation.
```

the supported extraction is:

```text
consultation_requested = true
```

This does **not** mean the appointment is booked.

---

### Potential urgency

If the customer says:

```text
I need someone to check on my mother today.
She is alone and not well.
```

the prototype may produce:

```text
urgency = potential
```

It must not diagnose the person or automatically declare an emergency.

---

### Plan

If the customer explicitly says:

```text
Care Connect
```

the prototype may produce:

```text
plan_interest = Care Connect
```

---

### Pricing

If the customer asks:

```text
How much does your monthly home care package cost?
```

the system can record:

```text
notes = ["pricing inquiry detected"]
```

It must not invent a price.

---

# 4. Lead Capture - Explicit Non-Responsibilities

Lead Capture does not:

- qualify the Lead,
- diagnose a patient,
- book appointments,
- invent prices,
- make downstream sales decisions,
- invent customer information,
- invent qualification criteria,
- own calendar logic,
- claim that a booking happened.

The clean boundary is:

```text
Lead Capture
      ↓
Lead
      ↓
Lead Qualification
```

---

# 5. Lead Qualification Agent

## 5.1 Purpose

Lead Qualification evaluates a Lead against approved qualification rules.

The question is:

> Does this Lead meet the business's approved qualification criteria?

---

## 5.2 Input

```text
Lead
+
Approved Qualification Rules
```

---

## 5.3 Output

```text
Qualification Result
```

Current qualification status values include:

```text
unknown
qualified
not_qualified
```

---

## 5.4 Responsibilities

Lead Qualification should:

- read Lead information,
- identify missing qualification information,
- apply approved qualification rules,
- determine qualification,
- identify routing,
- preserve uncertainty when rules do not support a decision.

---

## 5.5 Important Limitation

The complete production qualification rules were not confirmed in the Week 1 context.

Therefore:

```text
qualification_status = unknown
```

is a valid state.

The agent must not invent its own definition of a qualified Lead.

---

## 5.6 Lead Qualification Must Not

It must not:

- invent qualification criteria,
- diagnose,
- invent prices,
- book appointments,
- replace Sales Follow-up,
- silently turn missing data into a positive qualification result.

---

# 6. Content Agent

## 6.1 Purpose

The Content Agent creates content from an approved source brief.

The principle is:

```text
Approved Source
      ↓
Content Agent
      ↓
Platform Content
```

---

## 6.2 Responsibilities

Content should:

- use approved source information,
- adapt information to the target platform,
- keep claims consistent,
- avoid unsupported promises,
- avoid invented services,
- avoid invented prices,
- avoid invented medical claims.

---

## 6.3 Content Must Not

The Content Agent must not create facts simply to make content sound better.

It should not invent:

- services,
- prices,
- business policies,
- medical claims,
- customer promises.

---

# 7. Sales Follow-up Agent

## 7.1 Purpose

Sales Follow-up continues the customer conversation after Lead information is available.

The question is:

> What should the system do next in the customer conversation using approved information and rules?

---

## 7.2 Input

```text
Lead
+
Conversation
```

---

## 7.3 Output

```text
Response
+
Updated Lead
```

---

## 7.4 Responsibilities

Sales Follow-up may:

- continue appropriate prospect conversations,
- answer approved informational questions,
- ask for missing information,
- update Lead fields when the customer explicitly provides new information,
- detect consultation intent,
- identify human handoff needs,
- hand consultation requests to Scheduling.

---

## 7.5 Sales Follow-up Must Not

It must not:

- diagnose,
- invent pricing,
- make unsupported promises,
- claim a booking without a booking result,
- own calendar logic,
- create business rules that were never approved.

---

# 8. Scheduling Boundary

Scheduling is separate.

The distinction is:

```text
Customer asks for consultation
        ↓
consultation_requested = true
```

This is not the same as:

```text
status = booked
```

A real booking result must exist before the Lead can be treated as booked.

---

# 9. Agent Responsibility Matrix

| Responsibility | Lead Capture | Qualification | Content | Sales Follow-up | Scheduling |
|---|---:|---:|---:|---:|---:|
| Read inbound message | Yes | Read Lead | No | Yes | No |
| Extract explicit Lead data | Yes | No | No | Update when provided | No |
| Create Lead | Yes | No | No | No | No |
| Qualify Lead | No | Yes | No | No | No |
| Apply qualification rules | No | Yes | No | No | No |
| Create content | No | No | Yes | No | No |
| Continue prospect conversation | No | No | No | Yes | No |
| Detect consultation intent | Yes | Can read | No | Yes | No |
| Book appointment | No | No | No | No | Yes |
| Own calendar logic | No | No | No | No | Yes |
| Human handoff | Flag | Flag | No | Yes | Possible |
| Invent facts | No | No | No | No | No |

---

# 10. Scope Boundary Diagram

```text
Incoming Message
       ↓
Lead Capture
       ↓
Structured Lead
       ↓
Lead Qualification
       ↓
Qualification Result
       ↓
Sales Follow-up
       ↓
Consultation Request
       ↓
Scheduling
       ↓
Booking Result
```

Content runs as a separate approved-source process.

---

# 11. Final Scope Principle

The agents should not become one large system with unclear responsibility.

The Week 1 boundary is:

```text
Capture
  ≠
Qualification
  ≠
Content
  ≠
Sales Follow-up
  ≠
Scheduling
```

This separation should remain the basis for later implementation.
