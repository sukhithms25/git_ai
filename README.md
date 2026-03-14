# git_ai — Autonomous AI Developer Agent

> Give it a bug report. It fixes the code, commits the change, opens a Pull Request, and reviews it — all by itself.

---

## Problem Statement

Software teams waste hours on repetitive bug fixes — reading issue reports, finding the relevant code, writing the fix, committing, pushing, opening PRs, and waiting for reviews. This process is manual, slow, and error-prone.

**git_ai** automates the entire workflow using a local LLM. A developer describes a bug in plain English. The agent handles everything else autonomously.

---

## System Architecture

```
GitHub Issue
      |
      v
Issue Interpreter        <- Extracts keywords, component, location hints
      |
      v
Repository Analyzer      <- Scans codebase, finds relevant source files
      |
      v
Code Generator (LLM)     <- qwen2.5-coder:7b generates the fix
      |
      v
Patch Applier            <- Inserts fix safely, validates syntax, backs up file
      |
      v
Git Manager              <- Creates branch, stages files, commits
      |
      v
Pull Request Creator     <- Pushes branch, opens PR on GitHub via API
      |
      v
AI Review Engine         <- Reads PR diff, generates review, posts comment
```

---

## Full Pipeline (10 Steps)

```
[1/10]  Analyse issue
[2/10]  Scan repository
[3/10]  Detect relevant files
[4/10]  Load code content
[5/10]  Generate fix (LLM)
[6/10]  Apply patch to file
[7/10]  Create git branch + commit
[8/10]  Push branch to GitHub
[9/10]  Open Pull Request
[10/10] Post AI code review comment
```

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.12 |
| LLM | qwen2.5-coder:7b via Ollama (local, private) |
| Git operations | GitPython |
| GitHub API | PyGithub |
| Issue parsing | Regex + heuristic keyword maps |
| Code patching | Custom AST-aware insertion engine |
| Syntax validation | Python `compile()` built-in |

---

## Project Structure

```
git_ai/
├── agent/
│   ├── issue_interpreter_v2.py   # Parses issue text, extracts location hints
│   ├── repo_analyzer.py          # Scans repo for source files
│   └── code_generator.py         # Calls LLM to generate fix
├── utils/
│   ├── file_loader.py            # Reads files safely with encoding fallback
│   └── code_parser.py            # Extracts symbols and keyword lines
├── git_tools/
│   ├── patch_applier_v2.py       # Smart patch insertion with syntax validation
│   └── repo_manager.py           # Branch creation and git commits
├── github_tools/
│   ├── github_auth.py            # GitHub PAT authentication
│   └── pr_creator.py             # Push branch and open Pull Request
├── review_engine/
│   └── pr_reviewer.py            # Fetch PR diff, generate review, post comment
├── sample_project/
│   └── login.py                  # Demo buggy project
├── main.py                       # Full 10-step pipeline orchestrator
└── run_with_issue.py             # CLI entry point
```

---

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Ollama and pull the model

```bash
# Download Ollama from https://ollama.com/download
ollama pull qwen2.5-coder:7b
```

### 3. Set GitHub token

```bash
# Windows
setx GITHUB_TOKEN "ghp_your_token_here"

# Linux / Mac
export GITHUB_TOKEN="ghp_your_token_here"
```

Required token scopes: `repo`, `workflow`

---

## How to Run

### Option 1: CLI argument

```bash
python run_with_issue.py "Fix login crash when password is empty"
```

### Option 2: Interactive mode

```bash
python main.py ./sample_project
# Enter issue when prompted
```

### Option 3: Pipe input

```bash
echo "Fix login crash when password is empty" | python main.py ./sample_project
```

---

## Example Output

```
============================================================
  git_ai - AI Developer Brain  |  Full Pipeline
============================================================

[1/10] Analysing issue ...
  Input     : Fix login crash when password is empty
  Component : login
  Type      : bug
  Keywords  : fix, login, crash, password, empty

[2/10] Scanning repository ...
  [OK] 1 source file(s) detected

[3/10] Detecting relevant files ...
    * login.py

[4/10] Loading code content ...
  [OK] 1 file(s) loaded

[5/10] Generating fix (LLM) ...
  [OK] Fix generated

[6/10] Applying patch ...
  [OK] Patched -> login.py  (2 lines changed)

[7/10] Creating git branch and committing ...
  [OK] Branch  : ai-fix-login-260314-102330
  [OK] Commit  : 6161629f

[8/10] Pushing branch to GitHub ...

[9/10] Creating Pull Request ...
  [OK] Pull Request #8 created
  [OK] URL: https://github.com/sukhithms25/git_ai/pull/8

[10/10] Running AI code review ...
  [OK] Review posted - Verdict: APPROVED
  [OK] Comment URL: https://github.com/sukhithms25/git_ai/pull/8#issuecomment-...

============================================================
  [OK] Pipeline Complete - AI fix shipped to GitHub!
  Branch  : ai-fix-login-260314-102330
  Commit  : 6161629f
  PR #    : 8
  PR URL  : https://github.com/sukhithms25/git_ai/pull/8
  Verdict : APPROVED
  Review  : https://github.com/sukhithms25/git_ai/pull/8#issuecomment-...
============================================================
```

---

## Supported Issue Formats

```bash
# General
"Fix login crash when password is empty"

# Function-specific
"Fix bug in authenticate_user function"

# Before/after a specific call
"Insert validation before database.find_user call"

# File:function format
"Fix login.py:authenticate_user password bug"

# Line-specific
"Add null check at line 15 in login.py"
```

---

## Key Features

- **Fully local** — LLM runs on your machine via Ollama. No code leaves your system.
- **Safe patching** — Creates `.bak` backup before modifying any file. Auto-rollback on syntax errors.
- **Duplicate detection** — Will not insert the same fix twice.
- **Syntax validation** — Validates Python syntax after patching. Rejects broken patches.
- **Structured PR** — PR body includes issue context, component, and the exact patch code.
- **AI review** — After opening the PR, the agent reads the diff and posts a verdict (APPROVED / NEEDS CHANGES / REJECTED).

---

## Demo Scenario

### Setup

```bash
# Restore the buggy file
python -c "
content = open('sample_project/login.py').read()
print('Bugs present:', 'if not password' not in content)
"
```

### Run

```bash
python run_with_issue.py "Fix login crash when password is empty"
```

### Verify on GitHub

1. Open your repository on GitHub
2. Go to **Pull Requests**
3. See the AI-generated PR with patch description
4. Scroll to comments — see the AI review verdict

---

## 30-Second Pitch

> git_ai is an autonomous AI developer agent. You give it a bug report in plain English. It reads your codebase, finds the relevant code, generates a fix using a local LLM, applies the patch safely, commits the change to a new branch, opens a Pull Request on GitHub, and then reviews its own PR — all without any human intervention. It's a complete autonomous developer workflow from issue to reviewed PR.

---

## Limitations (Honest)

- Patch insertion is function-level, not line-level
- Works best on single-file bugs
- LLM quality depends on the model used
- GitHub token required for Phase 3

---

## Author

**Sukhith MS**
GitHub: [@sukhithms25](https://github.com/sukhithms25)

---

*Built for hackathon demonstration. Not production-ready.*
