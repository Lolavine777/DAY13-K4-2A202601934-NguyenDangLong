# Alert và Runbook

Mỗi alert đo một triệu chứng người dùng hoặc SLO thay vì tên implementation nội bộ.

## Alert 1

- Tên: High latency P95.
- Severity: Warning.
- SLI/SLO liên quan: `latency_p95_ms`, với mục tiêu P95 không vượt 3000 ms.
- Điều kiện và thời gian duy trì: `latency_p95 > 3000ms for 5 minutes`.
- Ảnh hưởng tới người dùng: Một nhóm request có phản hồi chậm rõ rệt hoặc timeout phía client.
- Ba bước kiểm tra đầu tiên: Xem panel latency theo feature và time range; mở một trace chậm trong Langfuse; lọc JSONL bằng correlation ID của trace để xác định span hoặc lỗi liên quan.
- Mitigation tạm thời: Tắt hoặc giảm traffic tới feature bị ảnh hưởng, sau đó disable incident nếu đó là practice scenario.
- Owner: SRE on-call.

## Alert 2

- Tên: Elevated error rate.
- Severity: Critical.
- SLI/SLO liên quan: `error_rate_pct`, với mục tiêu dưới 2%.
- Điều kiện và thời gian duy trì: `error_rate_pct > 5 for 3 minutes`.
- Ảnh hưởng tới người dùng: Request có thể nhận HTTP 500 và không nhận được câu trả lời.
- Ba bước kiểm tra đầu tiên: Xem error breakdown; mở trace lỗi gần nhất; lọc `request_failed` theo correlation ID để đọc error type và input đã được redact.
- Mitigation tạm thời: Disable incident gây lỗi hoặc chuyển feature bị lỗi sang fallback an toàn.
- Owner: API on-call.

## Alert 3

- Tên: Cost budget exceeded.
- Severity: Warning.
- SLI/SLO liên quan: `daily_cost_usd`, với ngân sách tối đa 2.50 USD mỗi ngày.
- Điều kiện và thời gian duy trì: `daily_cost_usd > 2.5`.
- Ảnh hưởng tới người dùng: Không nhất thiết lỗi ngay, nhưng ngân sách LLM có nguy cơ cạn và dịch vụ có thể bị giới hạn sau đó.
- Ba bước kiểm tra đầu tiên: Xem panel cost và tokens; lọc trace có output token cao; đối chiếu log cùng correlation ID và feature liên quan.
- Mitigation tạm thời: Giảm output token hoặc tắt feature gây chi phí tăng đột biến.
- Owner: Team lead.
