# Lead Data Dictionary --- Day 2 Draft

**Company:** Saathi Sneha Care\
**Date:** September 22, 2026

## 1. Evidence Rule

This is a **proposed target data model**, not a confirmed existing CRM
schema.

-   CONFIRMED = public evidence.
-   ASSUMPTION = reasonable hypothesis.
-   UNKNOWN = not publicly established.
-   TARGET = future-system proposal.

## 2. Core Fields

 | Field                    | Example            | Status            | Notes                                              |
|--------------------------|--------------------|-------------------|----------------------------------------------------|
| `lead_id`                | `lead_001`         | TARGET            | Unique identifier                                  |
| `name`                   | `Ram Sharma`       | ASSUMPTION        | Customer name                                      |
| `contact`                | phone/email        | ASSUMPTION        | Contact information                                |
| `channel`                | `facebook`         | TARGET            | Current conversation channel                       |
| `source`                 | `facebook_ad`      | TARGET            | Original acquisition source                        |
| `text`                   | customer message   | TARGET            | Raw inbound message                                |
| `need`                   | post-hospital care | ASSUMPTION        | Stated need                                        |
| `service_interest`       | post-hospital care | ASSUMPTION        | Listed service if identifiable                     |
| `patient_location`       | Kathmandu          | ASSUMPTION        | Parent/patient location                            |
| `urgency`                | urgent             | ASSUMPTION        | Relevant because urgent services exist             |
| `preferred_contact_time` | evening            | CONFIRMED concept | Contact page asks customer to state availability   |
| `plan_interest`          | Chronic Care       | ASSUMPTION        | Public plans exist                                 |
| `status`                 | new                | TARGET            | Lifecycle state                                    |
| `qualification_status`   | unknown            | UNKNOWN           | Internal rules not public                          |
| `consultation_requested` | true               | TARGET            | Scheduling signal                                  |
| `created_at`             | timestamp          | TARGET            | Technical field                                    |
| `updated_at`             | timestamp          | TARGET            | Technical field                                    |
| `notes`                  | ...                | TARGET            | Conversation context                               |


## 3. Source vs Channel

### Channel

``` text
facebook
whatsapp
instagram
website
phone
```

### Source

``` text
facebook_organic
facebook_ad
instagram
website
google_ad
referral
unknown
```

These are proposed values, not confirmed existing CRM values.

## 4. Status

Previously discussed candidate statuses:

``` text
new
contacted
booked
```

These are **TARGET/proposed** until the actual company status model is
confirmed.

Additional conceptual states:

``` text
qualified
needs_information
consultation_requested
```

Also proposed only.

## 5. Example Normalized Lead

``` json
{
  "lead_id": "lead_001",
  "name": null,
  "contact": null,
  "channel": "facebook",
  "source": "facebook_organic",
  "text": "My father needs help after being discharged from hospital.",
  "need": "post-hospital care",
  "service_interest": "post-hospital care",
  "patient_location": null,
  "urgency": null,
  "preferred_contact_time": null,
  "plan_interest": null,
  "status": "new",
  "qualification_status": "unknown",
  "consultation_requested": false,
  "notes": []
}
```

Missing values remain `null`; agents must not invent them.

## 6. Fields Requiring Future Confirmation

-   Exact required lead fields.
-   Exact CRM schema.
-   Existing lead status values.
-   Qualification status values.
-   Qualification information.
-   Lead ownership.
-   Source attribution.
-   Consent/privacy requirements.
-   Data retention.
-   Scheduling handoff fields.
-   Human approval requirements.
