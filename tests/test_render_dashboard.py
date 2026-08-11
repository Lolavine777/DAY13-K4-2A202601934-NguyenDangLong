from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_dashboard_renderer_writes_all_six_panels(tmp_path: Path) -> None:
    logs = tmp_path / "logs.jsonl"
    output = tmp_path / "dashboard.html"
    records = [
        {"event": "request_received"},
        {"event": "response_sent", "latency_ms": 120, "cost_usd": 0.002, "tokens_in": 20, "tokens_out": 80, "quality_score": 0.8},
        {"event": "request_received"},
        {"event": "request_failed", "error_type": "RuntimeError"},
        {"event": "response_sent", "latency_ms": 240, "cost_usd": 0.003, "tokens_in": 30, "tokens_out": 120, "quality_score": 0.9},
    ]
    logs.write_text("\n".join(json.dumps(record) for record in records), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "render_dashboard.py"),
            "--logs",
            str(logs),
            "--output",
            str(output),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    dashboard = output.read_text(encoding="utf-8")
    assert "Latency percentiles" in dashboard
    assert "Request traffic" in dashboard
    assert "Error rate and breakdown" in dashboard
    assert "Cost over time" in dashboard
    assert "Input and output tokens" in dashboard
    assert "Quality proxy" in dashboard
    assert "60 minutes" in dashboard
