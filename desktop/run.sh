#!/usr/bin/env bash
# Launch the Big Brother desktop app.
#
# Usage:  ./run.sh
set -e
cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
  echo "❌  No virtual environment found. Run the one-time setup first:"
  echo "      python3.12 -m venv .venv"
  echo "      .venv/bin/pip install -r requirements.txt"
  exit 1
fi

exec .venv/bin/python -m intellisight.app
