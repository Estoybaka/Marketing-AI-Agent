# Environment Setup — Marketing-AI-Agent (Week 3)

## 1. Project environment

| Item | Verified value |
|---|---|
| Operating environment | Windows + PowerShell |
| Code editor | Visual Studio Code |
| Python | `3.11.7` |
| Virtual environment | `.venv` |
| Virtual environment location reported by pip | `C:\\Priyanka\\GitHub\\Marketing-AI-Agent\\.venv` |
| Working project directory | `C:\\Priyanka\\GitHub\\Marketing-AI-Agent\\Week-3\\Day-4` |
| LLM provider | Google Gemini |
| Configured model used in the successful conversation | `gemini-3.5-flash-lite` |
| Lead database | SQLite (`leads.db`) |
| Automated testing | `pytest` |

## 2. Main technologies and verified versions

These versions were copied from the terminal output shared on October 10, 2026.

| Technology/package | Installed version | Purpose |
|---|---:|---|
| Python | 3.11.7 | Main programming language |
| `langgraph` | 1.2.12 | Stateful conversation workflow |
| `langchain` | 1.4.3 | LLM application framework and integration abstractions |
| `langchain-core` | 1.6.6 | Core LangChain interfaces and types |
| `langchain-google-genai` | 4.4.0 | LangChain integration for Google Gemini |
| `google-genai` | 2.29.0 | Google Gen AI Python SDK dependency |
| `python-dotenv` | 1.2.4 | Loads values from a `.env` file when called by the application |
| `pytest` | 8.4.2 | Automated testing |
| `pydantic` | 2.13.5 | Data validation and typed data models used by dependencies/project code |
| `langgraph-checkpoint` | 4.2.0 | LangGraph checkpoint support |
| `langgraph-prebuilt` | 1.1.0 | Prebuilt LangGraph components |
| `langgraph-sdk` | 0.4.5 | LangGraph SDK |
| `langsmith` | 0.14.3 | LangChain ecosystem tracing/development package; presence alone does not mean tracing is enabled |
| `openai` | 3.23.0 | Installed OpenAI SDK; the verified live conversation used Google Gemini, so this does not establish that OpenAI is used by this application |
| `langchain-openai` | 1.6.7 | Installed OpenAI integration package; its presence alone does not establish that the application uses it |
| `pip` | 23.2.1 | Python package installer |

SQLite is accessed through Python's built-in `sqlite3` module and normally does not need a separate pip installation.

## 3. Architecture at a glance

1. `main.py` provides the command-line chat interface and commands such as `/lead`, `/lead <ID>`, and `/quit`.
2. `lead_graph.py` defines the LangGraph workflow and integrates the configured Gemini model.
3. `lead_database.py` saves and retrieves lead records using SQLite.
4. `leads.db` stores the saved lead data.
5. The project's test files and `pytest` verify lead logic, database behavior, and integration.

## 4. Activate the environment

Open the project in VS Code and select **Terminal → New Terminal**. From the repository root, activate the existing environment with:

```powershell
.\.venv\Scripts\Activate.ps1
```

If the terminal is already in the Day 4 directory, use:

```powershell
..\..\.venv\Scripts\Activate.ps1
```

The prompt should begin with `(.venv)` when the environment is active.

Confirm Python and package versions:

```powershell
python --version
python -m pip show langgraph langchain langchain-google-genai python-dotenv pytest
python -m pip list
```

## 5. Run the project and tests

From the Day 4 project directory:

```powershell
cd C:\Priyanka\GitHub\Marketing-AI-Agent\Week-3\Day-4
python -m py_compile .\main.py
python -m pytest -q
python main.py
```

Useful interactive commands:

```text
/lead
/lead <ID>
/quit
```

## 6. Configuration and secrets

The project has a `.env` file. If the code loads it with `python-dotenv`, it can hold environment variables such as the Gemini API key.

- Never paste API keys into documentation or screenshots.
- Never commit `.env` with real secrets to a public repository.
- Keep a `.env.example` with placeholder values if you need to document required settings.
- The exact environment-variable name must match what the project code reads.

## 7. Dependency file status

The command below was run from the Day 4 working directory:

```powershell
Get-ChildItem requirements.txt, pyproject.toml, Pipfile -ErrorAction SilentlyContinue
```

It returned no entries, so none of those files was found **in that current directory**. This does not prove there is no dependency file elsewhere in the repository.

To save the current environment's installed packages as a reproducible dependency list, run from the repository root while `(.venv)` is active:

```powershell
python -m pip freeze > requirements.txt
```

Review the generated file before committing it. `pip freeze` records all installed packages in the active environment, including packages that may not be required directly by this project.

To inspect whether a dependency file already exists elsewhere in the repository, run from the repository root:

```powershell
Get-ChildItem -Path . -Filter requirements.txt -Recurse -File
Get-ChildItem -Path . -Filter pyproject.toml -Recurse -File
Get-ChildItem -Path . -Filter Pipfile -Recurse -File
```

## 8. Verification note

The user confirmed that the full `python -m pytest -q` test suite passed and that the interactive lead workflow, saving, and persistent lead retrieval behaved as expected.

This document records the environment information actually shown in the terminal. It does not claim that every installed package is imported by the application.
