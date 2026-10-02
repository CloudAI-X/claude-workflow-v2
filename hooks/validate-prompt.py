#!/usr/bin/env python3
"""
UserPromptSubmit hook - Validates user prompts before processing.
Can provide warnings or context to Claude based on the prompt content.
"""
import json
import re
import sys

# Keywords that might benefit from specific agent involvement
AGENT_HINTS = {
    r"\b(review|check|look at)\b.*\b(code|changes|pr|pull request)\b": "Tip: Consider using the code-reviewer agent for thorough code reviews.",
    r"\b(bug|error|crash|fail|broken)\b": "Tip: The debugger agent specializes in systematic root cause analysis.",
    r"\b(test|coverage|spec)\b": "Tip: The test-architect agent can help design comprehensive test strategies.",
    r"\b(security|auth|vulnerab\w*|owasp)\b": "Tip: The security-auditor agent can perform OWASP Top 10 checks.",
    r"\b(refactor|clean|improve|simplify)\b.*\b(code)\b": "Tip: The refactorer agent specializes in code structure improvements.",
    r"\b(document|readme|api docs)\b": "Tip: The docs-writer agent creates clear technical documentation.",
}

# Dangerous command patterns to warn about
DANGEROUS_PATTERNS = [
    (r"\brm\s+-rf\s+[/~]", "⚠️ Warning: Recursive delete from root/home detected"),
    (
        r"\bgit\s+push\s+.*--force",
        "⚠️ Warning: Force push detected - this rewrites history",
    ),
    (r"\bgit\s+reset\s+--hard", "⚠️ Warning: Hard reset will lose uncommitted changes"),
    (r"\bdrop\s+database\b", "⚠️ Warning: DROP DATABASE command detected"),
    (r"\btruncate\s+table\b", "⚠️ Warning: TRUNCATE TABLE will delete all data"),
]


def validate_prompt(prompt):
    """Validate the user prompt and provide helpful context."""
    messages = []

    prompt_lower = prompt.lower()

    # Check for agent hints
    for pattern, hint in AGENT_HINTS.items():
        if re.search(pattern, prompt_lower):
            messages.append(hint)
            break  # Only show one hint

    # Check for dangerous patterns
    for pattern, warning in DANGEROUS_PATTERNS:
        if re.search(pattern, prompt_lower, re.IGNORECASE):
            messages.append(warning)

    return messages


def main():
    try:
        input_data = json.load(sys.stdin)
        prompt = input_data.get("prompt", "")

        if not prompt:
            sys.exit(0)

        messages = validate_prompt(prompt)

        if messages:
            for msg in messages:
                print(msg)

        # UserPromptSubmit hooks should not block normal prompts
        sys.exit(0)

    except Exception as e:
        # Don't block on errors
        sys.exit(0)


if __name__ == "__main__":
    main()
