# Sample Lead Messages

## Day 1 — September 21, 2026

## Purpose

The project brief requires 3–5 sample messages that a lead might send.

These messages are intended to become test inputs later.

They are examples only and do not represent confirmed real customer behavior.

---

# Message 1 — General Service Inquiry

### Customer message

> Hi, I would like to know more about your services.

### Possible information available

```text
need: unknown
urgency: unknown
contact: unknown
source: potentially available from channel/campaign
```

### Expected system behavior to investigate later

- Lead Capture should recognize this as a potential inbound lead.
- Lead information should be recorded.
- Lead Qualification may need to ask what service the customer needs.
- The lead should not be marked as qualified without sufficient information.

### Open question

What is the minimum information required before this lead can be considered qualified?

---

# Message 2 — Specific Need

### Customer message

> Hi, I need help with your service. Can someone explain the process to me?

### Possible information available

```text
need: service-related inquiry
urgency: unknown
contact: unknown
```

### Expected system behavior to investigate later

- Capture the interaction.
- Identify the customer's need.
- Determine what information is missing.
- Continue qualification if appropriate.

### Open question

What exact questions should the Qualification Agent ask?

---

# Message 3 — Urgent Inquiry

### Customer message

> Hi, I need this service as soon as possible. Can someone contact me today?

### Possible information available

```text
need: unknown
urgency: potentially high
contact: may be available from platform
```

### Expected system behavior to investigate later

- Capture the lead.
- Preserve the urgency information.
- Determine the customer's exact need.
- Apply the company's actual urgency rules once those rules are defined.
- Potentially prioritize follow-up if company rules confirm that this is appropriate.

### Open question

What exactly does the company mean by an "urgent" lead?

---

# Message 4 — Pricing Inquiry

### Customer message

> How much does your service cost?

### Possible information available

```text
need: pricing/service inquiry
urgency: unknown
contact: may be available from platform
```

### Expected system behavior to investigate later

- Capture the lead.
- Identify that the customer is asking about pricing.
- Use approved company pricing information if the system is authorized to provide it.
- Determine whether additional qualification is required.

### Open question

Can an agent provide pricing automatically, and where should it retrieve current pricing from?

---

# Message 5 — Consultation / Booking Inquiry

### Customer message

> I would like to schedule a consultation. What times are available?

### Possible information available

```text
need: consultation
booking_intent: yes
```

### Expected system behavior to investigate later

Conceptually:

```text
Inbound message
      |
      v
Lead Capture
      |
      v
Qualification / intent detection
      |
      v
Sales Follow-up if required
      |
      v
Scheduling Agent
      |
      v
Calendar availability
      |
      v
Booking
```

### Open question

What exact information must Sales Follow-up pass to the Scheduling Agent?

---

# Test Categories Represented

| Message | Main scenario |
|---|---|
| 1 | General inquiry |
| 2 | Specific service need |
| 3 | Urgent request |
| 4 | Pricing inquiry |
| 5 | Consultation/booking request |

---

# Important Testing Note

These messages are not yet expected to produce final qualification decisions.

Before implementation, the team must define:

- Qualification criteria.
- Urgency rules.
- Required fields.
- Routing rules.
- Allowed automated responses.
- Human escalation conditions.
- Scheduling handoff requirements.

The messages can then be used as basic functional test cases.
