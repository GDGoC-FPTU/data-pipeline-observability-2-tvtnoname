# Experiment Report: Data Quality Impact on AI Agent

**Student ID:** AI20K-9999
**Name:** Nguyen Van A
**Date:** 2026-06-10

---

## 1. Ket qua thi nghiem

Chay `agent_simulation.py` voi 2 bo du lieu va ghi lai ket qua:

| Scenario | Agent Response | Accuracy (1-10) | Notes |
|----------|----------------|-----------------|-------|
| Clean Data (`processed_data.csv`) | Agent: Based on my data, the best choice is Laptop at $1200.0. | 10 | Agent nhận diện chính xác sản phẩm điện tử có giá tốt nhất và thông số hợp lệ. |
| Garbage Data (`garbage_data.csv`) | Agent: Based on my data, the best choice is Nuclear Reactor at $999999. | 1 | Agent bị đánh lừa bởi giá trị ngoại lai cực đoan (outlier) và đưa ra gợi ý phi thực tế. |

---

## 2. Phan tich & nhan xet

### Tai sao Agent tra loi sai khi dung Garbage Data?

Khi sử dụng dữ liệu rác (Garbage Data), AI Agent đã đưa ra câu trả lời hoàn toàn sai lệch và không thực tế (chọn lò phản ứng hạt nhân giá $999,999 cho truy vấn sản phẩm điện tử tốt nhất). Điều này xảy ra do các lỗi chất lượng dữ liệu nghiêm trọng sau:

1. **Giá trị ngoại lai cực đoan (Outliers)**: Sản phẩm 'Nuclear Reactor' với giá $999,999 đã làm sai lệch thuật toán tìm kiếm sản phẩm tốt nhất dựa trên giá cao nhất của Agent. Trong thực tế, các outlier này sẽ làm lệch phân phối dữ liệu huấn luyện hoặc thông tin ngữ cảnh, dẫn đến việc LLM đưa ra các phản hồi ảo tưởng (hallucination).
2. **Sai kiểu dữ liệu (Wrong Data Types)**: Bản ghi 'Broken Chair' có giá là chuỗi chữ `'ten dollars'`. Nếu Agent thực hiện các phép tính toán số học trên cột giá này, hệ thống sẽ lập tức bị crash với lỗi TypeError hoặc ValueError. Điều này làm mất tính ổn định và tin cậy của ứng dụng AI.
3. **Trùng lặp ID (Duplicate IDs)**: Bản ghi số 1 có hai sản phẩm khác nhau là 'Laptop' và 'Banana'. Trùng lặp ID gây ra sự không đồng nhất về dữ liệu (data inconsistency), làm rối loạn cơ chế lập chỉ mục (indexing) và truy vấn chính xác của cơ sở dữ liệu Vector hoặc RAG.
4. **Giá trị rỗng/Null**: Bản ghi 'Ghost Item' chứa các trường `None` hoặc trống. Khi đưa vào ngữ cảnh của LLM, các trường rỗng này tạo ra thông tin thiếu hụt, khiến LLM phản hồi thiếu chính xác hoặc không thể suy luận.

---

## 3. Ket luan

**Quality Data > Quality Prompt?** 

Tôi hoàn toàn đồng ý. Trong phát triển ứng dụng AI và LLM, chất lượng dữ liệu đóng vai trò quyết định hơn nhiều so với việc tối ưu hóa câu lệnh (Prompt). Nếu dữ liệu đầu vào chứa nhiều thông tin sai lệch, sai kiểu hoặc outlier, dù prompt có được thiết kế hoàn hảo đến đâu thì LLM vẫn sẽ truy xuất thông tin sai (garbage in, garbage out). Xây dựng một đường ống dẫn dữ liệu ETL chuẩn hóa và sạch sẽ là nền tảng cốt lõi để đảm bảo độ tin cậy và chính xác cho mọi ứng dụng AI.

