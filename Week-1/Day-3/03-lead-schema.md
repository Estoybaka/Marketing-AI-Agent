# Day 3 — Lead Schema

## Purpose

A lead record stores the information known about a potential customer.

> This is a TARGET schema draft. It is not a confirmed Saathi Sneha Care CRM schema.

## 1. Draft lead object

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

## 2. Field dictionary

| Field | Meaning | Status |
|---|---|---|
| `lead_id` | Unique identifier for the lead | TARGET |
| `name` | Customer/lead name if provided | TARGET |
| `contact` | Contact information if provided | TARGET |
| `channel` | Current conversation channel | TARGET |
| `source` | Original source of the lead | TARGET |
| `need` | Need expressed by the customer | TARGET |
| `service_interest` | Service the customer appears interested in | TARGET |
| `patient_location` | Location of person needing care, if provided | TARGET |
| `urgency` | Urgency stated by customer | TARGET |
| `preferred_contact_time` | Preferred contact time if provided | TARGET |
| `plan_interest` | Care plan mentioned by customer | TARGET |
| `status` | Lead lifecycle stage | TARGET |
| `qualification_status` | Qualification result | TARGET |
| `consultation_requested` | Whether consultation intent was expressed | TARGET |
| `notes` | Structured/free-form relevant notes | TARGET |
| `created_at` | Creation timestamp | TARGET |
| `updated_at` | Last update timestamp | TARGET |

## 3. Candidate status values

Proposed:

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

These are TARGET values, not confirmed CRM statuses.

## 4. Source vs channel

### Channel

Where the current conversation happens.

Examples:

```text
facebook
whatsapp
instagram
website
phone
```

### Source

Where the lead originally came from.

Examples:

```text
facebook_organic
facebook_ad
instagram
website
google_ad
referral
unknown
```

Example:

```text
source = facebook_ad
channel = whatsapp
```

The customer could discover the business through a Facebook advertisement and later continue the conversation on WhatsApp.

## 5. Important rule

Do not infer missing fields.

Example:

Customer:

> "I need care for my father."

Known:

```text
need = home care
```

Unknown:

```text
patient_location = unknown
urgency = unknown
contact = unknown
```

Do not guess these values.

## 6. Public business context

The public website presents home/professional care services and a customer journey involving consultation/assessment, personalized planning, care beginning, and ongoing updates.

The public existence of services and plans is CONFIRMED from the investigated public information.

The internal rules for assigning leads to services/plans are UNKNOWN.
