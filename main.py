"""
main.py

Orchestrator for the git_ai pipeline.

Phase-1 (steps 1-5):  Issue → Analysis → Fix suggestion
Phase-2 (steps 6-7):  Apply patch → Git branch + commit

Full pipeline:
  1  Interpret issue
  2  Scan repository
  3  Detect relevant files
  4  Load code
  5  Generate fix
  6  Apply patch to file
  7  Create git branch + commit
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.resolve()
sys.path.insert(0, str(ROOT))

from agent.repo_analyzer       import scan_repository
from agent.issue_interpreter   import interpret_issue, print_parsed_issue
from agent.code_generator      import generate_fix
from utils.file_loader         import load_files, format_file_block
from utils.code_parser         import extract_lines_with_keywords
from git_tools.patch_applier_v2 import apply_patch, PatchResult
from git_tools.repo_manager    import branch_and_commit, print_commit_result

# ── Config ────────────────────────────────────────────────────────────────────

MAX_RELEVANT_FILES = 5

# ── Helpers ───────────────────────────────────────────────────────────────────

def find_relevant_files(all_files: list[str], keywords: list[str]) -> list[str]:
    kw_lower = [kw.lower() for kw in keywords]

    def score(fp: str) -> int:
        return sum(1 for kw in kw_lower if kw in fp.lower())

    scored = sorted([(f, score(f)) for f in all_files], key=lambda x: x[1], reverse=True)
    matched = [f for f, s in scored if s > 0]
    if not matched:
        matched = [f for f, _ in scored[:MAX_RELEVANT_FILES]]
    return matched[:MAX_RELEVANT_FILES]


def build_code_blocks(
    relevant_files: list[str],
    repo_path: str,
    keywords: list[str],
) -> list[str]:
    loaded = load_files(relevant_files, repo_root=repo_path)
    blocks: list[str] = []
    for result in loaded:
        if result["error"]:
            blocks.append(format_file_block(result))
            continue
        highlighted = extract_lines_with_keywords(result["content"], keywords)
        if highlighted:
            snippet = f"[File: {result['path']}]\n" + "\n".join(highlighted) + "\n"
        else:
            snippet = format_file_block(result)
        blocks.append(snippet)
    return blocks


def _ok(label: str) -> None:
    print(f"  ✔ {label}")


def _fail(label: str, reason: str) -> None:
    print(f"  ✘ {label}: {reason}")

# ── Main pipeline ─────────────────────────────────────────────────────────────

def run(issue: str, repo_path: str) -> None:
    print("\n" + "═" * 60)
    print("  git_ai — AI Developer Brain  |  Phase 1 + 2")
    print("═" * 60)

    # ── Step 1: Interpret issue ───────────────────────────────────────────────
    print("\n[1/7] Analysing issue …")
    parsed = interpret_issue(issue)
    print_parsed_issue(parsed)

    # ── Step 2: Scan repository ───────────────────────────────────────────────
    print("[2/7] Scanning repository …")
    all_files = scan_repository(repo_path)
    if not all_files:
        print("  No source files found. Check the repo path.")
        return
    _ok(f"{len(all_files)} source file(s) detected")
    print()

    # ── Step 3: Detect relevant files ─────────────────────────────────────────
    print("[3/7] Detecting relevant files …")
    relevant = find_relevant_files(all_files, parsed.keywords)
    if not relevant:
        print("  No relevant files found.")
        return
    for f in relevant:
        print(f"    • {f}")
    print()

    # ── Step 4: Load code ─────────────────────────────────────────────────────
    print("[4/7] Loading code content …")
    code_blocks = build_code_blocks(relevant, repo_path, parsed.keywords)
    _ok(f"{len(code_blocks)} file(s) loaded")
    print()

    # ── Step 5: Generate fix ──────────────────────────────────────────────────
    print("[5/7] Generating fix (LLM) …")
    llm_response = generate_fix(parsed.raw_text, code_blocks)
    _ok("Fix generated")
    print()
    print("─" * 60)
    print("  AI Suggestion (before patch apply):")
    print("─" * 60)
    print(llm_response)
    print("─" * 60 + "\n")

    # ── Step 6: Apply patch ───────────────────────────────────────────────────
    print("[6/7] Applying patch …")
    patch_results: list[PatchResult] = []
    patched_files: list[str] = []

    for rel_file in relevant:
        result = apply_patch(
            file_path=rel_file,
            llm_response=llm_response,
            keywords=parsed.keywords,
            repo_root=repo_path,
        )
        patch_results.append(result)
        if result.success:
            _ok(f"Patched  → {rel_file}  ({result.lines_changed} lines changed)")
            patched_files.append(rel_file)
        else:
            _fail(f"Patch failed for {rel_file}", result.error)

    if not patched_files:
        print("\n  No files were patched. Stopping before git commit.")
        return
    print()

    # ── Step 7: Git branch + commit ───────────────────────────────────────────
    print("[7/7] Creating git branch and committing …")
    # Convert relative file paths to be relative to repo_path
    repo_root = Path(repo_path).resolve()
    abs_patched = [str((repo_root / f).resolve()) for f in patched_files]
    
    commit_result = branch_and_commit(
        repo_path=repo_path,
        modified_files=abs_patched,
        issue_text=parsed.raw_text,
        component=parsed.component,
    )
    print_commit_result(commit_result)

    # ── Summary ───────────────────────────────────────────────────────────────
    print()
    print("═" * 60)
    if commit_result.success:
        print("  ✔ Phase-2 Complete — AI fix committed to repository")
        print(f"  Branch : {commit_result.branch}")
        print(f"  Commit : {commit_result.commit_sha}")
        print()
        print("  Next steps:")
        print("    git log --oneline -5")
        print("    git diff HEAD~1")
    else:
        print("  Pipeline finished (git step failed — patch is on disk)")
    print("═" * 60 + "\n")


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    repo = sys.argv[1] if len(sys.argv) > 1 else "."

    if not sys.stdin.isatty():
        issue_text = sys.stdin.read().strip()
    else:
        print("\nEnter the issue description (press Enter twice to submit):")
        lines: list[str] = []
        try:
            while True:
                line = input()
                if line == "" and lines and lines[-1] == "":
                    break
                lines.append(line)
        except EOFError:
            pass
        issue_text = "\n".join(lines).strip()

    if not issue_text:
        print("No issue description provided. Exiting.")
        sys.exit(1)

    run(issue_text, repo)
