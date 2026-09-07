#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <ERRATA_CONTRACT_ADDRESS>" >&2
  exit 1
fi

ERRATA_ADDRESS="$1"

if ! command -v genlayer >/dev/null 2>&1; then
  echo "GenLayer CLI is not installed. Install with: npm install -g genlayer" >&2
  exit 1
fi

cd "$(dirname "$0")/.."
python scripts/preflight.py

genlayer network set studionet
genlayer network info
genlayer account

echo
echo "Deploying CanonGate wired to: $ERRATA_ADDRESS"
genlayer deploy --contract contracts/canon_gate.py --args "$ERRATA_ADDRESS"
echo
echo "Record the finalized deployment transaction and CanonGate address."
