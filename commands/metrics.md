---
allowed-tools: Read, Bash, Glob
description: "Summarise the per-turn records written by the track-metrics hook: activity over time, files changed, and latest commits."
---

## Context

- Metrics file: !`cat .claude/agent-metrics.jsonl 2>/dev/null || echo "NO_METRICS_FILE"`

## Task

Analyze the recorded metrics and present a summary.

**If the metrics file does not exist or the context above shows "NO_METRICS_FILE":**
Print exactly: "No metrics recorded yet. Metrics are automatically collected after each turn."

**If metrics data exists**, parse each JSON line and present:

1. **Overview**
   - Total turns logged (the hook writes one record each time Claude finishes responding)
   - Turns in the last 7 days (compare timestamps to now)
   - Average files changed per turn

2. **Recent Turns** (last 10)
   Format as a markdown table:

   | #   | Timestamp (UTC) | Files Changed | Commit |
   | --- | --------------- | ------------- | ------ |
   - Show the most recent 10 turns, newest first
   - For "Commit", show the short commit message or "—" if none

3. **Patterns**
   - Note any trends (e.g., turns with many file changes, frequency of commits)
   - If there are turns with 0 files changed, note how many were "no-op" turns

Keep the output concise and well-formatted.
