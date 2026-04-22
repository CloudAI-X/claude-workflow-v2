---
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task
description: Multi-perspective analysis using parallel subagents. Analyzes code from architecture, security, performance, and testing viewpoints simultaneously.
argument-hint: <file or directory to analyze, e.g., "src/api">
---

# Parallel Multi-Perspective Analysis

Analyze `$ARGUMENTS` from multiple perspectives simultaneously using parallel subagents.

## Process

1. **Identify Target**: Parse the file or directory to analyze
2. **Spawn Perspective Agents**: Launch 4 parallel subagents (one per perspective)
3. **Collect Results**: Retrieve all analyses via TaskOutput
4. **Synthesize**: Merge findings into unified recommendations

## Execution Pattern

**CRITICAL**: Launch ALL Task calls in a SINGLE message for true parallelism.

For the target, spawn 4 perspective-based subagents with `run_in_background: true`:

```
I'm launching 4 parallel analysis agents:

[Task 1]
description: "Architecture analysis"
prompt: "You are a software architect analyzing [target]. Evaluate:
- Component structure and boundaries
- Dependency patterns and coupling
- Design pattern usage
- Layering and separation of concerns
- Scalability considerations
- SOLID principle adherence

Provide findings with file:line references and improvement suggestions."
run_in_background: true

[Task 2]
description: "Security analysis"
prompt: "You are a security auditor analyzing [target]. Check for:
- OWASP Top 10 vulnerabilities
- Input validation gaps
- Authentication/authorization issues
- Hardcoded secrets or credentials
- Injection vulnerabilities (SQL, XSS, command)
- Insecure dependencies

Provide findings with severity levels (Critical/High/Medium/Low)."
run_in_background: true

[Task 3]
description: "Performance analysis"
prompt: "You are a performance engineer analyzing [target]. Look for:
- Algorithmic complexity issues (O(n²), O(n!))
- N+1 query patterns
- Memory leaks or inefficient allocations
- Blocking operations in async contexts
- Missing caching opportunities
- Unnecessary computations

Provide findings with estimated impact levels."
run_in_background: true

[Task 4]
description: "Testing analysis"
prompt: "You are a test architect analyzing [target]. Evaluate:
- Test coverage gaps
- Missing edge case tests
- Untested error paths
- Integration test opportunities
- Test code quality
- Mocking strategy effectiveness

Provide recommendations for improving test coverage."
run_in_background: true
```

After all complete, retrieve results:
```
TaskOutput: task_1_id
TaskOutput: task_2_id
TaskOutput: task_3_id
TaskOutput: task_4_id
```

## Output Format

```markdown
## Multi-Perspective Analysis: [Target]

### Summary
- **Perspectives analyzed**: 4
- **Total findings**: X
- **Critical issues**: Y
- **Execution time**: ~Zs (parallel)

---

### Architecture Perspective

#### Strengths
- [Pattern/decision] - [Why it's good]

#### Concerns
- [Issue] at file:line - [Description]
- [Issue] at file:line - [Description]

#### Recommendations
- [Improvement] - [Rationale]

---

### Security Perspective

#### Critical
- [Vulnerability] at file:line - [Impact]

#### High
- [Issue] at file:line - [Description]

#### Medium/Low
- [Issue] at file:line - [Description]

---

### Performance Perspective

#### High Impact
- [Bottleneck] at file:line - [Complexity/Impact]

#### Medium Impact
- [Issue] at file:line - [Description]

#### Optimization Opportunities
- [Opportunity] at file:line - [Expected improvement]

---

### Testing Perspective

#### Coverage Gaps
- [Untested area] - [Priority]

#### Missing Test Cases
- [Function/path] - [Suggested tests]

#### Quality Improvements
- [Issue in tests] - [Recommendation]

---

### Cross-Perspective Synthesis

#### Priority Actions (Ordered)
1. **[Highest priority]** - [From perspective] - [Why]
2. **[Second priority]** - [From perspective] - [Why]
3. **[Third priority]** - [From perspective] - [Why]

#### Interconnected Issues
- [Issue A] affects [Issue B]: [Explanation]

#### Recommended Approach
1. [First action to take]
2. [Second action to take]
3. [Third action to take]
```

## Example Usage

```
/project-starter:parallel-analyze src/api
```

This spawns 4 parallel analysts (architecture, security, performance, testing), completing in ~1/4 the time of sequential analysis.

## When to Use

- Before major refactoring efforts
- During architecture reviews
- Pre-release quality gates
- Technical debt assessment
- Code audit preparation
- New developer onboarding (understand quality state)

## Perspective Details

| Perspective | Focus Areas | Severity Levels |
|-------------|-------------|-----------------|
| Architecture | Structure, patterns, coupling | Concern, Suggestion |
| Security | Vulnerabilities, OWASP | Critical, High, Medium, Low |
| Performance | Complexity, bottlenecks | High, Medium, Optimization |
| Testing | Coverage, quality | Gap, Missing, Improvement |
