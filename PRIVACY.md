# Privacy Policy

This repository publishes a Claude Code plugin (also packaged with a Codex-compatible manifest) and related plugin resources for local installation in Claude Code or Codex-compatible clients.

## Data Handling

- The plugin bundle in this repository does not include a hosted backend or telemetry service.
- Any data access performed by installed skills, hooks, or local scripts happens in the user's own Claude Code (or Codex) session and local environment.
- Hook scripts run local tools only (git, and the project's own formatter, type checker, test and lint commands) and make no network requests of their own.
- Two hooks write plain-text logs inside the project: `log-commands.sh` appends every Bash command Claude runs to `.claude/command-history.log`, and `track-metrics.py` appends a timestamp, the changed-file count and the latest commit to `.claude/agent-metrics.jsonl` at the end of each turn. These files stay on your machine and are never rotated or uploaded. A secret typed into a command is logged as written, so keep both files out of version control (add them to `.gitignore`).

## Credentials

- Secrets are expected to be supplied by the user through local environment configuration.
- This repository should not be used to store production secrets or personal access tokens.

## Contact

For privacy questions, open an issue in this repository.
