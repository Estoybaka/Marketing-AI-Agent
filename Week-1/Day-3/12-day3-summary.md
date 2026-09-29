# Week 1 — Day 3 Summary

## Student

Priyanka

## Track

Marketing, Sales & Lead-Generation Sub-Agents

## Project

AI Agent / Multi-Agent System

## Day 3 objective

Design the data and interfaces required before implementation.

```text
Business Understanding
        |
        v
Data / Interface Design
        |
        v
Later Implementation
```

## 1. What was learned

### JSON

Learned how structured information can be represented using:

- objects
- arrays
- strings
- numbers
- booleans
- null
- nested objects

### Schemas

Learned that a schema describes:

- fields
- data types
- required/optional information
- valid structures

### API concepts

Understood the basic idea of:

```text
Request
   ↓
Processing
   ↓
Response
```

### State

Understood that workflow state stores information carried between agent steps.

### Agent contracts

Understood that every agent needs:

```text
Input
   ↓
Agent responsibility
   ↓
Output
```

## 2. Normalized message

TARGET:

```json
{
  "channel": "...",
  "sender_id": "...",
  "text": "...",
  "timestamp": "...",
  "attachments": []
}
```

The exact production fields remain subject to implementation/integration decisions.

## 3. Lead schema

A TARGET lead record includes:

```text
lead_id
name
contact
channel
source
need
service_interest
patient_location
urgency
preferred_contact_time
plan_interest
status
qualification_status
consultation_requested
notes
created_at
updated_at
```

This is not a confirmed CRM schema.

## 4. Proposed lifecycle

```text
NEW
 ↓
CONTACTED
 ↓
NEEDS_INFORMATION
 ↓
QUALIFIED
 ↓
CONSULTATION_REQUESTED
 ↓
BOOKED
 ↓
CONVERTED
```

Possible branches include:

```text
NOT_QUALIFIED
INACTIVE
HUMAN_HANDOFF
```

These are TARGET states.

## 5. Agent contracts

```text
Lead Capture
Normalized Message → Lead Record

Lead Qualification
Lead + Rules → Qualification Result

Sales Follow-up
Lead + Conversation → Response + Updated Lead

Scheduling
Consultation Request → Booking Result

Content
Source Brief → Platform Content
```

## 6. Validation principles

The system should:

- require a channel
- preserve sender information where available
- handle attachment-only messages carefully
- never invent customer information
- never assign qualification without approved rules
- not classify emergencies from keywords alone
- never invent pricing
- never provide medical diagnosis
- respect agent boundaries

## 7. Knowledge boundary

### Public/approved information

Potentially includes:

- services
- care plans
- public pricing
- public contact methods
- public consultation process
- approved FAQs
- approved source briefs

### UNKNOWN

- qualification rules
- CRM rules
- lead assignment
- escalation
- internal templates
- human approval
- exact scheduling workflow

## 8. Public-information constraint

All Day 3 business design is based on:

```text
Public website
+
Public social profiles
+
Clearly labeled assumptions
```

No internal company process should be treated as confirmed without evidence.

## 9. What Day 3 did NOT do

No production:

- Facebook integration
- Facebook webhooks
- WhatsApp API
- production LangGraph
- database selection
- LLM provider selection
- autonomous sales automation
- medical decision-making
- automatic content publishing
- deployment

## 10. Day 3 success criteria

By the end of Day 3, the student should be able to explain:

1. What information enters the system.
2. What information is stored in a lead.
3. What the proposed lead lifecycle is.
4. What each agent receives.
5. What each agent returns.
6. What the future LangGraph state contains.
7. What agents must not invent.
8. Which business and technical decisions remain UNKNOWN.

## 11. Transition to Day 4+

The project progression is:

```text
Day 1
Understanding
     ↓
Day 2
Business Investigation
     ↓
Day 3
Data + Interface Design
     ↓
Day 4+
Implementation
```

The next implementation work should begin only after the schemas, contracts, and unknowns have been reviewed.
