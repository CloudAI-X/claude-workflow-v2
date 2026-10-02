#!/usr/bin/env python3
"""
Post-task documentation suggestion hook.
Detects significant changes and suggests CLAUDE.md/AGENTS.md updates.
Runs on Stop event. Informational only - never blocks.
Suggestions are shown to the user via a JSON systemMessage on stdout.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile


def run_command(cmd: list[str], timeout: int = 15) -> tuple[bool, str]:
    """Run a command and return (success, output)."""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, cwd=os.getcwd()
        )
        return result.returncode == 0, result.stdout.strip()
    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    except FileNotFoundError:
        return False, "Command not found"
    except Exception as e:
        return False, str(e)


def get_diff_stat() -> list[str]:
    """Get git diff --stat lines for changes since HEAD."""
    success, output = run_command(["git", "diff", "--stat", "HEAD"])
    if not success or not output:
        # Also check for untracked files
        success2, output2 = run_command(["git", "status", "--porcelain"])
        if success2 and output2:
            return output2.split("\n")
        return []
    return output.split("\n")


def get_changed_files() -> list[str]:
    """Get list of changed file paths (staged, unstaged, and untracked)."""
    files = []

    # Staged and unstaged changes
    success, output = run_command(["git", "diff", "--name-status", "HEAD"])
    if success and output:
        for line in output.split("\n"):
            parts = line.split("\t", 1)
            if len(parts) == 2:
                files.append(line)

    # Untracked files, minus .claude/: that holds Claude Code config and the
    # logs this plugin's own hooks write, not project code worth documenting.
    success, output = run_command(["git", "ls-files", "--others", "--exclude-standard"])
    if success and output:
        for f in output.split("\n"):
            if f.strip() and not f.strip().startswith(".claude/"):
                files.append(f"A\t{f.strip()}")

    return files


def detect_new_directories(changed_files: list[str]) -> list[str]:
    """Detect new directories (top-most directories holding no tracked file)."""
    success, output = run_command(["git", "ls-files"])
    if not success:
        return []

    tracked_dirs = set()
    for f in output.split("\n"):
        d = os.path.dirname(f)
        while d:
            tracked_dirs.add(d)
            d = os.path.dirname(d)

    new_dirs = set()
    for entry in changed_files:
        parts = entry.split("\t", 1)
        if len(parts) == 2:
            status, filepath = parts
            if status.startswith("A") or status.startswith("?"):
                top_new = None
                d = os.path.dirname(filepath)
                while d:
                    if d not in tracked_dirs:
                        top_new = d
                    d = os.path.dirname(d)
                if top_new:
                    new_dirs.add(top_new)
    return sorted(new_dirs)


def detect_new_file_types(changed_files: list[str]) -> list[str]:
    """Detect new file extensions introduced by the changes."""
    new_extensions = set()

    # Get existing file extensions in the repo
    success, output = run_command(["git", "ls-files"])
    existing_extensions = set()
    if success and output:
        for f in output.split("\n"):
            ext = os.path.splitext(f)[1]
            if ext:
                existing_extensions.add(ext)

    # Check changed files for new extensions
    for entry in changed_files:
        parts = entry.split("\t", 1)
        if len(parts) == 2:
            status, filepath = parts
            if status.startswith("A") or status.startswith("?"):
                ext = os.path.splitext(filepath)[1]
                if ext and ext not in existing_extensions:
                    new_extensions.add(ext)

    return sorted(new_extensions)


def detect_deleted_files(changed_files: list[str]) -> list[str]:
    """Detect deleted files."""
    deleted = []
    for entry in changed_files:
        parts = entry.split("\t", 1)
        if len(parts) == 2:
            status, filepath = parts
            if status.startswith("D"):
                deleted.append(filepath)
    return deleted


def detect_config_changes(changed_files: list[str]) -> list[str]:
    """Detect modified configuration files."""
    config_patterns = [
        "package.json",
        "tsconfig.json",
        "pyproject.toml",
        "Cargo.toml",
        "go.mod",
        "Makefile",
        "Dockerfile",
        "docker-compose.yml",
        "docker-compose.yaml",
        ".eslintrc",
        ".prettierrc",
        "webpack.config",
        "vite.config",
        "next.config",
        "tailwind.config",
        "jest.config",
        "vitest.config",
        ".env.example",
        "requirements.txt",
        "setup.py",
        "setup.cfg",
    ]

    modified_configs = []
    for entry in changed_files:
        parts = entry.split("\t", 1)
        if len(parts) == 2:
            _, filepath = parts
            basename = os.path.basename(filepath)
            for pattern in config_patterns:
                if basename == pattern or basename.startswith(pattern):
                    modified_configs.append(filepath)
                    break
    return modified_configs


def count_changed_files(changed_files: list[str]) -> int:
    """Count the total number of changed files."""
    return len(changed_files)


def main():
    """Analyze changes and suggest documentation updates if significant."""
    try:
        # Read stdin (Stop event data) - consume it even if unused
        try:
            input_data = json.load(sys.stdin)
        except Exception:
            input_data = {}

        # Gather change information
        changed_files = get_changed_files()
        if not changed_files:
            # No changes detected, nothing to suggest
            sys.exit(0)

        suggestions = []

        # Check for new directories
        new_dirs = detect_new_directories(changed_files)
        for d in new_dirs:
            dir_name = d.split("/")[-1] if "/" in d else d
            suggestions.append(
                f"  - New directory '{d}/' created -> Document {dir_name} architecture in CLAUDE.md"
            )

        # Check for new file types
        new_types = detect_new_file_types(changed_files)
        type_labels = {
            ".rs": "Rust",
            ".go": "Go",
            ".py": "Python",
            ".ts": "TypeScript",
            ".tsx": "React/TSX",
            ".jsx": "React/JSX",
            ".vue": "Vue",
            ".svelte": "Svelte",
            ".rb": "Ruby",
            ".java": "Java",
            ".kt": "Kotlin",
            ".swift": "Swift",
            ".c": "C",
            ".cpp": "C++",
            ".zig": "Zig",
        }
        for ext in new_types:
            label = type_labels.get(ext, ext)
            suggestions.append(
                f"  - New file type '{ext}' ({label}) introduced -> Update stack info in CLAUDE.md"
            )

        # Check for deleted files
        deleted = detect_deleted_files(changed_files)
        if deleted:
            if len(deleted) <= 3:
                for f in deleted:
                    suggestions.append(
                        f"  - '{f}' deleted -> Check if removed feature needs doc cleanup"
                    )
            else:
                suggestions.append(
                    f"  - {len(deleted)} files deleted -> Review docs for removed features"
                )

        # Check for config changes
        config_changes = detect_config_changes(changed_files)
        for cfg in config_changes:
            basename = os.path.basename(cfg)
            suggestions.append(
                f"  - {basename} modified -> Update project dependencies/config section"
            )

        # Check for large refactors
        total_changed = count_changed_files(changed_files)
        if total_changed > 10:
            suggestions.append(
                f"  - {total_changed} files changed -> Consider running /project-starter:save-session-learnings"
            )

        # Stop fires every turn: show a given set of suggestions once per session
        if suggestions:
            text = "\n".join(suggestions)
            digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
            sid = re.sub(r"[^A-Za-z0-9_-]", "", str(input_data.get("session_id", "default"))) or "default"
            state_file = os.path.join(tempfile.gettempdir(), f"claude-doc-suggest-{sid}.txt")
            try:
                with open(state_file) as f:
                    seen = f.read().strip()
            except Exception:
                seen = ""
            if seen != digest:
                try:
                    with open(state_file, "w") as f:
                        f.write(digest)
                except Exception:
                    pass
                print(json.dumps({"systemMessage": "Documentation update suggested:\n" + text}))

    except Exception:
        # Never block on errors
        pass

    sys.exit(0)


if __name__ == "__main__":
    main()
