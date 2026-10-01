# Comprehensive Code Review - Workflow Guide

Exact prompts and expected behavior for the 6-agent code review workflow.

## The Workflow

### Step 1: Initiate the Review

Copy and paste this prompt (customize the bracketed parts):

```
I need a comprehensive review of [describe scope - e.g., "the recent changes",
"the auth module", "PR #123"].

Please:
1. Review code quality and patterns
2. Audit for security vulnerabilities
3. Analyze test coverage
4. Identify refactoring opportunities
5. Check documentation completeness

Provide a prioritized summary of findings with actionable recommendations.
```

### Step 2: Watch the Orchestration

The orchestrator agent will activate and create a plan:

```
[orchestrator agent activated]

I'll coordinate a comprehensive review. Let me create a plan:

Todo List:
1. [ ] Explore the codebase to understand scope
2. [ ] Delegate to code-reviewer for quality analysis
3. [ ] Delegate to security-auditor for vulnerability scan
4. [ ] Delegate to test-architect for coverage analysis
5. [ ] Delegate to refactorer for improvement suggestions
6. [ ] Delegate to docs-writer for documentation review
7. [ ] Synthesize all findings into summary
```

### Step 3: Agent Delegation

You'll see each specialist agent activate:

```
[orchestrator]: Delegating code quality review...

[code-reviewer agent activated]
Analyzing 12 files for quality issues...
→ Found 3 critical, 5 warnings
→ Report complete

[orchestrator]: Delegating security audit...

[security-auditor agent activated]
Running OWASP Top 10 checks...
→ Found 1 high, 2 medium severity issues
→ Report complete

[orchestrator]: Delegating test analysis...

[test-architect agent activated]
Analyzing test coverage...
→ Current coverage: 67%
→ Identified 8 untested code paths
→ Report complete

[orchestrator]: Delegating refactoring analysis...

[refactorer agent activated]
Scanning for technical debt...
→ Found 4 refactoring opportunities
→ Report complete

[orchestrator]: Delegating documentation review...

[docs-writer agent activated]
Checking documentation completeness...
→ Found 2 missing sections
→ Report complete
```

### Step 4: Final Summary

The orchestrator synthesizes all findings:

```
[orchestrator]: Synthesizing results...

## Comprehensive Review Summary

### Critical (Fix Before Merge)
1. **SQL Injection** in `src/api/users.js:45` - Use parameterized queries
2. **Missing auth check** in `src/routes/admin.js:23` - Add middleware

### High Priority
3. **No tests** for payment processing module
4. **Hardcoded config** should use environment variables

### Medium Priority
5. **Code duplication** in validation logic
6. **Missing JSDoc** for public API functions

### Low Priority
7. **Inconsistent naming** in utility functions
8. **Outdated README** sections

---
Total: 2 critical, 2 high, 2 medium, 2 low
Estimated fix time: 2-4 hours
```

## Alternative: Manual Step-by-Step

If you prefer more control, invoke each agent separately:

```
> Review the code quality of src/api/*.js

[code-reviewer activates]
[wait for report]

> Now audit these files for security issues

[security-auditor activates]
[wait for report]

> What tests should we add?

[test-architect activates]
[wait for report]

> Any refactoring suggestions?

[refactorer activates]
[wait for report]

> Check if documentation is complete

[docs-writer activates]
[wait for report]
```

## Iteration

After receiving the summary, you can ask for more details:

```
> Tell me more about the SQL injection finding

> Show me exactly how to fix the auth check issue

> Generate the missing tests for payment processing
```

## Creating a Slash Command

To make this a reusable command in your project:

1. Create `.claude/commands/comprehensive-review.md` in your project:

```markdown
---
description: Run comprehensive 6-agent code review
argument-hint: <scope - e.g., "recent changes", "auth module">
---

Review $ARGUMENTS comprehensively.

Check:
1. Code quality and patterns
2. Security vulnerabilities
3. Test coverage
4. Refactoring opportunities
5. Documentation completeness

Provide prioritized findings with actionable recommendations.
```

2. Invoke with: `/comprehensive-review the auth module`
