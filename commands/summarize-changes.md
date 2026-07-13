---
allowed-tools: Bash(git:*)
description: Summarize recent changes for standup, PR, or documentation
argument-hint: "[today|week|branch|pr] (default: today)"
---

## Context

- Current branch: !`git branch --show-current`
- Default branch: !`git remote show origin 2>/dev/null | grep 'HEAD branch' | cut -d' ' -f5 || echo "main"`
- Today's commits: !`git log --oneline --since="midnight" --author="$(git config user.email)" 2>/dev/null || echo "No commits today"`
- This week's commits: !`git log --oneline --since="1 week ago" --author="$(git config user.email)" 2>/dev/null | head -20 || echo "No commits this week"`
- Branch commits (vs main): !`git log --oneline $(git remote show origin 2>/dev/null | grep 'HEAD branch' | cut -d' ' -f5 || echo "main")..HEAD 2>/dev/null | head -20 || echo "No branch commits"`
- Files changed on branch: !`git diff --stat $(git merge-base HEAD origin/$(git remote show origin 2>/dev/null | grep 'HEAD branch' | cut -d' ' -f5 || echo "main"))..HEAD 2>/dev/null | tail -5 || echo "No changes"`

## Task

Generate a clear, concise summary based on the scope:

1. **today**: What I did today (for standup)
2. **week**: Weekly summary (for reports)
3. **branch**: All changes on this branch (for PR)
4. **pr**: Full PR description with sections

Format the output as:
- **Summary**: 1-2 sentence overview
- **Changes**: Bullet list of key changes
- **Files**: Main files affected
- **Impact**: What this enables or fixes

Scope: $ARGUMENTS
