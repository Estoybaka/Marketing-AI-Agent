# Day 3 — Knowledge Boundary

## Purpose

This document defines what the agents can currently rely on and what remains unknown.

## Evidence labels

Use four labels throughout the project:

### CONFIRMED

Directly visible in public information.

### ASSUMPTION

A reasonable inference from public information.

### UNKNOWN

Cannot be established from public information.

### TARGET

A proposed future design or behavior.

## 1. Public/approved business knowledge

Potential knowledge sources:

- Public services
- Public care plans
- Public pricing, if published
- Public contact methods
- Public service availability
- Public consultation process
- Approved FAQs
- Approved content/source briefs

## 2. Public business information identified so far

The public website presents:

- Professional/home care services in Nepal
- Support for families, including families abroad
- Caregiver support
- Hospital escort
- Chronic disease monitoring
- Doctor consultation
- Lab coordination
- Medication management
- Wellness checks
- Emergency/on-demand support
- Care plans such as Care Connect, Wellness Plus, and Chronic Care
- Family updates/reporting features

The existence of these publicly presented services/plans is treated as CONFIRMED from the public investigation.

## 3. Customer journey visible publicly

The public-facing journey can be represented as:

```text
Discovery
   ↓
Inquiry
   ↓
Free Consultation / Assessment
   ↓
Needs Assessment
   ↓
Personalized Plan
   ↓
Care Begins
   ↓
Ongoing Updates
```

This is a public marketing/customer-facing journey.

It does not prove the internal CRM or sales workflow.

## 4. Internal knowledge currently UNKNOWN

Do not invent:

- Qualification criteria
- Lead assignment rules
- CRM rules
- Internal escalation process
- Internal response templates
- Human approval rules
- Exact sales handoff process
- Exact scheduling workflow
- Existing automation
- Existing integrations
- Existing database

## 5. Example

Customer asks:

> "Which plan should I choose?"

Public information may show that multiple plans exist.

However, the internal rule for recommending a plan is UNKNOWN.

Therefore:

```text
Public fact:
Plans exist.

Unknown:
Exact internal recommendation rule.
```

The agent should not invent a recommendation policy.

## 6. Source hierarchy

For Day 3 design:

```text
Public company website/social information
             ↓
Approved project documentation
             ↓
Clearly labeled assumptions
             ↓
UNKNOWN where evidence is absent
```

Never convert an assumption into a confirmed fact.

## 7. Future knowledge base

TARGET:

Agents should eventually use an approved knowledge base rather than hard-coded assumptions.

The knowledge base should distinguish public/approved information from internal rules.
