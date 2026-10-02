
# Saathi Sneha Care FAQ Agent

## Objective
A small FAQ agent prototype using the six approved
Saathi Sneha Care FAQs.

## Implementations
- Pure Python: keyword-based matching and fixed answers.
- LangChain + LangGraph: LLM-assisted FAQ selection,
  LangGraph state handling, and approved fixed answers.

## Setup
1. Install Python.
2. Open the project folder in a terminal.
3. Install dependencies with:
   `python -m pip install -r requirements.txt`
4. For LangChain, configure the API key in `.env`.

## Run Pure Python
`python -m pure_python.faq_agent`

## Run LangChain + LangGraph
`python -m langchain_version.faq_agent`

## Run Pure Python tests
`python -m unittest discover -s tests -v`

## Safety
- Only answer from the supplied FAQ list.
- Use a fallback for unsupported questions.
- Do not invent prices, availability, or policies.
- Use approved answers as the final response text.

## Limitations
The Pure Python version relies on manually maintained
keywords. The LangChain version relies on an LLM to
select an FAQ and may misclassify questions. Both
versions require testing and review before production use.

## Future work
- Connect to the shared knowledge base.
- Add lead capture and consent handling.
- Integrate with the Marketing/Sales agent.
- Connect to the larger LangGraph orchestrator.
- Add channel adapters and conversation-level testing.