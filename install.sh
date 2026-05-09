#!/usr/bin/env bash
# Pop the Lock - one-line installer/runner.
# Usage:  curl -sSL https://raw.githubusercontent.com/tobin-wq/pop-the-lock/main/install.sh | bash
set -e

REPO_RAW="https://raw.githubusercontent.com/tobin-wq/pop-the-lock/main"
GAME_URL="$REPO_RAW/pop_the_lock.py"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: python3 is required but was not found." >&2
  echo "Install it from https://www.python.org/downloads/ and try again." >&2
  exit 1
fi

TMP_FILE="$(mktemp -t pop_the_lock.XXXXXX).py"
trap 'rm -f "$TMP_FILE"' EXIT

echo "Downloading Pop the Lock..."
if command -v curl >/dev/null 2>&1; then
  curl -fsSL "$GAME_URL" -o "$TMP_FILE"
elif command -v wget >/dev/null 2>&1; then
  wget -qO "$TMP_FILE" "$GAME_URL"
else
  echo "Error: need curl or wget to download the game." >&2
  exit 1
fi

clear
exec python3 "$TMP_FILE" </dev/tty
