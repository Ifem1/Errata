#!/usr/bin/env python3
from pathlib import Path
import ast
import sys

ROOT = Path(__file__).resolve().parents[1]
ERRATA = ROOT / "contracts" / "errata.py"
CANON_GATE = ROOT / "contracts" / "canon_gate.py"

checks = []

def check(name, condition):
    checks.append((name, bool(condition)))

for path in (ERRATA, CANON_GATE):
    try:
        ast.parse(path.read_text())
        check(f"python syntax: {path.name}", True)
    except Exception as exc:
        print(f"FAIL syntax {path}: {exc}")
        check(f"python syntax: {path.name}", False)

source = ERRATA.read_text()
canon_gate = CANON_GATE.read_text()

check("current py-genlayer dependency pin present", "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" in source)
check("custom equivalence validator present", "run_nondet_unsafe" in source)
check("validator re-fetches initial source", 'inspect_initial_once(url, subject, definition, include_source=True)' in source)
check("validator re-fetches later revision", 'inspect_revision_once(url, subject, definition, prior_statement, include_source=True)' in source)
check("verbatim evidence grounding present", "grounded(" in source)
check("sealed authority surface present", "authority_hosts" in source and "outside the sealed evidence surface" in source)
check("material correction relations present", all(x in source for x in ("REL_CORRECTS", "REL_RETRACTS", "REL_SUPERSEDES", "REL_AMENDS")))
check("lazy deterministic stale propagation present", "_claim_is_current_lazy" in source)
check("definition-hash pinning present", "expected_definition_hash" in source)
check("claim-hash pinning present", "expected_claim_hash" in source)
check("CanonGate uses typed Errata interface", "IErrata(self.errata_address)" in canon_gate)
check("CanonGate calls Errata view", ".view().is_claim_current" in canon_gate)
check("CanonGate has replay protection", "action already executed" in canon_gate)

for forbidden in ("frontend", "app", "web"):
    check(f"no {forbidden}/ directory", not (ROOT / forbidden).exists())
check("no package.json", not (ROOT / "package.json").exists())

failed = [name for name, ok in checks if not ok]
for name, ok in checks:
    print(("PASS" if ok else "FAIL") + "  " + name)

print(f"\n{len(checks) - len(failed)}/{len(checks)} preflight checks passed.")
if failed:
    sys.exit(1)
