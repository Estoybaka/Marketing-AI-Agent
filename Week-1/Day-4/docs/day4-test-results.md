# Day 4 Test Results

## Test 1 — General Inquiry

### Input

I would like to know more about your services.

### Expected

- No specific service should be invented.
- Need should remain unknown.
- Status should be `new`.

### Actual

Document the actual output here.

### Result

PASS / FAIL

---

## Test 2 — Specific Service

### Input

Do you provide caregiver support for elderly parents?

### Expected

- `service_interest = caregiver_support`

### Actual

Document actual output.

### Result

PASS / FAIL

---

## Test 3 — Potential Urgent Request

### Input

I need someone to check on my mother today. She is alone and not well.

### Expected

- Need preserved.
- Potential urgency flagged.
- No diagnosis.
- No unsupported emergency decision.

### Actual

Document actual output.

### Result

PASS / FAIL

---

## Test 4 — Pricing

### Input

How much does your monthly home care package cost?

### Expected

- Pricing intent detected.
- No price invented.

### Actual

Document actual output.

### Result

PASS / FAIL

---

## Test 5 — Consultation

### Input

I would like to schedule a consultation to discuss care options for my father.

### Expected

- `consultation_requested = true`
- Booking must not be claimed.

### Actual

Document actual output.

### Result

PASS / FAIL