# Agent Scope Draft --- Day 2

**Company:** Saathi Sneha Care\
**Date:** September 22, 2026

## 1. Architecture Context

``` text
Users
  |
  +---- Website
  +---- Facebook
  +---- WhatsApp
  +---- Instagram / other channels
  |
  v
Channel Adapter Layer
  |
  v
Marketing & Sales Agents
  |
  +---- Lead Capture
  +---- Lead Qualification
  +---- Sales Follow-up
  |
  v
Scheduling Agent
  |
  v
Consultation / Booking
```

Content operates around approved marketing source material.

## 2. Lead Capture Agent

### TARGET

-   Receive normalized inbound messages.
-   Detect potential lead intent.
-   Extract information supplied by the customer.
-   Preserve channel/source.
-   Create or update lead record.
-   Pass lead to qualification.

### Must not

-   Invent missing information.
-   Diagnose.
-   Invent qualification rules.
-   Own calendar.
-   Invent prices.

## 3. Lead Qualification Agent

### TARGET

-   Read lead record.
-   Identify missing information.
-   Apply approved qualification rules.
-   Route the lead.

### Inputs

``` text
Lead Record
+
Approved Qualification Rules
```

### Outputs

Potential states:

``` text
needs_information
qualified
not_qualified
ready_for_consultation
```

These labels are proposed and require confirmation.

### Critical constraint

Actual qualification criteria are **UNKNOWN**.

## 4. Content Agent

### TARGET

``` text
Approved Source Brief
        |
        v
Content Agent
        |
        +---- Facebook
        +---- Instagram
        +---- WhatsApp
        +---- TikTok
```

It should adapt approved information into platform-specific drafts.

It must not invent medical claims, pricing, or unapproved promises.

## 5. Sales Follow-up Agent

### TARGET

-   Continue prospect conversations.
-   Answer approved informational questions.
-   Provide approved service/plan information.
-   Follow approved follow-up rules.
-   Detect consultation intent.
-   Hand off to Scheduling.

### Must not

-   Diagnose.
-   Invent pricing.
-   Make unsupported promises.
-   Own calendar logic.

## 6. Scheduling Boundary

``` text
Sales Follow-up
      |
      | consultation requested
      v
Scheduling Agent
      |
      v
Calendar / Booking
```

Exact handoff fields are UNKNOWN.

## 7. Agent Boundary Table

  | Agent              | Owns                                      | Does not own                          |
|--------------------|-------------------------------------------|---------------------------------------|
| Lead Capture       | Capture/structure inbound lead            | Qualification, calendar               |
| Lead Qualification | Qualification once approved               | Medical diagnosis, scheduling         |
| Content            | Marketing content drafts                  | Autonomous publishing, medical advice |
| Sales Follow-up    | Prospect conversation/follow-up           | Calendar, diagnosis                   |
| Scheduling         | Consultation/booking                      | Lead qualification/content            |


## 8. Knowledge Requirements

Future agents will need approved information for:

-   Services
-   Care plans
-   Public pricing
-   Service availability
-   Consultation process
-   Approved FAQs
-   Escalation rules
-   Human handoff rules

The public website can be an initial source, but production use should
depend on approved knowledge.

## 9. Human-in-the-Loop Questions

UNKNOWN:

-   Which messages require human review?
-   Which medical/urgent messages must be escalated?
-   Who approves content?
-   Who approves pricing responses?
-   Who approves qualification?
-   Who receives urgent cases?
-   What happens outside normal response periods?
-   What is the emergency escalation path?
