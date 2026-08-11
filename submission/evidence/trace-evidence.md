# Langfuse trace evidence

Project: [My Project](https://jp.cloud.langfuse.com/project/cmsoez6r7000wad0fv4fbxaoe/traces)

| Scenario | Prompt metadata | Correlation ID | Trace |
|---|---|---|---|
| Baseline | `day13-chat`, `baseline`, v1 | `req-06109ff5` | [79648482039602a16d3b7c1e5bf5dc85](https://jp.cloud.langfuse.com/project/cmsoez6r7000wad0fv4fbxaoe/traces/79648482039602a16d3b7c1e5bf5dc85) |
| Candidate | `day13-chat`, `candidate`, v2 | `req-e358d65b` | [4083645850d1f178409cca4b9ec6d301](https://jp.cloud.langfuse.com/project/cmsoez6r7000wad0fv4fbxaoe/traces/4083645850d1f178409cca4b9ec6d301) |
| Challenge | `day13-chat`, `production`, v1 | `req-a4b6cdb7` | [5dd3f3199b16858aa73ca6dea0aa86fe](https://jp.cloud.langfuse.com/project/cmsoez6r7000wad0fv4fbxaoe/traces/5dd3f3199b16858aa73ca6dea0aa86fe) |

The challenge trace contains the `retrieve` span at 2.505 seconds and a generation at 2.662 seconds.
This connects the P95 latency symptom to the retrieval root cause without recording raw user identifiers.

## Screenshots

- [Trace inventory with 17 root traces and 68 observations](langfuse-traces.jpg)
- [Baseline trace v1 with the retrieve and generate span tree](langfuse-baseline-trace.jpg)
- [Candidate trace v2 with the retrieve and generate span tree](langfuse-candidate-trace.jpg)
