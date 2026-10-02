
import re
from data.faqs import FAQS, FALLBACK


def normalize(text: str) -> str:
    """Lowercase text and remove punctuation."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return " ".join(text.split())


def contains_phrase(text: str, phrase: str) -> bool:
    """Check for a whole phrase, not a partial word."""
    padded_text = f" {normalize(text)} "
    padded_phrase = f" {normalize(phrase)} "
    return padded_phrase in padded_text


def find_faq(question: str):
    """Find one clear FAQ match, or None."""
    scores = {}

    for faq in FAQS:
        score = 0

        # Match the official FAQ question too
        if contains_phrase(question, faq["question"]):
            score += 2

        # Score matching keywords
        for keyword in faq["keywords"]:
            if contains_phrase(question, keyword):
                score += 1

        scores[faq["id"]] = score

    highest = max(scores.values(), default=0)

    if highest == 0:
        return None

    winners = [
        faq_id for faq_id, score in scores.items()
        if score == highest
    ]

    # Avoid guessing if multiple FAQs score equally
    if len(winners) != 1:
        return None

    return winners[0]


def answer_question(question: str) -> dict:
    """Return a FAQ answer and its matched FAQ ID."""
    faq_id = find_faq(question)

    if faq_id is None:
        return {
            "faq_id": None,
            "answer": FALLBACK,
        }

    faq = next(item for item in FAQS if item["id"] == faq_id)

    return {
        "faq_id": faq_id,
        "answer": faq["answer"],
    }


def chat():
    print("Saathi Sneha Care FAQ Agent")
    print("Ask a question, or type 'exit' to quit.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() == "exit":
            print("Agent: Goodbye!")
            break

        if not question:
            continue

        result = answer_question(question)
        print(f"Agent: {result['answer']}\n")


if __name__ == "__main__":
    chat()