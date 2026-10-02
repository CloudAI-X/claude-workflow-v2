# Security Policy

## Reporting a Vulnerability

If you discover a security issue in the plugin surfaces shipped by this repository (Claude Code or Codex), please report it privately through [GitHub's private vulnerability reporting](https://github.com/CloudAI-X/claude-workflow-v2/security/advisories/new) (Security → Report a vulnerability). Please do not open a public issue for an undisclosed vulnerability.

## Scope

This policy covers the plugin surfaces shipped by this repository for both
Claude Code and Codex-compatible clients:

- `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`
- `agents/*.md` and `commands/*.md`
- `.codex-plugin/plugin.json`, `.codex/config.toml`, `.codex/agents/*.toml`, `.codex/hooks.json`
- `skills/*/SKILL.md`
- Hook scripts under `hooks/`
- The npm installer under `packages/add-skill/` (published as `install-claude-workflow-v2`)
- Configuration templates under `templates/`

## Response

We will triage credible reports, reproduce the issue, and ship a fix or mitigation as quickly as practical.
