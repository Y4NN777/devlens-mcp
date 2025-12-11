#!/bin/bash
# DevLens MCP Server Launcher
# This script uses local uv with the virtual environment Python

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the script directory
cd "$SCRIPT_DIR"

# Detect OS and set paths accordingly
OS="$(uname -s)"
case "$OS" in
    Linux*|Darwin*)
        # Linux or macOS
        UV_BIN="$HOME/.local/bin/uv"
        PYTHON_BIN="$SCRIPT_DIR/.venv/bin/python"
        ;;
    MINGW*|MSYS*|CYGWIN*)
        # Windows (Git Bash, MSYS2, Cygwin)
        UV_BIN="$HOME/.local/bin/uv.exe"
        PYTHON_BIN="$SCRIPT_DIR/.venv/Scripts/python.exe"
        ;;
    *)
        # Fallback for unknown OS
        UV_BIN="$HOME/.local/bin/uv"
        PYTHON_BIN="$SCRIPT_DIR/.venv/bin/python"
        ;;
esac

# Check if uv exists, fallback to cargo bin or system uv
if [ ! -f "$UV_BIN" ]; then
    if [ -f "$HOME/.cargo/bin/uv" ]; then
        UV_BIN="$HOME/.cargo/bin/uv"
    elif command -v uv &> /dev/null; then
        UV_BIN="uv"
    else
        echo "Error: uv not found. Please install uv from https://github.com/astral-sh/uv"
        exit 1
    fi
fi

# Use local uv with virtual environment Python
exec "$UV_BIN" run --python "$PYTHON_BIN" python -m devlens.server
    