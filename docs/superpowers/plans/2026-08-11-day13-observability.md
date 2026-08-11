# Day 13 Observability Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Complete the K4 observability requirements with verifiable logging, metrics, tracing, operational configuration, and submission artifacts.

**Architecture:** The API middleware supplies one correlation ID to structlog and HTTP responses.
The chat endpoint enriches the context once, and the logging processor sanitizes data before either the JSONL file or console renderer receives it.
Metrics, Langfuse metadata, dashboard configuration, and incident reporting consume those logs without changing the released challenge.

**Tech Stack:** Python 3.11+, FastAPI, structlog, Langfuse SDK v3, PyYAML, pytest.

## Global Constraints

- Do not modify `config/challenge.json`.
- Do not commit `.env`, credentials, raw PII, generated logs, or `.venv`.
- Keep exactly six dashboard panels specified by `config/dashboard.yaml`.
- Preserve individual authorship by committing each branch with its assigned member identity.
- Run a focused failing test before each production-code change.

### Task 1: API correlation and request context

**Files:**

- Modify: `app/middleware.py`
- Modify: `app/main.py`
- Test: `tests/test_chat_observability.py`

- [ ] Write focused tests for generated and propagated request IDs plus request metadata.
- [ ] Run those tests and confirm they fail against the starter implementation.
- [ ] Implement only context clearing, ID creation or propagation, headers, and request metadata binding.
- [ ] Run focused tests and the full suite.
- [ ] Commit on `develop/nguyen-dang-long`.

### Task 2: PII-safe structured logging

**Files:**

- Modify: `app/pii.py`
- Modify: `app/logging_config.py`
- Test: `tests/test_pii.py`

- [ ] Write focused tests for passport, Vietnamese address, and non-payload string redaction.
- [ ] Run the tests and confirm they fail against the starter implementation.
- [ ] Add the minimal PII patterns and process every serializable string or nested dictionary before JSON rendering.
- [ ] Run focused tests and the full suite.
- [ ] Commit on `develop/dao-minh-chien`.

### Task 3: Metrics and dashboard specification

**Files:**

- Modify: `app/metrics.py`
- Modify: `docs/dashboard-spec.md`
- Test: `tests/test_metrics.py`

- [ ] Write a focused test for error-rate calculation with both successful and failed requests.
- [ ] Run the test and confirm it fails because `error_rate_pct` is absent.
- [ ] Add the percentage to `snapshot()` without changing existing metric names.
- [ ] Complete the six-panel dashboard specification from the immutable dashboard contract.
- [ ] Run focused tests, the full suite, and `python scripts/validate_dashboard.py`.
- [ ] Commit on `develop/luong-minh-quan`.

### Task 4: SLOs, alerts, and runbooks

**Files:**

- Modify: `config/slo.yaml`
- Modify: `config/alert_rules.yaml`
- Modify: `docs/alerts.md`

- [ ] Define four SLO targets suitable for the supplied fake service.
- [ ] Define three user-symptom alerts with severity, owner, condition, and runbook anchors.
- [ ] Complete each runbook with impact, three first checks, mitigation, and owner.
- [ ] Parse the YAML and verify all alert anchors resolve.
- [ ] Commit on `develop/le-dang-tan`.

### Task 5: Trace correlation, prompt-version evidence, incident, and report

**Files:**

- Modify: `app/agent.py`
- Modify: `app/mock_rag.py`
- Modify: `app/mock_llm.py`
- Modify: `submission/REPORT.md`
- Test: `tests/test_agent_prompt_trace.py`

- [ ] Write a focused test requiring `correlation_id` in trace metadata.
- [ ] Run it and confirm it fails against the starter implementation.
- [ ] Add trace correlation and optional child spans for retrieval and generation.
- [ ] Run focused tests and the full suite.
- [ ] Add report content only after collecting real trace, prompt-version, dashboard, and challenge evidence.
- [ ] Commit source changes on `develop/vu-huu-an`.

### Task 6: Integration and acceptance

**Files:**

- Modify: `submission/REPORT.md`
- Create: `submission/evidence/*` from real runtime captures only

- [ ] Merge member branches without squashing individual commits.
- [ ] Start the API and run the load test.
- [ ] Run `python scripts/validate_logs.py` and require `Estimated Score: 100/100`.
- [ ] Run `python scripts/validate_dashboard.py` and require `HỢP LỆ: 6/6 panel`.
- [ ] Run `python -m pytest -q` and require all tests to pass.
- [ ] Run the released challenge and document the Metrics -> Traces -> Logs evidence chain.
