from collections import Counter

from app import metrics
from app.metrics import percentile


def test_percentile_basic() -> None:
    assert percentile([100, 200, 300, 400], 50) >= 100


def test_snapshot_reports_error_rate_across_successes_and_failures(monkeypatch) -> None:
    monkeypatch.setattr(metrics, "TRAFFIC", 2)
    monkeypatch.setattr(metrics, "ERRORS", Counter())
    metrics.record_error("RuntimeError")

    assert metrics.snapshot()["error_rate_pct"] == 33.33
