# Week 4 — Agent Integration, Conversation Testing, and Verification

## 1. Week 4 Objective

The objective of Week 4 is to test and integrate the existing AI agents, particularly:

- Lead Capture Agent
- Qualification & Routing Agent

The goal is to verify that the system understands customer messages, routes them to the appropriate workflow, collects required customer information, saves lead details correctly, and avoids inventing unsupported information.

The system should also recognize when a customer is ready to proceed with a potential booking.

## 2. What I Have Done in Week 4

### 2.1 Integration Service

I implemented an integration service in `integration/service.py` to connect the existing workflows.

The service:

- Accepts a customer message and conversation thread ID.
- Uses the routing component to classify the message.
- Routes FAQ questions to the FAQ workflow.
- Routes care requests and lead-related messages to the lead workflow.
- Supports messages that involve both FAQ questions and lead capture.
- Returns structured results for routing, FAQ responses, lead processing, and scheduling preparation.
- Validates required inputs such as the customer message and conversation thread ID.

### 2.2 Lead Capture and Persistence

I integrated the existing lead capture workflow with persistent lead storage.

The implementation supports:

- Collecting customer names and contact information.
- Capturing care requirements and other configured lead fields.
- Validating lead information before further processing.
- Saving lead information to a database.
- Continuing lead collection across multiple messages.
- Keeping conversations separate using different thread IDs.

I also improved the handling of vague care requests so the system can ask for clarification instead of assuming what type of care the customer needs.

### 2.3 Qualification and Routing

I tested the routing behavior for different customer messages.

The system is intended to distinguish between:

- FAQ questions.
- Care and lead-capture requests.
- Messages that contain both FAQ and lead-related questions.

Routing regression tests were added to cover previously misclassified messages.

### 2.4 FAQ Handling and Unsupported Information

I reviewed and tested FAQ behavior for supported questions and questions for which an exact answer is unavailable.

The system should:

- Use the available FAQ information.
- Avoid inventing prices or unsupported service details.
- Provide a safe fallback when an exact answer is unavailable.

### 2.5 Scheduling Preparation

I implemented a scheduling-preparation contract in `integration/scheduling_contract.py`.

It checks whether the required lead details and scheduling information are available before preparing a handoff.

The required information includes:

- Customer name.
- Care requirement.
- At least one contact method.
- Requested date.
- Requested time.
- Explicit customer readiness.

When the requirements are satisfied, the contract can return a `ready_for_handoff` status and a structured request payload.

**Important:** This is scheduling preparation, not a completed booking. The actual external Scheduling Agent has not yet been connected, and real-time appointment availability has not been verified.

### 2.6 Automated Tests

I ran the full repository test suite from the project root.

Command:

```powershell
python -m pytest -v
```

Latest recorded result:

**114 tests passed.**

I also checked dependency consistency.

Command:

```powershell
python -m pip check
```

Result:

```text
No broken requirements found.
```

The tests cover the existing FAQ and lead workflows, routing, lead persistence, conversation isolation, scheduling preparation, and related validation behavior.

## 3. How to Run the Tests

Open PowerShell in the repository root:

```powershell
cd C:\Priyanka\GitHub\Marketing-AI-Agent
```

Activate the virtual environment if it is not already active:

```powershell
.\.venv\Scripts\Activate.ps1
```

Check the Python version:

```powershell
python --version
```

Check dependencies:

```powershell
python -m pip check
```

Run the complete test suite:

```powershell
python -m pytest -v
```

The latest recorded result was 114 passing tests. Run the command again to verify the current working tree.

### Run the integration service tests

```powershell
python -m pytest .\integration\tests\test_service.py .\integration\tests\test_scheduling_contract.py -v
```

The previously recorded result for this focused test run was 19 passing tests. The result may change if the tests have subsequently been modified.

### Run the Week 3 lead graph database tests

```powershell
python -m pytest .\Week-3\Day-4\test_lead_graph_database.py -v
```

The previously recorded result was 8 passing tests.

## 4. How to Test the Agent With Customer Conversations

The Week 4 task requires testing the agent with 8–10 realistic customer conversations, including easy cases and challenging cases.

The following scenarios can be used for manual testing.

### Test 1 — Easy Care Request

**Customer:**

> I need care for my father. Can you help?

**Expected behavior:**

- The system recognizes a care-related request.
- The message is routed to the lead workflow.
- The agent begins collecting the required customer details.
- The agent asks for missing information rather than assuming it.

**Verify:**

- Correct route.
- Appropriate follow-up question.
- Correct lead updates, if any information was extracted.

### Test 2 — Vague Care Request

**Customer:**

> I need some help for my mom.

**Expected behavior:**

- The system recognizes a potential care request.
- It asks what kind of help is required.
- It does not assume that the customer needs a particular service.

**Verify:**

- The care requirement is not incorrectly guessed.
- The agent asks for clarification.

### Test 3 — Missing Information

**Customer:**

> I want to book a service.

**Expected behavior:**

- The system recognizes a potential service or booking request.
- It asks for the missing information.
- It does not claim that a booking has been completed.

**Verify:**

- Appropriate follow-up question.
- No unsupported booking confirmation.

### Test 4 — Price Question

**Customer:**

> How much does this cost?

**Expected behavior:**

- The message is routed to the FAQ workflow when appropriate.
- The agent uses available FAQ information.
- If the exact price is unavailable, it provides a safe fallback instead of inventing a price.

**Verify:**

- Appropriate route.
- Answer consistent with available FAQ information.
- No invented prices.

### Test 5 — Phone Number Only

**Customer:**

> Call me on 98XXXXXXXX.

**Expected behavior:**

- The system recognizes that the customer provided contact information.
- It asks for the remaining required lead details.
- It does not treat the lead as complete merely because a phone number was provided.

**Verify:**

- Phone number is extracted correctly when supported by the input.
- Remaining information is requested.
- Saved information is correct.

Use a fictional test number rather than a real customer's contact information.

### Test 6 — Booking Request

**Customer:**

> I want to arrange care for my mother starting next week.

**Expected behavior:**

- The system recognizes a care request.
- It collects the care requirement and missing customer details.
- It determines whether the customer is ready to proceed, according to the implemented workflow.
- It does not claim that an appointment has been booked.

**Verify:**

- Appropriate route.
- Correct follow-up questions.
- No unsupported claim about availability.

### Test 7 — Combined FAQ and Lead Request

**Customer:**

> I need a caregiver for my father. How much does your service cost?

**Expected behavior:**

- The system recognizes both the care request and the pricing question.
- Both relevant workflows are invoked when supported by the router.
- The price response uses available FAQ information.

**Verify:**

- Correct combined routing.
- Lead information is processed.
- No invented price.

### Test 8 — Multiple Messages in One Conversation

**Customer message 1:**

> I need care for my mother.

**Customer message 2:**

> My name is Test Customer.

**Customer message 3:**

> My phone number is 9800000000.

**Expected behavior:**

- The system continues collecting information across messages when supported by the conversation workflow.
- The information is associated with the correct conversation.
- Missing information is requested.

**Verify:**

- The correct name and phone number are saved.
- Previously collected information is retained where appropriate.
- The conversation state is not mixed with another customer's information.

Use fictional test details only.

### Test 9 — Unknown Pricing Detail

**Customer:**

> Can you guarantee the exact price and caregiver arrival time before I book?

**Expected behavior:**

- The system does not invent an exact price if none is available.
- It does not guarantee caregiver arrival without an authoritative basis.
- It provides a safe answer or asks the customer to contact the care team.

**Verify:**

- No fabricated price.
- No unsupported guarantee.
- Appropriate fallback behavior.

### Test 10 — Separate Customer Conversations

Create two separate conversation threads.

**Thread A:**

> I need care for my father. My name is Customer A.

**Thread B:**

> I need help for my mother. My name is Customer B.

**Expected behavior:**

- Each conversation has its own thread ID.
- The lead details remain associated with the correct conversation.
- One customer's information does not appear in the other customer's lead.

**Verify:**

- Correct thread IDs.
- Correct database records.
- No cross-conversation data leakage in the tested scenario.

## 5. Manual Testing Procedure

For each conversation:

1. Start the application or call the integration service using the project's existing entry point.
2. Submit the customer message.
3. Record the route selected by the router.
4. Review the FAQ answer or lead response.
5. Check which customer fields were extracted.
6. Inspect the saved lead using the existing database or lead-inspection utility.
7. Verify that missing information is requested.
8. Check that the agent does not invent prices, guarantees, or booking confirmations.
9. Record whether the scenario passed or failed.

Do not mark a scenario as passed merely because the program did not crash. Verify the actual response, routing result, and saved information.

## 6. Manual Test Results Template

Record the actual outcome of each conversation.

| Test | Scenario | Expected behavior | Actual result | Status |
|---|---|---|---|---|
| 1 | Easy care request | Begins lead collection | To be recorded | Pending verification |
| 2 | Vague request | Asks for clarification | To be recorded | Pending verification |
| 3 | Missing information | Requests missing details | To be recorded | Pending verification |
| 4 | Price question | Uses FAQ or safe fallback | To be recorded | Pending verification |
| 5 | Phone number only | Recognizes contact information | To be recorded | Pending verification |
| 6 | Booking request | Collects details and assesses readiness | To be recorded | Pending verification |
| 7 | Combined FAQ and lead request | Processes both intents | To be recorded | Pending verification |
| 8 | Multiple messages | Retains conversation information | To be recorded | Pending verification |
| 9 | Unknown pricing detail | Avoids unsupported claims | To be recorded | Pending verification |
| 10 | Separate conversations | Keeps leads isolated | To be recorded | Pending verification |

Update the status only after testing each scenario. Automated tests and manual conversation tests provide different kinds of evidence.

## 7. What Remains Pending

The following items are outside the demonstrated scope of the current integration prototype:

- Connecting the actual external Scheduling Agent.
- Checking real-time appointment availability.
- Completing and verifying an actual appointment booking.
- Automatically extracting and persisting requested appointment dates and times through the scheduling-preparation step.
- Testing all possible customer messages and production-level concurrency behavior.

These limitations should be documented accurately. They do not automatically mean that the stated Week 4 conversation-testing task is incomplete.

## 8. Final Assessment

Based on the current implementation and recorded test results:

- The integration service has been implemented.
- The existing FAQ and lead workflows are connected through the integration service.
- Routing, lead validation, persistence, and conversation isolation have automated test coverage.
- Scheduling-readiness and handoff preparation have been implemented.
- The latest recorded full test suite result is 114 passing tests.
- Dependency consistency was checked successfully.

The Week 4 task appears complete for the integration prototype and testing scope described in the project requirements, provided the required customer conversation scenarios were actually exercised and their behavior verified.

**Final distinction:** The tested integration prototype is not the same as a fully deployed system with a connected Scheduling Agent and confirmed real-world bookings.
