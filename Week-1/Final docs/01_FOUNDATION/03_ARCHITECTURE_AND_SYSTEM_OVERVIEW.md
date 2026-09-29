# Architecture and System Overview

## 1. Broader Target Architecture

- The wider project is a multi-agent system.

- The conceptual target is:

  ```text
       Users
       |
       +-- Website
       +-- WhatsApp
       +-- Other Channels
       |
       v
       LangGraph Orchestrator
       |
       +-- Scheduling Agent
       +-- Marketing / Sales Agent
       +-- Support Agent
       |
       v
       Shared Knowledge Base
       |
       +-- Services
       +-- Pricing
       +-- Calendar
       +-- CRM
  ```

- This architecture is a target direction, not a claim that all components are already deployed.

---

# 2. Assigned Marketing / Sales Track

- The assigned track contains:

  ```text
   Lead Capture
   Lead Qualification
   Content
   ```

---

# 3. Channel Architecture

- The discussed channel architecture is:

  ```
  Facebook
  WhatsApp
  TikTok
  Viber
     |
     v
  Channel Adapter Layer
     |
     v
  Marketing & Sales Agents
     |
     v
  Lead / Booking Record
     |
     v
  Shared CRM
  ```

- The Channel Adapter Layer is important because downstream agents should not contain platform-specific logic.

---

# 4. Channel Priorities

## Facebook

First implementation target.

## WhatsApp

Later two-way integration.

WhatsApp Business Cloud API was discussed, including possible outbound template approval.

## TikTok

V1 direction:

- outbound content,
- human monitoring for comments and direct messages.

## Viber

Later / nice-to-have.

These are project directions and do not mean the integrations already exist.

---

# 5. Normalized Message Boundary

- A channel-specific message should become:

```text
Channel-specific payload
        ↓
Channel Adapter
        ↓
NormalizedMessage
        ↓
Downstream agents
```

- This allows Lead Capture to work with a common contract.

- The normalized message contains:

   - `sender_id`
   - `channel`
   - `text`
   - `timestamp`
   - `attachments`

---

# 6. Lead Capture Boundary

```text
NormalizedMessage
        ↓
Lead Capture
        ↓
Lead
```

- Lead Capture is responsible for extraction.

- It is not responsible for:

  - qualification,
  - booking,
  - medical diagnosis,
  - pricing decisions.

---

# 7. Validation Boundary

```text
Lead
  ↓
Validation
  ↓
PASS / FAIL
```

Validation checks the Lead rather than creating missing information.

---

# 8. Lifecycle Boundary

```text
Validated Lead
      ↓
Lifecycle Rules
      ↓
Allowed transition?
      ↓
Updated Lead
```

Lifecycle rules prevent arbitrary status changes.

---

# 9. Workflow State

The minimal shared state introduced during Day 5 is:

```python
class GraphState(BaseModel):
    message: NormalizedMessage
    lead: Lead | None = None
    errors: list[str] = Field(default_factory=list)
```

Conceptually:

```text
GraphState
├── message
├── lead
└── errors
```

---

# 10. Complete Local Workflow

```text
Incoming Message
       ↓
NormalizedMessage
       ↓
GraphState
       ↓
Lead Capture Node
       ↓
capture_lead()
       ↓
Lead
       ↓
validate_lead()
       |
       +---- invalid → STOP
       |
       +---- valid
              ↓
        lifecycle rules
              ↓
       transition_lead()
              ↓
       Updated GraphState
```

This is the technical foundation completed by Day 5.

---

# 11. Future Agent Flow

The target multi-agent business flow is:

```text
Incoming Message
       ↓
Lead Capture
       ↓
Lead
       ↓
Lead Qualification
       ↓
Qualification Result
       ↓
Sales Follow-up
       ↓
Consultation Request
       ↓
Scheduling
       ↓
Booking Result
```

Content is a separate source-driven capability.

---

# 12. Architecture Principle

The most important technical principle established during Week 1 is:

> Keep business logic independent from workflow orchestration.

Business logic:

```text
capture_lead()
validate_lead()
transition_lead()
```

Workflow:

```text
lead_capture_node()
run_lead_workflow()
```

Shared state:

```text
GraphState
```

Future orchestration:

```text
LangGraph
```

This means the underlying business functions can be tested independently before introducing a larger orchestration framework.
