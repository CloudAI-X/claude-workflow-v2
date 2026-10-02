#!/usr/bin/env bash
# Warn when git operations target protected branches.
# Informational only - never blocks operations.

INPUT=$(cat)

if command -v jq &> /dev/null; then
    COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null)
else
    COMMAND=$(echo "$INPUT" | grep -o '"command"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*: *"\([^"]*\)".*/\1/')
fi

if [[ -z "$COMMAND" ]]; then
    exit 0
fi

if ! echo "$COMMAND" | grep -qE 'git (commit|push)'; then
    exit 0
fi

CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)

if [[ -z "$CURRENT_BRANCH" ]]; then
    exit 0
fi

PROTECTED_BRANCHES=("main" "master" "production")

for BRANCH in "${PROTECTED_BRANCHES[@]}"; do
    if [[ "$CURRENT_BRANCH" == "$BRANCH" ]]; then
        # Plain stdout on exit 0 only reaches the debug log, so pass the
        # warning to Claude as additionalContext. $BRANCH is one of the
        # literals above, so it is safe to embed in JSON.
        printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","additionalContext":"%s"}}\n' \
            "WARNING: You are on protected branch '$BRANCH'. Create a feature branch (git checkout -b feature/your-change) or use /project-starter:sync-branch before committing or pushing."
        exit 0
    fi
done

exit 0
