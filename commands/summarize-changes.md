---
allowed-tools: Bash(git:*)
description: Summarize recent changes for standup, PR, or documentation
argument-hint: "[today|week|branch|pr] (default: today)"
---

## Context

- Current branch: !`git branch --show-current`
- Default branch: !`git remote show origin 2>/dev/null | grep 'HEAD branch' | cut -d' ' -f5 || echo "main"`
- Git user: !`git config user.email 2>/dev/null || echo "unknown"`
- Today's commits (all authors): !`git log --oneline --since="midnight" 2>/dev/null || echo "No commits today"`
- This week's commits (all authors): !`git log --oneline --since="1 week ago" 2>/dev/null | head -20`
- Branch commits (vs origin's default branch): !`git log --oneline origin/HEAD..HEAD 2>/dev/null | head -20`
- Files changed on branch: !`git diff --stat origin/HEAD...HEAD 2>/dev/null | tail -5`

## Task

Generate a clear, concise summary based on the scope:

1. **today**: What I did today (for standup)
2. **week**: Weekly summary (for reports)
3. **branch**: All changes on this branch (for PR)
4. **pr**: Full PR description with sections

For **today** and **week**, report only the git user's own commits: re-run the log with `--author=<git user>` using the address shown above. If the two branch lists above are empty, compute them against the default branch shown above.

Format the output as:
- **Summary**: 1-2 sentence overview
- **Changes**: Bullet list of key changes
- **Files**: Main files affected
- **Impact**: What this enables or fixes

Scope: $ARGUMENTS
