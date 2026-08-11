# Báo cáo Day 13 Observability

## 1. Thông tin nhóm

- Tên nhóm: K4 - Day 13 Observability
- Repository URL: Git remote đã được cấu hình và push trên tất cả branch phân công.
- Commit SHA evidence tích hợp: `5d645c7`.
- Thành viên và vai trò:
  - Nguyễn Đăng Long - tích hợp API, correlation context và kiểm thử E2E.
  - Đào Minh Chiến - PII redaction và kiểm thử bảo mật log.
  - Lương Minh Quân - metrics, dashboard sáu panel và validator dashboard.
  - Lê Đăng Tấn - SLO, symptom alerts và runbook.
  - Vũ Hữu An - Langfuse tracing, prompt versioning, challenge evidence và báo cáo.

## 2. Kết quả kỹ thuật

- Điểm `validate_logs.py`: 100/100 trên 97 log records, 47 correlation IDs và 0 PII leak.
- Tổng số traces: 17 trace thật trong project Langfuse hiện tại, vượt mốc 10 trace của codelab.
- Số PII leak còn lại: 0.
- Link/đường dẫn dashboard: [dashboard.html](evidence/dashboard.html).

## 3. Logging và tracing

- Evidence correlation ID: `req-a4b6cdb7` liên kết session `k4-challenge-s01` với trace `5dd3f3199b16858aa73ca6dea0aa86fe` và các log request/response tương ứng.
- Evidence PII redaction: validator quét 97 records và báo `Potential PII leaks detected: 0`; trường người dùng trong log chỉ là `user_id_hash`.
- Evidence trace waterfall: [trace evidence](evidence/trace-evidence.md) có liên kết trực tiếp đến trace baseline, candidate và trace challenge.
- Giải thích một span đáng chú ý: trong trace challenge, span `retrieve` mất 2.505 giây trong tổng latency generation 2.662 giây, chỉ ra retrieval là nút thắt.

## 4. Prompt versioning

- Prompt name: `day13-chat`.
- Version/label baseline: v1, labels `baseline` và `production` sau rollback.
- Version/label candidate: v2, label `candidate`.
- Trace ID của mỗi version: v1 baseline `79648482039602a16d3b7c1e5bf5dc85`; v2 candidate `4083645850d1f178409cca4b9ec6d301`.
- Bằng chứng đổi label hoặc rollback: production đã chuyển v1 -> v2 và kiểm tra API trả version 2, sau đó rollback v2 -> v1 và kiểm tra API trả version 1. Giao diện Prompts hiện hiển thị v1 `production, baseline` và v2 `candidate`.

## 5. Dashboard, SLO và alerts

- Kết quả `validate_dashboard.py`: hợp lệ 6/6 panel theo dashboard contract.
- Evidence dashboard: [dashboard.html](evidence/dashboard.html) hiển thị traffic, P50/P95/P99 latency, error rate, quality score, token usage và cost.
- SLO đã chọn và lý do: latency P95 < 2.000 ms và daily cost <= $2.50 để kiểm soát trực tiếp hai tín hiệu ảnh hưởng trải nghiệm và ngân sách.
- Alert rules và runbook: [alert rules](../config/alert_rules.yaml) có ba symptom alerts `high_p95_latency`, `high_error_rate`, `cost_budget_burn`; [runbook](../docs/alerts.md) có hành động triage và rollback.

## 6. Điều tra challenge

- Challenge ID: `day13-k4-observability-v1`.
- Triệu chứng từ metrics: P50 2.662 ms, P95 3.112 ms, P99 3.112 ms, vượt ngưỡng 2.000 ms, trong khi error rate vẫn 0% và traffic là 5.
- Trace ID liên quan: `5dd3f3199b16858aa73ca6dea0aa86fe`.
- Log line/correlation ID liên quan: `req-a4b6cdb7`, session `k4-challenge-s01`.
- Root cause: incident `rag_slow` làm span `retrieve` chậm 2.505 giây.
- Fix action: tắt incident sau khi thu thập evidence và xác nhận `rag_slow: false`.
- Preventive measure: giữ alert P95 latency, dashboard latency percentiles và runbook yêu cầu mở trace rồi lọc log theo correlation ID trước khi rollback.

## 7. Đóng góp cá nhân

Với mỗi thành viên, ghi rõ nhiệm vụ và link commit/PR tương ứng.

| Thành viên | Phần việc | Commit/PR | Điều đã học |
|---|---|---|---|
| Nguyễn Đăng Long | Request correlation, context enrichment, tích hợp | `6cad71f` | Correlation ID biến metrics, traces và logs thành một luồng điều tra thống nhất. |
| Đào Minh Chiến | PII redaction | `f3748eb` | Redaction phải chạy đệ quy trước khi structured log được ghi ra disk. |
| Lương Minh Quân | Metrics và dashboard | `0d81a07` | Dashboard hữu ích khi panel gắn với một câu hỏi vận hành cụ thể. |
| Lê Đăng Tấn | SLO, alerts và runbook | `be2519e` | Alert theo triệu chứng giảm nhiễu và hướng điều tra rõ hơn. |
| Vũ Hữu An | Trace correlation, prompt versioning, evidence | `247b28d`, `678c972` | Prompt label và trace metadata giúp rollout, rollback có thể kiểm chứng. |
