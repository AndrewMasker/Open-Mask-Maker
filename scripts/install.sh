#!/bin/sh
# This is the Unix-Like install script.

set -e # Set this process to exit on errors
cd "$(dirname "$0")" # cd to the directory containing this script
export PATH="$HOME/.local/bin:$PATH" # Add the install path of uv to the install.sh process's PATH variable

if ! command -v uv >/dev/null 2>&1; then # Check if the uv command is recognized. Install if not
    echo "Installing uv..."
    if command -v curl >/dev/null 2>&1; then 
        curl -LsSf https://astral.sh/uv/install.sh | sh
    else 
        wget -qO- https://astral.sh/uv/install.sh | sh
    fi
fi

uv sync
echo "Install done."
exit 0