# Day 3 — Architecture

## Purpose

This document combines the message, lead, agent, and state designs into one target architecture.

> This is a TARGET architecture. It does not claim that the current company system already works this way.

## 1. Inbound lead flow

```text
                INBOUND CHANNELS
                       |
                       v
                Channel Adapters
                       |
                       v
                Normalized Message
                       |
                       v
                Lead Capture Agent
                       |
                       v
                   Lead Record
                       |
                       v
             Lead Qualification Agent
                       |
             +---------+---------+
             |                   |
             v                   v
       Need Information       Qualified
             |                   |
             +---------+---------+
                       |
                       v
               Sales Follow-up
                       |
                       v
          Consultation Requested?
                  /         \
                No           Yes
                |             |
                v             v
             Follow-up    Scheduling Agent
                              |
                              v
                       Booking / Calendar
```

## 2. Content flow

Content is a separate parallel workflow:

```text
Approved Source Brief
        |
        v
   Content Agent
        |
   +----+----+----+
   |    |    |    |
   v    v    v    v
Facebook Instagram WhatsApp TikTok
```

The content agent should transform approved information into platform-specific content.

It should not publish autonomously without authorization.

## 3. Why use a Channel Adapter?

Without normalization:

```text
Facebook → Lead Capture
WhatsApp → Lead Capture
Instagram → Lead Capture
Website → Lead Capture
```

Lead Capture would need to understand every platform's payload.

With normalization:

```text
Facebook ----\
WhatsApp -----\
Instagram ----- > Channel Adapter → Normalized Message
Website ------/
```

Lead Capture only needs to understand one internal message format.

## 4. Agent boundaries

### Lead Capture

Owns lead creation/update.

### Lead Qualification

Owns qualification only when approved rules exist.

### Sales Follow-up

Owns appropriate prospect conversation.

### Scheduling

Owns booking/calendar logic.

### Content

Owns content transformation from approved source material.

## 5. Scheduling boundary

```text
Sales Follow-up
       |
       | consultation requested
       v
Scheduling Agent
       |
       v
Calendar / Booking
```

The exact handoff contract is UNKNOWN.

## 6. Shared data direction

A future system may use shared lead/CRM information, but the actual database and CRM are UNKNOWN.

Do not permanently choose the production database on Day 3.
