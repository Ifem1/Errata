#!/usr/bin/env bash
set -euo pipefail

if ! command -v genlayer >/dev/null 2>&1; then
  echo "GenLayer CLI is not installed. Install with: npm install -g genlayer" >&2
  exit 1
fi

cd "$(dirname "$0")/.."
python scripts/preflight.py

echo "Using the currently selected GenLayer account. No private key is read from this repository."
genlayer network set studionet
genlayer network info
genlayer account

echo
echo "Deploying Errata..."
genlayer deploy --contract contracts/errata.py
echo
echo "Record the finalized deployment transaction and contract address before continuing."
