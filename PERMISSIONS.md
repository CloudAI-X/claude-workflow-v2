# Recommended Permissions

Add these to your project's `.claude/settings.local.json` as needed.

## How to Use

Create or edit `.claude/settings.local.json` in your project and add permissions from the sections below under the `permissions.allow` array:

```json
{
  "permissions": {
    "allow": []
  }
}
```

## MCP Servers

For library documentation lookup:

```json
"mcp__context7__resolve-library-id",
"mcp__context7__query-docs"
```

For web scraping:

```json
"mcp__firecrawl__firecrawl_scrape"
```

## Development Commands

Common npm commands:

```json
"Bash(npm install:*)",
"Bash(npm test:*)",
"Bash(npm run:*)",
"Bash(npx tsc:*)"
```

## Utility Commands

File and directory utilities:

```json
"Bash(chmod:*)",
"Bash(tree:*)"
```

## Framework-Specific Permissions

### Node.js / JavaScript

```json
"Bash(npm install:*)",
"Bash(npm test:*)",
"Bash(npm run:*)",
"Bash(npx:*)"
```

### Python

```json
"Bash(pip install:*)",
"Bash(pytest:*)",
"Bash(python:*)"
```

### Go

```json
"Bash(go build:*)",
"Bash(go test:*)",
"Bash(go run:*)"
```

### Rust

```json
"Bash(cargo build:*)",
"Bash(cargo test:*)",
"Bash(cargo run:*)"
```

## Deployment Permissions

Add deployment commands specific to your platform:

### Vercel

```json
"Bash(npx vercel:*)"
```

### Netlify

```json
"Bash(npx netlify:*)"
```

### Cloudflare Workers

```json
"Bash(npx wrangler deploy:*)"
```

### Docker

```json
"Bash(docker build:*)",
"Bash(docker run:*)"
```

## Example Complete Configuration

```json
{
  "permissions": {
    "allow": [
      "mcp__context7__resolve-library-id",
      "mcp__context7__query-docs",
      "Bash(npm install:*)",
      "Bash(npm test:*)",
      "Bash(npm run:*)",
      "Bash(npx tsc:*)",
      "Bash(chmod:*)"
    ]
  }
}
```
