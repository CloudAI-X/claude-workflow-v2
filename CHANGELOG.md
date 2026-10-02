# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.7] - 2026-10-02

### Security

- `protect-files.py` now protects `.git/` and warns on `.github/workflows/` for the absolute paths Claude Code actually sends (the patterns only matched relative paths before), and blocks every `.env.*` file except the `.env.example`, `.env.template` and `.env.sample` templates.
- `security-check.py` no longer skips secret scanning for any path that merely contains "test" or "spec" (for example a project folder named `latest-app`). Test and fixture locations are now matched on whole path segments and file-name conventions. Added the current OpenAI (`sk-proj-…`) and Anthropic key shapes.
- `format-on-edit.py` and `typescript-check.py` no longer call `npx`. They run the project's own `node_modules/.bin` tool (or one on `PATH`) and skip silently otherwise. Outside a TTY, `npx tsc` downloaded and ran an unrelated npm package named `tsc`.
- `security-patterns` skill: corrected examples that taught insecure code (mass assignment from `req.body`, bcrypt's 72-byte limit, OAuth without PKCE/`state`, login timing that reveals which emails exist, a zod `trim()` applied after the length check, unpinned JWT algorithm).
- `security-scan` command: the secret-detection greps used basic regular expressions and matched nothing; they now use `-E`, scan `.env`, JSON, YAML and JSX/TSX files, and exclude `.git` and `node_modules` by directory.

### Fixed

- **Hook warnings were invisible.** `pre-commit-check.py`, `branch-protection.sh`, `typescript-check.py`, the warning path of `protect-files.py`, `verify-on-complete.py` and `suggest-doc-updates.py` printed plain text and exited 0, which Claude Code only writes to its debug log. They now return JSON: `hookSpecificOutput.additionalContext` to inform Claude, `systemMessage` to inform the user.
- **Six commands aborted before reaching the model** in the default permission mode (`add-tests`, `commit-push-pr`, `quick-fix`, `refactor-guided`, `summarize-changes`, `sync-branch`), and `commit` aborted in a repository with no commits, because their `` !`…` `` context commands failed Claude Code's permission pre-check or exited non-zero. The context commands are now simple read-only forms.
- **npm installer did not activate hooks.** `npx install-claude-workflow-v2` copied the hook scripts to `.claude/hooks/` but never registered them. It now merges them into `.claude/settings.json` (additive, idempotent, existing settings untouched).
- `argument-hint` values are quoted strings in all ten commands that used a bare `[...]` (a YAML list, and a parse error in three files), so strict loaders such as GitHub Copilot CLI load them again (#24).
- `hooks/hooks.json` quotes `${CLAUDE_PLUGIN_ROOT}` so a plugin path containing spaces works.
- `suggest-doc-updates.py` reported "New directory created" for every new file in an existing directory, counted the plugin's own log files as project changes, and would have repeated the same suggestions every turn; it now reports only genuinely new top-level directories, once per session, and ignores `.claude/`.
- `validate-prompt.py`: the security hint never matched "vulnerability".
- `verify-on-complete.py` detects Bun's text lockfile (`bun.lock`).
- `track-metrics.py` crashed on Python 3.8 (type hints evaluated at import); `branch-protection.sh` and `log-commands.sh` no longer print a `jq` parse error on malformed input.
- `templates/mcp.json.template` pointed at eight npm packages that do not exist; it now uses the vendors' remote MCP endpoints and the maintained `@modelcontextprotocol` packages. `templates/settings.local.json.template` no longer installs a hook that relied on a non-existent `$CLAUDE_FILE_PATH` variable.
- Skills: corrected examples that did not work as written in `devops-infrastructure` (GHCR push without login or permission, Postgres containers without a password, dev dependencies left in the image, `uv sync` before the source is copied, end-of-life Node 20), `database-design` (zero-downtime migration lost writes, keyset pagination without a tie-breaker, trigger never attached), `error-handling` (pino calls that dropped their fields, a retry example that never retried), `optimizing-performance`, `designing-tests`, `designing-apis`, `managing-git`, `web-design-guidelines` and `vercel-react-best-practices` (two SWR imports that do not exist).
- Documentation: plugin install commands (`claude plugin marketplace add` + `project-starter@claude-workflow`), hook table triggers and behaviour, `/install-github-app`, `claude plugin validate` usage, the contributor hook-registration example, changelog years for 1.0.0 and 1.1.0, the privacy policy's description of the local command and metrics logs, and the security policy, which now points to private vulnerability reporting.

### Changed

- `orchestrator` agent: delegates when auto-delegated as a subagent (current Claude Code allows nested subagents), and task tracking no longer depends on `TodoWrite`.
- `parallel-execution` skill and the orchestration examples describe the current `Agent` tool (`Task` remains an alias), automatic delivery of background subagent results, and running dependent work in a second wave.
- `commit-push-pr` refuses to commit or push on the default branch without creating a feature branch or asking first. `dependency-upgrade` and `refactor-guided` stop on a dirty working tree instead of stashing or committing the user's changes.
- The four "output styles" are described as mode commands, which is what they are.
- CI: also validates hook script references in `hooks/hooks.json`, that `argument-hint` values are strings, and that the version agrees across all manifests and the changelog. `actions/checkout` updated to v7.0.1.

## [2.0.6] - 2026-02-14

First 2.x release. This entry consolidates the 2.0.x line, which shipped rapidly
after 1.2.0 and was not previously recorded here.

### Added

- **skills.sh cross-agent compatibility** — the workflow can be distributed to 38+ AI coding agents.
- **npm installer** (`packages/add-skill`) — `npx install-claude-workflow-v2` installs the plugin's agents, commands, skills, and hooks into a project.
- **Codex-compatible plugin artifacts** — `.codex/` and `.codex-plugin/` mirror the seven agents and 8 of the 14 hooks for Codex-compatible clients, with a CI validation workflow.

### Changed

- Plugin, marketplace, and npm package versions reconciled at `2.0.6` (across `plugin.json`, `marketplace.json`, and `package.json`).
- Reworked the `verify-on-complete.py` Stop hook.
- Refreshed the `error-handling` and `security-patterns` skills.

### Fixed

- Resolved a batch of audit findings across agents, hooks, skills, and documentation.
- `security-check.py` no longer blocks documentation/example files that contain illustrative credential strings, and routes its block reason to stderr so Claude receives it.
- Restored the `convex-backend` and `vercel-react-best-practices` skill reference documents (`AGENTS.md`) that two SKILL.md files link to.
- Removed references to the deprecated `TaskOutput` tool from the orchestrator agent and parallel commands.

## [1.2.0] - 2026-02-14

### Added

- **4 New Skills**
  - `database-design` - Schema design, indexing strategies, query optimization, migrations
  - `devops-infrastructure` - Docker, CI/CD, deployment strategies, IaC, monitoring
  - `error-handling` - Error patterns by language, structured logging, retry/circuit breakers
  - `security-patterns` - JWT/OAuth auth, RBAC, secrets management, CORS, rate limiting

- **7 New Commands**
  - `/project-starter:refactor-guided` - 4-phase systematic refactoring with safety rules
  - `/project-starter:dependency-upgrade` - Safe dependency upgrades with rollback
  - `/project-starter:plan` - Manus-style persistent PLAN.md with phase tracking
  - `/project-starter:tutorial` - Interactive guided tutorial for first-time users
  - `/project-starter:bootstrap-repo` - 10-agent parallel repo exploration and CODEBASE.md generation
  - `/project-starter:save-session-learnings` - Persist session discoveries to CLAUDE.md/AGENTS.md
  - `/project-starter:metrics` - View agent performance metrics and session history

- **5 New Hooks**
  - `pre-commit-check.py` - Detects debug statements, temp markers, large file content
  - `branch-protection.sh` - Warns on git operations targeting protected branches
  - `typescript-check.py` - Runs `tsc --noEmit` after editing .ts/.tsx files
  - `suggest-doc-updates.py` - Suggests CLAUDE.md updates when significant changes detected
  - `track-metrics.py` - Logs session telemetry to `.claude/agent-metrics.jsonl`

- **On-Demand Context Loading**
  - All 14 skills now include "When to Load" sections with trigger/skip conditions

- **CI/CD Pipeline**
  - `.github/workflows/validate.yml` - Plugin validation (JSON, scripts, frontmatter, links)

### Changed

- **All 7 Agents Upgraded** with:
  - Action-first directive (act before explaining)
  - Adaptive effort scaling (Instant/Light/Deep/Exhaustive)
  - Adversarial self-review protocol (5-point checklist)
  - Intellectual honesty framework (Certain/Likely/Uncertain)
  - Expanded auto-trigger keywords
  - Paired WRONG/CORRECT anti-pattern examples for each domain
- **`web-design-guidelines` skill** rewritten as self-contained 190-line reference (was 37-line external URL dependency)
- **Hook error messages** now include actionable remediation suggestions across all hooks
- **`debugger` agent** gains escalation protocol (after 3 failed attempts: web search, backtrack)
- **`security-auditor` agent** gains dependency vulnerability checking section

---

## [1.1.0] - 2026-01-07

### Added

- **Parallel Execution Support**
  - Orchestrator can now spawn N subagents simultaneously for N independent tasks
  - Uses `run_in_background: true` with Task tool for concurrent execution
  - Results collected via TaskOutput after all agents complete
  - Roughly Nx faster than sequential execution

- **New Commands**
  - `/project-starter:parallel-review` - Review multiple directories in parallel
  - `/project-starter:parallel-analyze` - Analyze code from architecture, security, performance, and testing perspectives simultaneously

- **New Skill**
  - `parallel-execution` - Patterns for spawning dynamic subagents, best practices for parallelization, and TodoWrite integration

### Changed

- Updated orchestrator agent with Parallel Execution Protocol section
- Enhanced verify-changes command with explicit parallel syntax
- Added parallel execution examples and diagrams to documentation

---

## [1.0.0] - 2026-01-01

### Added

- **7 Specialized Agents**
  - `orchestrator` - Coordinate complex multi-step tasks
  - `code-reviewer` - Review code quality and best practices
  - `debugger` - Systematic bug investigation and fixing
  - `docs-writer` - Create technical documentation
  - `security-auditor` - Security vulnerability detection
  - `refactorer` - Code structure improvements
  - `test-architect` - Design comprehensive test strategies

- **6 Knowledge Skills**
  - `project-analysis` - Understand any codebase structure and patterns
  - `testing-strategy` - Design test approaches (unit, integration, E2E)
  - `architecture-patterns` - System design guidance
  - `performance-optimization` - Speed up applications, identify bottlenecks
  - `git-workflow` - Version control best practices
  - `api-design` - REST/GraphQL API patterns

- **4 Output Styles**
  - `/project-starter:architect` - System design mode
  - `/project-starter:rapid` - Fast development mode
  - `/project-starter:mentor` - Learning/teaching mode
  - `/project-starter:review` - Code review mode

- **8 Automation Hooks**
  - Security scan (blocks commits with potential secrets)
  - File protection (blocks edits to lock files, .env, .git)
  - Auto-format (runs prettier/black/gofmt based on file type)
  - Command logging (logs to `.claude/command-history.log`)
  - Environment check (validates Node.js, Python, Git)
  - Prompt analysis (suggests appropriate agents)
  - Input notification (desktop notification when input needed)
  - Complete notification (desktop notification when task finishes)

- Cross-platform notification support (macOS, Linux, Windows)
- Comprehensive documentation (README, PERMISSIONS, MCP servers guide)
- MIT License

[2.0.7]: https://github.com/CloudAI-X/claude-workflow-v2/releases/tag/v2.0.7
[2.0.6]: https://github.com/CloudAI-X/claude-workflow-v2/releases/tag/v2.0.6
[1.2.0]: https://github.com/CloudAI-X/claude-workflow-v2/releases/tag/v1.2.0
[1.1.0]: https://github.com/CloudAI-X/claude-workflow-v2/releases/tag/v1.1.0
[1.0.0]: https://github.com/CloudAI-X/claude-workflow-v2/releases/tag/v1.0.0
