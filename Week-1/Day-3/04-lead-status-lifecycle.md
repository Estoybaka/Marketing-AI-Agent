# Day 3 — Lead Status Lifecycle

## Purpose

This document defines a proposed lifecycle for a lead.

> Important: these are TARGET states. The company's actual internal CRM lifecycle is UNKNOWN.

## 1. Proposed lifecycle

```text
NEW
 |
 v
CONTACTED
 |
 v
NEEDS_INFORMATION
 |
 v
QUALIFIED
 |
 v
CONSULTATION_REQUESTED
 |
 v
BOOKED
 |
 v
CONVERTED
```

## 2. Possible branches

```text
NEW
 |
 +------------------+
 |                  |
 v                  v
NOT_QUALIFIED     INACTIVE

HUMAN_HANDOFF can occur where human intervention is required.
```

## 3. Meaning of each proposed state

### NEW

A lead has been created but has not yet progressed.

### CONTACTED

A response/contact interaction has occurred.

### NEEDS_INFORMATION

Important information is still missing.

### QUALIFIED

The lead satisfies approved qualification rules.

> Current qualification rules are UNKNOWN.

Therefore an agent must not mark a lead as qualified merely because the request sounds suitable.

### CONSULTATION_REQUESTED

The customer has expressed a desire for consultation/assessment.

### BOOKED

A consultation/booking has been successfully scheduled.

### CONVERTED

The lead has progressed to the project's defined conversion outcome.

The exact business definition of "converted" is UNKNOWN.

### NOT_QUALIFIED

A lead does not meet approved qualification rules.

### INACTIVE

No further activity according to an approved inactivity rule.

### HUMAN_HANDOFF

Human review or intervention is required.

## 4. Example transition

```text
Customer asks about home care
        |
        v
NEW
        |
        v
CONTACTED
        |
        v
NEEDS_INFORMATION
        |
        v
[customer provides missing information]
        |
        v
QUALIFIED
        |
        v
CONSULTATION_REQUESTED
```

This is a TARGET example.

## 5. Important restrictions

Do not create a qualification transition unless approved qualification rules exist.

Do not create an emergency transition based only on a keyword.

Do not assume the company's current CRM uses these exact states.
