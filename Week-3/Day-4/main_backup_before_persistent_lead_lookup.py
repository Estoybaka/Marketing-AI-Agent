import uuid

from lead_graph import graph, DB_PATH
from lead_database import get_lead


def run_chat():
    """Run an interactive elder-care lead collection conversation."""

    thread_id = f"lead-{uuid.uuid4().hex[:12]}"
    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    print("\n" + "=" * 55)
    print("ELDER-CARE LEAD ASSISTANT")
    print("=" * 55)
    print("Tell me how we can help with your caregiving needs.")
    print("Commands: /quit to exit, /lead to view saved lead details.")
    print("-" * 55)

    while True:
        try:
            user_message = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nConversation ended.")
            break

        if not user_message:
            print("Agent: Please enter a message so I can help.")
            continue

        if user_message.lower() == "/quit":
            print("Agent: Thank you for contacting us. Goodbye!")
            break

        if user_message.lower() == "/lead":
            saved_lead = get_lead(thread_id, DB_PATH)

            if saved_lead is None:
                print("Agent: No lead information has been saved yet.")
            else:
                print("\n--- SAVED LEAD ---")
                print(f"Lead ID: {saved_lead['lead_id']}")
                print(f"Name: {saved_lead['name']}")
                print(f"Email: {saved_lead['email']}")
                print(f"Phone: {saved_lead['phone']}")
                print(f"Care need: {saved_lead['need']}")
                print(f"Urgency: {saved_lead['urgency']}")
                print(f"Source: {saved_lead['source']}")
                print(f"Status: {saved_lead['status']}")
                print(f"Complete: {saved_lead['lead_complete']}")
                print(f"Next field: {saved_lead['next_field']}")
            continue

        try:
            result = graph.invoke(
                {"user_message": user_message},
                config=config,
            )

            print(f"\nAgent: {result['response']}")

            if result.get("lead_complete"):
                print("\n[Lead collection complete]")
                print(f"Lead ID: {result.get('lead_id')}")
                print(f"Lead status: {result.get('status')}")
                print("Your information has been saved to the database.")

        except Exception as error:
            print("\nAgent: I couldn't process that message.")
            print(f"Technical details: {error}")
            print(
                "Your existing saved lead, if any, has not intentionally "
                "been deleted. You can try again or type /quit."
            )

    print(f"\nConversation ID: {thread_id}")
    print("Database:", DB_PATH)
    print("Thank you for testing the Elder-Care Lead Assistant.")


if __name__ == "__main__":
    run_chat()
