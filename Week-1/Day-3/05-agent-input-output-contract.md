# Day 3 — Agent Input/Output Contracts

## Purpose

Every agent needs a clear contract:

```text
What enters?
    ↓
What does the agent do?
    ↓
What leaves?
```

## 1. High-level contracts

| Agent | Input | Output |
|---|---|---|
| Lead Capture | Normalized Message | Lead Record |
| Lead Qualification | Lead + Approved Rules | Qualification Result |
| Sales Follow-up | Lead + Conversation | Response + Updated Lead |
| Scheduling | Consultation Request | Booking Result |
| Content | Approved Source Brief | Platform-specific Content |

These are TARGET contracts.

## 2. Lead Capture Agent

### Input

```text
Normalized Message
```

### Output

```text
Lead Record
```

### Responsibilities

- Capture available lead information.
- Preserve channel.
- Preserve source where known.
- Create or update a lead.
- Pass the lead forward.

### Must not

- Invent customer information.
- Diagnose.
- Invent pricing.
- Qualify without approved rules.
- Own calendar logic.

## 3. Lead Qualification Agent

### Input

```text
Lead + Approved Qualification Rules
```

### Output

```text
Qualification Result
```

### Responsibilities

- Read lead information.
- Identify missing information.
- Apply approved rules.
- Determine routing.

### Current limitation

Actual qualification criteria are UNKNOWN.

Therefore the production agent must not invent qualification rules.

## 4. Sales Follow-up Agent

### Input

```text
Lead + Conversation
```

### Output

```text
Response + Updated Lead
```

### Responsibilities

- Continue appropriate prospect conversations.
- Answer approved informational questions.
- Follow approved rules.
- Detect consultation intent.
- Hand off to Scheduling.

### Must not

- Diagnose.
- Invent pricing.
- Make unsupported promises.
- Own calendar logic.

## 5. Scheduling Agent

### Input

```text
Consultation Request
```

### Output

```text
Booking Result
```

### Boundary

Sales Follow-up identifies consultation intent and hands off.

Scheduling owns booking/calendar behavior.

Exact handoff contract is currently UNKNOWN.

## 6. Content Agent

### Input

```text
Approved Source Brief
```

### Output

```text
Platform-specific Content
```

### Responsibilities

- Convert one approved source brief into platform-specific versions.
- Preserve approved business information.

### Must not

- Invent medical claims.
- Invent prices.
- Publish autonomously without authorization.

## 7. Design principle

An agent should have one clear responsibility and should not silently take ownership of another agent's responsibility.
