"""Independent research-receipt checks; no production ledger or implementation imports."""

import json
from decimal import Decimal
from pathlib import Path


def test_six_cross_process_experiments_match_prespecified_financial_oracle():
    receipt = json.loads((Path(__file__).resolve().parents[1] / "evals" /
                          "durable-financial-provenance-measurements.json").read_text())
    assert receipt["audit_schema"] == "funnelscript-financial-audit-v1"
    assert receipt["source_sha256"] and len(receipt["source_sha256"]) == 64
    assert {(r["population"], r["seed"]) for r in receipt["runs"]} == {
        (size, seed) for size in (10, 100, 1000) for seed in (11, 29)}
    for item in receipt["runs"]:
        n = item["population"]
        assert item["sales"] == 3 * n // 10
        assert item["actions"] == 3 * n // 10 + 3
        assert item["entries"] == 2 * (3 * n // 10) + 3
        assert Decimal(item["cash"]) == Decimal(n) * Decimal("10.5")
        assert item["replay_agrees"] is True
        assert len(item["audit_sha256"]) == 64
        for key in ("population_seconds", "financial_seconds", "serialization_seconds",
                    "restoration_seconds_child", "replay_seconds_child", "total_seconds"):
            assert item[key] >= 0
