import re


FAQ_CUES = (
    "pay",
    "payment",
    "price",
    "pricing",
    "fee",
    "fees",
    "cancel",
    "cancellation",
    "upgrade",
    "downgrade",
    "extra visits",
    "more visits",
    "service area",
    "available",
    "ambulance",
    "how much",
    "how much does it cost",
    "how much does care cost",
    "what does it cost",
    "cost of care",
)

LEAD_CUES = (
    "my name is",
    "i am ",
    "i'm ",
    "my email",
    "my phone",
    "my number",
    "i need care",
    "need care for",
    "looking for care",
    "interested in care",
    "care for my",
    "help my mother",
    "help my father",
    "help my parent",
    "i need help for my mother",
    "i need help for my father",
    "i need help for my parent",
    "can you help my mother",
    "can you help my father",
    "can you help my elderly mother",
    "can you help my elderly father",
    "arrange support for my",
    "support for my father",
    "support for my mother",
     "my mother needs",
    "my father needs",
    "my parent needs",
    "mom needs help",
    "dad needs help",
    "needs daily support",
    "needs help at home",
    "needs help with daily activities",
    "needs someone to help",
    "help with daily activities",
    "i need some help for my mom",
    "i need help for my mom",
    "help for my mom",
    "help for my dad",
    "care for my mom",
    "care for my dad",
    "help for my elderly parent",
    "i want to book a service",
    "want to book a service",
    "book a service",
    "i want to book",
    "arrange a service",
    "call me",
    "my phone number is",
    "my number is",
    "phone number:",
    "contact me at",
    "guarantee a caregiver",
    "caregiver will arrive",
    "caregiver tomorrow",
    "arrive tomorrow",
    "available tomorrow",
    "correction:",
    "instead of",
    "also needs",
    "also need",
)


def classify_message(message: str) -> str:
    """Classify a message as FAQ, lead capture, or both."""
    if not isinstance(message, str) or not message.strip():
        return "faq"

    normalized = re.sub(r"\s+", " ", message.casefold()).strip()

    has_faq_intent = any(cue in normalized for cue in FAQ_CUES)
    has_lead_intent = any(cue in normalized for cue in LEAD_CUES)

    if has_faq_intent and has_lead_intent:
        return "both"
    if has_lead_intent:
        return "lead"
    return "faq"
