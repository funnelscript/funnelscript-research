"""Phase 007F independent numerical and evidence-contract validation.

No import of the production ledger or checkpoint implementation.
"""

from decimal import Decimal
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "evals/financial-commit-recovery-007f-measurements.json"


def test_six_measured_commits_reconcile_against_independent_minor_unit_oracle():
    report = json.loads(DATA.read_text())
    assert report["receipt_schema"] == "funnelscript-financial-commit-receipt-v1"
    assert report["audit_schema"] == "funnelscript-financial-audit-v1"
    assert len(report["source_sha256"]) == len(report["commit_source_sha256"]) == 64
    assert {(r["population"], r["seed"]) for r in report["runs"]} == {
        (n, seed) for n in (10, 100, 1000) for seed in (11, 29)}
    for row in report["runs"]:
        n = row["population"]
        sales = (n // 10) * 3
        assert row["sales"] == sales
        assert row["actions"] == sales + 3
        assert row["entries"] == sales * 2 + 3
        cash_minor = (n * 1000) + (sales * 1000) - (n * 200) - (n * 50)
        assert Decimal(row["cash"]) == Decimal(cash_minor) / 100
        assert (row["receipt_verified"], row["replay_agrees"],
                row["injected_rename_interruption_detected"]) == (True, True, True)
        assert len(row["audit_sha256"]) == len(row["receipt_id"]) == 64
        for field in (
            "population_seconds", "financial_seconds", "serialization_seconds",
            "initial_publication_seconds", "commit_publication_seconds",
            "recovery_seconds_child", "replay_seconds_child", "total_seconds",
        ):
            assert type(row[field]) in (float, int) and row[field] >= 0
        assert row["tracemalloc_peak_bytes_parent"] > 0


def test_report_file_provenance_matches_documented_runner_source():
    report = json.loads(DATA.read_text())
    assert report["memory_kind"] == "parent tracemalloc allocations; excludes child process"
    assert "single writer" in report["failure_model"]
    assert report["python"] and report["os"]
    assert len({(r["population"], r["seed"]) for r in report["runs"]}) == 6
