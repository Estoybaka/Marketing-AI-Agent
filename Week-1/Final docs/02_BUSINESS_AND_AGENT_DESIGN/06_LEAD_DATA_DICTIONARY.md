# Lead Data Dictionary - Detailed Specification

## 1. Purpose

The original Week 1 requirement was to define the Lead information that must be tracked.

The original required fields were:

```text
name
contact
need
urgency
source
```

During Day 3 and Day 4, the technical Lead model expanded this into a larger structure.

This document maps both the original requirement and the expanded model.

---

# 2. Lead Object

The target Lead structure is:

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

This is a technical target/data model. It is not a claim that this is already the production CRM schema.

---

# 3. Field Dictionary

## 3.1 `lead_id`

**Meaning:** Unique identifier for the Lead.

**Type:** String.

**Required:** Yes.

**Populated by:** System.

**When:** Lead creation.

**Example:**

```text
lead_101
```

**Rule:** Must exist before the Lead proceeds through validation.

**Implementation status:** Present in the Lead model and validation design.

---

## 3.2 `name`

**Meaning:** Customer's name.

**Type:** String / null.

**Required:** No at initial capture.

**Populated by:** Lead Capture when explicitly provided.

**Example:**

```text
Priyanka
```

**Rule:** If the customer does not provide a name, keep it unknown/null.

**Must not:** Invent a name.

**Implementation status:** Supported by Lead model.

---

## 3.3 `contact`

**Meaning:** Customer contact information.

**Type:** String / null.

**Required:** No at initial capture.

**Populated by:** Lead Capture when explicitly provided.

**Example:**

```text
+977...
```

**Rule:** Missing contact remains null.

**Must not:** Guess a phone number or email.

**Implementation status:** Supported by Lead model.

---

## 3.4 `channel`

**Meaning:** Current conversation channel.

**Type:** String.

**Required:** Yes.

**Populated by:** Channel Adapter / system.

**Examples:**

```text
facebook
whatsapp
instagram
website
phone
```

**Rule:** Channel must not be empty.

**Implementation status:** Implemented in the normalized message and Lead model; validation checks its presence.

---

## 3.5 `source`

**Meaning:** Original source of the Lead.

**Type:** String.

**Required:** Yes.

**Examples:**

```text
facebook_organic
facebook_ad
instagram
website
google_ad
referral
unknown
```

**Important distinction:**

```text
source  = facebook_ad
channel = whatsapp
```

This allows original acquisition source and current conversation channel to be tracked separately.

**Implementation status:** Required by validation and Lead model.

---

## 3.6 `need`

**Meaning:** The need stated by the customer.

**Type:** String / null.

**Required:** No.

**Populated by:** Lead Capture.

**Example:**

```text
check on my mother
```

**Rule:** Preserve the customer's stated meaning.

**Must not:** Create a more specific need that the customer did not state.

**Implementation status:** Supported by Lead model and extraction behavior.

---

## 3.7 `service_interest`

**Meaning:** Explicit service interest.

**Type:** String / null.

**Required:** No.

**Examples:**

```text
caregiver_support
hospital_escort
doctor_consult
```

Only explicitly supported interest should be stored.

**Implementation status:** Prototype supports caregiver-related extraction.

---

## 3.8 `patient_location`

**Meaning:** Location of the person receiving care.

**Type:** String / null.

**Required:** No.

**Example:**

```text
Kathmandu
```

**Rule:** Only store when explicitly provided.

**Implementation status:** Included in target Lead model.

---

## 3.9 `urgency`

**Meaning:** Supported urgency signal.

**Type:** String / null.

**Required:** No.

**Prototype value:**

```text
potential
```

**Supported examples include:**

- today
- as soon as possible
- urgent
- urgently
- immediately
- alone at home
- alone and not well

**Important:** A potential urgency flag is not a diagnosis or automatic emergency classification.

**Implementation status:** Prototype extraction supports the documented test case.

---

## 3.10 `preferred_contact_time`

**Meaning:** Customer's preferred contact time.

**Type:** String / null.

**Required:** No.

**Example:**

```text
after 6 PM
```

**Rule:** Do not invent a time.

**Implementation status:** Included in Lead model; exact production format remains to be confirmed.

---

## 3.11 `plan_interest`

**Meaning:** Explicitly named plan.

**Type:** String / null.

**Example:**

```text
Care Connect
```

**Rule:** Store a plan when the customer explicitly names it.

**Important:** The system must not automatically recommend a plan without approved business rules.

**Implementation status:** Prototype supports explicit `care connect` extraction.

---

## 3.12 `status`

**Meaning:** Current Lead lifecycle state.

**Type:** Controlled value.

**Documented values:**

```text
new
contacted
needs_information
qualified
consultation_requested
booked
converted
not_qualified
inactive
human_handoff
```

**Rule:** Status changes must follow allowed transitions.

**Implementation status:** Lifecycle module implemented during Day 5.

---

## 3.13 `qualification_status`

**Meaning:** Qualification state.

**Type:** Controlled value.

**Values:**

```text
unknown
qualified
not_qualified
```

**Rule:** Do not assign qualification without approved qualification rules.

**Implementation status:** Field exists; complete business qualification logic is not implemented.

---

## 3.14 `consultation_requested`

**Meaning:** Whether the customer explicitly requested a consultation.

**Type:** Boolean.

**Default:** False.

**Example:**

```text
true
```

**Important:**

```text
consultation_requested = true
```

does not mean:

```text
status = booked
```

**Implementation status:** Implemented in Lead Capture behavior.

---

## 3.15 `notes`

**Meaning:** Supporting notes that help preserve useful information.

**Type:** List of strings.

**Example:**

```text
["pricing inquiry detected"]
```

**Rule:** Notes must not be used to invent facts.

**Implementation status:** Supported.

---

## 3.16 `created_at`

**Meaning:** Lead creation time.

**Type:** Date/time.

**Populated by:** System.

**Implementation status:** Included in target model.

---

## 3.17 `updated_at`

**Meaning:** Last update time.

**Type:** Date/time.

**Populated by:** System.

**Implementation status:** Included in target model.

---

# 4. Original Week 1 Fields Mapped to Technical Fields

| Original Requirement | Technical Field |
|---|---|
| name | `name` |
| contact | `contact` |
| need | `need` |
| urgency | `urgency` |
| source | `source` |

The expanded model adds:

```text
channel
service_interest
patient_location
preferred_contact_time
plan_interest
status
qualification_status
consultation_requested
notes
created_at
updated_at
lead_id
```

---

# 5. Data Ownership

| Field | Main Owner |
|---|---|
| lead_id | System |
| name | Lead Capture |
| contact | Lead Capture |
| channel | Channel Adapter / System |
| source | Tracking / System |
| need | Lead Capture |
| service_interest | Lead Capture |
| patient_location | Lead Capture |
| urgency | Lead Capture / approved rules |
| preferred_contact_time | Lead Capture / later workflow |
| plan_interest | Lead Capture |
| status | Workflow / lifecycle |
| qualification_status | Lead Qualification |
| consultation_requested | Lead Capture / Sales Follow-up |
| notes | Relevant workflow/agent |
| created_at | System |
| updated_at | System |

---

# 6. Missing Data Rule

Missing data is a valid state.

Example:

```json
{
  "name": null,
  "contact": null,
  "patient_location": null
}
```

This is better than inventing values.

---

# 7. Validation Rules

The agreed rules include:

1. channel must not be empty;
2. sender ID should exist for channel conversations;
3. text may be empty only for supported attachment-only messages;
4. never infer missing customer information;
5. never assign qualification without approved rules;
6. do not classify emergencies solely from a keyword without escalation rules;
7. do not invent prices;
8. do not provide medical diagnosis;
9. invalid status values should be flagged;
10. unsupported qualification values should be flagged.

---

# 8. Lifecycle Values

The documented lifecycle values are:

```text
new
contacted
needs_information
qualified
consultation_requested
booked
converted
not_qualified
inactive
human_handoff
```

These are controlled workflow states.

They should not be treated as arbitrary text fields.

---

# 9. Implementation Status Summary

| Field Group | Week 1 Status |
|---|---|
| Basic Lead identity | Implemented |
| Name/contact | Model supported |
| Source/channel | Implemented and validated |
| Need | Model + extraction |
| Service interest | Prototype extraction |
| Urgency | Prototype extraction |
| Plan interest | Prototype extraction |
| Consultation request | Prototype extraction |
| Lifecycle | Implemented |
| Qualification state | Field implemented |
| Qualification rules | Not fully implemented |
| Notes | Implemented |
| Production CRM mapping | Not implemented |

---

# 10. Data Dictionary Conclusion

The Lead data design now connects the original business requirement to the technical workflow.

The most important data rule is:

> If the customer did not provide the information, the system must not invent it.
