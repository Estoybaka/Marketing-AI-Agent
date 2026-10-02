FAQS = [
    {
        "id": "FAQ1",
        "question": "Can I pay from abroad?",
        "answer": (
            "Yes. You can pay using international credit or debit cards "
            "through Stripe. Our prices are listed in USD, and your card "
            "is charged the listed amount directly, so there is no need "
            "to guess exchange rates."
        ),
    },
    {
        "id": "FAQ2",
        "question": "Can my parents pay locally?",
        "answer": (
            "Yes. We accept Khalti and cash for local payments. "
            "Families in Nepal can also pay monthly through the "
            "patient portal."
        ),
    },
    {
        "id": "FAQ3",
        "question": "Is there a setup or joining fee?",
        "answer": (
            "No, there are no hidden setup or joining fees. "
            "Your monthly plan price covers the included services. "
            "Any add-on services are billed separately and quoted "
            "to you in advance."
        ),
    },
    {
        "id": "FAQ4",
        "question": "Can I change or cancel the plan?",
        "answer": (
            "Yes. You can upgrade, downgrade, or cancel your plan "
            "at any time. Changes take effect from the next billing "
            "cycle, and there are no cancellation penalties."
        ),
    },
    {
        "id": "FAQ5",
        "question": "What if my parents need more visits?",
        "answer": (
            "Additional visits outside your plan can be booked "
            "individually. Your care coordinator can advise you "
            "on the most cost-effective option."
        ),
    },
    {
        "id": "FAQ6",
        "question": "Do you serve outside Kathmandu?",
        "answer": (
            "Our full service is currently available in Kathmandu "
            "Valley. We are expanding to Pokhara and Biratnagar. "
            "Please contact us to check availability in your area."
        ),
    },
]


FAQ_BY_ID = {
    faq["id"]: faq
    for faq in FAQS
}


FAQ_CONTEXT = "\n".join(
    f'{faq["id"]}: {faq["question"]}'
    for faq in FAQS
)

