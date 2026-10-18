"""Route customer messages through the Week 1, Week 2, and Week 3 components."""

import sys
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
WEEK1_DIR = REPOSITORY_ROOT / "Week-1" / "Day-4"
FAQ_AGENT_DIR = REPOSITORY_ROOT / "Week-2" / "saathi_faq_agent"
PURE_PYTHON_DIR = FAQ_AGENT_DIR / "pure_python"
LEAD_AGENT_DIR = REPOSITORY_ROOT / "Week-3" / "Day-4"

# Add the existing project directories without removing any current paths.
for directory in (
    FAQ_AGENT_DIR,
    PURE_PYTHON_DIR,
    LEAD_AGENT_DIR,
    WEEK1_DIR,
):
    directory_string = str(directory)
    if directory_string not in sys.path:
        sys.path.insert(0, directory_string)

from faq_agent import answer_question
import lead_graph
from integration.router import classify_message
from integration.scheduling_contract import prepare_scheduling_request
from src.models import NormalizedMessage
from src.state.graph_state import GraphState
from src.workflow.lead_workflow import run_lead_workflow


def handle_message(
    message: str,
    thread_id: str,
    db_path: str | Path | None = None,
    requested_date: str | None = None,
    requested_time: str | None = None,
    customer_ready: bool | None = None,
) -> dict:
    """Route a message and optionally prepare a scheduling handoff."""
    if not isinstance(message, str) or not message.strip():
        raise ValueError("Message must not be empty.")

    if not isinstance(thread_id, str) or not thread_id.strip():
        raise ValueError("A non-empty thread_id is required.")

    route = classify_message(message)

    result = {
        "route": route,
        "faq": None,
        "lead": None,
        "validation": None,
        "scheduling_preparation": None,
    }

    if route in ("faq", "both"):
        result["faq"] = answer_question(message)

    if route in ("lead", "both"):
        normalized_message = NormalizedMessage(
            sender_id=thread_id,
            channel="web",
            text=message,
            timestamp=datetime.now(),
            attachments=[],
        )

        week1_result = run_lead_workflow(
            GraphState(message=normalized_message)
        )

        result["validation"] = {
            "errors": week1_result.errors,
            "lead": (
                week1_result.lead.model_dump()
                if week1_result.lead is not None
                else None
            ),
        }

        # Never pass an invalid Week 1 lead into the persistent Week 3 graph.
        if week1_result.errors or week1_result.lead is None:
            return result

        graph_input = {"user_message": message}
        graph_config = {"configurable": {"thread_id": thread_id}}

        if db_path is None:
            lead_result = lead_graph.graph.invoke(
                graph_input,
                config=graph_config,
            )
        else:
            with patch.object(lead_graph, "DB_PATH", Path(db_path)):
                lead_result = lead_graph.graph.invoke(
                    graph_input,
                    config=graph_config,
                )

        result["lead"] = lead_result

        # Only prepare a scheduling request when the caller explicitly
        # supplies at least one scheduling-related argument.
        scheduling_requested = any(
            value is not None
            for value in (
                requested_date,
                requested_time,
                customer_ready,
            )
        )

        if scheduling_requested:
            result["scheduling_preparation"] = (
                prepare_scheduling_request(
                    lead=lead_result,
                    requested_date=requested_date,
                    requested_time=requested_time,
                    customer_ready=customer_ready is True,
                )
            )

    return result
