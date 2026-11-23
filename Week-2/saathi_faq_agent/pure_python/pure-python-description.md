# Saathi Sneha Care FAQ Agent — Simple Code Explanation

## 1. What does this program do?

This Python program is a **simple FAQ chatbot**.

It does not use AI, machine learning, or an LLM. Instead, it uses:

- A list of predefined FAQs from `data.faqs`
- Keywords associated with each FAQ
- Text normalization
- Phrase matching
- A simple scoring system

The overall flow is:

```text
User asks a question
        ↓
Normalize the question
        ↓
Compare it with every FAQ
        ↓
Check the official FAQ question
        ↓
Check the FAQ keywords
        ↓
Give each FAQ a score
        ↓
Find the highest score
        ↓
If exactly one FAQ wins → return its answer
If there is no clear winner → return fallback answer
```

---

## 2. Imports

```python
import re
from data.faqs import FAQS, FALLBACK
```

### `import re`

`re` is Python's **regular expression** module.

It is used here to remove punctuation and keep text simple.

For example:

```text
"Hello, how are you?"
```

can become:

```text
"hello how are you"
```

### `from data.faqs import FAQS, FALLBACK`

This imports two things from another file:

```text
data/
└── faqs.py
```

`FAQS` contains the predefined FAQ information.

It might look like:

```python
FAQS = [
    {
        "id": 1,
        "question": "What services do you provide?",
        "keywords": ["services", "help", "care"],
        "answer": "We provide..."
    }
]
```

`FALLBACK` is the response used when the program cannot confidently find an FAQ answer.

---

## 3. `normalize()` function

```python
def normalize(text: str) -> str:
    """Lowercase text and remove punctuation."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return " ".join(text.split())
```

This function prepares text before comparing it.

### Step 1: Convert to lowercase

```python
text = text.lower()
```

For example:

```text
"How Can I Contact You?"
```

becomes:

```text
"how can i contact you?"
```

This prevents uppercase/lowercase differences from affecting matching.

### Step 2: Remove punctuation

```python
re.sub(r"[^a-z0-9\s]", " ", text)
```

This keeps:

- English letters
- Numbers
- Whitespace

and replaces other characters with spaces.

For example:

```text
"How can I contact you?"
```

becomes approximately:

```text
"how can i contact you "
```

The `?` is removed.

### Step 3: Clean extra spaces

```python
return " ".join(text.split())
```

For example:

```text
"hello     how   are you"
```

becomes:

```text
"hello how are you"
```

So:

```text
"How can I CONTACT you???"
```

ultimately becomes:

```text
"how can i contact you"
```

---

## 4. `contains_phrase()` function

```python
def contains_phrase(text: str, phrase: str) -> bool:
    """Check for a whole phrase, not a partial word."""
    padded_text = f" {normalize(text)} "
    padded_phrase = f" {normalize(phrase)} "
    return padded_phrase in padded_text
```

This function checks whether a phrase exists inside some text.

It returns either:

```python
True
```

or:

```python
False
```

### Why are spaces added?

Suppose:

```text
text = "What is your location?"
phrase = "location"
```

After normalization:

```text
"what is your location"
"location"
```

The code adds spaces:

```text
" what is your location "
" location "
```

Then it checks whether:

```text
" location "
```

exists inside:

```text
" what is your location "
```

The result is:

```python
True
```

The spaces help prevent simple partial-word matches.

For example, a keyword such as `care` should not accidentally match the middle of another word such as `scared`.

---

## 5. `find_faq()` function

```python
def find_faq(question: str):
    """Find one clear FAQ match, or None."""
```

This is the **main matching function**.

Its job is to:

> Look through all FAQs and decide whether one FAQ clearly matches the user's question.

### Create a score dictionary

```python
scores = {}
```

The program will store results such as:

```python
{
    1: 3,
    2: 0,
    3: 1
}
```

This means:

- FAQ 1 → 3 points
- FAQ 2 → 0 points
- FAQ 3 → 1 point

The higher the score, the stronger the match.

---

## 6. Check every FAQ

```python
for faq in FAQS:
    score = 0
```

The program processes FAQs one at a time.

For every FAQ, its score starts at:

```python
0
```

---

## 7. Match the official FAQ question

```python
if contains_phrase(question, faq["question"]):
    score += 2
```

This checks whether the user's question contains the predefined FAQ question.

A match gives **2 points**.

For example, if the FAQ question is:

```text
How can I contact you?
```

and the user asks:

```text
How can I contact you?
```

the score increases by 2:

```text
0 → 2
```

The complete FAQ question gets more points than a single keyword because it is stronger evidence of a match.

---

## 8. Match keywords

```python
for keyword in faq["keywords"]:
    if contains_phrase(question, keyword):
        score += 1
```

Each FAQ can have several keywords.

For example:

```python
"keywords": ["contact", "phone", "email"]
```

The program checks each one.

If the user asks:

```text
How can I contact you by email?
```

then both `contact` and `email` may match.

The score would receive:

```text
+1 for contact
+1 for email
```

---

## 9. Example of scoring

Suppose an FAQ is:

```python
{
    "id": 1,
    "question": "How can I contact you?",
    "keywords": ["contact", "phone", "email"],
    "answer": "You can contact us..."
}
```

User asks:

```text
How can I contact you?
```

### Official question

Matches:

```text
+2
```

### Keyword

`contact` matches:

```text
+1
```

`phone` does not match:

```text
+0
```

`email` does not match:

```text
+0
```

### Final score

```text
2 + 1 = 3
```

So the program stores:

```python
scores[1] = 3
```

---

## 10. Save the FAQ score

```python
scores[faq["id"]] = score
```

After all FAQs are processed, the dictionary could look like:

```python
scores = {
    1: 3,
    2: 1,
    3: 0
}
```

---

## 11. Find the highest score

```python
highest = max(scores.values(), default=0)
```

This finds the largest score.

For:

```python
scores = {
    1: 3,
    2: 1,
    3: 0
}
```

the result is:

```python
highest = 3
```

The `default=0` handles the case where there are no scores.

---

## 12. What if nothing matched?

```python
if highest == 0:
    return None
```

If every FAQ has a score of zero, the program does not guess.

It returns:

```python
None
```

This means:

> No FAQ was found with a useful match.

---

## 13. Find all FAQs with the highest score

```python
winners = [
    faq_id for faq_id, score in scores.items()
    if score == highest
]
```

This creates a list containing every FAQ that achieved the highest score.

For example:

```python
scores = {
    1: 3,
    2: 1,
    3: 3
}
```

The highest score is:

```text
3
```

Therefore:

```python
winners = [1, 3]
```

---

## 14. Avoid guessing when there is a tie

```python
if len(winners) != 1:
    return None
```

This is an important safety feature.

If:

```python
winners = [1]
```

then exactly one FAQ wins.

But if:

```python
winners = [1, 3]
```

then two FAQs have the same score.

The program does **not** randomly choose one.

Instead, it returns:

```python
None
```

The chatbot will then use the fallback answer.

This is useful because a rule-based chatbot should avoid confidently giving an unrelated answer.

---

## 15. Return the winning FAQ ID

```python
return winners[0]
```

If:

```python
winners = [2]
```

then:

```python
winners[0]
```

is:

```text
2
```

So `find_faq()` returns the ID of FAQ 2.

---

# 16. `answer_question()` function

```python
def answer_question(question: str) -> dict:
    """Return a FAQ answer and its matched FAQ ID."""
```

This function turns the matching result into an actual answer.

### Step 1: Find the FAQ

```python
faq_id = find_faq(question)
```

For example:

```text
User question
      ↓
find_faq()
      ↓
FAQ ID = 2
```

---

## 17. If no FAQ was found

```python
if faq_id is None:
    return {
        "faq_id": None,
        "answer": FALLBACK,
    }
```

If `find_faq()` returns `None`, the function returns the fallback response.

For example:

```python
{
    "faq_id": None,
    "answer": "Sorry, I could not find an answer."
}
```

---

## 18. Find the complete FAQ

```python
faq = next(item for item in FAQS if item["id"] == faq_id)
```

If:

```python
faq_id = 2
```

this searches `FAQS` until it finds:

```python
item["id"] == 2
```

Then it retrieves the complete FAQ object.

For example:

```python
{
    "id": 2,
    "question": "How can I contact you?",
    "keywords": ["contact", "phone", "email"],
    "answer": "You can contact us by phone or email."
}
```

---

## 19. Return the final result

```python
return {
    "faq_id": faq_id,
    "answer": faq["answer"],
}
```

The function returns:

1. The matched FAQ ID
2. The answer

Example:

```python
{
    "faq_id": 2,
    "answer": "You can contact us by phone or email."
}
```

---

# 20. `chat()` function

```python
def chat():
```

This creates the command-line chatbot.

### Display the welcome message

```python
print("Saathi Sneha Care FAQ Agent")
print("Ask a question, or type 'exit' to quit.\n")
```

The user sees:

```text
Saathi Sneha Care FAQ Agent
Ask a question, or type 'exit' to quit.
```

---

## 21. Keep the conversation running

```python
while True:
```

This creates an infinite loop.

The chatbot keeps asking questions until `break` is executed.

---

## 22. Get the user's question

```python
question = input("You: ").strip()
```

`input()` waits for the user to type something.

For example:

```text
You: How can I contact you?
```

`.strip()` removes unnecessary spaces at the beginning and end.

For example:

```text
"   hello   "
```

becomes:

```text
"hello"
```

---

## 23. Exit the chatbot

```python
if question.lower() == "exit":
    print("Agent: Goodbye!")
    break
```

The program converts the input to lowercase.

Therefore all of these work:

```text
exit
EXIT
Exit
ExIt
```

When the user types `exit`:

1. It prints `Goodbye!`
2. `break` stops the `while` loop
3. The chatbot ends

---

## 24. Ignore empty questions

```python
if not question:
    continue
```

If the user presses Enter without typing anything, the question is empty.

`continue` means:

> Skip this iteration and ask for another question.

---

## 25. Get the answer

```python
result = answer_question(question)
```

The user's question is sent to `answer_question()`.

That function calls:

```python
find_faq()
```

which performs the matching and scoring.

The result might be:

```python
{
    "faq_id": 2,
    "answer": "You can contact us by phone or email."
}
```

---

## 26. Print the answer

```python
print(f"Agent: {result['answer']}\n")
```

The `f` makes this an **f-string**.

This:

```python
{result['answer']}
```

means:

> Insert the value stored under `"answer"` here.

The output becomes:

```text
Agent: You can contact us by phone or email.
```

---

# 27. `if __name__ == "__main__":`

```python
if __name__ == "__main__":
    chat()
```

This is a common Python pattern.

It means:

> Run `chat()` when this file is executed directly.

For example:

```bash
python main.py
```

will start the chatbot.

But if another Python file imports:

```python
from main import answer_question
```

the chatbot will not automatically start.

Only the requested function can be used.

---

# 28. Complete example flow

Suppose the user enters:

```text
You: How can I contact you?
```

The process is:

```text
User question
      ↓
chat()
      ↓
answer_question()
      ↓
find_faq()
      ↓
Check every FAQ
      ↓
Calculate scores
      ↓
Find highest score
      ↓
One clear winner?
      ↓
Yes
      ↓
Return FAQ ID
      ↓
Get its answer
      ↓
Print answer
```

For example:

```text
FAQ 1 → 0 points
FAQ 2 → 3 points
FAQ 3 → 1 point
```

FAQ 2 wins.

The chatbot prints:

```text
Agent: You can contact us by phone or email.
```

---

# 29. What happens when there is no match?

Suppose the user asks:

```text
What is the weather today?
```

and none of the FAQs contain matching phrases or keywords.

The scores might be:

```text
FAQ 1 → 0
FAQ 2 → 0
FAQ 3 → 0
```

Then:

```python
highest == 0
```

so:

```python
find_faq()
```

returns:

```python
None
```

Then `answer_question()` uses:

```python
FALLBACK
```

The chatbot gives the predefined fallback response.

---

# 30. What happens when two FAQs tie?

Suppose:

```text
FAQ 1 → 2 points
FAQ 2 → 2 points
FAQ 3 → 0 points
```

Then:

```python
highest = 2
```

and:

```python
winners = [1, 2]
```

There are two winners, so:

```python
len(winners) != 1
```

is true.

The function returns:

```python
None
```

and the chatbot uses the fallback answer.

This prevents the program from guessing.

---

# 31. Important limitation

This is a **rule-based FAQ chatbot**, not a true AI chatbot.

It does not deeply understand the meaning of language.

For example, a human can recognize that these questions are related:

```text
How can I contact you?
```

```text
How do I reach your team?
```

```text
Where can I get your phone number?
```

The program can recognize such variations only when the relevant words or phrases have been included in the FAQ questions or keyword lists.

Its knowledge mainly comes from:

```python
FAQS
```

and especially:

```python
keywords
```

---

# 32. Why keywords are important

Suppose an FAQ contains:

```python
"keywords": ["contact", "phone", "email"]
```

You can expand it with useful alternatives:

```python
"keywords": [
    "contact",
    "phone",
    "email",
    "reach",
    "call",
    "message"
]
```

This can help the chatbot recognize more ways of asking the same thing.

However, adding too many generic keywords can cause incorrect matches.

For example:

```text
help
service
information
question
```

may appear in many unrelated questions.

So keywords should be reasonably specific.

---

# 33. Main concepts to remember

### `normalize()`

Cleans text before comparison.

```text
"Hello!!!" → "hello"
```

### `contains_phrase()`

Checks whether a complete phrase appears in the text.

### `find_faq()`

Finds the best FAQ using scores.

```text
Question
   ↓
Compare FAQs
   ↓
Calculate scores
   ↓
Find highest score
   ↓
Return one clear FAQ ID
```

### `answer_question()`

Uses the FAQ ID to retrieve the actual answer.

### `chat()`

Handles the conversation with the user.

### `FALLBACK`

Used when there is no confident match.

---

# 34. Simple architecture

```text
┌─────────────────────────────┐
│           User              │
│  "How can I contact you?"   │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│          chat()             │
│      Gets user input        │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│      answer_question()      │
│       Gets the answer       │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│         find_faq()          │
│      Matching + scoring     │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│       data/faqs.py          │
│ FAQs + keywords + answers   │
└─────────────────────────────┘
```

---

# 35. The whole program in one sentence

> **The program cleans the user's question, compares it against predefined FAQ questions and keywords, scores the matches, returns an answer only when there is one clear winner, and otherwise uses a fallback response.**

---

# 36. Beginner-friendly mental model

You can think of the chatbot as a person with a folder of prepared answers.

When you ask a question, it:

1. Cleans your question.
2. Looks through every prepared FAQ.
3. Gives points to FAQs that contain matching information.
4. Finds the FAQ with the most points.
5. If exactly one FAQ wins, it gives that answer.
6. If nothing matches or multiple FAQs tie, it says it cannot confidently answer.
7. It repeats this process until you type `exit`.

The most important flow to remember is:

```text
Input
  ↓
normalize()
  ↓
find_faq()
  ↓
score FAQs
  ↓
choose one clear match
  ↓
answer_question()
  ↓
chatbot response
```

The most important external file is:

```text
data/faqs.py
```

because that is where the chatbot's actual FAQ knowledge comes from.
