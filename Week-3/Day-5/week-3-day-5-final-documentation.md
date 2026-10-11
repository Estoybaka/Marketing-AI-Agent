# Week 3 — Day 5: Final Testing, Evidence, Documentation, and Verification

## Project
**Project:** Marketing-AI-Agent  
**Week:** 3  
**Day:** 5  
**Feature:** Elder-Care Lead Assistant  
**Verification date:** October 10, 2026  
**Status:** Core implementation and testing verified; final documentation prepared.

## 1. Objective

Complete and verify the lead-capture workflow that:
- conducts an interactive conversation with a prospective caregiving customer;
- collects the customer's name, contact information, and care need;
- identifies which required information is still missing;
- manages the conversation through LangGraph;
- saves completed lead information to a SQLite database; and
- retrieves saved leads, including after restarting the application.

## 2. Week 3 learning plan

| Day | Focus | Outcome |
|---|---|---|
| Day 1 | Lead-capture design and conversational collection | Defined the information to collect and the conversation behavior. |
| Day 2 | Database and lead data model | Implemented persistent SQLite lead storage and a structured lead record. |
| Day 3 | Information extraction and missing-field detection | Added logic to identify collected information and determine the next field to request. |
| Day 4 | Interactive LangGraph conversation and saving | Connected the conversation flow to the lead-saving process. |
| Day 5 | Full testing, evidence, documentation, and final verification | Ran automated tests, checked a live conversation, and verified persistent lead retrieval. |

## 3. Main project components

The project includes these relevant files:

- `main.py` — command-line conversation interface and lead lookup commands.
- `lead_graph.py` — LangGraph conversation workflow and model integration.
- `lead_database.py` — SQLite persistence and database retrieval functions.
- `leads.db` — SQLite database containing saved lead records.
- `test_lead_logic.py` — lead-collection logic tests.
- `test_completed_lead.py` — completed-lead behavior tests.
- `test_lead_database.py` — database tests.
- `test_lead_graph_database.py` — LangGraph and database integration tests.
- `test_lead_graph_schema.py` and `test_full_lead_schema.py` — schema-related tests.
- `test_migration_and_status.py` — migration/status-related tests.
- `test_gemini_key.py` — model/API configuration test.

The exact set of files in the working directory may include additional tests or evidence files.

## 4. Lead information and collection behavior

The lead record supports these fields:

- Lead ID
- Name
- Email
- Phone
- Care need
- Urgency
- Source
- Status
- Completion flag
- Next field to collect

The assistant asks for missing information during the conversation. Once the required lead information has been collected, it reports completion and saves the lead to SQLite.

## 5. Live conversation evidence

A live model-backed conversation completed successfully:

```text
You: I am interested in your caregiver service.
Agent: Sure. May I have your name?

You: Anita Sharma
Agent: What is your phone number or email address?

You: anita@example.com
Agent: What kind of care service do you need?

You: I need care for my elderly father.
Agent: Thank you. I have recorded your information.

[Lead collection complete]
Lead ID: 1ddd2744-0d39-4007-9b34-b636bfb98485
Lead status: New
Your information has been saved to the database.
```

The saved lead was then retrieved and displayed:

```text
--- SAVED LEAD ---
Lead ID: 1ddd2744-0d39-4007-9b34-b636bfb98485
Name: Anita Sharma
Email: anita@example.com
Phone: None
Care need: I need care for my elderly father
Urgency: None
Source: None
Status: New
Complete: True
Next field: None
```

This demonstrates that the conversation reached completion and the saved record could be read back. Fields not collected during this example remained `None`.

## 6. Persistent lead lookup

The command-line interface supports:

- `/lead` — show the current conversation's saved lead when available; otherwise, list saved leads in the database.
- `/lead <ID>` — display the full details of the saved lead with the specified lead ID.
- `/quit` — exit the assistant.

The persistent lookup behavior was tested after the application was restarted. The saved lead list appeared, and `/lead 1ddd2744-0d39-4007-9b34-b636bfb98485` displayed Anita Sharma's record.

This distinguishes database persistence from current-session lookup: the SQLite database retains records across application restarts, and the updated interface makes older records discoverable.

## 7. Automated verification

The following checks were run during development and final verification:

| Check | Result |
|---|---|
| Python syntax compilation for `main.py` | Passed |
| Lead-collection logic tests (`python .\test_lead_logic.py`) | Previously reported 5 passed, 0 failed |
| Completed-lead tests | Previously recorded as passed |
| SQLite database tests | Previously recorded as passed |
| LangGraph + SQLite integration tests | Previously recorded as passed |
| Full test suite (`python -m pytest -q`) | User confirmed all tests passed on October 10, 2026 |
| Live conversation and lead saving | Passed |
| `/lead` saved-lead listing after restart | Passed |
| `/lead <ID>` individual lead lookup | Passed |

**Note:** The exact final total printed by `pytest` was not included in the final confirmation, so this report records the result as “all tests passed” without inventing a test count.

## 8. Commands used for final verification

Run these commands from the Day 4 project directory:

```powershell
cd C:\Priyanka\GitHub\Marketing-AI-Agent\Week-3\Day-4
python -m py_compile .\main.py
python -m pytest -q
python .\test_lead_logic.py
python main.py
```

In the running application, test:

```text
/lead
/lead 1ddd2744-0d39-4007-9b34-b636bfb98485
/quit
```

The lead ID above is the one captured in the successful live-conversation evidence. If using another database copy, select an ID shown by `/lead`.

## 9. Known observations

- The model configuration was changed to `gemini-3.5-flash-lite` after the previously selected model encountered a quota issue.
- A library warning reported that the temperature setting was ignored for this model. The warning was informational and did not prevent the demonstrated conversation from completing.
- In the captured live conversation, phone, urgency, and source were not collected, so their values remained `None`. The example still demonstrated completion according to the workflow's configured required fields.

## 10. Final verification summary

The demonstrated workflow can:
1. start a caregiving lead conversation;
2. request the missing required information;
3. complete the lead;
4. save the lead to SQLite;
5. retrieve saved lead information;
6. list persisted leads after an application restart; and
7. retrieve an individual lead by ID.

The user confirmed that the full `python -m pytest -q` test suite passed and that the new lookup commands behaved as expected.

**Conclusion:** Week 3 Day 5's core implementation and testing are complete. Save this report in the project's documentation folder and retain the terminal/test output as evidence. After confirming the report and evidence are stored in the project, Week 3 can be marked complete.
