---
allowed-tools: Bash(git:*), Bash(gh:*)
description: Commit staged changes, push to remote, and create a pull request
argument-hint: "[optional PR title or description hint]"
---

## Context

- Current branch: !`git branch --show-current`
- Default branch: !`git remote show origin 2>/dev/null | grep 'HEAD branch' | cut -d' ' -f5 || echo "main"`
- Git status: !`git status --short`
- Staged diff: !`git diff --cached`
- Unstaged diff: !`git diff`
- Commits ahead of origin: !`git log '@{u}..HEAD' --oneline 2>/dev/null || echo "No upstream branch"`
- Recent commits for style: !`git log --oneline -5 2>/dev/null || echo "No commits yet"`

## Task

Execute the full git workflow:

1. **Branch check**: If the current branch is the default branch (see the context above), do not commit or push to it. Create a feature branch first (`git checkout -b feature/<short-description>`), or stop and ask if the user really wants to work on the default branch.
2. **Commit**: If there are staged changes, create a conventional commit
3. **Push**: Push the current branch to origin (set upstream if needed)
4. **PR**: Create a pull request using `gh pr create`
   - Auto-generate title from commits
   - Include a summary of changes in the PR body
   - Link any related issues mentioned in commits

If any step fails, stop and report the issue.

$ARGUMENTS
