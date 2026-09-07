from pathlib import Path
import ast

ROOT = Path(__file__).resolve().parents[2]
ERRATA = ROOT / "contracts" / "errata.py"
CANON_GATE = ROOT / "contracts" / "canon_gate.py"


def test_contracts_are_valid_python_syntax():
    ast.parse(ERRATA.read_text())
    ast.parse(CANON_GATE.read_text())


def test_errata_contains_independent_validator_reobservation():
    source = ERRATA.read_text()
    assert "run_nondet_unsafe" in source
    assert "inspect_revision_once(url, subject, definition, prior_statement, include_source=True)" in source
    assert "inspect_initial_once(url, subject, definition, include_source=True)" in source


def test_material_corrections_have_deterministic_stale_cascade():
    source = ERRATA.read_text()
    assert "_stale_claim_cascade" in source
    assert "REL_CORRECTS" in source
    assert "REL_RETRACTS" in source
    assert "REL_SUPERSEDES" in source


def test_canon_gate_actually_calls_errata_interface():
    source = CANON_GATE.read_text()
    assert "IErrata(self.errata_address)" in source
    assert ".view().is_claim_current" in source
    assert "action already executed" in source


def test_repository_contains_no_frontend():
    forbidden = ["frontend", "web", "app", "package.json", "vite.config.ts", "next.config.js"]
    present = {p.name for p in ROOT.iterdir()}
    assert not any(item in present for item in forbidden)
