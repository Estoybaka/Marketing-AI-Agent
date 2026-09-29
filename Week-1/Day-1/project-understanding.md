# Project Understanding

## Day 1 — September 21, 2026

## Project Track

**Marketing, Sales & Lead-Generation Sub-Agents**

---

# 1. Project Overview

The project is to build a small suite of AI agents that supports the company's marketing, lead-generation, sales, and eventual consultation-booking workflow.

The four sub-agent responsibilities for this track are:

1. Lead Capture
2. Lead Qualification
3. Content
4. Sales Follow-up

The broader architecture also contains high-level agents for:

1. Scheduling
2. Marketing/Sales
3. Support

The Marketing/Sales area is the main area covered by this internship track.

> **Important:** The exact relationship between the high-level Marketing/Sales agent and the four sub-agents must be confirmed during the kickoff/technical discussion.

---

# 2. Confirmed Project Information

The following information comes directly from the project information provided by the senior/project brief.

## 2.1 Week 1 Tasks

Week 1 includes:

1. Audit the current funnel:
   - Website
   - Ads
   - Social
   - Current inbound-lead handling

2. Define the scope of each sub-agent:
   - Lead Capture
   - Lead Qualification
   - Content
   - Sales Follow-up

3. Map the data fields that need to be tracked per lead.

4. Set up the development environment on the agreed stack.

---

# 3. High-Level Architecture

The provided architecture shows a LangGraph orchestrator that coordinates three high-level areas:

```text
                         USERS
                    Website / WhatsApp
                            |
                            v
              +---------------------------+
              |   LangGraph Orchestrator  |
              |                           |
              |  +---------------------+  |
              |  | Scheduling Agent    |  |
              |  +---------------------+  |
              |                           |
              |  +---------------------+  |
              |  | Marketing/Sales     |  |
              |  +---------------------+  |
              |                           |
              |  +---------------------+  |
              |  | Support Agent       |  |
              |  +---------------------+  |
              +-------------+-------------+
                            |
                            v
                 Shared Knowledge Base
                 Services / Pricing /
                 Calendar / CRM
```

The architecture indicates that the orchestrator shares state between the high-level agents and that the agents read from and write to shared information.

---

# 4. My Track: Marketing, Sales & Lead Generation

The Marketing/Sales area is responsible for the lead-generation and sales-related workflow.

The project brief identifies four sub-agent responsibilities:

```text
Marketing / Sales
       |
       +-- Lead Capture
       |
       +-- Lead Qualification
       |
       +-- Content
       |
       +-- Sales Follow-up
```

These responsibilities should be treated as separate scopes rather than assuming that one agent does everything.

---

# 5. What Is an Agent Scope?

An agent scope defines:

- What the agent is responsible for.
- What information it receives.
- What information or action it produces.
- What tools/systems it can use.
- What the agent must not do.
- When the agent should hand work to another agent or a human.

A useful way to define every agent is:

```text
Agent
 |
 +-- Input
 |
 +-- Responsibility
 |
 +-- Output
 |
 +-- Tools / systems
 |
 +-- Boundaries
 |
 +-- Handoff conditions
```

The exact details below are my current understanding and must be validated against the company's requirements.

---

# 6. Lead Capture Agent

## Confirmed responsibility

The project says there will be an agent that captures leads from the company's inbound channels.

The Lead Capture Agent should therefore be concerned with turning an incoming customer interaction into a usable lead record or updating an existing lead record.

## Possible input

A normalized inbound message:

```json
{
  "channel": "...",
  "sender_id": "...",
  "text": "...",
  "timestamp": "...",
  "attachments": []
}
```

## Expected responsibility

The agent/system may need to:

- Identify that an interaction represents a potential lead.
- Capture available customer information.
- Create or update a lead record.
- Preserve the source/channel information.
- Pass relevant information to Lead Qualification.

## Current candidate lead fields

The project explicitly mentions a simple lead record containing:

- name
- contact
- need
- when they need it
- status

The Week 1 task additionally mentions:

- urgency
- source

Therefore the current candidate field list is:

```text
name
contact
need
when_needed
urgency
source
status
```

The final schema is still to be confirmed.

## Possible boundaries

The Lead Capture Agent should not automatically be assumed to:

- Qualify a lead.
- Decide sales priority.
- Book a consultation.
- Generate marketing content.
- Handle every customer-support question.

Those responsibilities belong elsewhere unless the final design explicitly combines them.

## Unknowns

- How duplicate leads are detected.
- Whether Lead Capture directly writes to the CRM.
- Whether Lead Capture asks the customer for missing information.
- Whether Lead Capture sends an immediate response.
- What exactly qualifies an interaction as a lead.
- What happens when lead creation fails.

---

# 7. Lead Qualification Agent

## Confirmed responsibility

The project says there will be an agent that qualifies and routes leads.

Therefore the Lead Qualification Agent should analyze captured lead information and determine how the lead should proceed.

## Possible input

- Lead record
- Customer message
- Conversation history
- Information collected by Lead Capture

## Possible responsibility

The agent may:

- Understand what the customer needs.
- Determine whether sufficient information is available.
- Determine urgency.
- Determine whether the lead is qualified.
- Identify missing information.
- Route the lead to the appropriate next step.

## Important distinction

Qualification should not be understood as simply:

> "An AI that talks to customers."

A better working definition is:

> The Lead Qualification Agent receives lead/conversation information, determines the information required for qualification, evaluates the lead according to company-defined criteria, and routes the lead appropriately.

## Unknowns

The following are not yet defined:

- Exact qualification criteria.
- Exact qualification categories.
- Exact urgency rules.
- Required qualification questions.
- Whether qualification is automatic.
- When human approval is required.
- What happens to unqualified leads.
- Who receives qualified leads.
- Whether the agent can disqualify a lead.

---

# 8. Content Agent

## Confirmed responsibility

The Content Agent should generate platform-appropriate variants of one source brief.

The project specifically gives the following design principle:

```text
One source brief
       |
       v
Content Agent
       |
       +-- Facebook version
       |
       +-- TikTok version
       |
       +-- Other platform-specific versions
```

The agent should not be thought of as independently writing unrelated content for every platform.

## Example

Source brief:

```text
Promote the company's consultation service.
```

The Content Agent may eventually produce:

```text
Facebook:
A longer explanatory post.

TikTok:
A short caption appropriate for TikTok.

WhatsApp:
A concise customer-oriented message.
```

## Possible input

- Source brief
- Campaign information
- Target audience
- Platform
- Brand guidelines
- Desired content type

## Possible output

- Platform-specific content variants.
- Potentially drafts for human review.
- Potentially content for publishing workflows.

## Unknowns

- Exact content types required.
- Whether the agent publishes automatically.
- Whether human approval is required.
- Which platforms must be supported.
- What brand guidelines exist.
- What company knowledge should be available to the agent.
- Whether content generation is connected to campaign management.

---

# 9. Sales Follow-up Agent

## Confirmed responsibility

The Sales Follow-up Agent should run sales follow-up and eventually help with booking consultation calls.

The project states that booking will eventually hand off into the Scheduling Agent.

Therefore the current conceptual flow is:

```text
Lead
  |
  v
Qualification
  |
  v
Sales Follow-up
  |
  v
Customer wants consultation
  |
  v
Scheduling Agent
  |
  v
Calendar
```

## Possible responsibility

The Sales Follow-up Agent may:

- Continue the sales conversation.
- Follow up with qualified leads.
- Determine whether the customer is ready for a consultation.
- Encourage the next appropriate sales step.
- Initiate a booking handoff to the Scheduling Agent.
- Update the lead status.

## Important boundary

The Sales Follow-up Agent should not automatically be considered the owner of the calendar.

The current brief indicates that consultation scheduling will eventually be handed to the Scheduling Agent.

## Unknowns

- Follow-up timing.
- Number of follow-ups.
- Follow-up channels.
- Follow-up message rules.
- Human approval requirements.
- Conditions for escalation.
- Conditions for stopping follow-up.
- Exact handoff contract with Scheduling Agent.

---

# 10. Agent Scope Summary

| Agent | Current responsibility | Candidate input | Candidate output | Major boundary |
|---|---|---|---|---|
| Lead Capture | Capture inbound leads | Normalized message | Lead record/update | Should not automatically own qualification |
| Lead Qualification | Qualify and route leads | Lead + conversation | Qualification/routing result | Exact qualification rules are unknown |
| Content | Generate platform-specific variants | Source brief + context | Content drafts/variants | Exact publishing workflow is unknown |
| Sales Follow-up | Follow up with leads and move toward consultation | Lead + qualification + conversation | Follow-up action/message/handoff | Scheduling should eventually be handled by Scheduling Agent |

---

# 11. Channel Architecture

The project requires a channel adapter layer.

The current target channels mentioned are:

- Facebook
- WhatsApp
- TikTok
- Viber

The architecture is:

```text
Facebook --------+
WhatsApp --------+
TikTok ----------+--> Channel Adapter --> Normalized Message
Viber -----------+
```

The key principle is:

> The same Lead Capture/Qualification logic should run regardless of which channel the message came from.

---

# 12. Why the Channel Adapter Exists

Different platforms provide different APIs and different message structures.

Without normalization:

```text
Lead Qualification
 |
 +-- Facebook-specific logic
 +-- WhatsApp-specific logic
 +-- TikTok-specific logic
 +-- Viber-specific logic
```

With normalization:

```text
Facebook ----+
WhatsApp ----+
TikTok ------+--> Channel Adapter --> Common Message --> Agents
Viber -------+
```

The agents can therefore primarily operate on the common internal message format rather than knowing every platform's API format.

---

# 13. Normalized Message Format

The project specifies:

```json
{
  "channel": "...",
  "sender_id": "...",
  "text": "...",
  "timestamp": "...",
  "attachments": []
}
```

## Field meanings

### channel

The platform from which the message originated.

Example:

```text
facebook
```

### sender_id

The sender's identifier on the relevant platform.

### text

The textual message content.

### timestamp

The time associated with the message/event.

### attachments

Files or media associated with the message.

Possible attachment types may include images, audio, documents, or video.

The exact attachment schema is not yet defined.

---

# 14. Two-Way Channel Adapter

The architecture describes the channel adapter as two-way.

Conceptually:

```text
                 INBOUND

Platform
   |
   v
Channel Adapter
   |
   v
Normalized Message
   |
   v
Agents


                 OUTBOUND

Agents
   |
   v
Channel Adapter
   |
   v
Platform
```

This means the adapter will eventually need to support both receiving messages and sending responses back through the appropriate platform.

Exact outbound message contracts are not yet defined.

---

# 15. Channel Priority

The project explicitly says:

> Start with one channel, not four.

## First priority: Facebook

Facebook should be implemented first.

The project describes Facebook as the initial channel because it has a clear API and is intended to provide the first end-to-end implementation.

The Facebook integration is expected to involve:

- Meta Graph API
- Messenger Platform

The project also notes that a verified Business/Developer account and app review are needed.

## Second priority: WhatsApp

WhatsApp is the next full two-way channel to consider.

The project specifies:

- WhatsApp Business Cloud API
- Registered Business Account
- Outbound message templates require pre-approval

## TikTok

For V1, TikTok is planned as outbound-only.

The project states that there is no general third-party inbound comment/DM API for this use case.

Therefore:

```text
TikTok content publishing
        |
        v
Possible automation

TikTok inbound comments/DMs
        |
        v
Human monitoring/reply
```

## Viber

Viber is considered a later/nice-to-have channel.

Its Business Messages API has an approval lead time similar to WhatsApp.

---

# 16. Target Lead Flow

The current target understanding is:

```text
                    Customer
                       |
                       v
                  Facebook
                       |
                       v
              Facebook API
                       |
                       v
              Channel Adapter
                       |
                       v
            Normalized Message
                       |
                       v
                Lead Capture
                       |
                       v
             Lead Qualification
                       |
                       v
                Lead / CRM
                       |
                       v
             Sales Follow-up
                       |
                       v
           Consultation Interest
                       |
                       v
              Scheduling Agent
                       |
                       v
                   Calendar
                       |
                       v
                  Booked
```

This is the target concept and must be validated during technical discussions.

---

# 17. Shared Knowledge Base / Shared Information

The architecture contains a shared knowledge base with information such as:

- Services
- Pricing
- Calendar
- CRM

The high-level agents are shown as reading from and writing to this shared information.

Important distinction:

The diagram does not yet establish whether these are literally stored in one physical database.

Possible conceptual separation:

```text
Business knowledge
    |
    +-- Services
    +-- Pricing

Operational systems
    |
    +-- CRM
    +-- Calendar
```

This must be clarified.

---

# 18. LangChain and LangGraph

The project specifies:

- Agents are built using LangChain.
- The orchestrator is built using LangGraph.

Current understanding:

```text
LangChain
    |
    +-- Agent implementation / agent components


LangGraph
    |
    +-- Orchestration
    +-- Workflow
    +-- Shared state
    +-- Agent coordination
```

Exact implementation patterns are to be discussed during the kickoff/technical session.

---

# 19. Current Technical Direction

The currently mentioned technology direction is:

```text
Programming language:
Python

Agent framework:
LangChain

Orchestration:
LangGraph

API/backend:
FastAPI

MCP:
FastMCP / MCP-related tooling

Development:
Local machine

IDE:
VSCode or Cursor
```

The exact:

- versions
- package manager
- repository structure
- database
- deployment
- authentication
- environment configuration
- testing setup

are not yet confirmed.

---

# 20. Current State vs Target State

The most important discovery principle for Week 1 is:

> Do not mix the current business process with the proposed architecture.

The current state describes what the company actually does today.

The target state describes what the software is intended to become.

The project brief provides significant information about the target state, but the actual current business funnel still needs to be audited.

---

# 21. Day 1 Status

## Confirmed

- Project track is Marketing, Sales & Lead Generation.
- Four sub-agent responsibilities are Lead Capture, Lead Qualification, Content, and Sales Follow-up.
- LangGraph is intended for orchestration.
- LangChain is intended for agents.
- Python is the programming language.
- FastAPI and FastMCP/MCP are part of the stated technical direction.
- A channel adapter is required.
- The normalized message fields are specified.
- Facebook is the first channel to implement.
- WhatsApp is a later full two-way channel.
- TikTok is outbound-only for V1.
- Viber is a later/nice-to-have channel.
- Content should generate platform-appropriate variants from one source brief.
- A simple lead record is required.
- Sales Follow-up will eventually hand off consultation booking to the Scheduling Agent.

## Unknown

- Exact current business funnel.
- Existing CRM.
- Existing lead-handling process.
- Existing website lead process.
- Existing advertising process.
- Existing social-media lead process.
- Exact qualification rules.
- Exact routing rules.
- Exact follow-up rules.
- Exact human-approval rules.
- Final lead schema.
- Exact knowledge-base implementation.
- Exact orchestrator workflow.
- Exact Scheduling handoff contract.
- Exact technical stack versions and project structure.

---

# 22. Core Learning From Day 1

The project should not be approached as:

> "Build four chatbots."

The current understanding is closer to:

> Build a coordinated system in which channel-specific communication is normalized, specialized agents handle specific business responsibilities, shared business/customer information is available to the appropriate components, and the LangGraph orchestrator coordinates the broader workflow.

The next engineering step is to convert this understanding into precise agent contracts, data models, workflows, and implementation tasks.
