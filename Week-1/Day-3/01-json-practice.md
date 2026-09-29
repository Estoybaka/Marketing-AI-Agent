# Day 3 — JSON Practice

## Purpose

This file introduces JSON, the basic data format we will use to represent messages, leads, and agent state.

> **Project rule:** This project is being designed from public information and clearly labeled assumptions only. JSON examples below are illustrative and are not claims about Saathi Sneha Care's internal systems.

## 1. What is JSON?

JSON (JavaScript Object Notation) is a structured way to represent information.

Example:

```json
{
  "name": "Example Customer",
  "need": "home care",
  "urgency": "unknown"
}
```

A JSON object contains **key-value pairs**.

- `name` → key
- `"Example Customer"` → value
- `need` → key
- `"home care"` → value

## 2. Common JSON data types

### String

```json
{
  "channel": "facebook"
}
```

### Number

```json
{
  "message_count": 3
}
```

### Boolean

```json
{
  "consultation_requested": false
}
```

### Null

```json
{
  "phone": null
}
```

`null` means the value is currently unavailable or not provided.

### Array

```json
{
  "attachments": []
}
```

An array can contain multiple values:

```json
{
  "services": [
    "caregiver_support",
    "wellness_checks"
  ]
}
```

### Nested object

```json
{
  "contact": {
    "phone": null,
    "email": null
  }
}
```

## 3. Example normalized message

This is a TARGET internal format, not a confirmed platform payload:

```json
{
  "channel": "facebook",
  "sender_id": "test_user_001",
  "text": "I need home care for my mother.",
  "timestamp": "2026-09-23T10:00:00",
  "attachments": []
}
```

## 4. Example lead

This is a TARGET schema draft:

```json
{
  "lead_id": "lead_001",
  "name": null,
  "contact": null,
  "channel": "facebook",
  "source": "facebook",
  "need": "home care",
  "service_interest": null,
  "patient_location": null,
  "urgency": null,
  "preferred_contact_time": null,
  "plan_interest": null,
  "status": "new",
  "qualification_status": "unknown",
  "consultation_requested": false,
  "notes": [],
  "created_at": "2026-09-23T10:00:00",
  "updated_at": "2026-09-23T10:00:00"
}
```

## 5. Important project rule

Never add information simply because it seems likely.

For example, if a customer says:

> "I need care for my father."

Do not invent:

```json
{
  "patient_location": "Kathmandu"
}
```

unless the customer or an approved source actually provides that information.

## 6. Practice tasks

Create five small JSON objects yourself:

1. General inquiry
2. Specific service inquiry
3. Urgent request
4. Pricing inquiry
5. Consultation request

For each object, identify:

- keys
- values
- data types
- missing information

## Learning checkpoint

You should be able to explain:

> JSON is a structured format used to pass and store information between parts of our system.



