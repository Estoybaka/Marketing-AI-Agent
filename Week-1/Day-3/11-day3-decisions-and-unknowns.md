# Day 3 — Decisions and Unknowns

## Purpose

This file records what we decided for the design and what we intentionally did not decide because evidence is missing.

## 1. Decisions / TARGET design choices

### Decision 1 — Normalize inbound messages

TARGET:

All inbound channel messages should be converted into a common internal format before reaching downstream agents.

### Decision 2 — Keep agent responsibilities separate

TARGET:

Lead Capture, Qualification, Sales Follow-up, Scheduling, and Content should have separate responsibilities.

### Decision 3 — Keep Scheduling separate

TARGET:

Sales Follow-up should hand consultation intent to Scheduling instead of owning calendar logic.

### Decision 4 — Preserve source and channel separately

TARGET:

`source` describes original lead origin.

`channel` describes the current conversation channel.

### Decision 5 — Use evidence labels

Use:

```text
CONFIRMED
ASSUMPTION
UNKNOWN
TARGET
```

### Decision 6 — Do not invent qualification rules

Qualification rules remain UNKNOWN.

### Decision 7 — Use approved/public information for responses

Agents should not invent prices, medical claims, or customer information.

## 2. Unknown technical decisions

The following remain UNKNOWN:

- Exact Python version
- Exact LangChain version
- Exact LangGraph version
- Exact FastAPI version
- Exact FastMCP/MCP implementation
- Database
- LLM/provider
- Package manager
- Repository structure
- Deployment
- Testing framework
- Production environment
- Authentication/security
- Persistence strategy

These should not be permanently selected prematurely.

## 3. Unknown business decisions

- Actual qualification criteria
- Actual lead status model
- Actual CRM
- Actual lead assignment
- Actual channel ownership
- Who monitors each channel
- Whether all channels share one team
- Whether messages are automatically captured today
- Internal escalation rules
- Internal response templates
- Human approval rules
- Exact scheduling workflow
- Exact sales-to-scheduling handoff

## 4. Unknown integration decisions

- Exact Facebook webhook behavior
- Exact WhatsApp Cloud API implementation
- Exact Instagram integration
- Exact TikTok workflow
- Exact Viber workflow
- Attachment format
- Conversation ID strategy
- Message ID strategy

## 5. Questions for the senior/mentor

1. What is the actual CRM, if one exists?
2. What are the real lead statuses?
3. What makes a lead qualified?
4. Who owns incoming leads?
5. What information must be collected before consultation?
6. What is the approved escalation process?
7. What is the exact scheduling handoff?
8. What are the approved pricing sources?
9. Which knowledge source is considered authoritative?
10. Which channels should be integrated first in implementation?
11. What database should the team use?
12. Which LLM/provider is approved?
13. What repository structure should be followed?
14. What are the deployment constraints?

## 6. Important principle

An UNKNOWN is not a failure.

It is better to record:

```text
UNKNOWN
```

than to create a false business rule and build the system around it.
