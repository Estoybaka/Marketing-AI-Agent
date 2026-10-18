# Day 4 Test Results

## Automated Test Run

- Python version: 3.11.7
- Test runner: pytest 8.4.2
- Environment: .venv-integration-check
- Test command: `python -m pytest .\Week-1\Day-4\tests -v`
- Result: **29 passed**
- Dependency check: `python -m pip check` reported no broken requirements.

## Scenario Coverage

### 1. General Inquiry
- Test: `test_general_inquiry_does_not_invent_service`
- Result: PASS

### 2. Specific Service
- Test: `test_specific_service_is_extracted`
- Result: PASS

### 3. Potential Urgent Request
- Tests: `test_potential_urgent_request`, `test_urgent_message_is_marked_potential`
- Result: PASS

### 4. Pricing
- Tests: `test_pricing_request_does_not_invent_price`, `test_pricing_question_does_not_invent_price`
- Result: PASS

### 5. Consultation
- Tests: `test_consultation_request`, `test_consultation_request_is_not_booking`
- Result: PASS

## Additional Coverage

The successful test run also covered lead validation, channel/source preservation,
caregiver-service detection, vague requests, lifecycle transitions, normalized
messages, graph state, and workflow behavior.

## Evidence Limitations

This report records automated test results. It does not claim that the example
messages above were manually executed and their full outputs captured.
