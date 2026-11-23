# Customer Care Agent Project

## 1. Understand the Customer

First, decide who will use your service.

### Example Customer

A son or daughter lives in another country and wants to arrange care for their parents in Nepal.

### Questions to Understand

- What does the customer need?
- What information will they give us?
- What questions will they ask first?
- What problems might they have?

### Example Customer Messages

1. "Hi, I live in Australia and my mother is in Kathmandu. I need someone to check on her regularly. Can you help?"
2. "I live abroad and need home care for my elderly father in Nepal."
3. "My mother lives alone in Kathmandu. Do you provide regular home visits?"
4. "I need someone to help take care of my parents. What services do you provide?"

### Main Agents

- Lead Capture Agent
- Qualification & Routing Agent


## 2. Make a Basic FAQ Agent

Create a simple agent that can answer 2–3 common questions.

Use the existing FAQ information instead of making up answers.

### Example 1

**Customer:**

"Do you provide home visits?"

**Agent:**

"Yes, we provide home-care visits. I can also help you understand the available services."

### Example 2

**Customer:**

"How can I book a consultation?"

**Agent:**

"I can collect your details and help arrange a consultation."

### Important Rule

The FAQ agent should only provide information that is available in the existing FAQ.

It should not invent:

- Prices
- Services
- Availability
- Guarantees
- Policies

### Main Agent

- Qualification & Routing Agent


## 3. Make the Agent Collect Customer Information

Once the customer shows interest, the agent should collect the important information needed to qualify the lead.

### Information to Collect

- Name
- Phone number or email
- What they need
- When they need it
- Status

### Lead Status

The lead should move through these stages:

`New → Contacted → Booked`

### Example

**Name:** Ram Sharma  
**Contact:** ram@email.com  
**Need:** Care for elderly mother  
**Required:** From next week  
**Status:** New

### Example Conversation

**Customer:**

"I need care for my elderly mother."

**Agent:**

"Sure, I can help. May I know your name?"

**Customer:**

"Ram Sharma."

**Agent:**

"Thank you, Ram. What type of care does your mother need?"

**Customer:**

"Regular home visits."

**Agent:**

"When would you like the service to start?"

**Customer:**

"From next week."

**Agent:**

"Thank you. May I have your phone number or email?"

### Main Agent

- Lead Capture Agent


## 4. Test It With 8–10 Conversations

Pretend to be different customers and test the agent.

Do not test only easy conversations.

### Test Cases

#### Easy

"I need care for my father. Can you help?"

The agent should understand the request and begin collecting information.

#### Vague

"I need some help for my mom."

The agent should ask what kind of help is required.

#### Missing Information

"I want to book a service."

The agent should ask for the missing information.

#### Price Question

"How much does this cost?"

The agent should use the available FAQ information.

If the price is not available, the agent should not invent a price.

#### Phone Number Only

"Call me on 98XXXXXXXX."

The agent should recognize that the customer has provided contact information and ask for the remaining required details.

#### Booking Request

"I want to arrange care for my mother starting next week."

The agent should collect the required details and determine whether the customer is ready to proceed.

### What to Check

For every conversation, check:

- Did the agent understand the customer's request?
- Did it ask the correct follow-up questions?
- Did it collect the required information?
- Did it save the information correctly?
- Did it avoid making up information?
- Did it identify when the customer was ready to book?

### Main Agents

- Lead Capture Agent
- Qualification & Routing Agent


## 5. Connect It to the Scheduling Agent

Once the customer has provided all the necessary information and is ready to book, the lead should be passed to the Scheduling Agent.

### Basic Flow

Customer → Lead Capture → Qualification → Scheduling

### Example

Customer wants a consultation.

↓

Agent collects:

- Name
- Contact
- Requirement
- Required date/time

↓

Agent confirms the customer is ready.

↓

Information is sent to the Scheduling Agent.

↓

Scheduling Agent books the consultation.

### Important Rule

The Qualification & Routing Agent should not claim that something is booked until the Scheduling Agent actually confirms the booking.

### Main Agents

- Sales Follow-up Agent
- Qualification & Routing Agent
- Scheduling Agent


## 6. Add Safety Rules

All agents must follow important safety rules.

### Rule 1: Don't Make Fake Promises

The agent must not make promises about availability or services unless the information is confirmed.

**Wrong:**

"We guarantee someone will visit tomorrow."

**Correct:**

"I can help you request a visit. Availability will need to be confirmed."

The agent should never invent:

- Availability
- Prices
- Services
- Booking confirmations
- Guarantees
- Staff availability
- Medical or care outcomes

### Rule 2: Don't Contact People Without Permission

The agent should not automatically contact someone just because their phone number or email address was found.

The customer must have agreed to be contacted.

For example, if someone provides a phone number but does not give permission for follow-up, the agent should not automatically send messages or make calls.

### Applies To

- Lead Capture Agent
- Sales Follow-up Agent
- Qualification & Routing Agent
- Scheduling Agent


## 7. Do a Bigger Test

After fixing the problems found during the first tests, perform another 15–20 test cases.

### Test Scenarios

- Customer asks a normal question
- Customer asks something covered by the FAQ
- Customer asks something not covered by the FAQ
- Customer gives incomplete information
- Customer gives incorrect information
- Customer changes their requirements
- Customer asks about price
- Customer wants to book
- Customer does not want to provide their phone number
- Customer provides only an email
- Customer provides only a phone number
- Customer asks for something the agent cannot promise
- Customer wants to cancel a booking
- Customer wants to change a booking
- Customer is ready for scheduling
- Customer is not ready to book
- Customer asks about service availability
- Customer gives unclear requirements

### Things to Check

For each test, verify:

1. The agent understands the customer.
2. The agent asks appropriate questions.
3. Required information is collected.
4. Information is saved correctly.
5. The lead status is correct.
6. The agent routes the customer correctly.
7. The agent does not invent information.
8. The agent respects contact permissions.
9. Scheduling only happens when appropriate.
10. Booking status is only confirmed by the Scheduling Agent.

### Main Focus

Test the whole system, not just individual agents.


## 8. Final Cleanup and Demo

After testing and fixing the problems, prepare the final version.

### Code

- Clean up the code
- Remove unnecessary files
- Remove unused code
- Add clear comments where necessary
- Make the project easy to understand

### Agents

- Lead Capture Agent works
- FAQ Agent works
- Qualification & Routing Agent works
- Sales Follow-up Agent works
- Scheduling Agent works

### Data

- Customer information is saved correctly
- Name is saved
- Contact information is saved
- Requirement is saved
- Required date/time is saved
- Lead status is saved correctly

### Safety

- No fake promises
- No invented prices
- No invented availability
- No fake booking confirmations
- No unauthorized follow-ups
- Customer consent is respected

### Scheduling

- Ready customers are routed to Scheduling
- Scheduling information is passed correctly
- Booking confirmation comes from the Scheduling Agent
- Customers can request cancellation or changes


## How the Whole System Works

```text
Customer
    ↓
Lead Capture Agent
    ↓
Qualification & Routing Agent
    ↓
Is Customer Ready?
    ↓
    ├── No → Follow-up
    │
    └── Yes
          ↓
    Scheduling Agent
          ↓
       Booked
