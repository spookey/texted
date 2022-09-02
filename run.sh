#!/usr/bin/env sh

DIR_SELF="$(cd "$(dirname "$0")" || exit 1; pwd)"

"$DIR_SELF/venv/bin/python3" "$DIR_SELF/texted.py" "$@"
exit "$?"
