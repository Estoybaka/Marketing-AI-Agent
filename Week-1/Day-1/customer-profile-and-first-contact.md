# Customer Profile and First Contact Understanding

## Week 1 — Day 1

**Project:** Marketing, Sales & Lead-Generation Sub-Agents
**Company:** Saathi Sneha Care

## 1. Customer Profile

### Primary Customer (Working Assumption)

The likely primary customer is an adult child or family member living abroad who wants to arrange professional care and support for their parent living in Nepal.

This is a working assumption based on the company's public positioning, not a confirmed description of every customer.

### Customer Situation

* The customer lives outside Nepal.
* Their parent or loved one lives in Nepal.
* They may not be physically available to provide regular care.
* They are looking for reliable care services and ways to stay informed about their parent's well-being.
* They may want to understand available services, care plans, costs and consultation options.

### Customer's Possible Goals

* Arrange suitable care for their parent.
* Understand which services are available.
* Receive updates about their parent's care.
* Understand the process of starting care.
* Discuss care options with the care team.
* Arrange a consultation.

These are potential goals to validate, not confirmed motivations of all customers.

## 2. What Matters in the First Message?

When a customer first contacts the company, the Lead Capture Agent should identify the information explicitly provided and leave missing information unknown.

| Information             | Why it matters                                     | Example              |
| ----------------------- | -------------------------------------------------- | -------------------- |
| Customer name           | Identify the person contacting the company         | Anil                 |
| Contact information     | Enable follow-up                                   | WhatsApp number      |
| Relationship to patient | Understand whom the care is for                    | Son                  |
| Customer location       | Understand their time zone for communication       | Australia            |
| Patient location        | Identify where care may be required                | Kathmandu            |
| Care need               | Understand the type of assistance requested        | Caregiver support    |
| Urgency                 | Understand when care is needed                     | As soon as possible  |
| Preferred contact time  | Help coordinate communication                      | Evening in Australia |
| Service interest        | Record a specific service if mentioned             | Hospital escort      |
| Consultation intent     | Identify whether the customer wants a consultation | Yes                  |
| Source                  | Track where the lead originated                    | Facebook ad          |
| Channel                 | Identify where the conversation is taking place    | WhatsApp             |

Not all this information needs to be collected in the first message. The agent should capture what is available and ask relevant follow-up questions only when appropriate.

Detailed medical information, payment details and other sensitive information should not be requested unnecessarily during initial lead capture.

## 3. Example Customer Journey

A possible customer journey is:

```
Customer discovers Saathi Sneha Care
↓
Customer sends an inquiry
↓
Lead Capture records available information
↓
Missing information is identified
↓
Further questions are asked where appropriate
↓
Lead Qualification applies approved criteria
↓
Sales Follow-up continues the conversation
↓
Scheduling Agent handles consultation booking, if requested
```

This is a conceptual target flow, not a confirmed description of the company's current internal process.


## 4. Sample Customer Messages

These are hypothetical examples for designing and testing the Lead Capture Agent.

### Message 1 — General Inquiry

**Customer message:**

"Hi, I live in Australia, and my mother is in Kathmandu. I want to know more about your home-care services."

**Information available:**

* Customer location: Australia
* Relationship: Daughter/son not specified
* Patient: Mother
* Patient location: Kathmandu
* Need: General home-care information
* Urgency: Unknown
* Contact details: Unknown

**Information missing:**

* Customer name
* Contact details
* Specific care requirements
* When care is needed

**Expected behavior:**

* Recognize a potential lead.
* Capture the information provided.
* Identify missing information.
* Continue with an appropriate question about the parent's care needs.

### Message 2 — Specific Care Requirement

**Customer message:**

"Hello, I am living in the UK. My father lives in Nepal and needs someone to help him with his daily activities. Can you provide a caregiver?"

**Information available:**

* Customer location: UK
* Patient: Father
* Patient location: Nepal (specific city unknown)
* Need: Caregiver support
* Urgency: Unknown
* Contact details: Unknown

**Information missing:**

* Customer name
* Contact details
* Father's exact location
* When caregiver support is needed
* Specific assistance required

**Expected behavior:**

* Capture the caregiver-support inquiry.
* Record the known information.
* Ask for relevant missing details.
* Avoid making a care recommendation before the required information and approved rules are available.

### Message 3 — Urgent Care Inquiry

**Customer message:**

"Hi, I am in Dubai. My mother has recently returned home from the hospital in Kathmandu, and I need someone to help her as soon as possible. Can your team contact me today?"

**Information available:**

* Customer location: Dubai
* Patient: Mother
* Patient location: Kathmandu
* Need: Post-hospital support
* Timing: As soon as possible
* Requested contact: Today

**Information missing:**

* Customer name
* Contact details
* Specific support required
* Exact care start date
* Preferred contact time

**Expected behavior:**

* Capture the request and urgency expressed by the customer.
* Flag the time-sensitive request for handling according to approved company procedures.
* Avoid giving medical advice or diagnosing the patient's condition.
* Escalate according to the company's confirmed urgent-care rules.

### Message 4 — Pricing Inquiry

**Customer message:**

"Hello, I live in the USA, and I want to arrange monthly care for my father in Nepal. Could you please tell me how much it costs?"

**Information available:**

* Customer location: USA
* Patient: Father
* Patient location: Nepal
* Need: Monthly care
* Intent: Pricing inquiry
* Specific plan: Unknown

**Information missing:**

* Customer name
* Contact details
* Father's city
* Required services
* Specific plan interest
* When care should begin

**Expected behavior:**

* Capture the pricing inquiry.
* Identify the missing service and location details.
* Use only approved, current pricing information if available.
* Avoid inventing prices or recommending an unverified plan.

### Message 5 — Consultation Request

**Customer message:**

"Hi, I am living in Canada, and my parents are in Kathmandu. I would like to schedule a consultation to understand what kind of care you can provide for them."

**Information available:**

* Customer location: Canada
* Patient: Parents
* Patient location: Kathmandu
* Need: Understanding available care options
* Consultation requested: Yes
* Urgency: Unknown

**Information missing:**

* Customer name
* Contact details
* Specific care requirements
* Preferred consultation time
* When care is needed

**Expected behavior:**

* Capture the consultation request.
* Record the information provided.
* Identify relevant missing details.
* Pass the consultation intent through the agreed workflow to Sales Follow-up and then the Scheduling Agent.

## 5. Lead Capture Principles

The Lead Capture Agent should:

1. Capture only information the customer has provided or that is available from verified channel metadata.
2. Keep unavailable information as `null` or `unknown`.
3. Distinguish the customer from the person receiving care.
4. Distinguish the message channel from the original lead source.
5. Record expressed urgency without inventing priority rules.
6. Identify missing information without asking every question at once.
7. Avoid making medical diagnoses, inventing prices or recommending plans without approved information.
8. Pass the captured lead to the next stage without independently qualifying it.

## 6. Open Questions

The following require confirmation from the senior or business team:

* Is the adult child abroad the primary customer segment?
* What are the most common countries from which customers contact the company?
* What information is mandatory at the initial contact stage?
* Should the agent ask about the customer's relationship to the patient?
* What information about the parent's care needs can be collected initially?
* What are the actual company rules for urgent requests?
* Which questions should be asked before a consultation?
* What privacy and consent requirements apply to collecting and storing patient information?

## 7. Completion Summary

**Completed in this document:**

* A working customer profile.
* Possible customer goals and situations.
* Important first-contact information.
* Five customer-specific hypothetical messages.
* Expected Lead Capture behavior.
* Boundaries and open questions.

**Remaining:** Validate the customer profile, mandatory fields and business rules with the senior or business team before treating them as confirmed requirements.
