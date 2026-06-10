# Nhật Ký Thực Hiện Vibe Code (Implementation & Vibe Code Log)

Tài liệu này dùng để ghi lại chi tiết quá trình tự thực hiện viết mã (vibe code) trong dự án. Đối với mỗi lần thực hiện, chúng ta sẽ lưu lại đường dẫn thư mục, mã nguồn chi tiết và giải thích cụ thể cho đoạn mã đó.

---

## Danh Sách Các Phiên Vibe Code

### 📌 Phiên 1: Triển khai ETL Pipeline & Observability
- **Đường dẫn thư mục chứa file:** `/Users/adminicstrator/github-classroom/GDGoC-FPTU/data-pipeline-observability-2-tvtnoname`
- **File thực hiện:** `solution.py`

#### 💻 Mã nguồn thực hiện:
```python
def extract(file_path):
    print(f"Extracting data from {file_path}...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Extraction successful. Found {len(data)} records.")
        return data
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: File {file_path} is not a valid JSON file.")
        return []


def validate(data):
    valid_records = []
    error_count = 0
    seen_ids = set()

    print("\n--- Starting Data Validation ---")
    for idx, record in enumerate(data):
        record_id = record.get('id')
        product_name = record.get('product', 'Unknown Product')
        
        # 1. Kiem tra trung lap ID (nang cao)
        if record_id in seen_ids:
            print(f"  [Reject] Record {idx} ({product_name}): Duplicate ID '{record_id}' detected.")
            error_count += 1
            continue
            
        # 2. Kiem tra price
        price_val = record.get('price')
        try:
            price_float = float(price_val)
            if price_float <= 0:
                print(f"  [Reject] Record {idx} ({product_name}): Invalid price '{price_val}' (must be > 0).")
                error_count += 1
                continue
        except (ValueError, TypeError):
            print(f"  [Reject] Record {idx} ({product_name}): Invalid price format '{price_val}' (cannot convert to float).")
            error_count += 1
            continue
            
        # 3. Kiem tra category
        cat_val = record.get('category')
        if cat_val is None or not isinstance(cat_val, str) or cat_val.strip() == '':
            print(f"  [Reject] Record {idx} ({product_name}): Empty or missing category.")
            error_count += 1
            continue
            
        # Net hop le
        seen_ids.add(record_id)
        valid_records.append(record)
        print(f"  [Accept] Record {idx} ({product_name}) is valid.")

    print(f"\nValidation complete. Valid: {len(valid_records)} records kept, Errors: {error_count} records dropped.")
    return valid_records


def transform(data):
    if not data:
        print("Warning: No data to transform.")
        return pd.DataFrame()
        
    df = pd.DataFrame(data)
    
    # Dam bao price la float
    df['price'] = df['price'].astype(float)
    
    # 1. Tinh discounted_price = price * 0.9
    df['discounted_price'] = df['price'] * 0.9
    
    # 2. Chuan hoa category sang Title Case
    df['category'] = df['category'].astype(str).str.title()
    
    # 3. Them cot processed_at
    df['processed_at'] = datetime.datetime.now().isoformat()
    
    print(f"Transformation complete. DataFrame shape: {df.shape}")
    return df


def load(df, output_path):
    if df.empty:
        print("Warning: Empty DataFrame, not saving.")
        return
    df.to_csv(output_path, index=False)
    print(f"Data saved to {output_path}")
```

#### 📖 Giải thích đoạn mã (Explanation):
1. **Trích xuất dữ liệu (`extract`)**: Sử dụng thư viện chuẩn `json` để đọc file đầu vào. Có bổ sung cơ chế bắt lỗi ngoại lệ `FileNotFoundError` và `JSONDecodeError` để tránh việc chương trình bị tắt đột ngột (crash) khi gặp sự cố vật lý hay lỗi cú pháp file dữ liệu.
2. **Xác thực dữ liệu chặt chẽ (`validate`)**: Duyệt qua từng sản phẩm để kiểm tra chất lượng dữ liệu:
   - Ép kiểu giá (`price`) sang float và loại bỏ các sản phẩm có giá trị $\le 0$ hoặc không thể quy đổi sang số.
   - Loại bỏ các sản phẩm có trường `category` bị khuyết (`None`/`NaN`), trống (`""`) hoặc chỉ chứa khoảng trắng.
   - Bổ sung kiểm tra trùng lặp mã sản phẩm (`id`) thông qua một `set()` lưu vết các ID đã duyệt qua.
   - In chi tiết log lý do từ chối (Reject) hoặc chấp nhận (Accept) từng bản ghi cùng thống kê tổng hợp cuối cùng để đảm bảo khả năng quan sát (observability).
3. **Biến đổi dữ liệu (`transform`)**: Tạo `pd.DataFrame` từ dữ liệu sạch, sau đó thực hiện:
   - Tính toán cột giá chiết khấu giảm 10% (`discounted_price = price * 0.9`).
   - Chuẩn hóa chữ cái đầu của danh mục thành chữ hoa dạng Title Case (`.str.title()`).
   - Thêm trường `processed_at` dạng ISO timestamp hiện tại để phục vụ việc theo dõi vết dữ liệu (data lineage).
4. **Lưu trữ dữ liệu (`load`)**: Xuất DataFrame kết quả ra định dạng CSV và lưu vào file `processed_data.csv`.

---
### 📌 Phiên 2: Cập Nhật Đường Dẫn Phục Vụ Chạy Stress Test
- **Đường dẫn thư mục chứa file:** `/Users/adminicstrator/github-classroom/GDGoC-FPTU/data-pipeline-observability-2-tvtnoname`
- **File thực hiện:** `agent_simulation.py`

#### 💻 Mã nguồn thực hiện:
```python
    # Test with Clean Data
    print("Testing with CLEAN data:")
    print(simulate_agent_response("What is the best electronic product?", "processed_data.csv"))
```

#### 📖 Giải thích đoạn mã (Explanation):
1. **Thay đổi đường dẫn dữ liệu sạch**: Điều chỉnh đường dẫn truyền vào hàm `simulate_agent_response` từ đường dẫn mẫu bên ngoài (`../exercise-etl-automation/solution-code/processed_data.csv`) thành `processed_data.csv` ngay tại thư mục làm việc để Agent truy xuất trực tiếp file dữ liệu sạch do pipeline ETL vừa tạo ra ở Phiên 1.

