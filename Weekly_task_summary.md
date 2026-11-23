# Marketing-AI-Agent — Simple Weekly Summary for Mentor Meeting

This document is written in simple words so I can explain clearly what I completed in Weeks 1, 2, and 3. Week 4 is my next task, which starts after this meeting, so it is described as upcoming work rather than completed work.

## Week 1 — Basic Lead Capture

### What I worked on

“In Week 1, I worked on the basic foundation for capturing leads. A lead is a person who shows interest in the care services. I created models to represent incoming messages and lead information. I also wrote logic to identify details that the person actually provides, such as their service need, interest in pricing, or possible urgency.

I added validation to check whether lead information and status changes were allowed. I also created a basic workflow to process a lead and wrote automated tests to check that the main parts worked correctly.”

### Main tasks completed

- Created a `NormalizedMessage` model to represent an incoming message, including the sender, channel, text, timestamp, and attachments.
- Created a `Lead` model to represent the information collected about a potential customer.
- Added logic to identify the user's stated needs and signals such as service interest, pricing questions, and possible urgency.
- Added validation to check lead data.
- Added rules for which lead-status changes are allowed.
- Created a basic lead-capture workflow.
- Tested the models, extraction logic, validation, status transitions, and workflow. The recorded test run had 29 passing tests.

### Simple way to explain the result

“By the end of Week 1, I had a basic lead-capture foundation that could process lead information, validate it, and handle allowed status changes. I also had automated tests for the main logic.”

---

## Week 2 — FAQ Agent

### What I worked on

“In Week 2, I built a simple FAQ agent using Python, LangChain, LangGraph, and Google Gemini. The purpose was to answer common questions about the care service.

I prepared six approved FAQs. The agent uses Gemini to select which FAQ matches the user's question, and then the application returns the answer written for that FAQ. If the question is outside the approved FAQs, it gives a fallback response instead of making up an answer. I manually tested the common questions and an unsupported question through the terminal.”

### Main tasks completed

- Used Python as the main programming language.
- Used LangChain to connect the language model with the application.
- Used LangGraph to organize the FAQ workflow into steps for selecting an FAQ and returning its answer.
- Used Google Gemini to select the relevant FAQ.
- Prepared six approved FAQ entries covering payment, fees, plan changes, extra visits, and service availability.
- Returned predefined answers so the agent would not invent prices, policies, or availability.
- Added fallback behavior for questions that were not covered by the approved FAQs.
- Manually tested the FAQ questions and an unsupported question in the terminal.

### Simple way to explain the result

“By the end of Week 2, I had a terminal-based FAQ prototype that could match a user's question to one of six approved FAQs and return the prepared answer. It could also respond with a fallback when it could not answer from the available FAQs.”

### Current limitation

“The FAQ agent was a prototype. It was not yet connected to the website, WhatsApp, CRM, live scheduling, or the main system that coordinates all agents.”

---

## Week 3 — Conversational Lead Capture and Saving Leads

### What I worked on

“In Week 3, I improved lead capture so it could collect information through a conversation instead of expecting all details in one message.

When someone shows interest in the service, the agent collects their name, their care need, and at least one contact method—an email address or phone number. If some information is missing, it asks for that information. It keeps track of details provided in earlier messages and saves the completed lead in an SQLite database. I also added commands to view saved leads and tested the workflow and database saving and retrieval.”

### Main tasks completed

- Built a conversational lead-capture workflow using LangGraph.
- Added logic to identify when a person shows interest in the service.
- Collected the person's name, care need, and at least one contact method: email or phone.
- Added logic to identify which required information was still missing.
- Made the workflow ask for missing details one at a time.
- Kept track of information across multiple messages in the same conversation.
- Added lead completion tracking and a field to indicate what information should be requested next.
- Saved lead records in SQLite using the `leads.db` database.
- Added commands such as `/lead` to view saved leads and `/lead <ID>` to retrieve a particular lead.
- Ran automated tests and checked whether leads could be saved and retrieved.

### Simple way to explain the result

“By the end of Week 3, I had a conversational lead-capture prototype that could ask for missing information, keep details across multiple messages, and save lead records in a database so they could be retrieved later.”

### Current limitation to explain honestly

“The lead-capture workflow is still a separate prototype. Full integration with the Week 2 FAQ agent, the scheduling agent, the customer-support agent, communication channels, and the main orchestrator has not yet been established. The automated logic and database checks passed, but live Gemini end-to-end verification should be confirmed because an earlier test was affected by API quota limits.”

---

## Week 4 — Upcoming Task: Test 8–10 Customer Conversations

**This task starts after today's meeting. It is planned work, not completed work yet.**

### What I will work on

“For Week 4, I will test the agent using 8–10 different customer conversations. I will not test only simple cases. I will also test vague requests, missing information, price questions, booking requests, and situations where the customer gives information across multiple messages.

I will check whether the agent understands the request, asks the right follow-up questions, saves the lead correctly, avoids making up information, and identifies when enough information has been collected for the next step.”

### Planned test cases

1. **Simple request:** “I need care for my father. Can you help?”
2. **Vague request:** “I need some help for my mom.”
3. **Missing information:** “I want to book a service.”
4. **Price question:** “How much does this cost?”
5. **Phone number only:** “Call me on 98XXXXXXXX.”
6. **Booking request:** “I want to arrange care for my mother starting next week.”
7. **Partial details:** The customer provides their name and care need but not their contact information.
8. **Information across multiple messages:** The customer provides different details in separate turns, and I check whether the agent remembers them.
9. **Unsupported guarantee:** “Can you guarantee a caregiver will arrive tomorrow?”
10. **Complete lead:** The customer provides all required information, and I check the confirmation and saved database record.

### What I will check

- Does the agent understand what the customer is asking?
- Does it ask a suitable follow-up question when information is unclear or missing?
- Does it collect the required lead information?
- Does it preserve details across multiple messages?
- Does it save the lead correctly and allow the record to be retrieved?
- Does it avoid inventing prices, availability, or guarantees?
- Does it distinguish collecting a booking request from actually confirming a booking?
- Does it identify when a lead is ready for the next step, according to rules approved by the mentor?

### How I will record the results

“I will record each test as Pass, Fail, or Needs Clarification. I will write down the expected behavior, what the agent actually did, and any issue I find. After testing, I can share the failures and ask which ones should be fixed first.”

---

## Overall Summary to Say to the Mentor

“Sir, in Week 1, I built the basic lead-capture foundation, including data models, validation, lead-status rules, and tests. In Week 2, I built a Python-based FAQ agent using LangChain, LangGraph, and Google Gemini, with six approved FAQs and a fallback response for unsupported questions. In Week 3, I extended lead capture into a multi-turn conversation that asks for missing details and saves leads in SQLite for later retrieval.

After this meeting, my Week 4 task is to test the agent with 8–10 realistic customer conversations, including difficult and incomplete cases. I will check the follow-up questions, information collection, database saving, and whether the agent avoids making up information.

I would also like to confirm the live Gemini verification status, the rules for deciding when a lead is ready for the next step, and how my agent should eventually connect with the scheduling and customer-support agents.”

## Questions I Can Ask at the Meeting

1. Are there any changes you want me to make to the work completed in Weeks 1–3?
2. For Week 4, should I test the lead-capture agent on its own or together with the qualification and routing agent?
3. What exact rules should I use to decide whether a lead is complete or ready for booking or routing?
4. What should the agent do when a customer asks about a price or availability that is not in the approved information?
5. What evidence do you want after Week 4: a test report, automated tests, a demo, or all three?
6. When should we begin integrating the lead-capture, scheduling, and customer-support agents?
