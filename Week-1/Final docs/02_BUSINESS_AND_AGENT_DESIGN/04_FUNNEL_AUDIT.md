# Funnel Audit - Website, Ads, Social, and Inbound Lead Handling

## 1. Audit Purpose

The Week 1 funnel audit is designed to answer four questions:

1. What does the public customer journey look like?
2. Where can a Lead enter?
3. What can be confirmed from public information?
4. What parts of the internal funnel are still unknown?

The Week 1 evidence rule is important:

> This is a public-information and clearly labeled assumption audit, not an invented internal process map.

Funnel = the journey from stranger → lead → customer → ongoing client.

---

# 2. Audit Status Labels

Each finding should be understood using these labels:

| Label | Meaning |
|---|---|
| CONFIRMED | Directly supported by available public evidence |
| ASSUMPTION | Reasonable working interpretation, not an internal fact |
| UNKNOWN | Not available or not confirmed |
| TARGET | Proposed future system behavior |

---

# 3. Website Audit

## 3.1 Website Investigated

- The public website investigated was:

  ```text
  https://www.saathisnehacare.com/
  ```

- The public site presents professional medical/home care in Nepal.

- The public positioning emphasizes:

   - parents living in Nepal,
   - families abroad,
   - professional home care,
   - health updates for family members,
   - care services and plans.

- These public-facing points are treated as confirmed public information.

---

# 4. Public Customer Journey

- The public website presents a journey that can be represented as:

   ```text
   Free Consultation
         ↓
   Personalized Plan
         ↓
   Care Begins
         ↓
   Stay Connected
   ```

- This is important for the funnel audit because it shows a public-facing journey from initial consultation to ongoing care.

- However:
**This is not automatically the internal Lead lifecycle.**

- The technical lifecycle created during Week 5 is a workflow model for the prototype.

- The public website journey and internal Lead lifecycle must remain separate unless the business confirms that they are intended to match.

---

# 5. Public Business Understanding

- The public positioning is oriented toward:

   - parents living in Nepal,
   - families abroad,
   - people needing professional home care,
   - families wanting updates about parents' health.

- A reasonable working assumption was:

  > A likely Lead may be an adult child or family member living away from Nepal who is looking for care/support for a parent or loved one in Nepal.


---

# 6. Public Services

- The public investigation identified services including:

   1. Caregiver Support
   2. Hospital Escort
   3. Chronic Disease Monitoring
   4. Doctor Consult
   5. Lab Coordination
   6. Medication Management
   7. Wellness Checks
   8. Emergency / on-demand support
   9. Other healthcare coordination

- The existence of these public services is confirmed by the public investigation.

- The internal rules for when a Lead should be matched to a particular service remain unknown.

---

# 7. Public Plans

- The public investigation identified:

   - Care Connect
   - Wellness Plus
   - Chronic Care

- Publicly described features included:

   - wellness checks,
   - family dashboard/app access,
   - dedicated care manager,
   - vitals,
   - family health reports,
   - medicine coordination/refills,
   - monthly doctor review.

- The public existence of services and plans is confirmed.

- The internal rule for recommending a particular plan is **UNKNOWN**.

- Therefore the Lead Capture system must not automatically choose a plan simply because a message sounds related to it.

---

# 8. Public Contact Entry Points

- Public entry points identified included:

   - WhatsApp
   - Messenger
   - Instagram
   - Phone
   - Website/contact journey

- The website stated that the care team would reach out within 24 hours and that an emergency line is available 24/7.

- These public statements are not enough to define the internal automation rules.

---

# 9. What Is Unknown About Inbound Handling

- The public information did not confirm:

   - which channel produces the most Leads,
   - who monitors each channel,
   - whether all channels share one team,
   - whether messages are automatically captured,
   - whether a CRM currently exists,
   - how inbound Lead ownership works,
   - how Leads are assigned,
   - how qualification is performed,
   - what makes a Lead sales-ready,
   - how human handoff works.

<!-- - These should remain questions for the kickoff. -->

---

# 10. Ads Audit

- The project identified Facebook as the first implementation target.

- This creates a useful source value:

   ```text
   facebook_ad
   ```

- However, the provided Week 1 context does not contain verified internal advertising data such as:

   - campaign list,
   - campaign budgets,
   - ad spend,
   - Lead volume,
   - conversion rate,
   - campaign routing,
   - campaign ownership,
   - CRM attribution process.

- Therefore none of these should be filled with invented values.

---

# 11. Social Audit

- The project discussed these channels:

   ```text
   Facebook
   WhatsApp
   TikTok
   Viber
   ```

- Public contact entry points also included:

   ```text
   Messenger
   Instagram
   Phone
   Website
   ```

- The planned channel direction was:

### Facebook

- First implementation target.

### WhatsApp

- Later two-way integration.

### TikTok

- V1 direction:

   - outbound content,
   - human monitoring for comments/DMs.

### Viber

- Later / nice-to-have.

- These are project directions, not proof that all integrations are active.

---

# 12. Source vs Channel

- This distinction is critical for funnel tracking.

## Channel

- The place where the current conversation happens.

- Examples:

   ```text
   facebook
   whatsapp
   instagram
   website
   phone
   ```

## Source

- Where the Lead originally came from.

- Examples:

   ```text
   facebook_organic
   facebook_ad
   instagram
   website
   google_ad
   referral
   unknown
   ```

- Example:

   ```text
   source  = facebook_ad
   channel = whatsapp
   ```

- This means:

   - the Lead originated from a Facebook advertisement,
   - but the current conversation is happening on WhatsApp.

- If source and channel are mixed, campaign attribution becomes unclear.

---

# 13. Working Funnel Hypothesis

- A working funnel model was:

   ```text
   Potential Customer
          ↓
   Discovery / Marketing
          ↓
   Customer Inquiry
          ↓
   Lead Capture
          ↓
   Need / Service Understanding
          ↓
   Qualification / Information Gathering
          ↓
   Consultation / Free Assessment
          ↓
   Plan Recommendation
          ↓
   Enrollment / Booking
          ↓
   Care Begins
   ```

- This is an **ASSUMPTION / TARGET model**.
- It is not a claim about the internal current workflow.

---

# 14. Funnel Gaps

- The main gaps identified during Week 1 are:

### Lead source

Unknown:

- exact active sources,
- exact campaign attribution,
- source ownership.

### Channel handling

Unknown:

- who handles each channel,
- response ownership,
- assignment process.

### Qualification

Unknown:

- exact qualification criteria,
- required qualification fields,
- sales-ready definition.

### Sales follow-up

Unknown:

- follow-up timing,
- sequence,
- escalation,
- human handoff.

### Scheduling

Unknown:

- booking platform,
- confirmation process,
- calendar ownership,
- handoff contract.

### CRM

Unknown:

- whether one exists,
- what system is used,
- which fields are stored,
- who owns records.

---

# 15. Funnel Audit Conclusion

- The Week 1 audit provides a useful public-facing view of the funnel and a working target model.

- It does not provide enough evidence to claim knowledge of internal Lead operations.

- Therefore the correct Week 1 conclusion is:

```text
Public Funnel Understanding
        +
Technical Target Model
        +
Explicit Unknowns
```

- The remaining internal process must be confirmed before it becomes production logic.
