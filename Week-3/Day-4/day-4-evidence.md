# Week 3 — Day 4 Evidence

## Interactive LangGraph Conversation and Database Saving

**Project:** Marketing AI Agent — Elder-Care Lead Generation and Funnel Automation System

**Date:** October 9, 2026

### Objective

Build an interactive conversational agent that collects elder-care leads, identifies missing information, saves lead records to SQLite, and confirms when lead collection is complete.

### Successful conversation

* User expressed interest in caregiver services.
* Agent asked for the user's name.
* User provided: Ram Sharma.
* Agent asked for a phone number or email address.
* User provided: [ram@example.com](mailto:ram@example.com).
* Agent asked about the care requirement.
* User provided: Care for my elderly mother.
* Agent confirmed that the information had been recorded.

### Database verification

* Lead ID was generated successfully.
* Name was saved as Ram Sharma.
* Email was saved as [ram@example.com](mailto:ram@example.com).
* Care need was saved as Care for my elderly mother.
* Lead status was New.
* Lead completion was True.
* Next field was None.
* The `/lead` command successfully retrieved the saved record.

### Test results

The complete automated test suite passed: 26 tests passed.

### Conclusion

The interactive LangGraph conversation and SQLite lead-saving flow worked successfully in the manual test. The application collected the required information, determined that the lead was complete, and displayed the saved record.

### Remaining verification

Verify that saved records remain available after restarting the application, and confirm that a new conversation receives a separate conversation ID.
