#!/bin/sh
# Runs Open Mask Maker inside the project's environment. For Unix-Like.

ROOT="$(cd "$(dirname "$0")/.." && pwd)" # Gives an absolute path of the root of the project
export PATH="$HOME/.local/bin:$PATH" # Adds the uv install folder to the run.sh process's PATH variable

# Checks if uv is found and exits with an error if it isn't
if ! command -v uv >/dev/null 2>&1; then 
    echo "uv not found. Run install.cmd first" >&2
    exit 1
fi

# Runs the mask-maker command in the project
exec uv run --project "$ROOT" mask-maker "$@"