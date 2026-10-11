import uuid

from lead_graph import graph, DB_PATH
from lead_database import get_lead, list_leads


def display_lead(saved_lead):
    """Display the details of one saved lead."""

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
    print("Tell us how we can help with your caregiving needs.")
    print("Commands:")
    print("  /lead       - View leads saved in the database")
    print("  /lead <ID>  - View one lead by its lead ID")
    print("  /quit       - Exit the assistant")
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

        command = user_message.lower()

        if command == "/quit":
            print("Agent: Thank you for contacting us. Goodbye!")
            break

        if command == "/lead" or command.startswith("/lead "):
            parts = user_message.split(maxsplit=1)

            # /lead <ID>: retrieve one specific saved lead.
            if len(parts) == 2:
                lead_id = parts[1].strip()
                all_leads = list_leads(DB_PATH)

                matching_lead = next(
                    (
                        lead for lead in all_leads
                        if str(lead["lead_id"]) == lead_id
                    ),
                    None,
                )

                if matching_lead is None:
                    print(f"Agent: No saved lead found with ID: {lead_id}")
                else:
                    display_lead(matching_lead)

                continue

            # /lead: preserve current-session lookup when possible.
            saved_lead = get_lead(thread_id, DB_PATH)

            if saved_lead is not None:
                display_lead(saved_lead)
                continue

            # If this is a new session, show leads from the database.
            saved_leads = list_leads(DB_PATH)

            if not saved_leads:
                print("Agent: No lead information has been saved yet.")
                continue

            print("\n--- SAVED LEADS ---")
            print(f"Total saved leads: {len(saved_leads)}")

            for lead in saved_leads:
                print("-" * 40)
                print(f"Lead ID: {lead['lead_id']}")
                print(f"Name: {lead['name']}")
                print(f"Email: {lead['email']}")
                print(f"Phone: {lead['phone']}")
                print(f"Care need: {lead['need']}")
                print(f"Status: {lead['status']}")
                print(f"Complete: {lead['lead_complete']}")

            print("\nTip: Enter /lead <ID> to view one lead's full details.")
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
