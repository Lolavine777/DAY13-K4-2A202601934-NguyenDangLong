# Challenge evidence

Challenge `day13-k4-observability-v1` ran with five official inputs after `rag_slow` was enabled.

| Signal | Observed value | Interpretation |
|---|---:|---|
| Traffic | 5 | The official workload was executed. |
| P50 latency | 2,662 ms | Above normal request latency. |
| P95 latency | 3,112 ms | Breaches the 2,000 ms SLO threshold. |
| Error rate | 0% | This is a latency incident, not an availability incident. |
| Slow trace | `5dd3f3199b16858aa73ca6dea0aa86fe` | `retrieve` took 2.505 seconds. |

The matching correlation ID is `req-a4b6cdb7` for session `k4-challenge-s01`.
After evidence collection, the incident was disabled and the control endpoint returned `rag_slow: false`.
