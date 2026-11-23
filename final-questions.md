# Mentor Meeting Questions --- Weeks 1--4

**Project:** Saathi Sneha Care AI Agent\
**Meeting:** Tomorrow\
**Purpose:** Review completed work, clarify Week 4 expectations, and
agree on next priorities.

------------------------------------------------------------------------

## 1. Quick Progress Summary

Use this as a short opening summary. Adjust anything that does not match
your latest code.

-   **Week 1 --- Lead foundation:** Built normalized-message and lead
    models, deterministic lead extraction, validation,
    lifecycle-transition rules, workflow/state structure, and automated
    tests. The recorded baseline was 29 passing tests.
-   **Week 2 --- FAQ agent:** Built a terminal-based FAQ prototype using
    Python, LangChain, LangGraph, and Gemini. It selects from approved
    FAQs, returns predefined answers, and uses a fallback for
    unsupported questions.
-   **Week 3 --- Conversational lead capture:** Developed multi-turn
    collection of a customer's name, contact, and care need, with
    LangGraph workflow logic and SQLite saving/retrieval. Automated
    tests and database persistence checks were reported as passing.
-   **Week 4 --- Conversation testing:** Test the Lead Capture Agent and
    Qualification & Routing Agent with 8--10 varied customer
    conversations. Check follow-up questions, data collection,
    persistence, unsupported claims, and booking readiness.

**Important verification point:** The Week 3 notes include a remaining
item to verify a complete live Gemini-powered conversation when API
access is available. Ask whether this should be completed before or
alongside Week 4 testing.

------------------------------------------------------------------------

## 2. The Most Important Questions to Ask

If meeting time is short, prioritize these questions.

1.  **"Could you review my Week 1--3 work and confirm whether it meets
    the expected requirements? Is there anything I should fix before
    moving further?"**

2.  **"For Week 4, should I test the Lead Capture Agent and
    Qualification & Routing Agent separately first, or should I test
    them together as one workflow?"**

3.  **"What exact rules should the Qualification & Routing Agent use to
    classify a lead---for example, when to ask more questions, when a
    lead is ready to proceed, and when to route or escalate it?"**

4.  **"Should I complete the live Gemini end-to-end verification for
    Week 3 first? My notes show that the SQLite and local logic checks
    passed, but live Gemini verification was still pending because of
    API quota limits."**

5.  **"Should I connect the Week 2 FAQ agent and Week 3 lead-capture
    graph now, or keep them as separate prototypes until the main
    orchestrator integration is assigned?"**

6.  **"What should I submit as Week 4 evidence: a manual test report,
    automated tests, a demo, or all three?"**

------------------------------------------------------------------------

## 3. Week 4 Testing Questions

-   "For the 8--10 conversations, do you have expected outputs or
    acceptance criteria for each scenario, or should I propose them for
    your review?"

-   "When a customer asks about price, should the agent answer only from
    approved FAQ data, and what should it do when the exact price is not
    available?"

-   "For a booking request, should the agent only collect information
    and identify readiness, or is it expected to check availability or
    create an actual booking?"

-   "What should happen when a message suggests urgency or a situation
    that needs human attention? Are there approved escalation rules?"

-   "For lead completion, is the required information still a name, a
    care need, and either a phone number or email address?"

-   "Should I test whether information persists across multiple turns
    and whether saved leads can still be retrieved after restarting the
    application?"

-   "Should I include negative cases such as invalid contact details,
    duplicate messages, a customer changing their answer, or a customer
    declining to share contact details?"

------------------------------------------------------------------------

## 4. Integration and Architecture

The prototypes have different scopes, so clarify the intended next step
before combining them.

-   "What is the expected boundary between the Lead Capture Agent and
    the Qualification & Routing Agent? What should each agent receive
    and return?"

-   "Should the Qualification & Routing Agent be a separate LangGraph
    node/agent, or should its logic be added to the existing lead
    workflow?"

-   "When should the Week 1 lead model and validation rules be reused by
    the Week 3 conversational lead-capture workflow?"

-   "Is SQLite acceptable for the current prototype, or should I prepare
    for a shared database or CRM? If a shared system is expected, which
    one?"

-   "Is integration with the main LangGraph orchestrator part of Week 4,
    or is Week 4 limited to testing the two agents?"

-   "Are website, WhatsApp, Facebook, FastAPI, or FastMCP integrations
    in scope now, or should I continue using the local terminal
    interface for these tests?"

------------------------------------------------------------------------

## 5. Reliability, Tools, and Development Standards

-   "Because the Week 2 FAQ agent uses Gemini to select an approved FAQ
    answer, should I add tests for incorrect FAQ selection and
    unsupported questions?"

-   "How should I handle Gemini quota limits during testing---use
    recorded test fixtures for logic tests and reserve live API calls
    for a smaller number of end-to-end checks?"

-   "Should I standardize Python and package versions across the Week
    1--3 projects now, before they are integrated? I think agreeing on
    versions early will reduce dependency conflicts and make the
    combined project easier to reproduce."

-   "Do you want a shared test command, dependency file,
    environment-variable convention, and README structure across all
    modules?"

-   "Should I add logging for each conversation step and routing
    decision so that failures can be traced during review?"

------------------------------------------------------------------------

## 6. Scope, Deliverables, and Priorities

-   "What is the single most important outcome you want me to
    demonstrate by the end of Week 4?"

-   "Which issues should I fix immediately, and which should be
    documented as future work?"

-   "Should I prepare a short demo showing the customer conversation,
    collected fields, routing decision, and saved database record?"

-   "After Week 4, what should be the next priority: improving
    qualification and routing, integrating the FAQ and lead agents,
    connecting a shared database/CRM, or adding a communication
    channel?"

------------------------------------------------------------------------

## 7. Suggested Meeting Order

1.  Give the brief Week 1--3 progress summary.

2.  Ask the mentor to confirm whether the completed work meets the
    requirements.

3.  Clarify the Qualification & Routing Agent's rules and the Week 4
    acceptance criteria.

4.  Confirm whether live Gemini verification is required now.

5.  Agree on whether agent integration is in scope.

6.  Confirm the expected evidence, priority fixes, and next milestone.

------------------------------------------------------------------------

## 8. Notes to Fill In During the Meeting

-   **Week 1--3 review / required fixes:**

-   **Qualification rules and routing destinations:**

-   **Week 4 test format and acceptance criteria:**

-   **Live Gemini verification required by:**

-   **Integration scope:**

-   **Database / CRM direction:**

-   **Version-standardization decision:**

-   **Week 4 deliverables and deadline:**

-   **Next task:**

------------------------------------------------------------------------

## Recommended Short Version

If you only have time for a few questions, ask these:

1.  "Could you review my Week 1--3 work and tell me if anything needs to
    be corrected?"

2.  "What exact rules should determine lead qualification, booking
    readiness, and routing?"
    \
3.  "Should I test the two Week 4 agents separately or together?"

4.  "Do I need to finish live Gemini verification before proceeding?"

5.  "Is integrating the FAQ and lead-capture workflows part of Week 4?"

6.  "What evidence should I present to consider Week 4 complete?"
