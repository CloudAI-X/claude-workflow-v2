#!/usr/bin/env python3
"""
Pre-commit security check hook.
Blocks commits that might contain secrets or security issues.
"""
import json
import re
import sys
import os

# Patterns that indicate potential secrets
SECRET_PATTERNS = [
    (r'(?i)(api[_-]?key|apikey)\s*[:=]\s*["\']?[a-zA-Z0-9_-]{20,}', "API key", "Move to .env file and use environment variables (e.g., process.env.API_KEY)"),
    (r'(?i)(secret|password|passwd|pwd)\s*[:=]\s*["\'][^"\']+["\']', "Password/Secret", "Use environment variables or a .env file, never hardcode credentials"),
    (r"(?i)bearer\s+[a-zA-Z0-9_-]{20,}", "Bearer token", "Move to .env file and use environment variables (e.g., process.env.AUTH_TOKEN)"),
    (r"ghp_[a-zA-Z0-9]{36}", "GitHub Personal Access Token", "Move to .env file and use environment variables (e.g., process.env.GITHUB_TOKEN)"),
    (r"github_pat_[a-zA-Z0-9]{22}_[a-zA-Z0-9]{59}", "GitHub PAT (fine-grained)", "Move to .env file and use environment variables (e.g., process.env.GITHUB_TOKEN)"),
    (r"sk-[a-zA-Z0-9]{48}", "OpenAI API Key", "Move to .env file and use environment variables (e.g., process.env.OPENAI_API_KEY)"),
    (r"sk-(?:proj|svcacct|admin)-[a-zA-Z0-9_-]{40,}", "OpenAI API Key", "Move to .env file and use environment variables (e.g., process.env.OPENAI_API_KEY)"),
    (r"sk-ant-[a-zA-Z0-9_-]{80,}", "Anthropic API Key", "Move to .env file and use environment variables (e.g., process.env.ANTHROPIC_API_KEY)"),
    (r"-----BEGIN (?:RSA |EC |DSA )?PRIVATE KEY-----", "Private key", "Store in a secrets manager (AWS Secrets Manager, Vault, etc.) — never commit private keys"),
    (r"(?i)aws[_-]?access[_-]?key[_-]?id\s*[:=]\s*[A-Z0-9]{20}", "AWS Access Key", "Move to .env file and use environment variables (e.g., process.env.AWS_ACCESS_KEY_ID)"),
    (
        r"(?i)aws[_-]?secret[_-]?access[_-]?key\s*[:=]\s*[a-zA-Z0-9/+=]{40}",
        "AWS Secret Key",
        "Move to .env file and use environment variables (e.g., process.env.AWS_SECRET_ACCESS_KEY)",
    ),
]

# Files to always skip
SKIP_FILES = {
    ".env.example",
    ".env.template",
    ".env.sample",
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
}

# Documentation/prose extensions where credential-shaped strings are almost
# always teaching examples (e.g. the security-patterns skill, sample reports),
# not real secrets. Scanning them produces false positives that block
# legitimate docs. Config/code (.json, .yml, .py, .js, ...) is still scanned.
SKIP_EXTENSIONS = {".md", ".markdown", ".mdx", ".txt", ".rst"}


# Directories and file names that hold tests/fixtures, where fake credentials
# are expected. Matched on whole path segments and file-name conventions — a
# substring match would also skip "latest-app/", "inspector/" or "contest.py".
SKIP_DIRS = {"examples", "test", "tests", "__tests__", "spec", "specs", "fixtures", "__fixtures__", "__mocks__"}
TEST_FILE_PATTERN = re.compile(r"^(test_.+|conftest\.py|.+[._-](test|spec)\.[^.]+)$", re.IGNORECASE)


def project_relative(file_path, cwd):
    """Return file_path relative to the project, so parent dirs don't count."""
    path = file_path.replace("\\", "/")
    root = (os.environ.get("CLAUDE_PROJECT_DIR") or cwd or "").replace("\\", "/").rstrip("/")
    if root and path.startswith(root + "/"):
        return path[len(root) + 1:]
    return path


def check_for_secrets(content, file_path, cwd=""):
    """Check content for potential secrets."""
    issues = []

    # Skip certain files
    if os.path.basename(file_path) in SKIP_FILES:
        return issues

    # Skip documentation/prose files — they carry intentional, illustrative
    # credential examples rather than live secrets.
    if os.path.splitext(file_path)[1].lower() in SKIP_EXTENSIONS:
        return issues

    # Skip example, test and fixture locations for the same reason.
    segments = project_relative(file_path, cwd).lower().split("/")
    if any(segment in SKIP_DIRS for segment in segments[:-1]):
        return issues
    if TEST_FILE_PATTERN.match(segments[-1]):
        return issues

    for pattern, secret_type, remediation in SECRET_PATTERNS:
        matches = re.findall(pattern, content)
        if matches:
            issues.append(f"Potential {secret_type} detected → {remediation}")

    return issues


def main():
    try:
        input_data = json.load(sys.stdin)
        tool_input = input_data.get("tool_input", {})

        # Get file path and content based on tool type
        file_path = tool_input.get("file_path", "")
        content = tool_input.get("content", "") or tool_input.get("new_string", "")

        if not file_path or not content:
            sys.exit(0)

        issues = check_for_secrets(content, file_path, input_data.get("cwd", ""))

        if issues:
            # On exit code 2, Claude Code ignores stdout and feeds stderr back
            # to the model as the block reason, so the explanation must go to
            # stderr (see code.claude.com/docs/en/hooks).
            print(f"🚫 BLOCKED - Security issue detected in {file_path}:", file=sys.stderr)
            for issue in issues:
                print(f"  - {issue}", file=sys.stderr)
            print("\nThis edit has been BLOCKED to prevent committing secrets.", file=sys.stderr)
            print(
                "If this is a false positive, review and adjust the patterns in security-check.py",
                file=sys.stderr,
            )
            print("See security-patterns skill for secure credential management.", file=sys.stderr)
            # Exit 2 to block the edit
            sys.exit(2)

    except Exception as e:
        # Don't block on errors
        sys.exit(0)


if __name__ == "__main__":
    main()
