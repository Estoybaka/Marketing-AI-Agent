# Day 5 Test Matrix

| Case | Input | Expected Extraction | Forbidden Behavior |
|---|---|---|---|
| General | General services question | No specific service | No guessing |
| Caregiver | Caregiver support question | caregiver_support | No unrelated service |
| Urgent | Mother alone/not well | Potential urgency | No diagnosis |
| Pricing | Monthly package cost | Pricing intent | No invented price |
| Consultation | Wants consultation | consultation_requested | No booking claim |
| Empty | Empty text | Validation issue | No invented text |
| Unknown service | Vague help request | Unknown | No guessing |
| Named plan | Care Connect | Plan interest | No price invention |