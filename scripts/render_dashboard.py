from __future__ import annotations

import argparse
import html
import json
from collections import Counter
from pathlib import Path
from statistics import mean


PANEL_TITLES = (
    "Latency percentiles",
    "Request traffic",
    "Error rate and breakdown",
    "Cost over time",
    "Input and output tokens",
    "Quality proxy",
)


def load_records(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def percentile(values: list[float], value: int) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    return ordered[round((len(ordered) - 1) * value / 100)]


def panel(title: str, value: str, detail: str, threshold: str) -> str:
    return f"""
    <section class=\"panel\">
      <h2>{html.escape(title)}</h2>
      <p class=\"value\">{html.escape(value)}</p>
      <p>{html.escape(detail)}</p>
      <p class=\"threshold\">SLO / threshold: {html.escape(threshold)}</p>
    </section>"""


def render(records: list[dict]) -> str:
    responses = [record for record in records if record.get("event") == "response_sent"]
    requests = [record for record in records if record.get("event") == "request_received"]
    errors = [record for record in records if record.get("event") == "request_failed"]
    latencies = [float(record.get("latency_ms", 0)) for record in responses]
    costs = [float(record.get("cost_usd", 0)) for record in responses]
    tokens_in = sum(int(record.get("tokens_in", 0)) for record in responses)
    tokens_out = sum(int(record.get("tokens_out", 0)) for record in responses)
    quality = [float(record.get("quality_score", 0)) for record in responses]
    error_rate = len(errors) / len(requests) * 100 if requests else 0.0
    breakdown = Counter(record.get("error_type", "unknown") for record in errors)
    panels = "\n".join(
        (
            panel(
                PANEL_TITLES[0],
                f"P50 {percentile(latencies, 50):.0f} ms | P95 {percentile(latencies, 95):.0f} ms | P99 {percentile(latencies, 99):.0f} ms",
                f"{len(responses)} completed responses",
                "P95 ≤ 3000 ms",
            ),
            panel(PANEL_TITLES[1], f"{len(requests)} requests", "Source: request_received events", "≥ 1 request/minute"),
            panel(PANEL_TITLES[2], f"{error_rate:.2f}%", f"Breakdown: {dict(breakdown) or 'none'}", "≤ 2%"),
            panel(PANEL_TITLES[3], f"${sum(costs):.6f}", f"Average ${mean(costs) if costs else 0:.6f}/response", "≤ $2.50/day"),
            panel(PANEL_TITLES[4], f"{tokens_in} in | {tokens_out} out", "Source: response_sent token fields", "≤ 50,000 tokens"),
            panel(PANEL_TITLES[5], f"{mean(quality) if quality else 0:.2f}", "Mean response quality proxy", "≥ 0.75"),
        )
    )
    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <title>Day 13 AI Observability Dashboard</title>
  <style>
    body {{ background: #0f172a; color: #e2e8f0; font: 16px system-ui, sans-serif; margin: 0; padding: 32px; }}
    header {{ display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 24px; }}
    h1 {{ margin: 0; }}
    .meta, .threshold {{ color: #94a3b8; }}
    .grid {{ display: grid; gap: 16px; grid-template-columns: repeat(3, minmax(0, 1fr)); }}
    .panel {{ background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 20px; }}
    h2 {{ font-size: 16px; margin: 0 0 16px; color: #cbd5e1; }}
    .value {{ color: #5eead4; font-size: 24px; font-weight: 700; min-height: 56px; }}
    @media (max-width: 800px) {{ .grid {{ grid-template-columns: 1fr; }} }}
  </style>
</head>
<body>
  <header><h1>Day 13 AI Observability</h1><p class=\"meta\">Time range: 60 minutes · Refresh: 30 seconds · Source: data/logs.jsonl</p></header>
  <main class=\"grid\">{panels}</main>
</body>
</html>"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Render the Day 13 six-panel dashboard from JSONL logs")
    parser.add_argument("--logs", type=Path, default=Path("data/logs.jsonl"))
    parser.add_argument("--output", type=Path, default=Path("submission/evidence/dashboard.html"))
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(load_records(args.logs)), encoding="utf-8")
    print(f"Dashboard written: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
