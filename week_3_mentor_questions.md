# Week 1–3 Mentor Questions

## Purpose

These questions are based on my Week 1 lead-capture work, Week 2 FAQ/LangGraph work, the Week 3 lead-collection requirement, and the new system architecture shared by the mentor.

---

## 1. Week 3 Lead Collection

**Question to mentor:**

> For Week 3, when a user shows interest, should the agent ask follow-up questions to collect their name, contact, and need, and then save the lead?

**Why I need this detail:**

I need to understand the expected conversation flow before implementing the lead collection.

---

## 2. Lead Storage

**Question to mentor:**

> Where should we save the lead information for Week 3 — in the CRM, database, or somewhere else?

**Why I need this detail:**

The Week 3 requirement says to save the lead, but the exact storage system has not been specified.

---

## 3. Connect Week 1 and Week 2

**Question to mentor:**

> Should I integrate my Week 1 lead-capture logic with the Week 2 LangGraph FAQ workflow?

**Why I need this detail:**

Week 1 focused on lead capture and Week 2 introduced the FAQ workflow using LangGraph. I need to know whether these should now work together.

---

## 4. Marketing/Sales Agent

**Question to mentor:**

> Should my lead-capture functionality become part of the Marketing/Sales agent in the new LangGraph orchestrator?

**Why I need this detail:**

The new architecture says the Marketing/Sales agent handles leads and campaigns, which matches the lead-capture work I have already done.

---

## 5. LangGraph Orchestrator

**Question to mentor:**

> Should I convert my current workflow into LangGraph nodes and connect it to the main orchestrator?

**Why I need this detail:**

The new architecture says the main orchestrator will be built using LangGraph, so I need to understand how my existing work should fit into it.

---

## 6. Shared State

**Question to mentor:**

> What information should be shared between the FAQ/Support agent and the Marketing/Sales agent? Should we use the same state for the user's message and lead information?

**Why I need this detail:**

The orchestrator is expected to share state between agents, so I need to know what state structure I should follow.

---

## 7. CRM / Database

**Question to mentor:**

> For the shared knowledge base and CRM, will you provide the database or CRM/API that we should connect to?

**Why I need this detail:**

The architecture mentions services, pricing, calendar, and CRM, but I need to know which actual technology or API I should use.

---

## 8. Facebook and WhatsApp

**Question to mentor:**

> For Facebook and WhatsApp, should I first make the agent work with the normalized message format locally and then connect the actual APIs?

**Why I need this detail:**

My Week 1 work already uses a common message structure with `channel`, `sender_id`, `text`, `timestamp`, and `attachments`. I need to know whether this should be completed locally before the real integrations.

---

# Most Important Questions to Ask First

If I only have time to ask a few questions, I will ask these:

1. **For Week 3, when a user shows interest, should the agent ask follow-up questions to collect their name, contact, and need, and then save the lead?**

2. **Where should we save the lead information — CRM, database, or somewhere else?**

3. **Should I integrate my Week 1 lead-capture logic with the Week 2 LangGraph FAQ workflow?**

4. **Should my lead-capture functionality become part of the Marketing/Sales agent in the new LangGraph orchestrator?**





# Week 2 Handoff and Kickoff Questions

## 1. Purpose

This document turns Week 1's remaining unknowns into clear questions for the next project discussion.

The rule is:

```text
Unknown
   ↓
Question
   ↓
Decision
   ↓
Documentation
   ↓
Implementation
   ↓
Test
```

---

# 2. What Is Ready for Week 2

The following are ready:

- project context,
- target architecture,
- public funnel audit,
- agent scope,
- Lead data dictionary,
- NormalizedMessage,
- Lead model,
- validation,
- lifecycle,
- GraphState,
- Lead Capture node,
- local workflow,
- tests,
- fixtures,
- Week 1 evidence.

---

# 3. Business Questions

## Lead Sources

1. What are the actual Lead sources today?
2. Which source should be tracked as the primary source?
3. Are Facebook Ads already producing Leads?
4. Are there other paid sources?
5. How should referrals be represented?

---

## Qualification

1. What exactly makes a Lead qualified?
2. Which fields are required before qualification?
3. What makes a Lead not qualified?
4. What is the definition of a sales-ready Lead?
5. Who owns the final qualification decision?

---

## Sales Follow-up

1. What can Sales Follow-up answer automatically?
2. Which questions require human approval?
3. How quickly should follow-up happen?
4. How many follow-up attempts are expected?
5. When should a Lead be moved to human handoff?

---

## Human Handoff

1. What exact situation triggers human handoff?
2. Who receives the handoff?
3. How is the handoff recorded?
4. What Lead information must be passed to the human?
5. How does the workflow know that a human has taken over?

---

# 4. Data Questions

1. Which Lead fields are mandatory?
2. Which fields are customer-provided?
3. Which fields can be internally enriched?
4. Which fields must remain nullable?
5. What are the final lifecycle values?
6. Who is allowed to change lifecycle status?
7. Which values are authoritative?

---

# 5. Channel Questions

1. Which channel should be integrated first?
2. What is the exact Facebook integration plan?
3. When should WhatsApp be integrated?
4. Which channels require human monitoring?
5. What is the expected channel-to-source mapping?

---

# 6. CRM Questions

1. Does a CRM already exist?
2. If yes, which CRM?
3. What is the authoritative Lead record?
4. Which fields must sync?
5. Who owns CRM updates?
6. Should AI-created Leads automatically enter the CRM?

---

# 7. Scheduling Questions

1. Which booking system is used?
2. Which calendar is authoritative?
3. What counts as a confirmed booking?
4. How is the booking result returned?
5. What happens when no appointment is available?
6. Who handles booking failures?

---

# 8. Content Questions

1. What is the approved source brief?
2. Who approves content?
3. Which platforms should Content support first?
4. What claims require approval?
5. What services and plans can be mentioned?
6. What content requires human review?

---

# 9. Technical Questions

The Week 1 context discussed:

- Python,
- LangChain,
- LangGraph,
- FastAPI,
- FastMCP / MCP,
- local development,
- VS Code / Cursor.

The following still need confirmation:

1. Exact Python version.
2. Exact package versions.
3. LLM/provider.
4. Package manager.
5. Final repository structure.
6. Database.
7. CRM integration method.
8. Deployment platform.
9. Testing framework/version.
10. Authentication/security design.
11. Environment variable strategy.
12. Logging and monitoring approach.

---

# 10. Recommended Week 2 Technical Starting Point

The technical sequence should be:

```text
Approved Business Rules
        ↓
Finalize Data Contracts
        ↓
Finalize Validation
        ↓
Finalize Lifecycle
        ↓
Finalize Agent Interfaces
        ↓
Add Orchestration
        ↓
Integrate First Real Channel
        ↓
Add Persistence / CRM
        ↓
Implement Qualification
        ↓
Connect Scheduling
        ↓
Add Monitoring
        ↓
End-to-End Testing
```

---

# 11. Handoff Principle

The Week 1 foundation should not be discarded.

The next phase should build on:

```text
NormalizedMessage
Lead
Validation
Lifecycle
GraphState
Workflow
Tests
```

The business rules should be added only after they are confirmed.

---

# Why We Should Standardize Python and Package Versions

Since all of our agents will eventually be integrated, I think it would be better if we agree on the same **Python and package versions** from the beginning.

If everyone uses different versions based on what they are familiar with, each agent may work correctly in its own environment, but we could face **dependency conflicts or API differences** when integrating them.

Standardizing later could also require us to downgrade or upgrade packages and modify code that has already been developed.

If we use the same stable versions from the start, we can develop and test under a **consistent environment** and make the final integration much easier.

## Strong Reasons

### 1. Avoid Dependency Conflicts

Different versions of **LangChain, LangGraph, FastAPI, or MCP-related packages** may have different dependencies.

One agent may require a package version that conflicts with another agent.

Using standardized versions from the beginning reduces the risk of these conflicts.

### 2. Avoid API Changes

Frameworks such as **LangChain and LangGraph** can change APIs between versions.

Code written for one version may require changes when moved to another version.

Using the same versions across the team ensures that everyone develops against the same APIs.

### 3. Easier Integration

If every agent is developed and tested using the same environment, combining them later becomes much more predictable.

We can focus on **agent logic and communication** instead of spending time solving environment and dependency problems.

### 4. Avoid Rewriting Existing Code

If versions are standardized only after development, some team members may need to change already-written code.

This can:

- Waste development time
- Require unnecessary code changes
- Introduce new bugs
- Delay integration

Agreeing on versions early helps avoid these problems.

### 5. Easier Debugging

If everyone uses the same versions, a problem that occurs in one environment is easier to reproduce in another developer's environment.

The team can therefore identify more easily whether a problem is caused by:

- The code
- A dependency
- The Python version
- The development environment

This makes debugging faster and more reliable.

### 6. Easier Deployment

The development environment should ideally be close to the final deployment environment.

Using fixed dependency versions makes it easier to reproduce the same environment during deployment.

We can use a dependency file such as:

- `requirements.txt`
- `pyproject.toml`

This allows everyone to install the same dependencies and versions.

## Conclusion

Since our agents will eventually be integrated into one system, it is better to **standardize the Python version and major package versions from the beginning**.

This will help us:

- Avoid dependency conflicts
- Avoid unexpected API differences
- Make integration easier
- Prevent unnecessary code rewrites
- Make debugging easier
- Make deployment more predictable

Instead of solving compatibility problems at the end of the project, we can establish a **common development environment now** and build all agents against it.
