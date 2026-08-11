# Day 13 Observability Design

## Goal

Complete the K4 observability lab without changing the released challenge contract.

## Request flow

`CorrelationIdMiddleware` clears the previous structlog context, accepts or creates a `req-<8 hex>` ID, binds it, and returns it in response headers.

The `/chat` endpoint adds non-sensitive request metadata to the context before the first application log.

The JSON logging processor redacts every string value that could be serialized to the JSONL log.

The agent adds the correlation ID to Langfuse trace metadata so an incident can be followed from metrics to a trace and then to the matching logs.

## Metrics and operations

Metrics expose an error-rate percentage calculated from successful requests plus recorded errors.

The dashboard contract remains the authoritative six-panel definition and is validated by the existing validator.

The SLO file defines latency, error-rate, cost, and quality targets.

Three symptom-based alerts link to concrete runbook sections.

## Evidence and collaboration

Every assigned component is implemented and committed from its member branch under that member's configured Git identity.

Runtime Langfuse screenshots, prompt label changes, dashboard screenshots, and incident evidence require an authenticated Langfuse project and cannot be fabricated.

The report only links real evidence and the matching commits or pull requests.
