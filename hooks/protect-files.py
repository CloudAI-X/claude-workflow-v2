#!/usr/bin/env python3
"""
Protect sensitive files from modification.
Blocks edits to production configs, lock files, and sensitive directories.
"""
import json
import sys
import os
import fnmatch

# Files/patterns to protect (exit code 2 = block)
# Each entry is (pattern, reason) for actionable messages
PROTECTED_PATTERNS_WITH_REASONS = [
    # Lock files (usually shouldn't be manually edited)
    ('package-lock.json', "Lock files should be updated via package manager (npm install), not edited directly"),
    ('yarn.lock', "Lock files should be updated via package manager (yarn install), not edited directly"),
    ('pnpm-lock.yaml', "Lock files should be updated via package manager (pnpm install), not edited directly"),
    ('Gemfile.lock', "Lock files should be updated via package manager (bundle install), not edited directly"),
    ('poetry.lock', "Lock files should be updated via package manager (poetry lock), not edited directly"),
    ('Cargo.lock', "Lock files should be updated via package manager (cargo update), not edited directly"),

    # Sensitive files
    ('.env', ".env files contain secrets — edit manually outside of Claude Code"),
    ('.env.local', ".env files contain secrets — edit manually outside of Claude Code"),
    ('.env.production', ".env files contain secrets — edit manually outside of Claude Code"),
    ('.env.*', ".env files contain secrets — edit manually outside of Claude Code"),
    ('**/secrets/*', "Secrets directory contains sensitive data — manage outside of Claude Code"),
    ('**/credentials/*', "Credentials directory contains sensitive data — manage outside of Claude Code"),

    # Git internals
    ('.git/*', ".git directory is managed by Git — never edit directly"),

    # CI/CD (warn but don't block)
    # '.github/workflows/*',
]

# Flat list for backward-compatible matching
PROTECTED_PATTERNS = [p for p, _ in PROTECTED_PATTERNS_WITH_REASONS]

# Map pattern to reason for lookup
PROTECTED_REASONS = {p: r for p, r in PROTECTED_PATTERNS_WITH_REASONS}

# Files that should warn but not block
WARN_PATTERNS = [
    '.github/workflows/*',
    'docker-compose.yml',
    'Dockerfile',
    '**/production/*',
]

# Env templates hold placeholders, not secrets — never block these
UNPROTECTED_BASENAMES = {'.env.example', '.env.template', '.env.sample'}

def matches_pattern(file_path, patterns):
    """Check if file matches any protected pattern."""
    file_path = file_path.replace('\\', '/')
    # Strip a single leading "./" prefix. Do NOT use lstrip('./') — it treats
    # './' as a character set and would eat leading dots, turning ".env" into
    # "env" and silently defeating dotfile protection.
    if file_path.startswith('./'):
        file_path = file_path[2:]
    if os.path.basename(file_path) in UNPROTECTED_BASENAMES:
        return None
    # Claude Code sends absolute paths, so also try every trailing sub-path:
    # "/repo/.git/config" has to match the relative pattern ".git/*", and the
    # last sub-path is the basename.
    parts = [p for p in file_path.split('/') if p]
    candidates = [file_path] + ['/'.join(parts[i:]) for i in range(len(parts))]
    for pattern in patterns:
        if any(fnmatch.fnmatch(c, pattern) for c in candidates):
            return pattern
    return None

def main():
    try:
        input_data = json.load(sys.stdin)
        file_path = input_data.get('tool_input', {}).get('file_path', '')
        
        if not file_path:
            sys.exit(0)
        
        # Check for blocked patterns
        blocked = matches_pattern(file_path, PROTECTED_PATTERNS)
        if blocked:
            reason = PROTECTED_REASONS.get(blocked, "This file is protected from edits")
            # Exit 2 blocks the tool call; Claude Code reads the reason from
            # stderr and ignores stdout on exit 2.
            print(f"BLOCKED: {file_path}", file=sys.stderr)
            print(f"   Matches protected pattern: {blocked}", file=sys.stderr)
            print(f"   Reason: {reason}", file=sys.stderr)
            print(
                "   Edit this file outside Claude Code, or adjust PROTECTED_PATTERNS "
                "in protect-files.py if this is intentional.",
                file=sys.stderr,
            )
            sys.exit(2)  # Block the operation
        
        # Check for warning patterns
        warned = matches_pattern(file_path, WARN_PATTERNS)
        if warned:
            # Don't block, just warn. Plain stdout on exit 0 only reaches the
            # debug log, so pass the warning to Claude as additionalContext.
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "additionalContext": (
                        f"WARNING: editing sensitive file {file_path} "
                        f"(matches pattern: {warned}). Double-check this change is intended."
                    ),
                }
            }))
            sys.exit(0)
            
    except Exception:
        sys.exit(0)

if __name__ == '__main__':
    main()
