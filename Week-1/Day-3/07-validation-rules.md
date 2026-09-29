# Day 3 — Validation Rules

## Purpose

Validation checks whether information entering or moving through the system is acceptable.

## Rule 1 — Channel

```text
channel must not be empty
```

Reason:

The system needs to know where the current conversation is occurring.

---

## Rule 2 — Sender ID

```text
sender_id should exist for channel conversations
```

Reason:

A channel conversation normally needs a sender identifier.

Exact platform requirements remain UNKNOWN.

---

## Rule 3 — Empty text

```text
text may be empty only for supported attachment-only messages
```

A completely empty message with no attachment should not be treated as a normal text message.

Exact supported attachment behavior remains UNKNOWN.

---

## Rule 4 — Never infer customer information

If the customer does not provide:

```text
name
contact
location
urgency
```

do not invent it.

Use:

```text
null
unknown
missing
```

depending on the field's design.

---

## Rule 5 — Qualification

Never assign a qualification status without approved qualification rules.

Current qualification criteria are UNKNOWN.

---

## Rule 6 — Urgency

Do not classify a medical emergency solely from a keyword.

For example:

```text
"Please help urgently."
```

can indicate stated urgency.

It does not by itself establish a medical diagnosis or emergency classification.

---

## Rule 7 — Pricing

Do not invent prices.

Use only approved/public pricing information when available.

If no approved price is available, the workflow should use an appropriate information request or human handoff.

---

## Rule 8 — Medical advice

Agents must not provide medical diagnosis.

The system is for lead capture, qualification, sales follow-up, content, and scheduling—not autonomous medical decision-making.

## Rule 9 — Scope

Each agent should stay inside its defined responsibility.

Example:

Lead Capture should not make qualification decisions.

Sales Follow-up should not own calendar logic.

## Validation checklist

Before accepting a record:

```text
[ ] Channel present
[ ] Sender identified where applicable
[ ] Message format valid
[ ] No invented customer data
[ ] No unsupported qualification
[ ] No invented pricing
[ ] No medical diagnosis
[ ] Correct agent scope
```
