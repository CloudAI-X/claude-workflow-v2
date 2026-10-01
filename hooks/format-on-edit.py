#!/usr/bin/env python3
"""
Auto-format files after Claude edits them.
Detects file type and runs appropriate formatter.
"""
import json
import shutil
import subprocess
import sys
import os

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


def get_formatter_command(file_path):
    """Return the formatter command for a given file type."""
    ext = os.path.splitext(file_path)[1].lower()
    
    formatters = {
        # JavaScript/TypeScript
        '.js': ['prettier', '--write'],
        '.jsx': ['prettier', '--write'],
        '.ts': ['prettier', '--write'],
        '.tsx': ['prettier', '--write'],
        '.json': ['prettier', '--write'],
        '.css': ['prettier', '--write'],
        '.scss': ['prettier', '--write'],
        '.md': ['prettier', '--write'],
        '.yaml': ['prettier', '--write'],
        '.yml': ['prettier', '--write'],
        
        # Python
        '.py': ['black', '--quiet'],
        
        # Go
        '.go': ['gofmt', '-w'],
        
        # Rust
        '.rs': ['rustfmt'],
    }
    
    return formatters.get(ext)

def main():
    try:
        input_data = json.load(sys.stdin)
        file_path = input_data.get('tool_input', {}).get('file_path', '')
        
        if not file_path or not os.path.exists(file_path):
            sys.exit(0)
        
        formatter = get_formatter_command(file_path)
        if formatter:
            tool = find_tool(formatter[0], os.path.dirname(file_path))
            if not tool:
                # Formatter not installed - skip silently
                sys.exit(0)
            cmd = [tool] + formatter[1:] + [file_path]
            try:
                subprocess.run(cmd, capture_output=True, timeout=10)
            except (subprocess.TimeoutExpired, FileNotFoundError):
                # Formatter not installed or timed out - skip silently
                pass
    except Exception:
        # Don't block on formatter errors
        pass

if __name__ == '__main__':
    main()
