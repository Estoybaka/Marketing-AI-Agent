# Day 3 — Normalized Message Schema

## Purpose

The Channel Adapter receives messages from different platforms and converts them into one common internal format.

## Architecture

```text
Facebook / WhatsApp / Website / Other Channels
                    |
                    v
             Channel Adapter
                    |
                    v
          Normalized Message
                    |
                    v
             Lead Capture
```

The Channel Adapter prevents downstream agents from needing separate platform-specific logic.

## 1. Initial normalized message

TARGET draft:

```json
{
  "channel": "...",
  "sender_id": "...",
  "text": "...",
  "timestamp": "...",
  "attachments": []
}
```

## 2. Field definitions

| Field | Type | Requirement | Status | Meaning |
|---|---|---|---|---|
| `channel` | string | Required for channel messages | TARGET | Current conversation channel |
| `sender_id` | string | Expected for channel conversations | TARGET | Platform/user identifier |
| `text` | string/null | Usually expected | TARGET | Message text |
| `timestamp` | string | Expected | TARGET | Message time |
| `attachments` | array | Optional | TARGET | Files/images/media associated with message |

## 3. Potential future fields

These should be considered, but are not confirmed:

```text
message_id
conversation_id
sender_name
metadata
```

### Why might they be useful?

- `message_id` → message identification/deduplication
- `conversation_id` → grouping messages into a conversation
- `sender_name` → human-readable sender information
- `metadata` → channel-specific information

These are TARGET design considerations, not confirmed company requirements.

## 4. Attachment draft

Possible TARGET structure:

```json
{
  "type": "image",
  "url": "...",
  "filename": "example.jpg"
}
```

The exact attachment structure is UNKNOWN until actual integrations are defined.

## 5. Empty messages

A message should normally contain text.

However, attachment-only messages may exist on supported channels.

Therefore:

```text
text empty + no attachment
→ invalid candidate message

text empty + supported attachment
→ potentially valid
```

Exact platform behavior remains UNKNOWN.

## 6. Example

```json
{
  "channel": "facebook",
  "sender_id": "test_user_001",
  "text": "I need care for my mother.",
  "timestamp": "2026-09-23T10:00:00",
  "attachments": []
}
```

## 7. What is confirmed vs unknown?

### CONFIRMED

Publicly visible channels/contact entry points include Facebook/Messenger, WhatsApp, Instagram, phone and website/contact journey.

### TARGET

A common normalized message contract should be used internally.

### UNKNOWN

- Exact Facebook webhook payload
- Exact WhatsApp payload
- Exact internal message ID
- Exact conversation ID
- Exact attachment format
- Whether a current internal normalization system already exists

## Design rule

Downstream agents should consume the normalized format rather than platform-specific payloads.
