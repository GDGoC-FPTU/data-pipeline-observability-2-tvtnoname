"""
==============================================================
Day 10 Lab: Build Your First Automated ETL Pipeline
==============================================================
Student ID: AI20K-9999
Name: Nguyen Van A

Nhiem vu:
   1. Extract:   Doc du lieu tu file JSON
   2. Validate:  Kiem tra & loai bo du lieu khong hop le
   3. Transform: Chuan hoa category + tinh gia giam 10%
   4. Load:      Luu ket qua ra file CSV

Cham diem tu dong:
   - Script phai chay KHONG LOI (20d)
   - Validation: loai record gia <= 0, category rong (10d)
   - Transform: discounted_price + category Title Case (10d)
   - Logging: in so record processed/dropped (10d)
   - Timestamp: them cot processed_at (10d)
==============================================================
"""

import json
import pandas as pd
import os
import datetime

# --- CONFIGURATION ---
SOURCE_FILE = 'raw_data.json'
OUTPUT_FILE = 'processed_data.csv'


def extract(file_path):
    """
    Task 1: Doc du lieu JSON tu file.

    Goi y:
       - Dung json.load() de doc file JSON
       - Xu ly truong hop file khong ton tai (FileNotFoundError)

    Returns:
        list: Danh sach cac records (dictionaries)
    """
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
    """
    Task 2: Kiem tra chat luong du lieu.

    Quy tac validation:
       - Price phai > 0 (loai bo gia am hoac bang 0)
       - Category khong duoc rong

    Goi y:
       - Dung record.get('price', 0) de lay gia
       - Dung record.get('category') de kiem tra category
       - In ra so luong record hop le va khong hop le

    Returns:
        list: Danh sach cac records hop le
    """
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

    print(f"\nValidation complete. Valid: {len(valid_records)} kept, Errors: {error_count} dropped.")
    return valid_records


def transform(data):
    """
    Task 3: Ap dung business logic.

    Yeu cau:
       - Tinh discounted_price = price * 0.9 (giam 10%)
       - Chuan hoa category thanh Title Case (vi du: "electronics" -> "Electronics")
       - Them cot processed_at = timestamp hien tai

    Goi y:
       - Dung pd.DataFrame(data) de tao DataFrame
       - df['discounted_price'] = df['price'] * 0.9
       - df['category'] = df['category'].str.title()
       - df['processed_at'] = datetime.datetime.now().isoformat()

    Returns:
        pd.DataFrame: DataFrame da duoc transform
    """
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
    """
    Task 4: Luu DataFrame ra file CSV.

    Goi y:
       - df.to_csv(output_path, index=False)
    """
    if df.empty:
        print("Warning: Empty DataFrame, not saving.")
        return
    df.to_csv(output_path, index=False)
    print(f"Data saved to {output_path}")


# ============================================================
# MAIN PIPELINE
# ============================================================
if __name__ == "__main__":
    print("=" * 50)
    print("ETL Pipeline Started...")
    print("=" * 50)

    # 1. Extract
    raw_data = extract(SOURCE_FILE)

    if raw_data:
        # 2. Validate
        clean_data = validate(raw_data)

        # 3. Transform
        final_df = transform(clean_data)

        # 4. Load
        if final_df is not None:
            load(final_df, OUTPUT_FILE)
            print(f"\nPipeline completed! {len(final_df)} records saved.")
        else:
            print("\nTransform returned None. Check your transform() function.")
    else:
        print("\nPipeline aborted: No data extracted.")
