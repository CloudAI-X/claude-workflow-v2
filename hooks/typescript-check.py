#!/usr/bin/env python3
"""
Post-edit TypeScript type checking hook.
Runs tsc --noEmit after editing .ts/.tsx files.
Informational only - never blocks operations.
"""
import json
import shutil
import subprocess
import sys
import os


TS_EXTENSIONS = {'.ts', '.tsx'}


def find_tool(name, start_dir):
    """Find a tool in the nearest node_modules/.bin, falling back to PATH.

    Deliberately not `npx <name>`: outside a TTY npx silently downloads and
    runs whatever registry package has that name (`npx tsc` fetches an
    unrelated, deprecated "tsc" package, not TypeScript).
    """
    directory = os.path.abspath(start_dir)
    while True:
        candidate = os.path.join(directory, 'node_modules', '.bin', name)
        if os.path.exists(candidate):
            return candidate
        parent = os.path.dirname(directory)
        if parent == directory:
            return shutil.which(name)
        directory = parent


def find_tsconfig(file_path):
    directory = os.path.dirname(os.path.abspath(file_path))
    while directory != os.path.dirname(directory):
        tsconfig = os.path.join(directory, 'tsconfig.json')
        if os.path.exists(tsconfig):
            return tsconfig
        directory = os.path.dirname(directory)
    return None


def main():
    try:
        input_data = json.load(sys.stdin)
        tool_input = input_data.get('tool_input', {})

        file_path = tool_input.get('file_path', '')
        if not file_path:
            sys.exit(0)

        ext = os.path.splitext(file_path)[1].lower()
        if ext not in TS_EXTENSIONS:
            sys.exit(0)

        tsconfig = find_tsconfig(file_path)
        if not tsconfig:
            sys.exit(0)

        project_dir = os.path.dirname(tsconfig)

        tsc = find_tool('tsc', project_dir)
        if not tsc:
            sys.exit(0)

        try:
            result = subprocess.run(
                [tsc, '--noEmit', '--pretty', 'false'],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=project_dir,
            )

            if result.returncode != 0 and result.stdout:
                message = (
                    "TypeScript errors found — fix these before committing to maintain type safety:\n"
                    f"  File edited: {os.path.basename(file_path)}\n"
                    f"{result.stdout[:2000]}\n"
                )
                if len(result.stdout) > 2000:
                    message += "  ... (truncated)\n"
                message += "Run 'npx tsc --noEmit' locally to see full error output."
                # Plain stdout on exit 0 only reaches the debug log, so hand
                # the errors to Claude as additionalContext.
                print(json.dumps({
                    "hookSpecificOutput": {
                        "hookEventName": "PostToolUse",
                        "additionalContext": message,
                    }
                }))

        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

    except Exception:
        pass

    sys.exit(0)


if __name__ == '__main__':
    main()
