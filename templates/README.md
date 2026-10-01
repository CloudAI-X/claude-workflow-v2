# Templates

These are files you copy to your own project and customize.

| File                           | Purpose                                       | Copy to                       |
| ------------------------------ | --------------------------------------------- | ----------------------------- |
| `CLAUDE.md.template`           | Team-shared development guidelines            | `CLAUDE.md`                   |
| `settings.json.template`       | Shared project settings                       | `.claude/settings.json`       |
| `settings.local.json.template` | Recommended permissions                       | `.claude/settings.local.json` |
| `mcp.json.template`            | MCP server configuration                      | `.mcp.json`                   |
| `mcp-servers-template.md`      | Catalogue of MCP servers and install commands | reference only                |
| `README.md`                    | This file                                     | —                             |

## CLAUDE.md.template

Team-shared development guidelines. Copy to your project root:

```bash
cp CLAUDE.md.template /path/to/your/project/CLAUDE.md
```

Then customize:
- Package manager commands
- Test/build/lint commands
- Code conventions
- Architecture decisions

## settings.local.json.template

Recommended permissions for Claude Code. Copy to your project's `.claude/` directory:

```bash
mkdir -p /path/to/your/project/.claude
cp settings.local.json.template /path/to/your/project/.claude/settings.local.json
```

This pre-allows a broad set of development commands so you don't get prompted every time. It includes interpreters and package runners (`python`, `npx`, `bun`), network tools (`curl`, `wget`) and `git push`, which together allow arbitrary code execution and data egress without a prompt — trim the list to what your project needs.
