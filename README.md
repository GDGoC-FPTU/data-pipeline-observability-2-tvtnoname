[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=24112743&assignment_repo_type=AssignmentRepo)
# Day 10 Lab: Data Pipeline & Data Observability

**Student Email:** student@example.com
**Name:** Nguyen Van A
**Student ID:** AI20K-9999

---

## Mo ta

Bài thực hành này xây dựng một pipeline ETL (Extract, Transform, Load) tự động bằng Python để trích xuất dữ liệu sản phẩm từ file JSON, kiểm tra tính đúng đắn của dữ liệu (xác thực giá bán và danh mục sản phẩm), chuyển đổi và chuẩn hóa định dạng, sau đó lưu kết quả đã làm sạch ra file CSV. Đồng thời thực nghiệm để so sánh phản hồi của AI Agent trên dữ liệu sạch và dữ liệu rác nhằm thấy rõ vai trò của Chất lượng dữ liệu (Data Quality).

---

## Cach chay (How to Run)

### Prerequisites
```bash
pip install pandas pytest
```

### Chay ETL Pipeline
```bash
python solution.py
```

### Chay Agent Simulation (Stress Test)
Để chạy mô phỏng hành vi của AI Agent, thực hiện các lệnh sau:
```bash
# 1. Sinh dữ liệu rác
python generate_garbage.py

# 2. Chạy file mô phỏng để xem so sánh
python agent_simulation.py
```

---

## Cau truc thu muc

```
├── solution.py              # ETL Pipeline script
├── processed_data.csv       # Output cua pipeline
├── experiment_report.md     # Bao cao thi nghiem
├── README.md                # File nay
└── docs/
    └── document.md          # Tài liệu ghi nhận vibe code
```

---

## Ket qua

Đường ống dẫn dữ liệu ETL đã hoạt động tốt và ổn định:
- Đã đọc 5 bản ghi từ file raw_data.json.
- Loại bỏ thành công 2 bản ghi lỗi: 1 bản ghi có giá trị âm (Mystery Box) và 1 bản ghi thiếu danh mục sản phẩm (Phone).
- Lưu thành công 3 bản ghi sạch đã qua chuyển đổi (Laptop, Chair, Monitor) vào processed_data.csv.
- Thử nghiệm Stress Test cho thấy AI Agent hoạt động chính xác 100% với dữ liệu sạch nhưng trả về kết quả sai hoàn toàn (chọn lò phản ứng hạt nhân có giá trị ngoại lai $999999) khi gặp dữ liệu rác.
