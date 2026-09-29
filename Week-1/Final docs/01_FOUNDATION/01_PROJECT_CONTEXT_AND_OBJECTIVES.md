# AI Agent Project : -  Project Context and Week 1 Objectives

## 1. Document Purpose

- This document is the starting point for the Week 1 documentation set.

- It explains:

    - what the project is,
    - what the assigned track is,
    - what Week 1 was expected to achieve,
    - how the work was approached,
    - what evidence rules were followed,
    - what has and has not been treated as confirmed.

- This document should be read before the technical design documents because the technical work is intentionally built from the business and data understanding established earlier.

---

# 2. Project Identity

- **Project:** AI Agent / Multi-Agent System

- **Track:** Marketing, Sales & Lead-Generation Sub-Agents

- **Week:** Week 1

- **Technical stage at the end of Week 1:** Local Lead Capture workflow foundation

- The project is being built incrementally.

- The working principle is:

    ```text
    Understand
        ↓
    Investigate
        ↓
    Design
        ↓
    Implement locally
        ↓
    Test
        ↓
    Understand the result
        ↓
    Add the next architectural concept
        ↓
    Test again
        ↓
    Integrate later
    ```

- The project is not being treated as a system where production integrations are added before the basic data flow is understood.

---

# 3. Core Project Purpose

- The concrete Week 1 technical purpose is a **Local Lead Capture Prototype**.

- The core flow established by the end of Week 1 is:

    ```text
    Incoming Message
        ↓
    Normalize Message
        ↓
    Extract supported Lead information
        ↓
    Create Lead
        ↓
    Validate Lead
        ↓
    Apply controlled lifecycle rules
        ↓
    Pass information through workflow state
    ```

- The system should be able to answer a simple question:

    > If a customer sends a message, can the system turn that message into a structured Lead without inventing information?

- The Week 1 work then extends this question into workflow design:

    > Once a Lead exists, can the workflow validate it and move it through controlled states without mixing responsibilities?

---

# 4. Broader Multi-Agent Architecture

- The wider project is conceptually a multi-agent system coordinated through LangGraph.

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

- This is a **TARGET architecture**.

- It describes the intended direction.
---

# 5. Assigned Track

- The assigned track is: **Marketing, Sales & Lead-Generation Sub-Agents**

- The planned components are:

    1. Lead Capture Agent
    2. Lead Qualification Agent
    3. Content Agent
    4. Sales Follow-up Agent

- Scheduling remains a separate responsibility.

- The separation matters because each agent should have a clear job.

- For example:

    ```text
    Lead Capture
        ↓
    "What information did the customer provide?"

    Lead Qualification
        ↓
    "Does the Lead meet approved qualification rules?"

    Sales Follow-up
        ↓
    "What should happen next in the customer conversation?"

    Scheduling
        ↓
    "Can a real consultation be booked?"
    ```

- These questions should not be handled by one large function.

---

# 6. Week 1 Business Tasks

## Task 1 - Audit the current funnel

- Investigate:

    - website
    - ads
    - social
    - current inbound Lead handling

- The purpose is to understand where Leads may enter the system and what is publicly visible about the customer journey.

---

## Task 2 - Define the scope of each sub-agent

- The four scopes are:

    - Lead Capture
    - Lead Qualification
    - Content
    - Sales Follow-up

- The purpose is to define responsibility boundaries before implementing more agents.

---

## Task 3 - Map Lead data fields

- The original required Lead fields were:

    - name
    - contact
    - need
    - urgency
    - source

- During the technical design this was expanded into a larger Lead structure.

- The expanded structure supports:

    - customer information,
    - source/channel tracking,
    - service and plan interest,
    - urgency,
    - lifecycle,
    - qualification state,
    - consultation intent,
    - notes,
    - timestamps.

---

## Task 4 - Set up the development environment

- The project direction discussed:

    - Python
    - LangChain
    - LangGraph
    - FastAPI
    - FastMCP / MCP
    - local development
    - VS Code / Cursor

- Exact versions and production setup details were not confirmed in the provided Week 1 context.


---

# 7. Evidence Discipline

- A major agreement from the beginning was that unknown internal business information must not be invented.

- The project uses four labels.

## CONFIRMED

- Information directly supported by the available evidence.

- Example:

- The public website presents services and plans.

---

## ASSUMPTION

- A reasonable interpretation used for design, but not confirmed as an internal business rule.

- Example:

   A likely Lead may be an adult child or family member living away from Nepal who is looking for care for a parent or loved one.

---

## UNKNOWN

- Information that was not available from public information or was not confirmed.

- Examples:

    - actual Lead qualification rules,
    - current CRM,
    - exact Lead routing,
    - current internal ownership of channels.

---

## TARGET

- A proposed future design.

- Examples:

    - future LangGraph orchestration,
    - future real channel integration,
    - future shared CRM.

---

# 8. Important Working Agreements

- The following agreements were established during the first days:

1. Start from zero and understand the project first.
2. Documentation comes before large implementation.
3. Day 1 is for understanding, not coding.
4. Never guess the current business process.
5. Use `UNKNOWN` when evidence is unavailable.
6. Separate `CURRENT` from `TARGET`.
7. Facebook is the first implementation target.
8. Normalize messages before downstream agents.
9. Keep agent scopes separate.
10. Scheduling remains separate.
11. Content begins from one approved source brief.
12. Lead Capture does not qualify.
13. Qualification does not invent its own rules.
14. Sales Follow-up does not own calendar logic.
15. Agents must not invent customer information.
16. Agents must not invent prices.
17. Agents must not make medical claims or diagnoses.
18. Build a small local system before production integration.

---

# 9. Why the Project Was Built Incrementally

- The project is also a learning exercise.

- The implementation was deliberately ordered so that each new concept could be understood.

- The learning path was:

    ```text
    Python dictionaries / JSON
            ↓
    Data models
            ↓
    Functions
            ↓
    Validation
            ↓
    Lead Capture
            ↓
    Test cases
            ↓
    Automated tests
            ↓
    Lifecycle
            ↓
    Shared workflow state
            ↓
    Node-like functions
            ↓
    Workflow
            ↓
    Future LangGraph orchestration
    ```


---

# 10. Week 1 End State

- At the end of Week 1, the project should have two connected parts.

## Business discovery

 ```text
Funnel Audit
    +
Agent Scope
    +
Lead Data Dictionary
```

## Technical foundation

```text
NormalizedMessage
    ↓
Lead
    ↓
Validation
    ↓
Lifecycle
    ↓
GraphState
    ↓
Workflow
    ↓
Tests
```

