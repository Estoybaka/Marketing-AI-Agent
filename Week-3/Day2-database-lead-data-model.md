# Week 3 – Day 2: Database + Lead Data Model

**Project:** Elder-Care Lead Generation and Funnel Automation System  
**Week:** 3  
**Day:** 2  
**Task:** Database + Lead Data Model  
**Status:** ✅ COMPLETED

---

## 1. Day 2 Objective

The purpose of Week 3 Day 2 was to design the database structure that will store and manage leads captured by the Lead Capture Agent.

The work focused on:

- Understanding basic database concepts.
- Defining the lead data model.
- Deciding which fields are required.
- Choosing appropriate data types.
- Defining validation rules.
- Defining allowed values for controlled fields.
- Defining the lead completion rule.
- Defining the `next_field` logic.
- Defining the lead lifecycle/status.
- Creating and validating sample lead records.
- Preparing a clear schema that can later guide implementation.

> **Important:** This document represents the completed design and learning work for Day 2. It does not claim that a production database has already been deployed or connected to the application.

---

# 2. Database Fundamentals

Before designing the project database, the following basic concepts were established.

| Term | Definition | Project Example |
|---|---|---|
| Database | An organized system used to store and retrieve information. | Storage system for elder-care leads. |
| Table | A structured collection of related records arranged in rows and columns. | `Leads` table. |
| Record | One complete row representing one individual lead. | Anita's lead record. |
| Field | A category/column that stores one type of information. | `name`, `email`, `need`, `status`. |
| Value | The actual information stored in a field for one record. | `Anita` is the value of `name`. |
| Schema | The blueprint defining a table's fields, types, rules, and constraints. | Final `Leads` schema. |
| Primary Key | A unique identifier for each record. | `lead_id = L001`. |
| NULL | Indicates that information is currently unavailable or was not provided. | `phone = NULL`. |

### Example

If a lead provides:

```text
name = Anita
```

Then:

- `name` is the **field**.
- `Anita` is the **value**.
- Anita's entire row is the **record**.
- The `Leads` table contains Anita's record.
- The database stores the table and its information.

---

# 3. Final Lead Data Model

The initial database model contains one primary table called `Leads`.

```text
LEADS
├── lead_id
├── name
├── email
├── phone
├── need
├── urgency
├── source
├── status
├── created_at
├── next_field
└── lead_complete
```

---

# 4. Complete Lead Data Dictionary

| Field | Type | Required? | Provided/Set By | Definition / Rule |
|---|---|---|---|---|
| `lead_id` | Text | Yes | System | Unique system-generated ID, such as `L001`. Primary key. |
| `name` | Text | Yes | Customer | Name of the lead/customer. |
| `email` | Text | Conditional | Customer | Email address. Email OR phone must exist. |
| `phone` | Text | Conditional | Customer | Phone number. Email OR phone must exist. |
| `need` | Text | Yes | Customer → Agent | Description of the care/service need. |
| `urgency` | Enum | No / qualification | Agent / Qualification | `Low`, `Medium`, or `High`. |
| `source` | Enum | No | System / Channel | `Website`, `Facebook`, `WhatsApp`, `Referral`, or `Other`. |
| `status` | Enum | Yes | System / Agents | `New`, `Qualified`, `Follow-up`, `Converted`, or `Lost`. Default is `New`. |
| `created_at` | Date/Time | Yes | System | Timestamp automatically created when the lead is created. |
| `next_field` | Text/Enum | No / agent state | Lead Capture Agent | Identifies the next missing information the agent should request. |
| `lead_complete` | Boolean | Yes | System / Logic | `true` only when the lead completion rule is satisfied. |

---

# 5. Why Email and Phone Are Separate Fields

The original concept used one general `contact` field.

This was improved by separating contact information into:

```text
email
phone
```

This is better because each field represents one clear piece of information.

A customer may provide:

### Only email

```text
email = anita@gmail.com
phone = NULL
```

### Only phone

```text
email = NULL
phone = +977-9812345678
```

### Both

```text
email = anita@gmail.com
phone = +977-9812345678
```

### Neither

```text
email = NULL
phone = NULL
```

In the last case, the lead is not complete.

### Contact completion rule

At least one of the following must exist:

```text
email OR phone
```

Both can also be present.

---

# 6. Data Types and Design Decisions

| Field | Chosen Type | Reason |
|---|---|---|
| `lead_id` | Text | IDs such as `L001` are identifiers, not quantities. |
| `name` | Text | Names are textual information. |
| `email` | Text | Email addresses contain letters, symbols, and numbers. |
| `phone` | Text | Phone numbers can contain `+`, spaces, hyphens, country codes, and leading zeros. |
| `need` | Text | Care requirements are descriptive and can vary in length. |
| `urgency` | Enum | Only `Low`, `Medium`, and `High` are accepted. |
| `source` | Enum | Only defined lead sources are accepted. |
| `status` | Enum | Only defined lifecycle states are accepted. |
| `created_at` | Date/Time | Records when the lead was created. |
| `next_field` | Text/Enum | Stores the next information the Lead Capture Agent should request. |
| `lead_complete` | Boolean | Only `true` or `false` are needed. |

## Why phone is Text instead of Number

A phone number should be stored as text.

For example:

```text
+977-9812345678
```

A phone number is not something the system mathematically calculates.

It may contain:

- `+`
- country codes
- spaces
- hyphens
- leading zeros

Therefore:

```text
phone = TEXT
```

is the correct design choice.

---

# 7. Primary Key: `lead_id`

`lead_id` is the primary key.

A primary key uniquely identifies each record.

## Why not use name?

Names can be duplicated.

For example:

```text
Anita
Anita
```

Two different people may have the same name.

## Why not use email?

Email is not ideal as the primary key because:

- Email may be missing.
- Email can change.
- Some leads may only provide a phone number.

## Final decision

Use:

```text
lead_id
```

Example:

```text
L001
L002
L003
L004
```

Each ID must be unique.

---

# 8. NULL and Missing Data Policy

The project uses `NULL` consistently when information has not been provided or is currently unavailable.

For example:

```text
email = NULL
```

means that an email address is currently unavailable.

The project should not mix different representations such as:

```text
None
""
"N/A"
"unknown"
NULL
```

for the same meaning.

## Project rule

Use:

```text
NULL
```

for missing information.

### Examples

| Situation | Correct Value |
|---|---|
| No email provided | `email = NULL` |
| No phone provided | `phone = NULL` |
| Urgency not determined | `urgency = NULL` |
| Source not known | `source = NULL` |

---

# 9. Controlled Values

Some fields should not accept arbitrary values.

## 9.1 Urgency

Allowed values:

```text
Low
Medium
High
```

### Low

Used when the customer is planning ahead.

Example:

```text
"We may need care next month."
```

### Medium

Used when care is needed soon but not immediately.

Example:

```text
"We need someone starting next week."
```

### High

Used when the need is immediate or very urgent.

Example:

```text
"We need someone starting tomorrow."
```

Another example:

```text
"My father is being discharged from the hospital tomorrow and needs care."
```

> These are the project's initial urgency rules and can be refined later during qualification implementation.

---

# 10. Source Values

Allowed values:

```text
Website
Facebook
WhatsApp
Referral
Other
```

Examples:

```text
source = Website
```

or:

```text
source = Referral
```

---

# 11. Status Values

Allowed values:

```text
New
Qualified
Follow-up
Converted
Lost
```

### New

The lead has just been captured.

### Qualified

The lead has enough information and meets the project's qualification criteria.

### Follow-up

The lead requires additional communication.

### Converted

The lead successfully became a customer or moved to the service.

### Lost

The lead is no longer an active opportunity or did not convert.

---

# 12. Lead Completion Rule

A lead is complete when all of the following conditions are true:

1. `name` exists.
2. `need` exists.
3. At least one contact method exists:
   - `email`, OR
   - `phone`.

The formal rule is:

```text
lead_complete =
    name exists
    AND need exists
    AND (email exists OR phone exists)
```

## Complete example

```text
name = Anita
email = anita@gmail.com
phone = NULL
need = Overnight care for father
```

Result:

```text
lead_complete = true
```

because:

- Name exists.
- Need exists.
- Email exists.

## Incomplete example

```text
name = Sarah
email = NULL
phone = NULL
need = Care for elderly grandfather
```

Result:

```text
lead_complete = false
```

because both contact methods are missing.

---

# 13. Important Distinction: Complete vs Status

`lead_complete` and `status` are different concepts.

For example:

```text
lead_complete = true
status = New
```

is completely valid.

It means:

> The lead contains the minimum required information, but the lead has not yet gone through the next stage of qualification.

Therefore:

```text
lead_complete
```

answers:

> "Do we have the minimum required lead information?"

while:

```text
status
```

answers:

> "Where is this lead in the business process?"

---

# 14. `next_field` Logic

`next_field` is the Lead Capture Agent's working state.

It tells the agent what information should be requested next.

## Rules

| Missing Information | `next_field` |
|---|---|
| Name missing | `name` |
| Need missing | `need` |
| Both email and phone missing | `email_or_phone` |
| Email missing but phone exists | `NULL` |
| Phone missing but email exists | `NULL` |
| Name, need, and contact complete | `NULL` |

### Example 1

```text
name = NULL
email = anita@gmail.com
phone = NULL
need = Care for elderly father
```

The missing required field is:

```text
name
```

Therefore:

```text
next_field = name
```

### Example 2

```text
name = Anita
email = NULL
phone = NULL
need = Care for father
```

The system needs a contact method.

Therefore:

```text
next_field = email_or_phone
```

### Example 3

```text
name = Anita
email = anita@gmail.com
phone = NULL
need = Care for father
```

The lead is complete.

Therefore:

```text
next_field = NULL
```

---

# 15. System-Generated Fields

The system is responsible for generating or calculating several fields.

| Field | System Responsibility |
|---|---|
| `lead_id` | Generate a unique ID. |
| `created_at` | Automatically record the creation date/time. |
| `status` | Set initial value to `New` and update it as the lead progresses. |
| `lead_complete` | Calculate from the lead completion rule. |
| `next_field` | Determine which required information is still missing. |

## `created_at`

The customer should not provide this value.

It should be generated by the system when the lead record is created.

---

# 16. Lead Status Lifecycle

A typical lead lifecycle is:

```text
New
  ↓
Qualified
  ↓
Follow-up
  ↓
Converted
```

A lead can also move to:

```text
Lost
```

when it is no longer an active opportunity.

Example:

```text
New → Qualified → Follow-up → Converted
```

Another possible path:

```text
New → Qualified → Lost
```

---

# 17. Validation Rules

The following validation rules were finalized.

1. `lead_id` must be unique.
2. `name` must not be `NULL` for a complete lead.
3. `need` must not be `NULL` for a complete lead.
4. At least one of `email` or `phone` must exist for a complete lead.
5. `email` must be stored as text when provided.
6. `phone` must be stored as text when provided.
7. `urgency`, when provided, must be `Low`, `Medium`, or `High`.
8. `source`, when provided, must be `Website`, `Facebook`, `WhatsApp`, `Referral`, or `Other`.
9. `status` must be `New`, `Qualified`, `Follow-up`, `Converted`, or `Lost`.
10. `created_at` must be system-generated.
11. `lead_complete` must be calculated using the defined completion rule.
12. Missing values must use `NULL` consistently.

---

# 18. Sample Lead Records

## Record 1 – Anita

```text
lead_id = L001
name = Anita
email = anita@gmail.com
phone = NULL
need = Overnight care for father
urgency = NULL
source = NULL
status = New
created_at = system-generated
next_field = NULL
lead_complete = true
```

### Validation

- Name exists ✅
- Need exists ✅
- Email exists ✅
- Lead complete ✅

---

## Record 2 – Raj

```text
lead_id = L002
name = Raj
email = NULL
phone = +977-9812345678
need = Daytime care for mother
urgency = NULL
source = NULL
status = New
created_at = system-generated
next_field = NULL
lead_complete = true
```

### Validation

- Name exists ✅
- Need exists ✅
- Phone exists ✅
- Lead complete ✅

---

## Record 3 – Sarah

```text
lead_id = L003
name = Sarah
email = NULL
phone = NULL
need = Help/care at home for grandfather
urgency = NULL
source = NULL
status = New
created_at = system-generated
next_field = email_or_phone
lead_complete = false
```

### Validation

- Name exists ✅
- Need exists ✅
- Email missing ❌
- Phone missing ❌
- Lead incomplete ✅
- Next field correctly set to `email_or_phone` ✅

---

## Record 4 – Maya

```text
lead_id = L004
name = Maya
email = NULL
phone = +977-9800000000
need = Daytime care for 78-year-old mother
urgency = Medium
source = Referral
status = New
created_at = system-generated
next_field = NULL
lead_complete = true
```

### Validation

- Name exists ✅
- Need exists ✅
- Phone exists ✅
- Urgency is valid ✅
- Source is valid ✅
- Lead complete ✅

---

## Record 5 – David

```text
lead_id = L005
name = David
email = david@example.com
phone = NULL
need = Daytime care for 85-year-old father
urgency = High
source = Website
status = New
created_at = system-generated
next_field = NULL
lead_complete = true
```

### Validation

- Name exists ✅
- Need exists ✅
- Email exists ✅
- High urgency is valid ✅
- Website source is valid ✅
- Lead complete ✅

---

## Record 6 – Priya

```text
lead_id = L006
name = Priya
email = NULL
phone = +977-9811111111
need = Care for elderly mother
urgency = High
source = Facebook
status = New
created_at = system-generated
next_field = NULL
lead_complete = true
```

### Validation

- Name exists ✅
- Need exists ✅
- Phone exists ✅
- High urgency is valid ✅
- Facebook source is valid ✅
- Lead complete ✅

---

# 19. Sample Records Summary

| Lead ID | Name | Email | Phone | Need | Urgency | Source | Status | Next Field | Complete |
|---|---|---|---|---|---|---|---|---|---|
| L001 | Anita | anita@gmail.com | NULL | Overnight care for father | NULL | NULL | New | NULL | true |
| L002 | Raj | NULL | +977-9812345678 | Daytime care for mother | NULL | NULL | New | NULL | true |
| L003 | Sarah | NULL | NULL | Help/care at home for grandfather | NULL | NULL | New | email_or_phone | false |
| L004 | Maya | NULL | +977-9800000000 | Daytime care for 78-year-old mother | Medium | Referral | New | NULL | true |
| L005 | David | david@example.com | NULL | Daytime care for 85-year-old father | High | Website | New | NULL | true |
| L006 | Priya | NULL | +977-9811111111 | Care for elderly mother | High | Facebook | New | NULL | true |

---

# 20. Future Database Relationship

The initial Day 2 design uses a single `Leads` table to keep the first implementation simple.

A future version may add a `Follow-ups` table.

Example:

```text
FOLLOW_UPS
├── followup_id
├── lead_id
├── message
└── date
```

The `lead_id` in the `Follow-ups` table would reference:

```text
Leads.lead_id
```

This would create a one-to-many relationship:

```text
One Lead
   ↓
Many Follow-ups
```

For example:

```text
L001
 ├── Follow-up 1
 ├── Follow-up 2
 └── Follow-up 3
```

This relationship is identified for future implementation but is not required to complicate the initial Day 2 model.

---

# 21. Final Schema

The final conceptual schema is:

```text
TABLE: Leads

lead_id        TEXT        PRIMARY KEY, NOT NULL
name           TEXT        REQUIRED
email          TEXT        OPTIONAL / CONDITIONAL
phone          TEXT        OPTIONAL / CONDITIONAL
need           TEXT        REQUIRED
urgency        ENUM        Low | Medium | High
source         ENUM        Website | Facebook | WhatsApp | Referral | Other
status         ENUM        New | Qualified | Follow-up | Converted | Lost
created_at     DATETIME    REQUIRED, SYSTEM-GENERATED
next_field     TEXT/ENUM   AGENT STATE
lead_complete  BOOLEAN     REQUIRED
```

---

# 22. Database Design Rules – Final Version

The final rules for the project are:

```text
1. Every lead receives a unique lead_id.

2. name is required.

3. need is required.

4. At least one contact method is required:
   email OR phone.

5. Email and phone are stored separately.

6. Phone is stored as text.

7. Missing values use NULL.

8. urgency uses:
   Low | Medium | High

9. source uses:
   Website | Facebook | WhatsApp | Referral | Other

10. status uses:
    New | Qualified | Follow-up | Converted | Lost

11. New leads start with:
    status = New

12. created_at is generated by the system.

13. lead_complete is true only when:
    name exists
    AND need exists
    AND (email exists OR phone exists)

14. next_field identifies the next missing information.

15. lead_id is the primary key.
```

---

# 23. Day 2 Exercises Completed

## Exercise 1 – Identify Database Terms

Example:

```text
name = Anita
```

Answer:

```text
name = field
Anita = value
```

Anita's entire row is a:

```text
record
```

The collection of similar records is the:

```text
Leads table
```

---

## Exercise 2 – Choose the Primary Key

Possible choices:

```text
name
email
lead_id
```

Correct answer:

```text
lead_id
```

Reason:

A primary key must uniquely identify each record. Names can repeat and emails can be missing or changed.

---

## Exercise 3 – Determine Whether a Lead Is Complete

Given:

```text
name = Anita
email = anita@gmail.com
phone = NULL
need = Care for father
```

Answer:

```text
lead_complete = true
```

Reason:

Name exists, need exists, and email exists.

---

## Exercise 4 – Determine Whether a Lead Is Complete

Given:

```text
name = Sarah
email = NULL
phone = NULL
need = Care for grandfather
```

Answer:

```text
lead_complete = false
```

Reason:

Both contact methods are missing.

Correct:

```text
next_field = email_or_phone
```

---

## Exercise 5 – Choose the Correct Phone Data Type

Question:

Should this be stored as a number or text?

```text
+977-9812345678
```

Correct answer:

```text
TEXT
```

Reason:

Phone numbers are identifiers/contact details and may contain symbols, country codes, formatting, and leading zeros.

---

# 24. Day 2 Evidence

The following work was completed during Day 2:

- [x] Database fundamentals understood.
- [x] Table concept understood.
- [x] Record concept understood.
- [x] Field concept understood.
- [x] Value concept understood.
- [x] Schema concept understood.
- [x] Leads table designed.
- [x] Lead fields finalized.
- [x] Email and phone separated.
- [x] Contact requirement defined.
- [x] Data types selected.
- [x] Controlled values defined.
- [x] Primary key defined.
- [x] NULL policy defined.
- [x] Lead completion rule defined.
- [x] `next_field` logic defined.
- [x] Lead status lifecycle defined.
- [x] Validation rules defined.
- [x] Sample lead records created.
- [x] Sample records validated.
- [x] Future Follow-ups relationship documented.
- [x] Final schema documented.

---

# 25. Day 2 Completion Checklist

| Task | Status |
|---|---|
| Understand database fundamentals | ✅ COMPLETED |
| Define the Leads table | ✅ COMPLETED |
| Finalize all lead fields | ✅ COMPLETED |
| Separate email and phone | ✅ COMPLETED |
| Define data types | ✅ COMPLETED |
| Define required and conditional fields | ✅ COMPLETED |
| Define allowed enum values | ✅ COMPLETED |
| Define primary key | ✅ COMPLETED |
| Define NULL policy | ✅ COMPLETED |
| Define lead completion rule | ✅ COMPLETED |
| Define `next_field` logic | ✅ COMPLETED |
| Define lead status lifecycle | ✅ COMPLETED |
| Create sample records | ✅ COMPLETED |
| Validate sample records | ✅ COMPLETED |
| Document future relationship concept | ✅ COMPLETED |
| Prepare Day 2 documentation | ✅ COMPLETED |

---

# 26. Final Day 2 Outcome

Week 3 Day 2 successfully established the complete conceptual database and lead data model for the elder-care lead-generation system.

The Lead Capture Agent now has a clearly defined structure for:

- Identifying a lead.
- Storing the lead's name.
- Storing email and/or phone.
- Recording the customer's care need.
- Recording urgency.
- Recording the lead source.
- Tracking lead status.
- Recording creation time.
- Knowing which field should be requested next.
- Determining whether the lead has the minimum required information.

The resulting model is detailed enough to guide the later database implementation and Lead Capture Agent integration.

---

# 27. Final Status

> ## ✅ WEEK 3 – DAY 2 COMPLETED

### Completed

**Learning:** ✅  
**Database design:** ✅  
**Lead data model:** ✅  
**Data dictionary:** ✅  
**Validation rules:** ✅  
**Completion logic:** ✅  
**Sample records:** ✅  
**Evidence:** ✅  
**Documentation:** ✅

### Not claimed as completed

Actual production database deployment or application/database connection has **not** been claimed as part of this documentation. Those are implementation activities to be completed when required by the project schedule.

---

## 28. Key Takeaway

The most important result from Day 2 is that the project now has a clear answer to:

> **"What information do we store about every lead, what format should it have, what is required, and when is a lead considered complete?"**

The answer is defined by the `Leads` schema and rules in this document.
