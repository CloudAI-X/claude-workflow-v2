---
description: Security-focused code scan. Checks for hardcoded secrets, vulnerable dependencies, and common security issues.
---

# Security Scan

Security-focused code scanning. Run before commits and PRs to catch vulnerabilities.

## Phase 1: Secret Detection

Scan for hardcoded credentials:

```bash
# Common secret patterns (-E: extended regex, so ? and {n} work)
grep -rnE "(password|passwd|secret|token|api[_-]?key)[[:space:]]*[=:][[:space:]]*['\"]" --include="*.js" --include="*.jsx" --include="*.ts" --include="*.tsx" --include="*.py" --include="*.go" --include="*.java" --include="*.rb" --include="*.json" --include="*.yml" --include="*.yaml" --exclude-dir=node_modules --exclude-dir=.git . 2>/dev/null

# Secrets in .env files (templates excluded)
grep -rnE "^[A-Za-z0-9_]*(PASSWORD|SECRET|TOKEN|API_KEY)[A-Za-z0-9_]*=.+" --include=".env*" --exclude=".env.example" --exclude=".env.template" --exclude=".env.sample" --exclude-dir=node_modules --exclude-dir=.git . 2>/dev/null

# AWS keys
grep -rnE "AKIA[0-9A-Z]{16}" --exclude-dir=node_modules --exclude-dir=.git . 2>/dev/null

# Private keys
find . \( -name "*.pem" -o -name "*.key" -o -name "id_rsa" \) -not -path "./node_modules/*" -not -path "./.git/*" 2>/dev/null
```

## Phase 2: Dependency Audit

Check for vulnerable dependencies:

### Node.js

```bash
npm audit --json 2>/dev/null | head -100
# or
yarn audit --json 2>/dev/null | head -100
```

### Python

```bash
pip-audit 2>/dev/null || safety check 2>/dev/null
```

### Go

```bash
govulncheck ./... 2>/dev/null
```

### Rust

```bash
cargo audit 2>/dev/null
```

## Phase 3: Code Pattern Analysis

Check for dangerous patterns:

### SQL Injection

- String concatenation in SQL queries
- Unparameterized queries
- Dynamic table/column names from user input

### Command Injection

- Shell execution with user input (`exec`, `system`, `subprocess`)
- Unsanitized path construction

### XSS Vulnerabilities

- `innerHTML` with user data
- `dangerouslySetInnerHTML` without sanitization
- Unescaped template variables

### Path Traversal

- User input in file paths without sanitization
- Missing `..` checks

## Phase 4: Configuration Check

Verify security settings:

- [ ] Debug mode disabled in production configs
- [ ] HTTPS enforced (no HTTP URLs in prod)
- [ ] CORS properly configured
- [ ] Security headers present (CSP, X-Frame-Options, etc.)
- [ ] No default/weak passwords in configs

## Output Format

```
## Security Scan: [PASS/FAIL/WARNINGS]

### Secrets Detected: [count]
1. **CRITICAL** - `file:line`
   - Type: [API key/password/token/private key]
   - Action: Remove immediately and rotate credential

### Vulnerable Dependencies: [count]
1. **[package@version]** - Severity: [Critical/High/Medium/Low]
   - CVE: [CVE number if available]
   - Fixed in: [version]
   - Action: Update to [version]

### Code Vulnerabilities: [count]
1. **[Vulnerability Type]** - `file:line`
   - Risk: [description]
   - Fix: [remediation steps]

### Configuration Issues: [count]
1. **[Issue]**
   - Current: [state]
   - Recommended: [secure state]

### Recommendations
1. [Prioritized action items]
```

## NEVER Commit If

- Secrets detected in code (rotate and remove)
- Critical CVEs in dependencies (update first)
- Obvious injection vulnerabilities (fix first)

## Usage

This command ships with the project-starter plugin. Invoke with: `/project-starter:security-scan`
