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

# 12. Final Handoff State

Week 1 ends with a controlled local foundation and a documented list of business decisions still required.

The next phase therefore begins from a known state rather than from an unclear prototype.
