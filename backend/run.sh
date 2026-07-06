#!/usr/bin/env bash
# Start the IntelliSight backend with auto-reload (development mode).
#
# Usage:  ./run.sh
set -e
cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
  echo "❌  No virtual environment found."
  echo "    Run the one-time setup first:"
  echo "      python3 -m venv .venv"
  echo "      .venv/bin/pip install -r requirements.txt"
  exit 1
fi

source .venv/bin/activate
echo "🚀  Starting IntelliSight backend on http://127.0.0.1:8000  (Ctrl+C to stop)"
exec uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
