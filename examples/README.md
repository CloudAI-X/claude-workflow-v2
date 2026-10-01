# Multi-Agent Orchestration Examples

Learn how to use multiple agents together for complex software engineering tasks.

## Overview

The project-starter plugin includes 7 specialized agents that can work together:

| Agent | Purpose | Triggers On |
|-------|---------|-------------|
| **orchestrator** | Master coordinator for complex tasks | "implement", "add feature", multi-step tasks |
| **code-reviewer** | Quality, security, performance review | "review", "check", PR workflows |
| **debugger** | Root cause analysis | "debug", "fix", error messages |
| **security-auditor** | OWASP Top 10 vulnerability detection | "security", "audit", "vulnerabilities" |
| **test-architect** | Test strategy and implementation | "test", "coverage", "write tests" |
| **refactorer** | Code structure improvements | "refactor", "clean up", "improve" |
| **docs-writer** | Technical documentation | "document", "README", "explain" |

## Available Examples

### [Comprehensive Code Review](orchestration/comprehensive-code-review/) (Sequential)

A 6-agent sequential workflow for thorough code analysis:

```
orchestrator → code-reviewer → security-auditor → test-architect → refactorer → docs-writer
```

**Use when:** You want a complete quality assessment of code changes before merging.

**What you get:**
- Code quality findings
- Security vulnerabilities
- Test coverage recommendations
- Refactoring suggestions
- Documentation updates

---

### [Parallel Execution](orchestration/parallel-execution/) (Parallel)

N-agent parallel workflow for maximum speed:

```
     Orchestrator
          │
    ┌─────┼─────┬─────┬─────┐
    │     │     │     │     │
    ▼     ▼     ▼     ▼     ▼
 Agent  Agent Agent Agent Agent
    │     │     │     │     │
    └─────┴─────┴─────┴─────┘
          │
          ▼
   Results (delivered automatically)
          │
          ▼
     Synthesis
```

**Use when:** You have N independent tasks that can run simultaneously.

**What you get:**
- ~Nx speed improvement (N tasks in parallel)
- Same quality as sequential execution
- Unified synthesized results

**Key Rule:** ALL Agent tool calls (`Task` in older versions) MUST be in a SINGLE message for true parallelism. Results are delivered automatically when each background subagent finishes (`TaskOutput` is deprecated).

## How Orchestration Works

The **orchestrator** agent coordinates multi-agent workflows by:

1. **Understanding** - Analyzing the task and codebase
2. **Planning** - Creating a detailed task list
3. **Delegating** - Spawning specialist agents via the Task tool
4. **Integrating** - Combining results from all specialists
5. **Verifying** - Running tests and quality checks
6. **Delivering** - Summarizing changes and creating PRs

```
         User Request
              │
              ▼
     ┌────────────────┐
     │  Orchestrator  │  ← Plans and coordinates
     └───────┬────────┘
             │
    ┌────────┼────────┬───────────┐
    ▼        ▼        ▼           ▼
┌────────┐ ┌──────┐ ┌──────┐ ┌──────────┐
│ Code   │ │ Sec  │ │ Test │ │  Docs    │
│ Review │ │ Audit│ │ Arch │ │  Writer  │
└────────┘ └──────┘ └──────┘ └──────────┘
    │        │        │           │
    └────────┴────────┴───────────┘
              │
              ▼
      Aggregated Results
```

## Quick Start

1. **Load the plugin:**
   ```bash
   claude --plugin-dir /path/to/claude-workflow
   ```

2. **Choose an example** from the list above

3. **Follow the workflow guide** in the example's `workflow.md`

4. **Verify it works** using the example's `verification.md`

## Creating Your Own Workflows

You can create custom multi-agent workflows by:

1. Understanding which agents are available (see table above)
2. Defining the sequence/parallel execution pattern
3. Writing clear prompts that trigger the orchestrator
4. Including keywords that activate specialist agents

See the [orchestrator agent](../agents/orchestrator.md) for delegation patterns.
