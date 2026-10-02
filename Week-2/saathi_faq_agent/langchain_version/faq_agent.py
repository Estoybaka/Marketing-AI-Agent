import os
from typing import TypedDict, Optional
from google.genai.types import AutomaticFunctionCallingConfig

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END

from data.faqs import FAQS, FAQ_BY_ID, FAQ_CONTEXT


# Load environment variables from .env
load_dotenv()


# -------------------------------
# 1. Define the graph state
# -------------------------------

class FAQState(TypedDict):
    question: str
    faq_id: Optional[str]
    answer: str


# -------------------------------
# 2. Select the matching FAQ
# -------------------------------

def select_faq(question: str) -> Optional[str]:
    """
    Ask Gemini to select the most relevant FAQ ID.
    Returns None if no FAQ is relevant.
    """

    model_name = os.getenv(
        "GOOGLE_MODEL",
        "gemini-3.8-flash"
    )

    llm = ChatGoogleGenerativeAI(
        model=model_name,
        temperature=0,
        max_retries=2,
    )

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
You are a FAQ-matching assistant for Saathi Sneha Care.

Your task is to match the user's question to one of the
provided FAQs.

Available FAQs:
{faq_context}

Rules:
- Select an FAQ only if it clearly answers the user's question.
- The user's wording may be different from the FAQ wording.
- Do not make up new FAQ IDs.
- If none of the FAQs is relevant, return NOT_FOUND.
- Return only one FAQ ID, such as FAQ1, FAQ2, or NOT_FOUND.
- Do not explain your choice.
            """
        ),
        (
            "human",
            "{question}"
        ),
    ])

    llm_no_afc = llm.bind(
        automatic_function_calling=AutomaticFunctionCallingConfig(
         disable=True
        )
    )

    chain = prompt | llm_no_afc

    result = chain.invoke({
        "faq_context": FAQ_CONTEXT,
        "question": question,
    })

    # Extract text from the model response
    content = result.content

    if isinstance(content, str):
        candidate = content.strip()
    elif isinstance(content, list):
        candidate = " ".join(
            block.get("text", "")
            for block in content
            if isinstance(block, dict)
        ).strip()
    else:
        return None

    # Remove possible Markdown formatting
    candidate = candidate.replace("`", "").strip()

    # Accept only a known FAQ ID
    for faq_id in FAQ_BY_ID:
        if candidate.casefold() == faq_id.casefold():
            return faq_id

    return None


# -------------------------------
# 3. LangGraph node: FAQ selection
# -------------------------------

def faq_selection_node(state: FAQState) -> FAQState:
    """
    Select the FAQ that best matches the user's question.
    """

    question = state["question"]

    faq_id = select_faq(question)

    return {
        "question": question,
        "faq_id": faq_id,
        "answer": "",
    }


# -------------------------------
# 4. LangGraph node: answer
# -------------------------------

def answer_node(state: FAQState) -> FAQState:
    """
    Return the approved answer for the selected FAQ.
    The model does not generate the final answer.
    """

    faq_id = state["faq_id"]

    if faq_id is None:
        answer = (
            "I'm sorry, I couldn't find an exact answer to that "
            "question in our FAQs. Please contact the Saathi "
            "Sneha Care team for further assistance."
        )
    else:
        answer = FAQ_BY_ID[faq_id]["answer"]

    return {
        "question": state["question"],
        "faq_id": faq_id,
        "answer": answer,
    }


# -------------------------------
# 5. Build the LangGraph workflow
# -------------------------------

def build_faq_graph():
    """
    Build and compile the FAQ workflow.
    """

    graph = StateGraph(FAQState)

    graph.add_node(
        "faq_selection",
        faq_selection_node
    )

    graph.add_node(
        "answer",
        answer_node
    )

    graph.add_edge(
        START,
        "faq_selection"
    )

    graph.add_edge(
        "faq_selection",
        "answer"
    )

    graph.add_edge(
        "answer",
        END
    )

    return graph.compile()


# -------------------------------
# 6. Run the FAQ agent
# -------------------------------

faq_graph = build_faq_graph()


def ask_faq(question: str) -> str:
    """
    Send a question to the FAQ agent and return its answer.
    """

    question = question.strip()

    if not question:
        return "Please enter a question."

    try:
        result = faq_graph.invoke({
            "question": question,
            "faq_id": None,
            "answer": "",
        })

        return result["answer"]

    except Exception as error:
        print(f"Error while processing the question: {error}")

        return (
            "Sorry, I'm having trouble answering right now. "
            "Please try again in a moment."
        )


# -------------------------------
# 7. Terminal chat interface
# -------------------------------

if __name__ == "__main__":
    print("Saathi Sneha Care FAQ Agent")
    print("Type 'exit' to stop.\n")

    while True:
        user_question = input("You: ").strip()

        if user_question.casefold() in {"exit", "quit"}:
            print("FAQ Agent: Goodbye!")
            break

        answer = ask_faq(user_question)

        print(f"\nFAQ Agent: {answer}\n")
