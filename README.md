# Marketing AI Agent - Customer Care Prototype



A Python-based customer care prototype for Saathi Sneha Care, designed to help overseas family members arrange elderly care services for their parents in Nepal.



The project combines FAQ answering, customer lead capture, qualification, routing, consent handling, and scheduling-handoff preparation.



## 1. Current Features



- **FAQ Agent:** Answers questions using the existing Saathi Sneha Care FAQ knowledge base.

- **Lead Capture:** Collects customer name, phone or email, care requirements, and timing.

- **Lead Qualification:** Validates and processes customer information.

- **Conversation Routing:** Routes messages to the FAQ Agent, Lead Agent, or both.

- **Database:** Persists lead information using SQLite.

- **Contact Consent:** Tracks unanswered, accepted, declined, and revoked contact consent.

- **Follow-up Preparation:** Creates follow-up drafts only when explicit contact consent exists. Messages are not automatically sent.

- **Scheduling Preparation:** Validates information for a possible Scheduling Agent handoff.



## 2. Current Project Limitations



The following work is intentionally pending:



- Actual Scheduling Agent integration and real appointment booking.

- Automatic normalization of natural-language timing into structured appointment dates and times.

- Live verification of Gemini extraction accuracy across real customer conversations.



**Important:** A scheduling request being prepared does not mean an appointment is booked. A lead must not be marked `Booked` without confirmation from the Scheduling Agent.



The 20 customer scenarios are automated integration tests using a deterministic test extractor. They are not 20 manually conducted conversations and do not establish live Gemini extraction accuracy.



## 3. Project Structure



```text

Marketing-AI-Agent/

│

├── Week-1/                 # Lead models and validation workflow

├── Week-2/                 # FAQ Agent

├── Week-3/                 # Lead capture and SQLite persistence

├── Week-4/                 # Integration task documentation

├── integration/            # Routing, service, and scheduling contract

│   └── tests/              # Integration and customer scenario tests

│

├── requirements.txt        # Application dependencies

├── requirements-dev.txt    # Development and testing dependencies

├── environment_setup.md    # Environment setup instructions

├── Whole-task.md           # Original project requirements

├── Week-4-Task-Report.md   # Week 4 implementation report

└── README.md               # Project overview and instructions

```



## 4. Requirements



- Python 3.11 or compatible Python version

- Gemini API key for live lead extraction

- Dependencies listed in `requirements-dev.txt`



## 5. Installation



From the repository root, create and activate a virtual environment:



```powershell

python -m venv .venv

.\\.venv\\Scripts\\Activate.ps1

```



Install dependencies:



```powershell

python -m pip install -r requirements-dev.txt

```



Create a `.env` file in the repository root and add your Gemini API key:



```text

GEMINI_API_KEY=your_api_key_here

```



Never share or commit your actual API key.



## 6. Run the Lead Capture Application



From the repository root:



```powershell

cd .\\Week-3\\Day-4

python main.py

```



Available interactive commands include:



- `/lead` — start a lead conversation.

- `/lead <ID>` — open an existing lead conversation.

- `/quit` — exit the application.



## 7. Run Tests



Run the complete test suite from the repository root:



```powershell

python -m pytest -q

```



Run integration tests separately:



```powershell

python -m pytest .\\integration\\tests\\ -q

```



## 8. Latest Verified Test Results



**Verification date:** November 5, 2026



| Test group | Passing tests |

|---|---:|

| Week 1 | 29 |

| Week 2 | 15 |

| Week 3 | 53 |

| Integration | 64 |

| **Full repository suite** | **161** |



The 20 automated customer scenarios passed as part of the integration suite.



Test counts describe the latest verified run and may change after further development.



## 9. Documentation



- [Original Project Requirements](Whole-task.md)

- [Environment Setup](environment_setup.md)

- [Week 4 Task Report](Week-4-Task-Report.md)

- [Integration Verification Report](integration/VERIFICATION_REPORT.md)



## 10. Data and Security



- `.env` files are excluded through `.gitignore`.

- Local SQLite database files are excluded through `.gitignore`.

- Do not share customer contact information or real customer records in demonstrations.

- Contact consent must be explicit before follow-up.

- An unanswered or ambiguous consent response must not be treated as agreement.

- Follow-up drafts are not automatically sent.



---



**Project status:** Customer care prototype and automated integration testing completed for the current scope. Actual Scheduling Agent integration remains pending.

