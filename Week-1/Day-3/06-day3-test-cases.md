# Day 3 Test Cases

## Purpose

These test cases are used to check whether the proposed Marketing, Sales & Lead-Generation agent workflow can correctly handle different types of inbound customer messages.

The test cases are based on:

* Public information about Saathi Sneha Care
* Project assumptions
* The proposed lead schema
* The proposed normalized message structure
* The proposed agent responsibilities

These examples are **test data only**. They are not real customer records and do not represent confirmed internal Saathi Sneha Care workflows.

---

# Evidence Labels

Throughout this document:

* **CONFIRMED** — supported by public information.
* **ASSUMPTION** — reasonable project assumption based on the available public information.
* **UNKNOWN** — information that is not publicly available.
* **TARGET** — proposed system behavior or design for this project.

---

# Test Case 1 — General Service Inquiry

## Customer Message

> "I would like to know more about your services."

## 1. Normalized Message

```json
{
  "channel": "facebook",
  "sender_id": "sample_sender_101",
  "text": "I would like to know more about your services.",
  "timestamp": "2026-09-23T11:00:00",
  "attachments": []
}
```

### Field Explanation

| Field       | Value                 | Status              |
| ----------- | --------------------- | ------------------- |
| channel     | `facebook`            | TARGET test input   |
| sender_id   | `sample_sender_101`   | TARGET test input   |
| text        | Customer's message    | TARGET test input   |
| timestamp   | `2026-09-23T11:00:00` | TARGET sample value |
| attachments | `[]`                  | TARGET sample value |

The sender ID is a sample value and does not represent a real Facebook user.

---

## 2. Lead Record After Initial Capture

```json
{
  "lead_id": "lead_101",
  "name": null,
  "contact": null,
  "channel": "facebook",
  "source": "facebook_organic",
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
  "created_at": "2026-09-23T11:00:00",
  "updated_at": "2026-09-23T11:00:00"
}
```

### What is known from the message?

* The person wants information about Saathi Sneha Care's services.
* No specific service has been identified.
* No customer name has been provided.
* No contact information has been provided.
* No patient location has been provided.
* No urgency has been stated.
* No consultation has been explicitly requested.

### Missing Information

* Name
* Contact information
* Specific need
* Service interest
* Patient location
* Urgency
* Preferred contact time
* Plan interest

### Next Step

**TARGET:** Lead Capture → Lead Qualification / Information Gathering

The system should identify what information is still needed rather than inventing it.

---

# Test Case 2 — Specific Service Inquiry

## Customer Message

> "Do you provide caregiver support for elderly parents?"

## 1. Normalized Message

```json
{
  "channel": "facebook",
  "sender_id": "sample_sender_102",
  "text": "Do you provide caregiver support for elderly parents?",
  "timestamp": "2026-09-23T11:05:00",
  "attachments": []
}
```

---

## 2. Lead Record After Initial Capture

```json
{
  "lead_id": "lead_102",
  "name": null,
  "contact": null,
  "channel": "facebook",
  "source": "facebook_organic",
  "need": "care support for elderly parent",
  "service_interest": "caregiver_support",
  "patient_location": null,
  "urgency": null,
  "preferred_contact_time": null,
  "plan_interest": null,
  "status": "new",
  "qualification_status": "unknown",
  "consultation_requested": false,
  "notes": [],
  "created_at": "2026-09-23T11:05:00",
  "updated_at": "2026-09-23T11:05:00"
}
```

### What is explicitly present?

The customer is asking whether caregiver support is available for an elderly parent.

Saathi Sneha Care publicly describes caregiver support as one of its care services.

**Evidence status:**

* Public availability of caregiver support: **CONFIRMED**
* Customer's interest in caregiver support: **TARGET extraction from message**
* Customer qualification: **UNKNOWN**
* Internal eligibility criteria: **UNKNOWN**

### Missing Information

* Name
* Contact information
* Patient location
* Urgency
* Preferred contact time
* Exact care requirements
* Plan interest

### Important Rule

The system should **not automatically decide that the customer is qualified**.

There are no confirmed public qualification rules available for this project.

### Next Step

**TARGET:** Lead Capture → Qualification / Information Gathering

---

# Test Case 3 — Potential Urgent Request

## Customer Message

> "I need someone to check on my mother today. She is alone and not well."

## 1. Normalized Message

```json
{
  "channel": "facebook",
  "sender_id": "sample_sender_103",
  "text": "I need someone to check on my mother today. She is alone and not well.",
  "timestamp": "2026-09-23T11:10:00",
  "attachments": []
}
```

---

## 2. Lead Record After Initial Capture

```json
{
  "lead_id": "lead_103",
  "name": null,
  "contact": null,
  "channel": "facebook",
  "source": "facebook_organic",
  "need": "check on mother",
  "service_interest": null,
  "patient_location": null,
  "urgency": "potentially_urgent",
  "preferred_contact_time": "today",
  "plan_interest": null,
  "status": "new",
  "qualification_status": "unknown",
  "consultation_requested": false,
  "notes": [
    "Customer indicates that the mother is alone and not well."
  ],
  "created_at": "2026-09-23T11:10:00",
  "updated_at": "2026-09-23T11:10:00"
}
```

### What is explicitly present?

The customer says:

* Their mother is alone.
* Their mother is not well.
* They want someone to check on her today.

### What should NOT be assumed?

The system should **not diagnose the mother's condition**.

It should also not automatically label this as a medical emergency solely because words such as "not well" or "today" appear.

Therefore:

`urgency = "potentially_urgent"`

is safer as a **TARGET classification** than:

`urgency = "high"`

because the project's actual emergency/escalation rules are **UNKNOWN**.

### Missing Information

* Customer name
* Contact information
* Mother's location
* Exact care requirement
* Severity of the situation
* Preferred contact details/time
* Whether emergency assistance is required
* Whether a consultation is requested

### Next Step

**TARGET:** Lead Capture → Human/appropriate escalation or Qualification, depending on approved escalation rules.

### Important Boundary

The agent must not provide a medical diagnosis or make an independent emergency decision.

The actual escalation procedure is **UNKNOWN** and must be confirmed with the mentor/company.

---

# Test Case 4 — Pricing Inquiry

## Customer Message

> "How much does your monthly home care package cost?"

## 1. Normalized Message

```json
{
  "channel": "facebook",
  "sender_id": "sample_sender_104",
  "text": "How much does your monthly home care package cost?",
  "timestamp": "2026-09-23T11:15:00",
  "attachments": []
}
```

---

## 2. Lead Record After Initial Capture

```json
{
  "lead_id": "lead_104",
  "name": null,
  "contact": null,
  "channel": "facebook",
  "source": "facebook_organic",
  "need": "home care",
  "service_interest": null,
  "patient_location": null,
  "urgency": null,
  "preferred_contact_time": null,
  "plan_interest": null,
  "status": "new",
  "qualification_status": "unknown",
  "consultation_requested": false,
  "notes": [
    "Customer is asking about the cost of a monthly home care package."
  ],
  "created_at": "2026-09-23T11:15:00",
  "updated_at": "2026-09-23T11:15:00"
}
```

### What is known?

The customer is asking about pricing for a monthly home-care package.

### What is NOT known?

The customer has not identified a specific plan.

The public website describes different care plans, but this message alone does not tell us which plan the customer wants.

Therefore:

```json
"plan_interest": null
```

is correct.

### Important Pricing Rule

The system must **not invent a price**.

If a specific price is publicly available in the approved knowledge source, the system may use that information.

If the price is not publicly available or approved:

**TARGET:** tell the customer that the team can provide the relevant pricing information / arrange further assistance, rather than generating a number.

### Missing Information

* Customer name
* Contact information
* Specific service requirement
* Specific plan
* Patient location
* Urgency
* Preferred contact time

### Next Step

**TARGET:** Lead Capture → Sales Follow-up / Information Gathering

---

# Test Case 5 — Consultation Request

## Customer Message

> "I would like to schedule a consultation to discuss care options for my father."

## 1. Normalized Message

```json
{
  "channel": "facebook",
  "sender_id": "sample_sender_105",
  "text": "I would like to schedule a consultation to discuss care options for my father.",
  "timestamp": "2026-09-23T11:20:00",
  "attachments": []
}
```

---

## 2. Lead Record After Initial Capture

```json
{
  "lead_id": "lead_105",
  "name": null,
  "contact": null,
  "channel": "facebook",
  "source": "facebook_organic",
  "need": "care options for father",
  "service_interest": null,
  "patient_location": null,
  "urgency": null,
  "preferred_contact_time": null,
  "plan_interest": null,
  "status": "new",
  "qualification_status": "unknown",
  "consultation_requested": true,
  "notes": [],
  "created_at": "2026-09-23T11:20:00",
  "updated_at": "2026-09-23T11:20:00"
}
```

### What is explicitly present?

The customer explicitly wants to schedule a consultation.

Therefore:

```json
"consultation_requested": true
```

is appropriate.

### What should not happen?

The Lead Capture Agent should **not book the consultation itself**.

The proposed architecture separates:

**Sales Follow-up → Scheduling Agent → Calendar/Booking**

The exact internal scheduling process is **UNKNOWN**.

### Missing Information

* Customer name
* Contact information
* Father's location
* Specific care requirement
* Preferred consultation time
* Urgency
* Specific service interest

### Next Step

**TARGET:**

```text
Lead Capture
      ↓
Qualification / Information Gathering
      ↓
Sales Follow-up
      ↓
Consultation Requested
      ↓
Scheduling Agent
```

---

# Comparison of the Five Test Cases

| Test                | Customer Intent              | Extracted Information                   | Missing Information                                  | Proposed Next Step                      |
| ------------------- | ---------------------------- | --------------------------------------- | ---------------------------------------------------- | --------------------------------------- |
| 1. General          | General service inquiry      | Wants information about services        | Almost all lead details                              | Qualification / information gathering   |
| 2. Specific Service | Caregiver support inquiry    | Caregiver support for elderly parent    | Contact, location, urgency, exact requirements       | Qualification                           |
| 3. Potential Urgent | Immediate care/check request | Mother alone/not well, wants help today | Location, severity, contact, exact requirement       | Appropriate escalation / qualification  |
| 4. Pricing          | Pricing inquiry              | Wants monthly home-care pricing         | Specific plan, contact, location, requirements       | Sales follow-up / information gathering |
| 5. Consultation     | Consultation request         | Explicit consultation request           | Contact, location, preferred time, care requirements | Sales Follow-up → Scheduling            |

---

# What These Test Cases Teach Us

These five examples represent five different inbound situations:

```text
General Inquiry
      ↓
Need more information

Specific Service Inquiry
      ↓
Identify service + gather missing details

Potential Urgent Request
      ↓
Identify potential urgency + follow approved escalation rules

Pricing Inquiry
      ↓
Provide approved pricing information or route to human/team

Consultation Request
      ↓
Pass consultation intent toward Scheduling
```

---

# Important Data Design Principle

The system should distinguish between:

### 1. Customer-provided information

Information directly stated by the customer.

Example:

> "I would like to schedule a consultation."

This supports:

```json
"consultation_requested": true
```

### 2. Extracted information

Information structured from the customer's message.

Example:

> "caregiver support for elderly parents"

can be structured as:

```json
"service_interest": "caregiver_support"
```

### 3. Missing information

Information that the customer has not provided.

Example:

```json
"patient_location": null
```

### 4. Unknown business rules

Information that we do not know from public sources.

Example:

```text
What makes a lead "qualified"?
```

This remains:

**UNKNOWN**

and must not be invented.

---

# Validation Rules Applied to These Tests

Every test case should follow these rules:

### Rule 1 — Do not invent customer information

If the customer does not provide their name:

```json
"name": null
```

Do not create a name.

---

### Rule 2 — Do not invent contact information

If no phone/email/contact information is provided:

```json
"contact": null
```

---

### Rule 3 — Do not invent location

If the customer's or patient's location is not stated:

```json
"patient_location": null
```

---

### Rule 4 — Do not invent pricing

Never generate a price simply because the customer asks:

> "How much does it cost?"

Use an approved public source if a price exists. Otherwise, leave the price unresolved and route appropriately.

---

### Rule 5 — Do not invent qualification

All five examples initially remain:

```json
"qualification_status": "unknown"
```

unless approved qualification rules are later provided.

---

### Rule 6 — Do not diagnose

The urgent example says:

> "She is alone and not well."

The system should not infer a disease or medical condition.

---

### Rule 7 — Do not automatically declare an emergency

The urgent example should trigger attention, but the actual emergency classification and escalation rules are **UNKNOWN**.

---

### Rule 8 — Do not let Lead Capture perform Scheduling

For the consultation request:

```text
consultation_requested = true
```

does not mean:

```text
booking confirmed
```

Those are different events.

---

# Final Expected Flow

These five test cases should ultimately demonstrate the following target architecture:

```text
Customer
   │
   ▼
Facebook / Other Channel
   │
   ▼
Channel Adapter
   │
   ▼
Normalized Message
   │
   ▼
Lead Capture Agent
   │
   ▼
Lead Record
   │
   ▼
Qualification / Information Gathering
   │
   ├───────────────┐
   │               │
   ▼               ▼
More Information   Qualified
   │               │
   └───────┬───────┘
           ▼
     Sales Follow-up
           │
           ▼
 Consultation Requested?
           │
          Yes
           ▼
    Scheduling Agent
           │
           ▼
    Calendar / Booking
```

This is a **TARGET architecture**, not a claim that Saathi Sneha Care currently operates this exact automated workflow.

---

# Day 3 Success Criteria

After completing these five tests, you should be able to explain:

1. What information comes from the customer.
2. What information is extracted from the message.
3. What information is missing.
4. What belongs in the Lead Record.
5. What remains `UNKNOWN`.
6. Which agent should handle the next step.
7. Why the system must not invent customer data.
8. Why qualification rules must come from an approved source.
9. Why pricing must come from an approved source.
10. Why urgent situations require approved escalation rules.
11. Why consultation requests should eventually be handed to Scheduling.
12. Why the five examples are test cases rather than evidence of the company's internal workflow.

## Key Principle

> **Public information tells us what the company publicly offers. It does not tell us exactly how the company's internal CRM, qualification, escalation, sales, or scheduling processes work.**

Therefore, throughout Week 1:

**Public information = evidence**

**Reasonable interpretation = ASSUMPTION**

**Unavailable internal information = UNKNOWN**

**Our proposed system design = TARGET**
