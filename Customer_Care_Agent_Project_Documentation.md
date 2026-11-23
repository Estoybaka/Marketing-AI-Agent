# Customer Care Agent Project

## Project Progress, Implementation & Remaining Work

**Project:** Saathi Sneha Care -- Customer Care Agent\
**Documentation date:** 5 November 2026\
**Purpose:** Explain the work completed so far, how the system works,
what has been tested, and what remains before the full project can be
considered complete.

------------------------------------------------------------------------

## 1. Executive Summary

The project is a customer-care assistant for a care service in Nepal. It
is designed mainly for people living abroad who want to arrange care for
an elderly parent or family member in Nepal.

The current implementation brings together:

-   A FAQ agent that answers from the existing FAQ knowledge only.
-   Lead capture and qualification that collect customer details and
    understand the care requirement.
-   Routing that decides whether a message should go to the FAQ flow,
    lead flow, or both.
-   SQLite persistence for lead information.
-   Explicit contact-consent handling.
-   A sales follow-up draft capability that does not send messages
    automatically.
-   A scheduling handoff contract that checks whether the information
    needed for a scheduling request is present.

**Current result:** The latest full repository test run reported **161
passing tests**, and the expanded integration suite reported **64
passing tests**. The customer-scenario suite contains **20 automated
scenarios**.

**Important project boundary:** The actual Scheduling Agent has not yet
been connected. The current system can prepare and validate a scheduling
handoff, but it does not make a real appointment or confirm a booking.
That integration is pending the teammate who is building the Scheduling
Agent.

The most accurate description of the current state is:

> **Core customer-care implementation completed for the current scope.
> Actual Scheduling Agent integration and final end-to-end verification
> remain pending.**

------------------------------------------------------------------------

## 2. Customer Problem and Intended Users

### Intended customer

A son or daughter may live in another country while their elderly parent
lives in Nepal. They want to understand the available care options,
explain the parent's needs, provide contact details, and request the
next step.

Example:

> "I live in Australia and my mother is in Kathmandu. I need someone to
> check on her regularly. Can you help?"

### What the assistant needs to understand

The assistant should identify:

-   Who is requesting care.
-   Who needs care and where that person is located.
-   What type of help is required.
-   When the service may be needed.
-   How the customer can be contacted.
-   Whether the customer explicitly agrees to follow-up.
-   Whether the customer is ready to proceed to scheduling.

### Main responsibilities

The project separates the customer-care work into responsibilities:

1.  **Lead Capture Agent:** gathers and updates customer information.
2.  **FAQ Agent:** answers supported questions using existing FAQ
    content.
3.  **Qualification & Routing:** determines which flow should handle the
    message and whether the customer is ready for the next step.
4.  **Sales Follow-up capability:** prepares a follow-up draft when
    consent and lead-completion conditions are met.
5.  **Scheduling Agent:** intended to handle appointment booking; the
    real integration is not yet complete.

------------------------------------------------------------------------

## 3. Work Completed by Assignment Section

### Section 1 --- Understand the Customer

**Status: Completed for the current project scope**

The target customer and the typical customer journey have been
identified: a person living abroad wants to arrange care for a parent or
family member in Nepal.

The system is designed to recognize common needs such as regular home
visits and care for an elderly parent, ask for missing details, answer
supported questions, and route the conversation appropriately.

### Section 2 --- Make a Basic FAQ Agent

**Status: Implemented and tested**

The project includes an FAQ knowledge base with six FAQ topics:

1.  Payments from abroad.
2.  Local payment methods.
3.  Setup or joining fees.
4.  Changing or cancelling a plan.
5.  Extra visits.
6.  Service areas.

The FAQ implementation includes a pure-Python keyword-based agent and a
LangChain-based implementation.

The FAQ agent returns an answer from the available FAQ content. When it
cannot find a suitable answer, it uses a fallback that directs the
customer to the Saathi Sneha Care team.

**Safety boundary:** The agent must not invent prices, services,
availability, guarantees, or policies. For example, a question about a
service area not confirmed by the FAQ should not be answered with an
unsupported availability promise.

### Section 3 --- Make the Agent Collect Customer Information

**Status: Implemented and tested**

The lead-capture flow collects or tracks:

-   Customer name.
-   Phone number or email address.
-   Care requirement.
-   When the service is needed.
-   Lead status.

Additional information is also supported, including urgency, patient
location, service interest, preferred contact time, and notes.

The project stores lead information in SQLite. The lead flow can ask for
missing information and update an existing lead as the customer provides
corrections or additional requirements.

The system supports the following application statuses:

-   `New`
-   `Contacted`
-   `Booked`
-   `Qualified`
-   `Follow-up`
-   `Converted`
-   `Lost`

The allowed status transitions are validated. A lead cannot be marked
`Booked` through the normal application save flow unless the Scheduling
Agent has confirmed the booking. The system also prevents creating a new
lead directly with `Booked` status.

**Important distinction:** The assignment's simple lifecycle is
`New → Contacted → Booked`. The implementation includes additional
statuses to represent qualification, follow-up, conversion, and lost
leads. `Booked` remains protected by the scheduling-confirmation rule.

### Section 4 --- Test It With 8--10 Conversations

**Status: Initial conversation testing completed**

The project has been tested against common customer-message patterns,
including:

-   Straightforward care requests.
-   Vague requests that need clarification.
-   Incomplete information.
-   FAQ and price questions.
-   Customers who provide only a phone number or email.
-   Customers who express interest in booking.

The tests check whether the system understands the message, asks for
missing details, saves information, avoids unsupported answers, and
identifies when a customer may be ready for scheduling.

### Section 5 --- Connect It to the Scheduling Agent

**Status: Partially prepared; actual integration pending**

The project includes a scheduling handoff contract. It checks whether
the required information is available before a request is considered
ready for handoff. The preparation checks include:

-   Customer name.
-   Contact information.
-   Care requirement.
-   Requested date.
-   Requested time.
-   Customer readiness.

The integration tests verify that a ready request can be prepared for
handoff and that an unready request is not treated as ready.

**What is not implemented yet:**

-   Connecting to the actual Scheduling Agent being built by the
    teammate.
-   Sending the request to that agent through its real interface.
-   Receiving and validating the Scheduling Agent's booking
    confirmation.
-   Updating the lead to `Booked` based on a real confirmation.
-   Testing real cancellation and rescheduling requests through that
    agent.

The user and teammate are currently on leave, so this dependency is
intentionally deferred. The current project must not claim that a
consultation has been booked merely because a handoff request is ready.

### Section 6 --- Add Safety Rules

**Status: Core safeguards implemented; full-system verification pending
Scheduling Agent integration**

The current implementation includes the following safeguards:

#### No invented information or promises

The FAQ agent uses the existing FAQ content and falls back when it
cannot find a supported answer. The project does not treat scheduling
preparation as a confirmed booking.

#### Explicit contact consent

Contact consent is represented as a three-state value:

-   `None`: consent has not been given or declined.
-   `True`: the customer explicitly agreed.
-   `False`: the customer explicitly declined.

Providing a phone number or email address does not automatically mean
the customer has agreed to follow-up.

The system asks for permission to contact the customer and processes
clear yes/no answers when it is waiting for that consent response. It
also supports changing or revoking a previous decision.

Ambiguous replies do not grant consent. The system asks the customer to
reply clearly with yes or no.

#### No automatic follow-up sending

The Sales Follow-up capability prepares a draft only. It checks that
consent is explicitly `True` and that the lead meets the completion
requirements. The current implementation does not send the message
automatically and does not change the lead status simply because a draft
was prepared.

#### No false booking confirmation

The lead database protects the `Booked` status so that the application
cannot mark a lead as booked without scheduling confirmation. The real
confirmation flow still needs to be connected and tested with the
teammate's Scheduling Agent.

### Section 7 --- Do a Bigger Test

**Status: 20 automated customer scenarios completed for the current
integration scope**

The integration scenario suite contains 20 scenarios. The scenarios
cover customer questions, FAQ routing, incomplete information, lead
capture, corrections, additional requirements, contact preferences,
consent, and scheduling readiness.

Examples of covered cases include:

-   A normal customer question.
-   A question covered by the FAQ.
-   A question outside the available FAQ information.
-   Incomplete customer details.
-   A customer correcting a care requirement.
-   A customer adding another requirement without losing the earlier
    one.
-   A customer declining to provide a phone number but providing an
    email address.
-   A customer giving an ambiguous answer to the consent question.
-   A customer agreeing to or declining follow-up.
-   A customer revoking previously given consent.
-   A customer ready for scheduling handoff.
-   A customer not ready for scheduling.
-   A question about service availability in Pokhara.

The suite checks routing, persistence, consent behavior, and
scheduling-preparation behavior.

**Testing limitation:** These customer scenarios use a deterministic
test extractor in place of live Gemini extraction. They are useful for
repeatable integration testing, but they do not prove that live Gemini
extraction will interpret every real customer message correctly.
Live/manual conversation testing remains a recommended validation step.

**Latest reported results:**

  Test area                        Latest reported result
  ------------------------------ ------------------------
  Week 1 tests                                  29 passed
  Week 2 tests                                  15 passed
  Week 3 tests                                  53 passed
  Integration tests                             64 passed
  Full repository test suite               **161 passed**
  Automated customer scenarios              **20 passed**

These are the latest results reported from the user's test runs on 5
November 2026. They describe the test state at that time; rerun the
commands below after any later code changes.

### Section 8 --- Final Cleanup and Demo

**Status: Core-scope cleanup and documentation completed; final
integrated demo pending**

The following cleanup and documentation work has been completed:

-   A root `README.md` was prepared with project overview, setup
    instructions, run instructions, test commands, limitations, and
    verification results.
-   The integration verification report was updated.
-   `.gitignore` includes common Python cache, virtual-environment,
    environment-file, log, and local SQLite database patterns.
-   Searches for common unfinished-code markers such as `TODO`, `FIXME`,
    `NotImplementedError`, `breakpoint()`, and `pdb.set_trace()`
    returned no matches in the searched Python project files.
-   Python compilation checks completed without reported errors.
-   The full test suite was run and reported 161 passing tests.

**Still needed for the final full-project demo:**

-   Connect the real Scheduling Agent.
-   Demonstrate a complete customer-to-scheduling flow.
-   Demonstrate that the lead becomes `Booked` only after a real booking
    confirmation.
-   Verify cancellation and rescheduling behavior with the real
    Scheduling Agent.
-   Manually test representative conversations using the live extraction
    model.
-   Confirm that appointment date and time are passed in the format
    expected by the Scheduling Agent.

------------------------------------------------------------------------

## 4. Current System Flow

The current customer-care implementation can be understood as follows:

``` text
Customer message
       |
       v
Qualification & Routing
       |
       +----------------------+
       |                      |
       v                      v
   FAQ route              Lead route
       |                      |
       v                      v
 FAQ Agent              Lead Capture Agent
       |                      |
       |                      v
       |                Collect/update details
       |                      |
       |                      v
       |                Save lead in SQLite
       |                      |
       |                      v
       |                Ask for explicit consent
       |                      |
       |                      v
       |                Check readiness
       |                      |
       |                      v
       |             Scheduling handoff preparation
       |                      |
       |                      v
       |              Actual Scheduling Agent
       |                 NOT CONNECTED YET
       |                      |
       |                      v
       |             Confirmed booking response
       |                 NOT IMPLEMENTED YET
       |
       v
 Supported FAQ answer or safe fallback
```

The FAQ and lead flows can both run when a message needs both kinds of
handling. Consent responses are recognized in an existing conversation
so that a clear yes/no answer is handled by the lead flow rather than
being mistaken for an ordinary FAQ question.

------------------------------------------------------------------------

## 5. Important Implementation Details

### Lead storage

Lead information is stored in a local SQLite database. The database
layer validates supported statuses and permitted transitions. It also
includes migration handling for older database schemas.

Local SQLite database files may contain customer information and are
covered by `.gitignore` patterns. Real customer data and API keys should
not be placed in public documentation or shared unnecessarily.

### AI extraction

The lead-capture graph uses Gemini structured output to extract
information from customer messages. The API key is read from the
environment using `GEMINI_API_KEY`; it should be stored in a local
`.env` file and must not be committed or shared.

### Follow-up behavior

The current Sales Follow-up capability creates a draft only. It is not
an email/SMS delivery integration. Explicit consent is required before a
follow-up draft can be prepared.

### Scheduling data

The current lead field `when_needed` can preserve a natural-language
phrase such as "next week." It is not yet a normalized appointment
date/time. The scheduling handoff contract can accept explicit date and
time values, but the real Scheduling Agent's expected interface and data
format must be confirmed before integration.

------------------------------------------------------------------------

## 6. What Remains To Be Done

The following work should be resumed when the teammate's Scheduling
Agent is available.

  -----------------------------------------------------------------------
  Priority                Remaining task          Why it is needed
  ----------------------- ----------------------- -----------------------
  1                       Review the teammate's   Confirm its input
                          Scheduling Agent        fields, output, and
                          interface               error behavior.

  2                       Connect the             Replace the current
                          customer-care handoff   preparation-only
                          to the real agent       boundary with a real
                                                  integration.

  3                       Normalize and pass      Ensure both agents
                          appointment date/time   interpret the requested
                                                  appointment
                                                  consistently.

  4                       Handle scheduling       Distinguish confirmed,
                          responses               unavailable, failed,
                                                  and incomplete
                                                  requests.

  5                       Update lead status from Set `Booked` only after
                          actual confirmation     receiving valid
                                                  confirmation.

  6                       Test cancellation and   Verify the customer can
                          rescheduling            request changes without
                                                  false claims.

  7                       Run end-to-end tests    Validate the complete
                          with both agents        flow, not only the
                                                  customer-care side.

  8                       Perform live/manual     Check real Gemini
                          conversation testing    extraction and
                                                  customer-facing
                                                  responses.

  9                       Prepare the final       Demonstrate the
                          integrated demo         complete system to the
                                                  mentor.
  -----------------------------------------------------------------------

### Dependencies

The actual Scheduling Agent connection depends on the teammate
completing or sharing the agent and its integration contract. Until
then, the current handoff preparation should remain clearly described as
preparation---not a completed booking integration.

------------------------------------------------------------------------

## 7. How to Run and Verify the Project

Run these commands from the repository root in PowerShell, with the
project's virtual environment activated.

### Run the full test suite

``` powershell
python -m pytest -q
```

Expected latest reported result on 5 November 2026:

``` text
161 passed
```

The exact result may change if code or tests are modified.

### Run the integration tests

``` powershell
python -m pytest .\integration\tests\ -q
```

Latest reported result:

``` text
64 passed
```

### Run the 20 customer scenarios

``` powershell
python -m pytest .\integration\tests\test_customer_scenarios.py -q
```

Latest reported result:

``` text
20 passed
```

### Run the lead-capture command-line application

``` powershell
cd .\Week-3\Day-4
python main.py
```

The interactive application supports:

-   `/lead` --- start a new lead conversation.
-   `/lead <ID>` --- open an existing lead.
-   `/quit` --- exit.

The root `README.md` and `integration/VERIFICATION_REPORT.md` contain
additional setup and verification information.

------------------------------------------------------------------------

## 8. Suggested Mentor Demo

A clear demo can be delivered in this order:

1.  **Explain the customer:** A family member living abroad wants to
    arrange care for a parent in Nepal.
2.  **Show an FAQ question:** Ask a supported payment or service-area
    question and show that the answer comes from the FAQ content.
3.  **Show lead capture:** Start a conversation and provide a name,
    contact detail, care need, and timing.
4.  **Show clarification:** Provide an incomplete or vague requirement
    and demonstrate that the agent asks a follow-up question.
5.  **Show persistence:** Display the saved lead and its current status.
6.  **Show consent:** Demonstrate that contact details alone do not
    grant permission and that an ambiguous response does not count as
    consent.
7.  **Show follow-up safety:** Explain that the system prepares a draft
    only and does not send it automatically.
8.  **Show scheduling preparation:** Demonstrate a ready-for-handoff
    request and explain that it is not a booking.
9.  **Show tests:** Run the full test suite and show the latest test
    output.
10. **Explain the remaining dependency:** The real Scheduling Agent
    integration and complete end-to-end demo will follow once the
    teammate's agent is available.

Do not demonstrate a simulated handoff as though it were a real
appointment booking. Be explicit about what is implemented and what is
pending.

------------------------------------------------------------------------

## 9. Final Project Status

### Completed for the current implementation scope

-   Customer and use-case understanding.
-   FAQ knowledge base and FAQ response flow.
-   Lead capture, qualification, and SQLite persistence.
-   Routing between FAQ and lead handling.
-   Lead status validation and transition rules.
-   Explicit consent, refusal, ambiguous-response handling, and consent
    revocation.
-   Follow-up draft preparation without automatic sending.
-   Scheduling handoff readiness checks.
-   20 deterministic customer integration scenarios.
-   Core cleanup, README, and verification documentation.
-   Latest reported full test result: 161 passed.

### Pending

-   Actual connection to the teammate's Scheduling Agent.
-   Real appointment booking and confirmation response handling.
-   Structured appointment date/time normalization as required by the
    final scheduling interface.
-   Real cancellation and rescheduling integration.
-   Live/manual validation of Gemini extraction.
-   Final end-to-end demonstration of both agents working together.

### Recommended status statement for the mentor

> I have completed the core Customer Care Agent implementation,
> including the FAQ agent, lead capture and qualification, routing,
> SQLite persistence, explicit contact-consent safeguards, follow-up
> draft preparation, and scheduling handoff validation. I added 20
> automated customer scenarios and the latest full repository test run
> passed 161 tests. The actual Scheduling Agent is being developed
> separately by my teammate, so its integration, real booking
> confirmation, cancellation/rescheduling tests, and final end-to-end
> demonstration are pending until that agent is available.

------------------------------------------------------------------------

**Documentation note:** This document records the implementation and
test results reported on 5 November 2026. It does not claim that the
real Scheduling Agent is integrated or that live customer bookings have
been tested.
