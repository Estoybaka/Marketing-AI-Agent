# Week 3 — Day 4 Testing Evidence

## Project

Marketing AI Agent — Caregiver Lead Collection

## Local Test Results

### 1. Lead Logic Tests

File: `test_lead_logic.py`

* Tests run: 5
* Passed: 5
* Failed: 0

Verified:

* Existing lead information is preserved.
* Missing fields are detected.
* Empty extracted values do not erase saved information.
* Incomplete leads are not marked complete.
* Complete leads are recognized.

### 2. Completed-Lead Tests

File: `test_completed_lead.py`

* Tests run: 4
* Passed: 4
* Failed: 0

Verified:

* Additional care details can update a lead.
* Unchanged information is not falsely reported as updated.
* Corrected contact information replaces the previous value.
* Missing required fields continue to be requested.

### 3. Python Syntax Check

Command:
`python -m py_compile lead_graph.py`

Result: Passed. Python returned to the terminal prompt without a syntax error.

### 4. Integration Test Status

Gemini and LangGraph end-to-end scenarios have not yet been verified against the updated application.

Reason: Gemini free-tier quota was previously exhausted.

### 5. Current Conclusion

The nine local logic tests pass, and the updated Python file compiles successfully. End-to-end integration, persistent database storage, and final application verification remain outstanding.

### 6. SQLite Database Tests

File: `test_lead_database.py`

* Tests run: 7
* Passed: 7
* Failed: 0

Verified:

* Database and table initialization.
* Saving and retrieving a lead.
* Preserving existing information when incoming values are empty.
* Correcting existing contact information.
* Keeping separate conversations' leads isolated.
* Listing saved leads.
* Handling unknown conversation IDs.

Result: All seven SQLite database tests passed.

Note: These tests verify the database module in isolation. Integration with the Gemini-powered LangGraph conversation remains to be verified.


# Week 3 — Day 4 Testing Evidence

## Project

Marketing AI Agent — Caregiver Lead Collection

## 1. Lead Logic Tests

File: `test_lead_logic.py`

* Tests run: 5
* Passed: 5
* Failed: 0

Verified:

* Existing lead information is preserved.
* Missing fields are detected.
* Empty extracted values do not erase saved information.
* Incomplete leads are not marked complete.
* Complete leads are recognized.

## 2. Completed-Lead Tests

File: `test_completed_lead.py`

* Tests run: 4
* Passed: 4
* Failed: 0

Verified:

* Additional care details can update a lead.
* Unchanged information is not falsely reported as updated.
* Corrected contact information replaces the previous value.
* Missing required fields continue to be requested.

## 3. SQLite Database Tests

File: `test_lead_database.py`

* Tests run: 7
* Passed: 7
* Failed: 0

Verified:

* Database and table initialization.
* Saving and retrieving a lead.
* Preserving existing information when incoming values are empty.
* Correcting existing contact information.
* Keeping separate conversations' leads isolated.
* Listing saved leads.
* Handling unknown conversation IDs.

## 4. LangGraph + SQLite Integration Tests

File: `test_lead_graph_database.py`

* Tests run: 4
* Passed: 4
* Failed: 0

Verified:

* Incomplete leads are saved.
* Complete leads are saved.
* Corrected contact information is saved.
* Different conversations retain separate leads.

Note: Information extraction was mocked during these integration tests. These results verify graph and database integration, not live Gemini extraction.

## 5. Python Syntax Check

Command:

`python -m py_compile lead_graph.py lead_database.py test_lead_graph_database.py`

Result: Passed. Python returned to the terminal prompt without a syntax error.

## 6. Real SQLite Persistence Verification

Verified using the actual `leads.db` database.

Operations performed:

* Saved a sample lead using `save_lead()`.
* Retrieved it using `get_lead()`.
* Retrieved it again through `list_leads()` in a separate command.

Verification record:

* Thread ID: `manual-verification-001`
* Name: Ram Sharma
* Contact: [ram@example.com](mailto:ram@example.com)
* Need: Care for elderly mother

Result: Saving, retrieval, and persistence across separate commands were verified successfully.

Note: The sample lead is verification data, not a lead collected through a live Gemini-powered conversation.

## 7. Live Gemini Verification

Status: Pending.

The Gemini free-tier quota was previously exhausted. Live extraction and the complete user-agent conversation still need to be verified when API access is available.

## 8. Current Conclusion

The isolated lead-logic tests, completed-lead tests, SQLite database tests, and LangGraph + SQLite integration tests passed. Real SQLite saving and retrieval were also verified.

The remaining major verification is the live Gemini-powered conversation, including extracting user information, asking for missing fields, and saving the completed lead.
