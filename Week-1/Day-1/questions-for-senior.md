# Questions for Senior

## Day 1 — September 21, 2026

## Purpose

This document contains questions that need to be answered before finalizing the agent design and implementation.

Questions are grouped by priority and topic.

---

# Priority Definitions

## P0 — Blocking

Answers could change the architecture, data model, agent responsibilities, or implementation plan.

## P1 — Important

Needed for detailed workflow design but may not block initial exploration.

## P2 — Later

Useful for implementation hardening, optimization, and production readiness.

---

# P0 — Blocking Questions

## 1. Current Business Funnel

1. What is the actual current lead-generation funnel?
2. How do customers currently discover the company?
3. Which website is the main entry point?
4. Which advertisements currently generate leads?
5. Which social platforms currently generate leads?
6. Where does a customer go after clicking an advertisement?
7. What happens when a customer sends an inbound message?
8. Who currently handles inbound leads?
9. Which parts of the process are manual?
10. Which parts are already automated?
11. What happens from first contact until booking?

---

# 2. Existing CRM / Lead Storage

1. Does the company currently use a CRM?
2. If yes, which CRM?
3. Where are leads currently stored?
4. Is there an existing database?
5. Who has access to the CRM?
6. Which fields are currently stored?
7. Are conversations stored?
8. Are lead statuses stored?
9. Are bookings stored?
10. Is there an API for the CRM?
11. Can the AI agents read from the CRM?
12. Can the AI agents write to the CRM?
13. How are duplicate leads handled?

---

# 3. Exact Scope of the Four Sub-Agents

1. What exactly should Lead Capture do?
2. What exactly should Lead Qualification do?
3. What exactly should Content do?
4. What exactly should Sales Follow-up do?
5. What should each agent explicitly NOT do?
6. Are these four separate agents in code?
7. Are they subgraphs/nodes inside the Marketing/Sales workflow?
8. Is there a high-level Marketing/Sales agent that calls these four sub-agents?
9. How should the four sub-agents share state?

---

# 4. Lead Qualification

1. What exactly defines a qualified lead?
2. What makes a lead unqualified?
3. What information is required before a lead can be qualified?
4. What questions should the agent ask?
5. How is urgency defined?
6. What makes a lead high priority?
7. What categories should leads be assigned to?
8. What happens if the agent does not have enough information?
9. Can the agent disqualify a lead?
10. Who receives qualified leads?
11. Which decisions require human approval?
12. Are there documented qualification rules already?

---

# 5. Lead Data Model

The current brief mentions:

```text
name
contact
need
when_needed
status
```

The Week 1 task also mentions:

```text
urgency
source
```

Questions:

1. Is this the final lead schema?
2. Should `source` and `channel` both be stored?
3. What exactly does `source` mean?
4. What exactly does `channel` mean?
5. What does `contact` contain?
6. Can a lead have multiple contact methods?
7. What format should contact information use?
8. What values are allowed for `status`?
9. Are `new`, `contacted`, and `booked` the complete status list?
10. Should conversation history be stored on the lead?
11. Should timestamps be stored?
12. Should agent decisions/reasons be stored?
13. Should lead assignment information be stored?
14. Should a unique lead ID be generated?
15. How should duplicate leads be detected?

---

# 6. Channel Architecture

1. Is Facebook definitely the first implementation channel?
2. What exact Facebook APIs should we use?
3. Which Facebook events must be handled?
4. Are Page messages required?
5. Are Page comments required?
6. Which Meta account/app will be used?
7. Who provides the Meta developer credentials?
8. Has the Meta Business/Developer account already been created?
9. Has app review been completed?
10. What webhook events should the adapter receive?
11. What outbound messages should the adapter support?
12. What is the exact normalized message schema?
13. Should the normalized schema include a message ID?
14. Should it include a conversation ID?
15. How should attachments be represented?
16. How should channel-specific errors be represented?
17. How should outbound messages be mapped back to a specific channel?

---

# 7. WhatsApp

1. When should WhatsApp implementation begin?
2. Is the WhatsApp Business Account already available?
3. Who manages the account?
4. Which phone number will be used?
5. Are message templates already available?
6. Which templates require approval?
7. Is WhatsApp required during the internship or only planned for later?
8. Should the same normalized message schema be used for WhatsApp?

---

# 8. TikTok

1. Is TikTok required for the internship deliverable?
2. Is TikTok strictly outbound-only for V1?
3. Which Content Posting API features are required?
4. Who will manually monitor comments/DMs?
5. Does content need human approval before publishing?
6. How should TikTok-generated content be tracked?

---

# 9. Viber

1. Is Viber required during the internship?
2. If not, should we only design the adapter interface for future support?
3. Is a Viber Business Messages account already available?
4. Who handles Viber approval?
5. What is the expected timeline for integration?

---

# 10. Content Agent

1. What is the exact purpose of the Content Agent?
2. What is the definition of a source brief?
3. What content types should it generate?
4. Which platforms must it support?
5. Should one source brief generate variants for multiple platforms?
6. What platform-specific differences should be considered?
7. What brand guidelines must be followed?
8. Where are brand guidelines stored?
9. Does the agent need access to services/pricing information?
10. Does the agent publish content automatically?
11. If not, who approves content?
12. What happens after content is approved?
13. Are there existing examples of company content we should use as references?

---

# 11. Sales Follow-up

1. What triggers the first follow-up?
2. How quickly should a follow-up happen?
3. How many follow-ups should happen?
4. How much time should be between follow-ups?
5. Which channel should be used?
6. Can the agent send messages automatically?
7. Does a human approve messages?
8. What should happen when the customer replies?
9. What should happen when the customer does not reply?
10. When should follow-up stop?
11. When should a lead be escalated to a human?
12. What information should be passed to Scheduling?
13. What event triggers the Scheduling handoff?

---

# 12. Scheduling Handoff

1. What exactly does the Scheduling Agent own?
2. Does Sales Follow-up only identify booking intent?
3. How is booking intent passed to Scheduling?
4. What data must be included in the handoff?
5. Which calendar system is used?
6. Can Scheduling read calendar availability?
7. Can Scheduling create bookings?
8. Who sends the booking confirmation?
9. Does the lead status become `booked` automatically?
10. What happens if no calendar slot is available?

---

# 13. Human-in-the-Loop

1. Which actions can agents perform automatically?
2. Which actions require human approval?
3. When should an agent escalate?
4. Who receives an escalation?
5. Can a human override an agent decision?
6. How should overrides be recorded?
7. What happens when an agent is uncertain?
8. What happens when the customer asks something outside the agent's scope?
9. Does generated marketing content require approval?
10. Does an outbound sales message require approval?
11. Can agents create or modify CRM records without approval?

---

# 14. Shared Knowledge Base

1. What exactly is the "Shared Knowledge Base"?
2. Is it one physical system or several connected systems?
3. Where are service details stored?
4. Where is pricing stored?
5. Where is calendar information stored?
6. Where is CRM information stored?
7. Which agents can read each data source?
8. Which agents can write to each data source?
9. How is information updated?
10. How do we prevent agents from using outdated pricing or service information?

---

# 15. LangGraph Orchestration

1. What is the exact LangGraph workflow?
2. What is the entry point into the graph?
3. What state is shared between agents?
4. Which nodes represent the four Marketing/Sales sub-agents?
5. Does the high-level Marketing/Sales agent call the sub-agents?
6. How does routing work?
7. What conditions determine the next agent?
8. What happens when an agent fails?
9. What happens when no agent can handle the request?
10. How is human handoff represented in the graph?
11. How is conversation state persisted?

---

# 16. LangChain

1. Which LangChain version should be used?
2. What LangChain components are expected?
3. Are agents expected to use tools?
4. Which tools should each agent have?
5. How should prompts be stored?
6. How should prompts be versioned?
7. What model/provider should be used?
8. Are structured outputs required?
9. Are tool calls expected to use structured schemas?

---

# 17. FastAPI / Backend

1. Which FastAPI version should be used?
2. What API endpoints are required?
3. Which endpoint receives Facebook webhooks?
4. Which endpoint sends outbound messages?
5. Should the API expose agent execution directly?
6. How should authentication work?
7. How should errors be returned?
8. How should webhook verification work?
9. How should background processing work?
10. Is a message queue required?

---

# 18. FastMCP / MCP

1. What exactly should MCP be used for in this project?
2. Which tools should be exposed through MCP?
3. Should CRM access be an MCP tool?
4. Should calendar access be an MCP tool?
5. Should knowledge-base access be an MCP tool?
6. Who owns the MCP servers?
7. Which agents are allowed to call each MCP tool?
8. What authentication/security is required?

---

# 19. Development Environment

1. Which Python version should we use?
2. Should we use VSCode or Cursor?
3. Which package manager should we use?
4. Should we use `uv`, Poetry, pip, or another tool?
5. What repository should we use?
6. What branching strategy should we follow?
7. What is the expected project directory structure?
8. Which environment variables are required?
9. How should API keys be stored locally?
10. Is there a `.env.example` file?
11. What linting tool should we use?
12. What formatting tool should we use?
13. What testing framework should we use?

---

# 20. Database / Persistence

1. Which database should be used?
2. Is a database already available?
3. Should lead records be stored in the existing CRM or a separate database?
4. Where should conversation history be stored?
5. Where should agent state be stored?
6. How long should data be retained?
7. How should database migrations be managed?

---

# 21. Security

1. How should API keys be stored?
2. Which secrets will be provided?
3. How should webhook requests be verified?
4. What customer data can agents access?
5. What data should not be exposed to agents?
6. Are there privacy requirements?
7. How should access to CRM/customer information be controlled?

---

# 22. Testing

1. What is the expected testing strategy?
2. Should every agent have unit tests?
3. Should the full graph have integration tests?
4. How should Facebook webhooks be tested?
5. Is there a staging environment?
6. How should outbound messages be tested without contacting real customers?
7. What sample lead conversations should be used?
8. What constitutes a successful end-to-end test?

---

# P1 — Important Questions

## Current Business Process

- What are the most common lead types?
- What are the most common customer questions?
- What are the most common reasons for contacting the company?
- What are the common reasons a lead does not convert?
- What information do sales staff usually need before contacting someone?

## Lead Handling

- How quickly are leads normally contacted?
- Are leads currently prioritized?
- Is there a standard sales script?
- Are follow-ups documented?

## Content

- What existing content should be used as examples?
- What tone should generated content use?
- What language/languages should be supported?
- Are there platform-specific content rules?

## Operations

- Who owns the CRM?
- Who owns the social accounts?
- Who owns API credentials?
- Who approves production changes?

---

# P2 — Later Questions

- Detailed observability requirements.
- Detailed metrics and dashboards.
- Prompt versioning strategy.
- Cost monitoring.
- Model evaluation methodology.
- Performance/load requirements.
- Production deployment process.
- Disaster recovery.
- Long-term scalability.
- Detailed analytics for lead conversion.

---

# Questions To Ask First During the Kickoff

The following should be the initial discussion rather than asking every question above at once:

1. Can you walk me through the actual current customer/lead funnel from first discovery to booking?
2. Where are leads currently stored?
3. What exactly makes a lead qualified?
4. What are the exact responsibilities and boundaries of the four sub-agents?
5. Which parts are automated today and which are manual?
6. What is the final lead data schema?
7. What is the exact Facebook flow we should implement first?
8. What should the normalized message schema look like in the final implementation?
9. How should Sales Follow-up hand off to Scheduling?
10. What human approval/escalation points are required?
11. What is the agreed Python/LangChain/LangGraph/FastAPI/FastMCP stack and versioning?
12. What repository and development workflow should I use?

---

# Notes

Answers should be added beneath each question during or after the kickoff.

Do not replace unanswered questions with assumptions.

Use:

```text
ANSWER:
...

SOURCE:
...

DATE CONFIRMED:
...

NOTES:
...
```
