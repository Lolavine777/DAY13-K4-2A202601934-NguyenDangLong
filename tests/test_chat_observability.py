from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from app import logging_config
from app.main import app


def test_chat_response_log_exposes_quality_for_dashboard(
    monkeypatch, tmp_path: Path
) -> None:
    log_path = tmp_path / "logs.jsonl"
    monkeypatch.setattr(logging_config, "LOG_PATH", log_path)

    with TestClient(app) as client:
        response = client.post(
            "/chat",
            json={
                "user_id": "student-01",
                "session_id": "session-01",
                "feature": "qa",
                "message": "Explain observability",
            },
        )

    assert response.status_code == 200
    events = [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines()]
    response_event = next(event for event in events if event["event"] == "response_sent")
    assert response_event["quality_score"] == response.json()["quality_score"]


def test_chat_propagates_correlation_id_and_enriches_api_logs(
    monkeypatch, tmp_path: Path
) -> None:
    log_path = tmp_path / "logs.jsonl"
    monkeypatch.setattr(logging_config, "LOG_PATH", log_path)

    with TestClient(app) as client:
        response = client.post(
            "/chat",
            headers={"x-request-id": "req-client01"},
            json={
                "user_id": "student-02",
                "session_id": "session-02",
                "feature": "monitoring",
                "message": "Explain correlation IDs",
            },
        )

    assert response.status_code == 200
    assert response.headers["x-request-id"] == "req-client01"
    assert response.headers["x-response-time-ms"]
    events = [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines()]
    api_events = [event for event in events if event["service"] == "api"]
    assert all(event["correlation_id"] == "req-client01" for event in api_events)
    assert all(event["user_id_hash"] for event in api_events)
    assert all(event["session_id"] == "session-02" for event in api_events)
    assert all(event["feature"] == "monitoring" for event in api_events)
    assert all(event["model"] == "claude-sonnet-4-5" for event in api_events)
    assert all(event["env"] for event in api_events)
