#!/usr/bin/env bash
# Log all bash commands executed by Claude for auditing
LOG_FILE="${CLAUDE_PROJECT_DIR:-$(pwd)}/.claude/command-history.log"
mkdir -p "$(dirname "$LOG_FILE")"

# Read JSON from stdin
INPUT=$(cat)

# Extract command using jq if available, otherwise use grep
if command -v jq &> /dev/null; then
    COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null)
    DESCRIPTION=$(echo "$INPUT" | jq -r '.tool_input.description // "No description"' 2>/dev/null)
else
    COMMAND=$(echo "$INPUT" | grep -o '"command"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*: *"\([^"]*\)".*/\1/')
    DESCRIPTION="(jq not installed)"
fi

if [ -n "$COMMAND" ]; then
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$TIMESTAMP] $COMMAND" >> "$LOG_FILE"
fi
