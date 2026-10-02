# Week 2 – FAQ Agent Development

## Saathi Sneha Care – Marketing/Sales AI Agent

**Prepared by:** Priyanka

**Project:** Saathi Sneha Care – AI Agent

**Task:** Build a small agent that can answer 2–3 basic questions using the FAQ list.

**Status:** Completed and tested

---

## 1. Introduction

As part of Week 2 of the Saathi Sneha Care AI Agent project, I developed a small FAQ-based AI agent that can answer frequently asked questions using the provided FAQ list.

The main objective was to build a basic agent that understands users' questions, identifies the relevant FAQ, and returns an appropriate answer.

The prototype was developed using Python, LangChain, LangGraph, and Google's Gemini model.

## 2. Objective

The objective of this task was to:

* Build a small AI-powered FAQ agent.
* Use the provided Saathi Sneha Care FAQ list as its knowledge source.
* Understand different ways users may phrase a question.
* Identify the FAQ relevant to a user's question.
* Return the corresponding predefined answer.
* Provide a fallback response when a question is not covered by the FAQ list.

## 3. Technologies Used

| Technology    | Purpose                                                      |
| ------------- | ------------------------------------------------------------ |
| Python        | Main programming language                                    |
| LangChain     | Connecting the language model with the FAQ selection process |
| LangGraph     | Managing the agent's workflow                                |
| Google Gemini | Matching user questions to relevant FAQs                     |
| Pydantic      | Previously explored for structured output                    |
| python-dotenv | Loading environment variables                                |
| VS Code       | Development environment                                      |

## 4. Project Structure

The project is organized into the following files:

```text
saathi_faq_agent/
│
├── data/
│   ├── __init__.py
│   └── faqs.py
│
├── langchain_version/
│   ├── __init__.py
│   └── faq_agent.py
│
├── .env
└── .venv/
```

**File descriptions:**

* `data/faqs.py`: Stores the six FAQs and their predefined answers.
* `langchain_version/faq_agent.py`: Contains the Gemini connection, FAQ matching function, LangGraph workflow, and terminal chat interface.
* `.env`: Stores the Gemini API key and model configuration.
* `.venv/`: Contains the project's Python virtual environment.

## 5. FAQ Knowledge Base

The FAQ agent uses six questions provided for Saathi Sneha Care.

| FAQ ID | Question                             | Main answer                                                                                                               |
| ------ | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| FAQ1   | Can I pay from abroad?               | International credit/debit cards through Stripe, with prices in USD.                                                      |
| FAQ2   | Can my parents pay locally?          | Khalti, cash, and monthly payments through the patient portal.                                                            |
| FAQ3   | Is there a setup or joining fee?     | No hidden setup or joining fees; add-ons are quoted separately.                                                           |
| FAQ4   | Can I change or cancel the plan?     | Plans can be upgraded, downgraded, or cancelled, with changes effective next billing cycle and no cancellation penalties. |
| FAQ5   | What if my parents need more visits? | Additional visits can be booked individually, with advice from a care coordinator.                                        |
| FAQ6   | Do you serve outside Kathmandu?      | Full service is currently in Kathmandu Valley, with expansion to Pokhara and Biratnagar.                                  |

The answers are stored in Python so the agent can retrieve the approved wording instead of generating new service information.

## 6. Agent Workflow

The FAQ agent follows a simple workflow:

```text
       User asks a question
                |
                v
       Receive user input
                |
                v
     Gemini matches the FAQ
                |
                v
       Select a FAQ ID
                |
                v
      LangGraph processes it
                |
                v
      Retrieve approved answer
                |
                v
       Return answer to user
                |
                v
              End
```

If no FAQ matches the user's question, the agent returns a fallback message asking the user to contact the Saathi Sneha Care team.

## 7. Implementation

### 7.1 FAQ storage

The FAQs are stored as Python dictionaries containing an ID, question, and answer. A dictionary indexed by FAQ ID makes it possible to retrieve the answer corresponding to a selected FAQ.

### 7.2 FAQ selection using Gemini

Gemini is used to identify which FAQ best matches the user's question. The model is instructed to return only a valid FAQ ID or `NOT_FOUND`.

The application checks the returned ID against the available FAQ IDs before using it.

### 7.3 LangGraph workflow

LangGraph manages the workflow through two main nodes:

* **FAQ selection node:** Identifies the relevant FAQ ID using Gemini.
* **Answer node:** Retrieves the predefined answer or returns the fallback message.

The nodes are connected in sequence, from the start of the graph to the end.

### 7.4 Fallback handling

When the user asks a question that is not covered by the FAQ list, the agent returns a message similar to:

"I'm sorry, I couldn't find an exact answer to that question in our FAQs. Please contact the Saathi Sneha Care team for further assistance."

This prevents the agent from presenting unsupported information as an approved answer.

## 8. Testing and Results

The FAQ agent was run from the project root using:

```bash
python -m langchain_version.faq_agent
```

The following test cases were checked:

| No. | User question                        | Expected behavior                                | Result |
| --- | ------------------------------------ | ------------------------------------------------ | ------ |
| 1   | Can I pay from abroad?               | Return the Stripe and USD payment FAQ.           | Passed |
| 2   | Can my parents pay locally?          | Return the Khalti, cash, and patient portal FAQ. | Passed |
| 3   | Is there a joining fee?              | Explain that there are no hidden joining fees.   | Passed |
| 4   | Can I cancel my plan anytime?        | Return the plan change and cancellation FAQ.     | Passed |
| 5   | What if my parents need more visits? | Explain the additional visit process.            | Passed |
| 6   | Do you serve outside Kathmandu?      | Return the current service area FAQ.             | Passed |
| 7   | Can you book me a flight?            | Return the fallback response.                    | Passed |

All listed test cases were reported as completed successfully during manual testing.

### Sample test

**Input:**

```text
Can I pay from abroad?
```

**Output:**

```text
Yes. You can pay using international credit or debit cards
through Stripe. Our prices are listed in USD, and your card
is charged the listed amount directly, so there is no need
to guess exchange rates.
```

The response matched the corresponding predefined FAQ answer.

## 9. Error Handling and Improvements

During development, the following issues were encountered and addressed:

* **Module import issue:** The application was run from the project root using Python's module execution syntax.
* **Gemini model configuration:** The model configuration was updated following a model availability error.
* **API connection interruption:** A retry configuration was included to help handle transient connection failures.
* **AFC warning:** The Gemini integration displayed an Automatic Function Calling warning. The configuration was adjusted to disable AFC, and subsequent testing returned answers without displaying the warning.

## 10. Current Scope and Limitations

The completed prototype is a small FAQ agent that runs through a terminal interface.

It currently:

* Uses a predefined FAQ knowledge base.
* Uses Gemini to match questions to FAQ IDs.
* Uses LangGraph to manage the workflow.
* Retrieves predefined answers.
* Provides a fallback for questions outside the FAQ list.

The current prototype does not yet include:

* Website or WhatsApp integration.
* CRM integration.
* Live appointment scheduling.
* Automatic updates to the FAQ knowledge base.
* A production deployment or monitoring system.

These features are outside the scope of the task described for Week 2 unless separately assigned.

## 11. Conclusion

The Week 2 task was to build a small agent capable of answering two to three basic questions using the provided FAQ list.

The prototype was implemented using Python, LangChain, LangGraph, and Google Gemini. It supports all six available FAQs, returns predefined answers, and handles questions outside the FAQ list through a fallback response.

The test cases were manually checked, and the agent successfully returned the expected answers during testing.

**The Week 2 FAQ agent development task is complete based on the requirement provided by the mentor.**

## 12. Next Steps

Potential next steps, subject to mentor guidance, include:

* Review the implementation with the mentor.
* Add further FAQs if required.
* Connect the FAQ agent to the wider Saathi Sneha Care AI agent architecture.
* Explore integration with a website or WhatsApp interface in a later milestone.

---

**End of Report**
