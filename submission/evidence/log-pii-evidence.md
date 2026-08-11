# Structured log and PII-redaction evidence

`scripts/validate_logs.py` analyzed 97 records, found 47 unique correlation IDs, and reported 0 potential PII leaks.

## Redaction probe

A local synthetic probe was passed through `app.logging_config.scrub_event` before logging.
The stored result contains only redaction markers:

```json
{"event":"pii_probe","payload":{"card":"[REDACTED_CREDIT_CARD]","email":"[REDACTED_EMAIL]","phone":"[REDACTED_PHONE_VN]"}}
```

## Metrics to trace to logs join

The official challenge correlation ID is `req-a4b6cdb7` in session `k4-challenge-s01`.
Its structured request and response events retain only a one-way `user_id_hash`:

```json
{"event":"request_received","correlation_id":"req-a4b6cdb7","session_id":"k4-challenge-s01","user_id_hash":"f00ba60b3772","model":"claude-sonnet-4-5"}
{"event":"response_sent","correlation_id":"req-a4b6cdb7","session_id":"k4-challenge-s01","latency_ms":2660,"tokens_in":35,"tokens_out":100,"cost_usd":0.001605,"quality_score":0.8}
```

The matching Langfuse trace is `5dd3f3199b16858aa73ca6dea0aa86fe`.
