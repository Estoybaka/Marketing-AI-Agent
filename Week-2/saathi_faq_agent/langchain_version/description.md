# Saathi Sneha Care FAQ Agent — Detailed Code Explanation

## 1. What this program does

This program is an **AI-powered FAQ agent** for Saathi Sneha Care.

Instead of manually matching keywords, it uses **Google Gemini** to understand the user's question and choose the most relevant FAQ from a predefined list.

The important design choice is:

> Gemini selects the FAQ, but Python provides the final approved answer.

This means the AI is used for **understanding and matching**, while the final response comes directly from trusted FAQ data.

### Simple flow

```text
User question
      ↓
Gemini understands the question
      ↓
Selects an FAQ ID
      ↓
Python validates the FAQ ID
      ↓
Python retrieves the approved FAQ answer
      ↓
Final answer
```

The application uses:

* Python
* Google Gemini
* LangChain
* LangGraph
* TypedDict
* `.env` environment variables
* A predefined FAQ dataset

---

# 2. Imported libraries

```python
import os
from typing import TypedDict, Optional
from google.genai.types import AutomaticFunctionCallingConfig

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END

from data.faqs import FAQS, FAQ_BY_ID, FAQ_CONTEXT
```

Let's understand each import.

## `import os`

Python's `os` module allows the program to interact with environment variables and the operating system.

Here it is used to read the Gemini model name:

```python
os.getenv("GOOGLE_MODEL", "gemini-3.8-flash")
```

This means:

> Look for an environment variable called `GOOGLE_MODEL`. If it does not exist, use `gemini-3.8-flash`.

---

## `TypedDict`

```python
from typing import TypedDict
```

`TypedDict` lets us define the expected structure of a dictionary.

Our graph state contains:

```text
question
faq_id
answer
```

This makes the structure easier to understand and helps with type checking.

---

## `Optional`

```python
from typing import Optional
```

`Optional[str]` means:

> This value can contain a string OR `None`.

For example:

```python
faq_id: Optional[str]
```

Before an FAQ is selected:

```python
None
```

After a match is found:

```python
"FAQ3"
```

---

# 3. Automatic function calling configuration

```python
from google.genai.types import AutomaticFunctionCallingConfig
```

This is used later to disable automatic function calling:

```python
AutomaticFunctionCallingConfig(
    disable=True
)
```

In this application, Gemini only needs to return an FAQ ID.

We don't want the model to automatically call tools or functions.

---

# 4. Loading environment variables

```python
from dotenv import load_dotenv
```

Then:

```python
load_dotenv()
```

This loads variables from a `.env` file into the environment.

A `.env` file might contain something like:

```text
GOOGLE_API_KEY=your_api_key_here
GOOGLE_MODEL=gemini-3.8-flash
```

The exact variables depend on how the project is configured.

## Why use `.env`?

It keeps configuration and sensitive credentials outside the Python source code.

Instead of writing an API key directly into:

```python
api_key = "..."
```

the application can load it from the environment.

---

# 5. LangChain imports

## `ChatGoogleGenerativeAI`

```python
from langchain_google_genai import ChatGoogleGenerativeAI
```

This gives LangChain a way to communicate with Google's Gemini models.

The code later creates:

```python
llm = ChatGoogleGenerativeAI(...)
```

`llm` means **Large Language Model**.

---

## `ChatPromptTemplate`

```python
from langchain_core.prompts import ChatPromptTemplate
```

This helps construct a structured prompt for Gemini.

Instead of manually creating one large string, the prompt is divided into:

* system instructions
* human/user question

---

# 6. LangGraph imports

```python
from langgraph.graph import StateGraph, START, END
```

These are used to build the workflow.

### `StateGraph`

Creates a graph where different functions/nodes process shared state.

### `START`

Represents the beginning of the workflow.

### `END`

Represents the end of the workflow.

Our graph is:

```text
START
  ↓
faq_selection
  ↓
answer
  ↓
END
```

---

# 7. FAQ data

```python
from data.faqs import FAQS, FAQ_BY_ID, FAQ_CONTEXT
```

These values come from another file:

```text
data/faqs.py
```

The exact structure depends on the project, but their purposes are roughly:

### `FAQS`

The complete FAQ collection.

### `FAQ_BY_ID`

A dictionary that allows quick lookup using an FAQ ID.

For example:

```python
FAQ_BY_ID["FAQ1"]
```

could return:

```text
{
    "question": "...",
    "answer": "..."
}
```

### `FAQ_CONTEXT`

A formatted version of the FAQ information that is provided to Gemini.

This gives Gemini enough information to decide which FAQ matches the user's question.

---

# 8. Defining the graph state

```python
class FAQState(TypedDict):
    question: str
    faq_id: Optional[str]
    answer: str
```

This is one of the most important parts of the program.

The LangGraph workflow needs a shared piece of information called **state**.

The state contains three values.

---

## `question`

```python
question: str
```

This stores the user's question.

Example:

```text
"Can I pay with Khalti?"
```

---

## `faq_id`

```python
faq_id: Optional[str]
```

This stores the FAQ selected by Gemini.

Example:

```text
FAQ2
```

Before selection:

```python
None
```

If there is no suitable FAQ:

```python
None
```

---

## `answer`

```python
answer: str
```

This stores the final answer that will be returned to the user.

---

# 9. The `select_faq()` function

```python
def select_faq(question: str) -> Optional[str]:
```

This function's job is:

> Ask Gemini which FAQ best matches the user's question.

It returns either:

```text
FAQ1
FAQ2
FAQ3
...
```

or:

```python
None
```

if no FAQ is relevant.

---

# 10. Selecting the Gemini model

```python
model_name = os.getenv(
    "GOOGLE_MODEL",
    "gemini-3.8-flash"
)
```

The program first checks whether `GOOGLE_MODEL` exists in the environment.

If it exists:

```text
GOOGLE_MODEL=some-model
```

that model will be used.

If it does not exist, the fallback model name is:

```text
gemini-3.8-flash
```

So conceptually:

```text
Environment variable exists?
        ↓
     Yes → use it
        ↓
      No → use default
```

---

# 11. Creating the Gemini model

```python
llm = ChatGoogleGenerativeAI(
    model=model_name,
    temperature=0,
    max_retries=2,
)
```

Three important settings are used.

## `model`

```python
model=model_name
```

Specifies which Gemini model should process the request.

---

## `temperature=0`

Temperature controls how random or creative the model's output can be.

For FAQ matching, creativity is not desirable.

We want the model to consistently choose the best FAQ.

Therefore:

```python
temperature=0
```

is appropriate.

The goal is:

```text
Consistent matching
```

rather than:

```text
Creative writing
```

---

## `max_retries=2`

```python
max_retries=2
```

If a temporary problem occurs while communicating with the model, LangChain can retry the request.

This provides some resilience against temporary failures.

---

# 12. Creating the prompt

```python
prompt = ChatPromptTemplate.from_messages([
```

The prompt contains two messages.

---

## System message

```python
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
)
```

This tells Gemini exactly what role it should perform.

The model is not being asked to answer the user's question directly.

It is being asked to **select an FAQ**.

---

# 13. The `{faq_context}` placeholder

Inside the system prompt we have:

```text
{faq_context}
```

This is a placeholder.

Later, when the chain is executed, it is replaced with:

```python
FAQ_CONTEXT
```

So Gemini receives the available FAQ information.

Conceptually:

```text
System prompt
      +
FAQ context
      +
User question
      ↓
Gemini
```

---

# 14. Matching different wording

One important instruction says:

```text
The user's wording may be different from the FAQ wording.
```

This is important because users rarely ask questions using exactly the same words as the FAQ.

For example, the FAQ might say:

```text
"Can I pay with Khalti?"
```

The user might ask:

```text
"Can my parents pay locally?"
```

A keyword-only system may struggle with this.

Gemini can understand that the two questions may have the same meaning.

---

# 15. Preventing made-up FAQ IDs

The prompt says:

```text
Do not make up new FAQ IDs.
```

This is important.

Suppose the available FAQs are:

```text
FAQ1
FAQ2
FAQ3
```

The model should never invent:

```text
FAQ99
```

or:

```text
FAQ_SUPPORT
```

It must choose from the provided IDs or return:

```text
NOT_FOUND
```

---

# 16. The `NOT_FOUND` instruction

The prompt tells Gemini:

```text
If none of the FAQs is relevant, return NOT_FOUND.
```

For example, if the user asks something completely unrelated:

```text
"What is the weather today?"
```

and there is no weather FAQ, Gemini should return:

```text
NOT_FOUND
```

The application then uses its fallback response.

---

# 17. Human message

The second message is:

```python
(
    "human",
    "{question}"
)
```

This represents the actual question asked by the user.

For example:

```text
"Can I pay with Khalti?"
```

So the final prompt effectively contains:

```text
SYSTEM:
You are a FAQ-matching assistant...
Available FAQs:
...

USER:
Can I pay with Khalti?
```

---

# 18. Disabling automatic function calling

```python
llm_no_afc = llm.bind(
    automatic_function_calling=AutomaticFunctionCallingConfig(
        disable=True
    )
)
```

This creates a version of the model with automatic function calling disabled.

In this project, Gemini only needs to return text such as:

```text
FAQ3
```

We do not need Gemini to automatically execute functions.

This keeps the workflow simple and controlled.

---

# 19. Creating the chain

```python
chain = prompt | llm_no_afc
```

This is LangChain's pipe syntax.

It means:

```text
Prompt
  ↓
Gemini model
```

The output of the prompt goes into the model.

So:

```python
chain
```

represents the complete operation:

```text
build prompt → send it to Gemini → receive response
```

---

# 20. Calling Gemini

```python
result = chain.invoke({
    "faq_context": FAQ_CONTEXT,
    "question": question,
})
```

The program sends two values into the prompt.

### `faq_context`

```python
"faq_context": FAQ_CONTEXT
```

This provides the FAQ information.

### `question`

```python
"question": question
```

This provides the user's actual question.

Gemini then returns its result.

For example:

```text
FAQ4
```

---

# 21. Extracting Gemini's response

```python
content = result.content
```

The response from LangChain is stored in `result`.

The actual generated content is accessed through:

```python
result.content
```

---

# 22. Handling a string response

```python
if isinstance(content, str):
    candidate = content.strip()
```

If Gemini returns normal text, the program stores it in:

```python
candidate
```

`.strip()` removes unnecessary whitespace.

For example:

```text
"  FAQ3  "
```

becomes:

```text
"FAQ3"
```

---

# 23. Handling a list response

The code also supports responses where the content is represented as a list:

```python
elif isinstance(content, list):
    candidate = " ".join(
        block.get("text", "")
        for block in content
        if isinstance(block, dict)
    ).strip()
```

This extracts text from dictionary blocks.

For example, if the response contains multiple content blocks, the code combines their text.

This makes the response-processing code more robust.

---

# 24. Handling an unexpected response

```python
else:
    return None
```

If the response is neither a string nor a supported list structure, the function returns:

```python
None
```

That means:

> We could not safely identify an FAQ.

---

# 25. Removing Markdown backticks

```python
candidate = candidate.replace("`", "").strip()
```

Sometimes an AI model might return:

```text
`FAQ3`
```

instead of:

```text
FAQ3
```

The code removes the backticks.

After that:

```text
`FAQ3`
```

becomes:

```text
FAQ3
```

---

# 26. Validating the FAQ ID

This is one of the most important safety steps.

```python
for faq_id in FAQ_BY_ID:
    if candidate.casefold() == faq_id.casefold():
        return faq_id

return None
```

The program does not blindly trust Gemini.

It checks whether Gemini's response actually exists in:

```python
FAQ_BY_ID
```

Suppose the valid IDs are:

```text
FAQ1
FAQ2
FAQ3
FAQ4
```

If Gemini returns:

```text
FAQ3
```

the program accepts it.

If Gemini returns:

```text
FAQ999
```

the program rejects it.

---

# 27. Why use `casefold()`?

```python
candidate.casefold()
```

and:

```python
faq_id.casefold()
```

allow case-insensitive comparison.

So these can be treated as equivalent:

```text
FAQ3
faq3
Faq3
```

This prevents a harmless capitalization difference from causing a failed match.

---

# 28. Why validation is important

Without validation, the model could theoretically return something unexpected.

For example:

```text
FAQ999
```

The program should never use that as a key unless it actually exists.

The validation step creates a boundary:

```text
Gemini
  ↓
Suggested FAQ ID
  ↓
Python validation
  ↓
Only valid FAQ ID continues
```

This is a strong design choice.

---

# 29. `faq_selection_node()`

```python
def faq_selection_node(state: FAQState) -> FAQState:
```

This is a **LangGraph node**.

Its job is to take the current graph state and select an FAQ.

First:

```python
question = state["question"]
```

It gets the user's question from the state.

Then:

```python
faq_id = select_faq(question)
```

It calls the Gemini-based FAQ selection function.

Finally, it returns the updated state:

```python
return {
    "question": question,
    "faq_id": faq_id,
    "answer": "",
}
```

At this point, the state might look like:

```python
{
    "question": "Can I pay with Khalti?",
    "faq_id": "FAQ2",
    "answer": ""
}
```

---

# 30. `answer_node()`

```python
def answer_node(state: FAQState) -> FAQState:
```

This is the second LangGraph node.

Its job is to provide the final answer.

The important design decision is that this node does **not** ask Gemini to write the answer.

Instead:

```python
faq_id = state["faq_id"]
```

gets the selected FAQ.

---

# 31. If no FAQ was found

```python
if faq_id is None:
```

If Gemini could not identify a valid FAQ, the program uses a predefined fallback:

```python
answer = (
    "I'm sorry, I couldn't find an exact answer to that "
    "question in our FAQs. Please contact the Saathi "
    "Sneha Care team for further assistance."
)
```

This prevents the model from inventing an answer.

---

# 32. If an FAQ was found

Otherwise:

```python
answer = FAQ_BY_ID[faq_id]["answer"]
```

This is extremely important.

The final answer comes directly from:

```python
FAQ_BY_ID
```

rather than from Gemini.

For example:

```text
Gemini selects FAQ3
        ↓
Python looks up FAQ3
        ↓
Python retrieves FAQ3's approved answer
```

---

# 33. Why the model does not generate the final answer

This architecture is safer for an FAQ system.

Imagine the FAQ contains an approved answer:

```text
Our organization provides...
```

Instead of asking Gemini to rewrite it, the program retrieves the exact stored answer.

This reduces the risk of:

* hallucination
* changing important information
* inventing services
* giving unsupported claims
* accidentally changing approved wording

So the AI is responsible for:

```text
Understanding the question
```

while the application is responsible for:

```text
Providing the trusted answer
```

---

# 34. Returning the final state

```python
return {
    "question": state["question"],
    "faq_id": faq_id,
    "answer": answer,
}
```

After this node, the state might look like:

```python
{
    "question": "Can I pay with Khalti?",
    "faq_id": "FAQ2",
    "answer": "..."
}
```

The graph can now finish.

---

# 35. Building the LangGraph workflow

```python
def build_faq_graph():
```

This function creates the complete workflow.

## Creating the graph

```python
graph = StateGraph(FAQState)
```

This says:

> Create a graph whose shared state follows the `FAQState` structure.

---

# 36. Adding the first node

```python
graph.add_node(
    "faq_selection",
    faq_selection_node
)
```

This creates a node named:

```text
faq_selection
```

and connects it to:

```python
faq_selection_node
```

---

# 37. Adding the second node

```python
graph.add_node(
    "answer",
    answer_node
)
```

This creates the second node:

```text
answer
```

which runs:

```python
answer_node
```

---

# 38. Connecting START to FAQ selection

```python
graph.add_edge(
    START,
    "faq_selection"
)
```

This means:

```text
START → faq_selection
```

When the workflow begins, the FAQ-selection node runs first.

---

# 39. Connecting FAQ selection to answer

```python
graph.add_edge(
    "faq_selection",
    "answer"
)
```

This means:

```text
faq_selection → answer
```

After Gemini selects the FAQ, the answer node runs.

---

# 40. Connecting answer to END

```python
graph.add_edge(
    "answer",
    END
)
```

This means:

```text
answer → END
```

After the final answer is created, the workflow finishes.

---

# 41. Complete LangGraph structure

```text
       START
         |
         v
 +----------------+
 | faq_selection  |
 |                |
 | Ask Gemini     |
 | to choose FAQ  |
 +----------------+
         |
         v
 +----------------+
 |     answer     |
 |                |
 | Get approved   |
 | answer from    |
 | FAQ_BY_ID      |
 +----------------+
         |
         v
        END
```

This is the main purpose of LangGraph in this application.

---

# 42. Compiling the graph

```python
return graph.compile()
```

Before the graph can be executed, it is compiled.

The compiled graph represents the executable workflow.

---

# 43. Creating the FAQ graph

```python
faq_graph = build_faq_graph()
```

This runs the graph-building function once.

Now:

```python
faq_graph
```

contains the compiled workflow.

---

# 44. `ask_faq()` function

```python
def ask_faq(question: str) -> str:
```

This is the main function that the rest of the application can use.

You give it a question:

```python
ask_faq("Can I pay with Khalti?")
```

and it returns the final answer.

---

# 45. Cleaning the question

```python
question = question.strip()
```

This removes unnecessary spaces before and after the user's question.

For example:

```text
"   Can I pay with Khalti?   "
```

becomes:

```text
"Can I pay with Khalti?"
```

---

# 46. Empty question handling

```python
if not question:
    return "Please enter a question."
```

If the user submits an empty input, the program doesn't call Gemini.

Instead, it immediately responds:

```text
Please enter a question.
```

This is both simpler and more efficient.

---

# 47. Running the graph

```python
result = faq_graph.invoke({
    "question": question,
    "faq_id": None,
    "answer": "",
})
```

This starts the LangGraph workflow.

The initial state is:

```python
{
    "question": question,
    "faq_id": None,
    "answer": ""
}
```

Then LangGraph processes the nodes.

---

# 48. What happens inside `invoke()`

For a question such as:

```text
"Can I pay with Khalti?"
```

the workflow becomes:

```text
Initial state
    ↓
faq_selection_node
    ↓
select_faq()
    ↓
Gemini
    ↓
FAQ2
    ↓
answer_node
    ↓
FAQ_BY_ID["FAQ2"]["answer"]
    ↓
Final state
```

Then:

```python
return result["answer"]
```

returns only the final answer.

---

# 49. Error handling

The graph execution is inside:

```python
try:
    ...
except Exception as error:
```

This means the application is prepared for unexpected errors.

For example:

* API failure
* network problem
* configuration issue
* unexpected response format
* graph execution error

If something goes wrong, the program prints the error:

```python
print(f"Error while processing the question: {error}")
```

Then it returns a user-friendly message:

```text
Sorry, I'm having trouble answering right now. Please try again in a moment.
```

---

# 50. Why not show the technical error to the user?

A technical error could look confusing:

```text
AuthenticationError: ...
```

A normal user doesn't need to see that.

Instead, the application gives a simple message.

The technical error is printed for the developer to inspect.

---

# 51. Terminal chat interface

The final section is:

```python
if __name__ == "__main__":
```

This means:

> Run this section when this Python file is executed directly.

---

# 52. Starting the chatbot

```python
print("Saathi Sneha Care FAQ Agent")
print("Type 'exit' to stop.\n")
```

The terminal displays:

```text
Saathi Sneha Care FAQ Agent
Type 'exit' to stop.
```

---

# 53. Getting user input

```python
user_question = input("You: ").strip()
```

The program waits for the user to type a question.

For example:

```text
You: Can I pay with Khalti?
```

---

# 54. Exit command

```python
if user_question.casefold() in {"exit", "quit"}:
```

The user can type:

```text
exit
```

or:

```text
quit
```

The use of `casefold()` means variations such as:

```text
EXIT
Exit
exit
```

are also recognized.

---

# 55. Ending the program

```python
print("FAQ Agent: Goodbye!")
break
```

`break` exits the `while True` loop.

The application then stops.

---

# 56. Asking the FAQ agent

If the user did not type `exit` or `quit`:

```python
answer = ask_faq(user_question)
```

The question is sent through the entire workflow.

Then:

```python
print(f"\nFAQ Agent: {answer}\n")
```

prints the final answer.

---

# 57. Complete example

Suppose the user enters:

```text
You: Can I pay with Khalti?
```

The program performs:

### Step 1 — Receive question

```text
Can I pay with Khalti?
```

### Step 2 — Put it into graph state

```python
{
    "question": "Can I pay with Khalti?",
    "faq_id": None,
    "answer": ""
}
```

### Step 3 — FAQ selection node runs

```python
select_faq(question)
```

### Step 4 — Gemini receives

```text
Available FAQs:
...

User:
Can I pay with Khalti?
```

### Step 5 — Gemini returns

```text
FAQ2
```

### Step 6 — Python validates it

Python checks whether `FAQ2` exists.

If it exists, it is accepted.

### Step 7 — Answer node runs

```python
FAQ_BY_ID["FAQ2"]["answer"]
```

### Step 8 — Approved answer is returned

The terminal displays:

```text
FAQ Agent: [approved FAQ answer]
```

---

# 58. What happens when there is no matching FAQ?

Suppose the user asks:

```text
What is the capital of France?
```

and none of the FAQs covers that topic.

Gemini should return:

```text
NOT_FOUND
```

The Python validation does not find a valid FAQ ID.

Therefore:

```python
faq_id = None
```

The answer node uses the fallback:

```text
I'm sorry, I couldn't find an exact answer to that question in our FAQs. Please contact the Saathi Sneha Care team for further assistance.
```

This prevents the chatbot from inventing an answer.

---

# 59. Why this is more advanced than the previous keyword chatbot

A basic keyword-based FAQ system might work like:

```text
User question
     ↓
Search for keywords
     ↓
Score matching FAQs
     ↓
Choose highest score
     ↓
Return answer
```

This new system works like:

```text
User question
     ↓
Gemini understands meaning
     ↓
Select FAQ
     ↓
Validate FAQ ID
     ↓
Retrieve approved answer
```

The second system can understand different ways of asking the same thing.

---

# 60. Keyword matching vs AI matching

Imagine the FAQ is:

```text
How can I contact Saathi Sneha Care?
```

The user asks:

```text
How do I get in touch with you?
```

A keyword system may not find many matching words.

Gemini can understand that:

```text
get in touch
```

and:

```text
contact
```

can have the same meaning.

This is one of the main benefits of using an LLM.

---

# 61. Important architecture decision

The most important architectural idea is:

```text
LLM = FAQ selection
Python = trusted answer retrieval
```

Not:

```text
LLM = generate everything
```

This makes the application more controlled.

The model is given a narrow task:

> Which existing FAQ answers this question?

It is not asked:

> What should I tell the user?

---

# 62. Why this can reduce hallucinations

An LLM can sometimes generate information that was not provided to it.

That is commonly called a **hallucination**.

This application reduces that risk because the final answer is retrieved from:

```python
FAQ_BY_ID
```

For example:

```python
answer = FAQ_BY_ID[faq_id]["answer"]
```

The model does not rewrite the answer.

---

# 63. Why output validation matters

The model is still an AI system, so its output should not automatically be trusted as an application identifier.

The code therefore checks:

```python
for faq_id in FAQ_BY_ID:
```

Only a real FAQ ID can continue.

This is an important general software engineering principle:

> Validate model output before using it in application logic.

---

# 64. Why LangGraph is used

For this simple application, LangGraph might initially look like extra complexity.

But it gives the application a clear workflow.

The workflow is:

```text
START
 ↓
Select FAQ
 ↓
Return approved answer
 ↓
END
```

As the application grows, more nodes could be added.

For example:

```text
START
 ↓
Detect language
 ↓
Select FAQ
 ↓
Check confidence
 ↓
Retrieve answer
 ↓
Log interaction
 ↓
END
```

LangGraph is useful when an AI application has multiple processing steps.

---

# 65. Possible future expansion

The current graph is simple:

```text
START
  ↓
FAQ selection
  ↓
Answer
  ↓
END
```

A future version could include:

```text
START
   ↓
Question validation
   ↓
Language detection
   ↓
FAQ selection
   ↓
Confidence checking
   ↓
Approved answer retrieval
   ↓
Conversation logging
   ↓
END
```

This is where graph-based architecture becomes more valuable.

---

# 66. Project structure

A possible project structure is:

```text
project/
│
├── .env
├── main.py
│
└── data/
    └── faqs.py
```

The exact structure may differ depending on the project.

The important relationship is:

```text
main.py
   ↓
data/faqs.py
```

The main program imports the FAQ data from the data module.

---

# 67. Role of each major component

| Component              | Purpose                                            |
| ---------------------- | -------------------------------------------------- |
| `.env`                 | Stores configuration/environment variables         |
| `FAQS`                 | Stores FAQ information                             |
| `FAQ_BY_ID`            | Allows FAQ lookup by ID                            |
| `FAQ_CONTEXT`          | Provides FAQ information to Gemini                 |
| Gemini                 | Understands the user's question and selects an FAQ |
| LangChain              | Connects prompts and the Gemini model              |
| LangGraph              | Controls the processing workflow                   |
| `FAQState`             | Stores information moving through the graph        |
| `select_faq()`         | Uses Gemini to select an FAQ                       |
| `faq_selection_node()` | LangGraph node for FAQ selection                   |
| `answer_node()`        | Retrieves the approved answer                      |
| `ask_faq()`            | Main function used to ask questions                |
| Terminal loop          | Provides a simple chat interface                   |

---

# 68. Important concepts to remember

## LLM

**Large Language Model**

In this project, Gemini is the LLM.

Its job is to understand the user's natural-language question.

---

## Prompt

Instructions and information sent to the model.

Here the prompt tells Gemini:

```text
You are a FAQ-matching assistant...
```

and provides the FAQ context.

---

## Chain

A sequence connecting processing steps.

Here:

```python
chain = prompt | llm_no_afc
```

means:

```text
Prompt → Gemini
```

---

## Node

A function that performs one step in a LangGraph workflow.

There are two nodes:

```text
faq_selection
answer
```

---

## State

Information shared between nodes.

Here:

```python
question
faq_id
answer
```

---

## Graph

The complete workflow connecting nodes.

Here:

```text
START → faq_selection → answer → END
```

---

## Fallback

The response used when the system cannot find a suitable FAQ.

---

# 69. Simple mental model

If you find LangChain and LangGraph confusing, think about the program this way:

### Gemini is the brain for understanding.

```text
"What is the user asking?"
```

### FAQ data is the knowledge base.

```text
"What approved information do we have?"
```

### Python is the controller.

```text
"Is Gemini's selected FAQ actually valid?"
```

### LangGraph is the workflow manager.

```text
"What step should happen first, second, and last?"
```

So:

```text
User
 ↓
Gemini understands
 ↓
Python validates
 ↓
FAQ data provides answer
 ↓
User receives answer
```

---

# 70. Why the architecture is useful for a healthcare/care-related FAQ system

For a care-related organization, it can be useful to keep the final FAQ answers controlled.

The model can help understand natural language without being allowed to freely invent organizational information.

For example:

```text
User:
"Can my parents pay locally?"

        ↓

Gemini:
FAQ2

        ↓

Python:
Is FAQ4 valid?

        ↓

Yes

        ↓

FAQ_BY_ID["FAQ4"]["answer"]

        ↓

Approved response
```

This separation between **understanding** and **answer generation** is a valuable design pattern.

---

# 71. Comparison with the previous program

The previous FAQ chatbot was mostly rule-based.

It used things such as:

```python
normalize()
contains_phrase()
```

and keyword scoring.

The new system uses:

```text
Gemini + LangChain + LangGraph
```

### Previous approach

```text
Keywords
   ↓
Score
   ↓
FAQ
```

### New approach

```text
Natural language
   ↓
Gemini semantic understanding
   ↓
FAQ ID
   ↓
Validated lookup
   ↓
Approved answer
```

The new approach is more flexible for natural-language questions, but it also introduces dependencies such as an LLM API, network access, model availability, and API cost/limits.

---

# 72. Main strengths

The system has several good design decisions:

1. **Natural-language understanding**

   * Users don't need to use exact FAQ wording.

2. **Controlled answers**

   * Final answers come from predefined FAQ data.

3. **Output validation**

   * Gemini cannot directly choose an arbitrary database key.

4. **Clear workflow**

   * LangGraph separates FAQ selection and answer retrieval.

5. **Fallback handling**

   * Unknown questions receive a controlled response.

6. **Error handling**

   * Unexpected runtime problems are caught.

7. **Configurable model**

   * The model can be changed through an environment variable.

---

# 73. Limitations

The application also has some limitations.

### 1. It depends on Gemini

If the API is unavailable, FAQ selection may fail.

### 2. It requires an API key/configuration

The Google Gemini service must be configured correctly.

### 3. It may cost money or be subject to API limits

Depending on the API/account configuration, requests may have usage limits or costs.

### 4. FAQ quality matters

If the FAQ data is incomplete or poorly written, the agent cannot provide information that does not exist in the knowledge base.

### 5. Model selection can still be imperfect

Gemini may occasionally select the wrong FAQ, especially if two FAQs are very similar.

### 6. No conversation memory

The current program treats each question independently.

It does not remember previous questions or answers.

---

# 74. One important improvement to consider

A future version could include a confidence or verification step.

For example:

```text
User question
      ↓
Gemini selects FAQ
      ↓
Check confidence/relevance
      ↓
Is match strong enough?
   ↙           ↘
 Yes            No
 ↓               ↓
Answer         Fallback
```

This could make the system more conservative when two FAQs are similar.

---

# 75. Another possible improvement

The application could log:

```text
User question
Selected FAQ
Timestamp
Result
```

This could help developers understand:

* which FAQs are frequently used
* which questions have no answer
* where new FAQs are needed
* where Gemini frequently makes mistakes

---

# 76. Final architecture diagram

```text
                    ┌──────────────────────┐
                    │        USER          │
                    │                      │
                    │ "What services do    │
                    │  you provide?"       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      LangGraph       │
                    │       START          │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   FAQ SELECTION      │
                    │                      │
                    │    LangChain         │
                    │         +            │
                    │       Gemini         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    FAQ ID            │
                    │                      │
                    │       FAQ2           │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Python Validation  │
                    │                      │
                    │ Is FAQ2 valid?       │
                    └──────────┬───────────┘
                               │
                         Yes   │
                               ▼
                    ┌──────────────────────┐
                    │    ANSWER NODE       │
                    │                      │
                    │ FAQ_BY_ID["FAQ2"]    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   APPROVED ANSWER    │
                    │                      │
                    │ Stored FAQ response  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │         END          │
                    └──────────────────────┘
```

---

# 77. Final one-sentence explanation

This application uses **Gemini to understand which predefined FAQ best matches a user's question, uses LangGraph to manage the selection-and-answer workflow, validates the selected FAQ ID, and returns the approved answer stored in the FAQ data instead of allowing the model to generate the final response.**

---

# 78. Short version to remember for an interview or presentation

If someone asks you:

> "How does your FAQ agent work?"

You can say:

> "The user sends a question to the agent. Gemini analyzes the question and selects the most relevant FAQ ID from our predefined FAQ list. We then validate that ID in Python and retrieve the approved answer from our FAQ data. LangGraph manages this workflow from FAQ selection to answer retrieval. The important part is that Gemini does not generate the final answer, which helps keep the responses controlled and based only on our predefined information."
