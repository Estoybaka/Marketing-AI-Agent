# Week 1 Plan, Deliverables, and Completion Criteria


# 1. Week 1 Workstreams

- Week 1 had two connected workstreams.

## Workstream A - Business Discovery

```text
Website
Ads
Social

Inbound Lead Handling
       ↓
Funnel Audit
       ↓
Agent Scope
       ↓
Lead Data Dictionary
```

## Workstream B - Technical Foundation

```text
Message
   ↓
NormalizedMessage
   ↓
Lead Capture
   ↓
Lead
   ↓
Validation
   ↓
Lifecycle
   ↓
GraphState
   ↓
Workflow
   ↓
Tests
```

- The technical foundation supports the business model, but it does not replace the business discovery work.

---

# 3. Day 1 Completion Focus

- Day 1 was focused on understanding.

- Expected results:

   - understand project purpose,
   - understand broad architecture,
   - identify assigned agents,
   - agree on evidence rules,
   - establish boundaries,
   - avoid premature coding.

- A major Day 1 conclusion was:

   ```text
   Do not code an imagined production system.
   ```

- Instead:

   ```text
   Understand → Evidence → Boundaries → Data Design → Implementation
   ```

---

# 4. Day 2 Completion Focus

- Day 2 focused on public business investigation.

- Expected results:

   - investigate public website,
   - identify public customer journey,
   - identify services,
   - identify plans,
   - identify public contact paths,
   - identify social/channel directions,
   - separate public facts from internal unknowns.

---

# 5. Day 3 Completion Focus

- Day 3 was the bridge from business understanding to technical design.

- Expected results:

   - define `NormalizedMessage`,
   - define Lead structure,
   - define agent input/output contracts,
   - define initial lifecycle,
   - define validation rules,
   - define five core behavioral test cases.

---

# 6. Day 4 Completion Focus

- Day 4 converted the design into a local prototype.

- Expected results:

   - local Python project,
   - project structure,
   - Pydantic models,
   - deterministic Lead Capture,
   - validation,
   - five core tests,
   - automated tests,
   - decisions/unknowns documentation.

- The Day 4 pipeline was:

   ```text
   Sample Message
         ↓
   Normalized Message
         ↓
   Lead Capture
         ↓
   Lead Record
         ↓
   Validation
         ↓
   Expected Test Result
   ```

---

# 7. Day 5 Completion Focus

- Day 5 moved the project from isolated functions into workflow thinking.

- Tasks:

   1. Review Day 4 implementation.
   2. Verify existing tests.
   3. Add explicit extraction thinking.
   4. Introduce lifecycle/status-transition thinking.
   5. Create lifecycle module.
   6. Introduce minimal shared state.
   7. Convert Lead Capture into a node-like function.
   8. Add expanded tests.
   9. Add negative tests.
   10. Create test fixtures.
   11. Prepare LangGraph boundary.
   12. Document Day 5 decisions and unknowns.

- The recorded final Day 5 result was:

   ```text
   29 passed
   ```

---

# 8. Day 6 Completion Focus

- Day 6 is the close-out day for Week 1.

- The plan is:

   1. Finish Funnel Audit
   2. Finalize Agent Scope
   3. Finalize Lead Data Dictionary
   4. Verify Development Environment
   5. Run all tests
   6. Create Week 1 evidence
   7. Create Week 1 Final Report
   8. Prepare Kickoff Questions


- Day 6 shifts the focus from mainly technical construction to closing the business/discovery requirements and producing evidence.

---

# 9. Day 6 Completion Model

- The intended relationship is:

   ```text
   Week 1 Original Requirements
               ↓
   What We Investigated
               ↓
   What We Implemented
               ↓
   What Is Confirmed
               ↓
   What Remains Unknown
               ↓
   Evidence
               ↓
   Final Report
               ↓
   Kickoff Questions
   ```

---

# 10. Week 1 Deliverable Set

The final documentation is organized into dedicated documents:

### Foundation

- Project Context and Objectives
- Week 1 Plan and Expected Outputs
- Architecture and System Overview

### Business and Agent Design

- Funnel Audit
- Sub-Agent Scope
- Lead Data Dictionary

### Technical Design

- Data Models and Interface Design

### Day-by-Day

- Day-by-Day Implementation Log

### Week 1 Final

- Evidence and Deliverables
- Decisions and Open Items
- Final Report

### Handoff

- Week 2 Handoff and Kickoff

---

# 11. Completion Status Language

- Every final document should distinguish between:

   - **Completed**
   - **Confirmed**
   - **Partially completed**
   - **Not implemented**
   - **Unknown**
   - **Target / Future**

- This prevents a technical prototype from being mistaken for a production integration.
