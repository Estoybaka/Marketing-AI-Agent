# Day 2 --- Questions, Decisions & Assumptions

**Company:** Saathi Sneha Care\
**Date:** September 22, 2026

## 1. Decisions

### Evidence approach

Use:

-   Public website.
-   Public social profiles.
-   Clearly labeled assumptions.


### Day 2 scope

Focus on:

-   Customer journey.
-   Funnel.
-   Lead lifecycle.
-   Lead data.
-   Agent boundaries.
-   Unknowns.
-   Automation opportunities.

### Facebook priority

Facebook remains the first implementation target.

### Common message format

``` json
{
  "channel": "...",
  "sender_id": "...",
  "text": "...",
  "timestamp": "...",
  "attachments": []
}
```

### Scheduling boundary

Sales Follow-up detects consultation intent and hands off to Scheduling.

## 2. Publicly Confirmed Facts

-   Saathi Sneha Care presents professional home care for parents in
    Nepal.
-   The website addresses families, including families abroad.
-   Free consultation/assessment is publicly offered.
-   Personalized care plans are publicly described.
-   A nurse and care coordinator are described as supporting care.
-   Ongoing health updates are publicly described.
-   WhatsApp, Messenger and Instagram contact options are shown.
-   Phone contact is shown.
-   Website states a response time of within 24 hours.
-   Website states an emergency line is available 24/7.
-   Multiple home-care services are listed.
-   Multiple care plans are listed.
-   The care team is publicly described as assessing needs and
    recommending care/plan options.
-   The plans page states full service is currently available in
    Kathmandu Valley and mentions expansion to Pokhara and Biratnagar.

## 3. Assumptions

-   A person contacting the company can be treated as a potential lead.
-   A lead may ask about a service or plan.
-   A lead may not know which service they need.
-   Lead information needs to be structured.
-   Channel and source should be tracked separately.
-   Follow-up may be required.
-   Qualification information may be needed before consultation.
-   Different channels may eventually require adapters.

## 4. Unknowns

-   CRM.
-   Database.
-   Lead statuses.
-   Qualification criteria.
-   Sales stages.
-   Follow-up schedule.
-   Lead assignment.
-   Facebook/WhatsApp/Messenger integrations.
-   Advertising/source tracking.
-   Scheduling process.
-   Calendar system.
-   Human approval rules.
-   Existing AI/automation.
-   Repository.
-   LLM/provider.
-   Deployment environment.

## 5. Questions to Validate Later

### Lead Capture

1.  What counts as a lead?
2.  What fields are mandatory?
3.  Is a contact required?
4.  How are duplicates handled?

### Qualification

5.  What makes a lead qualified?
6.  What information is required?
7.  What makes a lead unsuitable?
8.  Are rules service-specific?
9.  Who makes the final decision?

### Follow-up

10. How soon should a new lead receive a response?
11. How many follow-ups?
12. Over what period?
13. Which channels?
14. When is a lead inactive?

### Scheduling

15. When does Sales hand off to Scheduling?
16. What information is passed?
17. Which calendar/booking system?
18. Who confirms appointments?

### CRM

19. Is there a CRM?
20. What fields/statuses?
21. How is source attribution handled?
22. How is conversation history stored?

### Healthcare / Safety

23. Which messages require immediate human escalation?
24. What counts as an emergency?
25. What can AI answer?
26. What must always be handled by a human/clinical professional?

## 6. Facebook Investigation --- Fill Later

-   Page bio: \[FILL THIS\]
-   Contact buttons: \[FILL THIS\]
-   Messenger: \[FILL THIS\]
-   WhatsApp: \[FILL THIS\]
-   Website: \[FILL THIS\]
-   Recent post themes: \[FILL THIS\]
-   Common public questions: \[FILL THIS\]
-   Calls to action: \[FILL THIS\]
-   Lead-generation posts: \[FILL THIS\]
-   Public offers: \[FILL THIS\]
-   Other observations: \[FILL THIS\]


## 7. Reflection

### What I know
- The public customer journey is clearly defined: Discovery → Inquiry → Free consultation/assessment → Needs assessment → Personalized plan → Care begins → Ongoing updates.
- Contact channels that exist publicly: WhatsApp (+977 976-8621361), website contact form, Facebook (SaathiSnehaCare6), and phone.
- Website promises a response within 24 hours and states that an emergency line is available 24/7.
- Free consultation / needs assessment is publicly offered.
- Core services and care plans (Care Connect, Wellness Plus, Chronic Care) are listed on the website.
- Real-time updates, visit summaries, lab results, and family dashboard are part of the public value proposition.
- Facebook page exists and is linked from the website, but full content requires login.

### What I inferred
- Lead capture happens mainly through WhatsApp, Facebook, and the website contact form.
- A structured lead record is needed to normalize multi-channel conversations.
- Statuses such as `new`, `contacted`, `needs_information`, `qualified`, `consultation_requested`, and `booked` are practical for routing between agents.
- Different agents (Lead Capture, Qualification, Sales Follow-up, Scheduling, Content) should own clear stages and hand off cleanly.
- Preferred contact time is important because the contact page explicitly asks customers when they are free.
- Patient location and urgency matter because service availability and urgent services are publicly highlighted.

### What I do not know
- Exact internal qualification rules.
- How the CRM is structured and updated.
- Real sales pipeline stages used by the team.
- Exact follow-up cadence and ownership after first contact.
- Precise scheduling workflow and calendar tools.
- Whether Messenger, Instagram, or other channels are actively monitored.
- Actual company status model (the statuses we used are only proposed).
- Any existing lead scoring or prioritization logic.

### What I need from the mentor/team later
- Confirmation of the real lead statuses used internally.
- Clarification of qualification criteria (what makes a lead “qualified”).
- Details of the current CRM / tools and how updates are recorded.
- Ownership and process for scheduling free consultations.
- Any existing follow-up SLAs or cadence rules.
- Confirmation of which channels are actively managed and by whom.

### Most important automation opportunity
Automating the early pipeline from **inbound capture → structured lead → first response (within 24h) → information collection → qualification → consultation booking**.  
This is the highest-leverage area because the public journey is clear, response-time promises exist, and multi-channel inbound is already happening.

### Biggest uncertainty
The gap between the well-documented public customer journey and the completely opaque internal processes (qualification, CRM updates, sales handoff, and scheduling). Without clarity on these internal rules, any automation risks creating friction or incorrect handoffs.
