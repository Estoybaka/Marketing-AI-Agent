# Day 4 — Decisions and Unknowns

## CONFIRMED

- The Day 4 prototype uses the Day 3 normalized message contract.
- Lead Capture receives a normalized message.
- Lead Capture produces a lead record.
- Missing customer information should remain unknown/null.
- Lead Capture should not invent pricing.
- Lead Capture should not perform medical diagnosis.
- Lead Capture should not perform qualification.

## ASSUMPTIONS

- A local Python prototype is sufficient for the Day 4 implementation phase.
- The Day 3 target Lead schema is suitable for the prototype.
- Simple deterministic extraction rules are sufficient for the initial prototype.

## UNKNOWN

- Actual production CRM schema.
- Actual lead qualification criteria.
- Actual internal escalation rules.
- Actual lead assignment workflow.
- Actual production channel adapter implementation.
- Production database choice.
- Production LLM/provider choice.
- Production deployment architecture.

## TARGET

- Lead Capture will later become a LangGraph node.
- Channel adapters will provide normalized messages.
- Qualification will be handled separately.
- Scheduling will remain separate from Lead Capture.