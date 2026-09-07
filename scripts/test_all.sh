#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

python scripts/preflight.py
python -m pytest tests/unit -q

if command -v gltest >/dev/null 2>&1; then
  gltest tests/direct -v -s
else
  echo
  echo "gltest is not installed; direct-mode tests were not executed."
  echo "Install: python -m pip install -r requirements-test.txt"
fi
