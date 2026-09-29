# Current State vs Target State

## Day 1 — September 21, 2026

---

# 1. Purpose

This document separates:

1. **Current State** — how the company/business currently operates.
2. **Target State** — the proposed system we are expected to build.

These must not be mixed.

A target architecture should not be presented as if it already exists.

---

# 2. Status Labels

Use the following labels throughout this document:

- **CONFIRMED** — explicitly stated in the project information.
- **UNKNOWN** — not provided yet and must be investigated.
- **ASSUMPTION** — my interpretation that has not yet been verified.
- **TARGET** — part of the proposed system/architecture.
- **OUT OF SCOPE / LATER** — explicitly not a current implementation priority.

---

# 3. Current State — Business Funnel

The project requires an audit of:

- Website
- Ads
- Social
- Current inbound-lead handling

However, the project information provided so far describes the proposed architecture more clearly than the current business process.

Therefore, the actual current funnel is currently:

```text
Marketing / Discovery
        |
        v
       ?
        |
        v
Customer contacts company
        |
        v
       ?
        |
        v
Lead handling
        |
        v
       ?
        |
        v
Qualification
        |
        v
       ?
        |
        v
Sales follow-up
        |
        v
       ?
        |
        v
Consultation / booking
```

Most of these current-state steps remain **UNKNOWN** and require business discovery.

---

# 4. Current Funnel Audit

## 4.1 Marketing / Discovery

### Need to determine

- What marketing channels currently generate leads?
- Which advertisements are currently running?
- Which social platforms are actively used?
- What type of content attracts customers?
- Do ads send users to the website?
- Do ads send users directly to WhatsApp?
- Do ads send users to Facebook/Messenger?
- Are there other customer-entry points?
- Which marketing campaigns generate the most inbound inquiries?

### Status

**UNKNOWN — requires audit.**

---

# 5. Website Funnel

## Need to determine

- What website does the customer use?
- Where can a visitor contact the company?
- Is there a contact form?
- Is there a WhatsApp button?
- Is there another chat system?
- Where does a website form submission go?
- Is website lead information stored automatically?
- Does a website lead enter an existing CRM?
- Who receives website inquiries?
- Is website handling currently manual or automated?

### Status

**UNKNOWN — requires audit.**

---

# 6. Advertising Funnel

## Need to determine

- Which advertisements are currently running?
- Which platforms are used for advertising?
- Where does an advertisement send the user?
- Is the destination a website, WhatsApp, Messenger, or another channel?
- How is the source of an advertisement tracked?
- Can the company identify which advertisement generated a lead?
- Is campaign/source information stored in the CRM?

### Status

**UNKNOWN — requires audit.**

---

# 7. Social Funnel

The project mentions social channels including Facebook, TikTok, and Viber/WhatsApp-related communication.

## Need to determine

- Which social platforms are actively used for lead generation?
- Which platforms currently receive inbound messages?
- Which platforms receive comments that become leads?
- Who monitors social messages?
- Who responds?
- Is there a manual process?
- Are conversations recorded anywhere?
- Are leads created from social interactions?

### Status

**UNKNOWN — requires audit.**

---

# 8. Current Inbound Lead Handling

## Need to determine

When a customer sends a message:

1. Who sees it?
2. How quickly is it handled?
3. Is the response manual?
4. Is an automated response sent?
5. How is customer information recorded?
6. Is the customer added to a CRM?
7. Is the conversation stored?
8. Is the lead assigned to a salesperson?
9. How is qualification performed?
10. How is urgency determined?
11. How is follow-up tracked?

### Status

**UNKNOWN — requires audit.**

---

# 9. Current CRM / Lead Storage

The target architecture references a shared CRM, but the current CRM implementation has not yet been provided.

## Need to determine

- Does a CRM already exist?
- Which CRM is used?
- Who owns it?
- Which fields are currently stored?
- Are conversations stored?
- Are lead statuses stored?
- Are appointments stored?
- Can the CRM be accessed through an API?
- How are duplicate leads handled?
- Are leads assigned to staff?
- Are historical leads available?

### Status

**UNKNOWN.**

---

# 10. Current Lead Qualification

## Need to determine

- What does the company consider a qualified lead?
- Who currently qualifies leads?
- Is qualification manual?
- What questions are asked?
- What information is required?
- How is urgency determined?
- How is priority determined?
- What happens to an unqualified lead?
- What happens when information is missing?
- Who receives a qualified lead?

### Status

**UNKNOWN.**

---

# 11. Current Sales Follow-up

## Need to determine

- Who follows up with leads?
- How are leads prioritized?
- How quickly does follow-up happen?
- Which communication channel is used?
- How many follow-ups are made?
- How is follow-up status tracked?
- What happens when the customer does not respond?
- When does a lead stop receiving follow-ups?
- When is the lead handed to another employee?

### Status

**UNKNOWN.**

---

# 12. Current Consultation / Booking

## Need to determine

- How does a customer request a consultation?
- Who currently schedules consultations?
- Is there a calendar system?
- Which calendar is used?
- Does the customer select a time?
- Does a staff member select a time?
- Where is the booking recorded?
- How is booking confirmation sent?
- What information is passed to the scheduling process?

### Status

**UNKNOWN.**

---

# 13. Current Post-Booking Process

## Need to determine

- What happens after a consultation is booked?
- Who receives the booking?
- What happens before the consultation?
- Is the customer sent reminders?
- What happens after the consultation?
- How is the final customer status recorded?

### Status

**UNKNOWN.**

---

# 14. Target State — High-Level Architecture

The provided architecture indicates a LangGraph orchestrator coordinating:

```text
                         Users
                           |
                    Website / WhatsApp
                           |
                           v
              +---------------------------+
              | LangGraph Orchestrator    |
              |                           |
              | Scheduling Agent          |
              | Marketing/Sales Agent     |
              | Support Agent             |
              +-------------+-------------+
                            |
                            v
                 Shared Knowledge Base
              Services / Pricing / Calendar / CRM
```

This is the proposed target architecture, not a description of the current system.

---

# 15. Target State — Marketing/Sales Track

The Marketing/Sales area contains the following responsibilities:

```text
                Marketing / Sales
                       |
        +--------------+--------------+
        |              |              |
        v              v              v
   Lead Capture   Lead Qualification  Content
                       |
                       |
                 Sales Follow-up
```

A more detailed conceptual flow is:

```text
Inbound Message
      |
      v
Lead Capture
      |
      v
Lead Qualification
      |
      v
Lead / CRM Record
      |
      v
Sales Follow-up
      |
      v
Consultation Interest
      |
      v
Scheduling Agent
      |
      v
Calendar / Booking
```

---

# 16. Target State — Channel Adapter

The target architecture includes:

```text
Facebook --------+
WhatsApp --------+
TikTok ----------+--> Channel Adapter
Viber -----------+
                       |
                       v
                Normalized Message
                       |
                       v
                Marketing/Sales
                     Agents
```

The purpose is to make downstream agent logic independent of the specific source channel.

---

# 17. Target Normalized Message

The current target schema is:

```json
{
  "channel": "...",
  "sender_id": "...",
  "text": "...",
  "timestamp": "...",
  "attachments": []
}
```

## Meaning

| Field | Meaning |
|---|---|
| `channel` | Platform from which the message originated |
| `sender_id` | Sender identifier from that platform |
| `text` | Text content of the message |
| `timestamp` | Time associated with the message |
| `attachments` | Attached media/files |

The final validation rules and attachment schema are not yet defined.

---

# 18. Target Channel Strategy

## Phase 1 — Facebook

**CONFIRMED TARGET PRIORITY**

The project explicitly says to start with Facebook.

Expected technology:

- Meta Graph API
- Messenger Platform

The project notes that a verified Business/Developer account and app review are required.

---

## Phase 2 — WhatsApp

**TARGET / LATER**

Expected technology:

- WhatsApp Business Cloud API

Requirements mentioned:

- Registered Business Account
- Pre-approved outbound message templates

---

## TikTok

**OUTBOUND-ONLY FOR V1**

The project states that the Content Posting API supports publishing but there is no general third-party inbound comment/DM API for this use case.

Therefore:

```text
Content Agent
      |
      v
TikTok publishing
```

while:

```text
TikTok comments / DMs
      |
      v
Human monitoring / reply
```

---

## Viber

**LATER / NICE TO HAVE**

Viber Business Messages API is mentioned, with approval lead time similar to WhatsApp.

It is not a core first implementation priority.

---

# 19. Target Lead Record

The project gives a simple lead record:

```text
name
contact
need
when_needed
status
```

The Week 1 task additionally specifies:

```text
urgency
source
```

Therefore the current candidate schema is:

```text
Lead
 |
 +-- name
 +-- contact
 +-- need
 +-- when_needed
 +-- urgency
 +-- source
 +-- status
```

The explicitly mentioned status values are:

```text
new
contacted
booked
```

Additional statuses must not be invented without confirmation.

---

# 20. Source vs Channel

These fields should not automatically be treated as identical.

Example:

```text
source = facebook_ad
channel = whatsapp
```

A user could discover the company through a Facebook advertisement and later contact the company through WhatsApp.

Therefore the final definitions of `source` and `channel` must be clarified.

---

# 21. Target Content Workflow

The Content Agent should generate platform-appropriate variants from one source brief.

```text
                  Source Brief
                       |
                       v
                 Content Agent
                       |
          +------------+------------+
          |            |            |
          v            v            v
       Facebook      TikTok      WhatsApp
        variant      variant       variant
```

This avoids maintaining separate unrelated content-generation workflows for every platform.

---

# 22. Target Sales-to-Scheduling Handoff

The project says Sales Follow-up will eventually hand off consultation booking to the Scheduling Agent.

Therefore:

```text
Lead
  |
  v
Qualification
  |
  v
Sales Follow-up
  |
  v
Customer ready for consultation
  |
  v
Scheduling Agent
  |
  v
Calendar
  |
  v
Booking
```

The exact handoff data contract is not yet defined.

---

# 23. Shared Knowledge Base

The architecture identifies shared information such as:

- Services
- Pricing
- Calendar
- CRM

The target architecture shows agents reading from and writing to shared information.

However, it is unknown whether this is:

1. One physical knowledge base/database, or
2. Several systems accessed through a common agent/tool layer.

This needs confirmation.

---

# 24. Current vs Target Summary

| Area | Current State | Target State |
|---|---|---|
| Lead source | Unknown | Multiple channels, starting with Facebook |
| Message handling | Unknown | Channel adapter |
| Message format | Unknown | Normalized common message |
| Lead capture | Unknown/manual process to audit | Lead Capture Agent |
| Qualification | Unknown/manual process to audit | Lead Qualification Agent |
| Content | Unknown | Content Agent |
| Sales follow-up | Unknown/manual process to audit | Sales Follow-up Agent |
| CRM | Existing system unknown | Shared CRM/information layer |
| Scheduling | Current process unknown | Scheduling Agent |
| Orchestration | Current system unknown | LangGraph |
| Agent framework | Current system unknown | LangChain |
| Backend | Current system unknown | FastAPI direction |
| Language | Current system unknown | Python |
| TikTok | Current process unknown | Outbound-only for V1 |
| Viber | Current process unknown | Later/nice-to-have |

---

# 25. Critical Discovery Gap

The project currently gives us a strong description of the **target system**, but not enough information about the **current company funnel**.

Therefore the most important Week 1 discovery work is:

```text
Current business process
        |
        v
Document actual process
        |
        v
Identify manual steps
        |
        v
Identify existing systems
        |
        v
Identify pain points
        |
        v
Map automation opportunities
        |
        v
Compare with target architecture
```

Do not design the final implementation only from the target diagram.

The current process must first be understood.
