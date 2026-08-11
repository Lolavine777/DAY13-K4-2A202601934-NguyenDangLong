# Yêu cầu dashboard

Contract có thể kiểm tra bằng máy nằm tại `config/dashboard.yaml`. Hướng dẫn dựng và kiểm tra runtime nằm tại [DASHBOARD_SETUP.md](DASHBOARD_SETUP.md).

Dashboard chính cần đủ 6 nhóm thông tin:

1. Latency P50/P95/P99.
2. Traffic: request count hoặc QPS.
3. Error rate và breakdown theo loại lỗi.
4. Cost theo thời gian.
5. Tổng token input/output.
6. Quality proxy.

| Panel | Đơn vị | Ngưỡng hiển thị |
| --- | --- | --- |
| Latency percentiles | ms | P95 ≤ 3000 ms |
| Request traffic | requests/phút | ≥ 1 request/phút |
| Error rate and breakdown | % | ≤ 2% |
| Cost over time | USD | tổng ≤ $2.50 |
| Input and output tokens | tokens | ≤ 50,000 |
| Quality proxy | score 0-1 | ≥ 0.75 |

Nguồn dữ liệu của cả sáu panel là `data/logs.jsonl`.
Tất cả panel dùng time range 60 phút và refresh 30 giây theo contract.

Tiêu chuẩn trình bày:

- Khoảng thời gian mặc định: 1 giờ.
- Tự refresh mỗi 15–30 giây nếu công cụ hỗ trợ.
- Có threshold hoặc SLO line.
- Ghi rõ đơn vị.
- Chỉ giữ 6–8 panel quan trọng ở lớp chính.
- Screenshot phải nhìn được tên panel và khoảng thời gian.

Kiểm tra contract trước khi chụp evidence:

```bash
python scripts/validate_dashboard.py
```
