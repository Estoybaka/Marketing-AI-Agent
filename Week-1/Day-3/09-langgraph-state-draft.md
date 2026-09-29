# Day 3 — LangGraph State Draft

## Purpose

This is a conceptual state design for the future LangGraph implementation.

> This is NOT production LangGraph code.

## 1. What is state?

State is the information the workflow currently knows and carries between steps.

For example:

```text
message
    ↓
lead
    ↓
qualification
    ↓
sales
    ↓
scheduling
```

The workflow needs to retain relevant information as it moves.

## 2. Initial state draft

```python
state = {
    "message": {},
    "conversation": {},
    "lead": {},
    "qualification": {},
    "sales": {},
    "scheduling": {},
    "content": {},
    "errors": []
}
```

## 3. State fields

### `message`

Current normalized inbound message.

### `conversation`

Relevant conversation context.

### `lead`

Current lead record.

### `qualification`

Qualification information/result.

### `sales`

Sales/follow-up information.

### `scheduling`

Consultation and booking information.

### `content`

Information used by the content workflow.

### `errors`

Errors encountered during processing.

## 4. Conceptual graph

```text
Normalized Message
       |
       v
Lead Capture
       |
       v
Lead Record
       |
       v
Lead Qualification
       |
   +---+---+
   |       |
   v       v
Need     Qualified
Info        |
   |        |
   +---+----+
       |
       v
Sales Follow-up
       |
       v
Consultation Requested?
      /       \
    No         Yes
    |           |
    v           v
Follow-up   Scheduling
                |
                v
             Booking
```

## 5. Important distinction

### State

The larger set of information being carried through the workflow.

### Status

One field describing the lead's lifecycle stage.

For example:

```json
{
  "lead": {
    "status": "qualified"
  }
}
```

`qualified` is a status.

The complete state may also contain:

```text
message
conversation
lead
qualification
sales
scheduling
errors
```

## 6. What is still unknown?

- Exact LangGraph version.
- Exact production state schema.
- Persistence strategy.
- Database.
- Error/retry strategy.
- Authentication/security implementation.
- Deployment environment.

These should not be permanently decided on Day 3.
