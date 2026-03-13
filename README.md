# git_ai — AI Developer Brain (Phase 1)

An autonomous AI agent that reads a bug report, scans a repository, identifies the relevant code, and suggests a patch — all locally.

## Pipeline

```
Issue Description + Repository Path
          ↓
    Repository Analysis
          ↓
  Relevant File Detection
          ↓
      Code Reasoning
          ↓
    Patch Suggestion
```

## Project Structure

```
git_ai/
├── agent/
│   ├── issue_interpreter.py   # Extracts keywords from issue text
│   ├── repo_analyzer.py       # Scans repo for source files
│   └── code_generator.py      # Calls LLM to generate a fix
├── utils/
│   ├── file_loader.py         # Reads file contents safely
│   └── code_parser.py         # Extracts symbols & keyword lines
├── sample_project/
│   └── login.py               # Dummy buggy project for testing
├── main.py                    # Orchestrates the full pipeline
└── requirements.txt
```

## Setup

```bash
pip install -r requirements.txt
```

> **LLM backend:** This project uses [Ollama](https://ollama.com) for local inference.
> Pull a model before running: `ollama pull codellama`
> If Ollama is not running, the system falls back to a built-in mock response automatically.

## Usage

```bash
# Point at a repository and describe the issue
python main.py ./sample_project

# Or pipe the issue in
echo "Fix login crash when password empty" | python main.py ./sample_project
```

## Example Output

```
============================================================
  AI Developer Brain — Phase 1
============================================================

── Issue Analysis ────────────────────────────────
  Input     : Fix login crash when password empty
  Component : login
  Type      : bug
  Keywords  : fix, login, crash, password, empty
──────────────────────────────────────────────────

[1/5] Analysing issue …
[2/5] Scanning repository …
       1 source file(s) detected.

[3/5] Detecting relevant files …
  Relevant files:
    • login.py

[4/5] Loading code content …
[5/5] Generating fix (calling LLM) …

============================================================
  SUGGESTED PATCH
============================================================
if not password or not password.strip():
    return {"error": "Password is required"}, 400
============================================================
```

## Phase 2 (coming next)

- Git branch creation
- Apply generated patch
- Commit changes
- Open a Pull Request automatically