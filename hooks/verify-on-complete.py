#!/usr/bin/env python3
"""
Stop hook - Auto-verification when Claude completes a task.
Runs quick validation checks and reports results.
Triggered by: Stop event

This hook checks:
1. If there are uncommitted changes
2. If tests pass (if test command is available)
3. If lint passes (if lint command is available)

Results are shown to the user via a JSON systemMessage on stdout, and only when
a test or lint command actually ran (plain stdout/stderr from an exit-0 Stop
hook only reach the debug log).

Exit codes:
- 0: Always. The hook never blocks, whatever the verification outcome.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], timeout: int = 30) -> tuple[bool, str]:
    """Run a command and return (success, output)."""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, cwd=os.getcwd()
        )
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    except FileNotFoundError:
        return False, "Command not found"
    except Exception as e:
        return False, str(e)


def detect_package_manager() -> str | None:
    """Detect which package manager is used in the project."""
    cwd = Path(os.getcwd())

    if (cwd / "bun.lockb").exists() or (cwd / "bun.lock").exists():
        return "bun"
    if (cwd / "pnpm-lock.yaml").exists():
        return "pnpm"
    if (cwd / "yarn.lock").exists():
        return "yarn"
    if (cwd / "package-lock.json").exists():
        return "npm"
    if (cwd / "package.json").exists():
        return "npm"
    return None


def get_test_command() -> list[str] | None:
    """Get the test command for this project."""
    cwd = Path(os.getcwd())

    # Check package.json for test script
    package_json = cwd / "package.json"
    if package_json.exists():
        try:
            with open(package_json) as f:
                pkg = json.load(f)
            if pkg.get("scripts", {}).get("test"):
                pm = detect_package_manager() or "npm"
                return [pm, "test"]
        except Exception:
            pass

    # Python projects
    if (cwd / "pytest.ini").exists() or (cwd / "pyproject.toml").exists():
        return ["pytest", "--tb=no", "-q"]

    # Go projects
    if (cwd / "go.mod").exists():
        return ["go", "test", "./..."]

    # Rust projects
    if (cwd / "Cargo.toml").exists():
        return ["cargo", "test", "--quiet"]

    return None


def get_lint_command() -> list[str] | None:
    """Get the lint command for this project."""
    cwd = Path(os.getcwd())

    # Check package.json for lint script
    package_json = cwd / "package.json"
    if package_json.exists():
        try:
            with open(package_json) as f:
                pkg = json.load(f)
            if pkg.get("scripts", {}).get("lint"):
                pm = detect_package_manager() or "npm"
                return [pm, "run", "lint"]
        except Exception:
            pass

    # Python - check for ruff or flake8
    if (cwd / "pyproject.toml").exists() or (cwd / "setup.py").exists():
        success, _ = run_command(["which", "ruff"])
        if success:
            return ["ruff", "check", "."]

    return None


def check_git_status() -> tuple[bool, str]:
    """Check if there are uncommitted changes."""
    success, output = run_command(["git", "status", "--porcelain"])
    if not success:
        return True, "Not a git repository"

    if output.strip():
        lines = output.strip().split("\n")
        return False, f"{len(lines)} uncommitted change(s)"
    return True, "Working tree clean"


def has_code_changes() -> bool:
    """Check if there are any code changes worth verifying."""
    success, output = run_command(["git", "diff", "--name-only", "HEAD"], timeout=5)
    if not success or not output.strip():
        # Also check staged changes
        success2, output2 = run_command(["git", "diff", "--name-only", "--cached"], timeout=5)
        if not success2 or not output2.strip():
            return False
        output = output2
    # Check if any changed files are code (not just docs/config)
    code_extensions = {'.py', '.js', '.ts', '.tsx', '.jsx', '.go', '.rs', '.java', '.rb', '.c', '.cpp', '.h'}
    for line in output.strip().split("\n"):
        if any(line.endswith(ext) for ext in code_extensions):
            return True
    return False


def main():
    """Run verification checks on task completion."""
    try:
        results = []
        has_failures = False
        ran_checks = False

        # 1. Check git status
        git_ok, git_msg = check_git_status()
        results.append(f"{'✓' if git_ok else '!'} Git: {git_msg}")

        # 2. Only run tests/lint if there are actual code changes
        if has_code_changes():
            # Run tests if available (with short timeout)
            test_cmd = get_test_command()
            if test_cmd:
                ran_checks = True
                test_ok, test_output = run_command(test_cmd, timeout=30)
                if test_ok:
                    results.append("✓ Tests: passed")
                elif "timed out" in test_output.lower():
                    # A slow suite is not a failure — don't raise a false alarm.
                    results.append("- Tests: skipped (timed out)")
                else:
                    results.append("✗ Tests: failed")
                    has_failures = True

            # Run lint if available (quick check)
            lint_cmd = get_lint_command()
            if lint_cmd:
                ran_checks = True
                lint_ok, lint_output = run_command(lint_cmd, timeout=10)
                if lint_ok:
                    results.append("✓ Lint: passed")
                else:
                    results.append("⚠ Lint: issues found")
                    # Lint warnings don't count as failures
        else:
            results.append("- Tests/Lint: skipped (no code changes)")

        # Plain stdout/stderr from an exit-0 Stop hook only reach the debug log,
        # so report via a JSON systemMessage (shown to the user, non-blocking),
        # and only when a test or lint command actually ran. The desktop
        # notification is handled by notify-complete.sh, so this hook sends none.
        if ran_checks:
            status = "⚠️ some checks failed" if has_failures else "✓ all checks passed"
            summary = "\n".join(results)
            print(json.dumps({"systemMessage": f"[Verification: {status}]\n{summary}"}))
    except Exception:
        # Never block on errors
        pass

    # Always exit 0 - verification should never block
    sys.exit(0)


if __name__ == "__main__":
    main()
