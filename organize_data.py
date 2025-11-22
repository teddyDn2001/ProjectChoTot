#!/usr/bin/env python3
"""
Script để tổ chức file dữ liệu vào thư mục data/ chung
Chạy: python organize_data.py
"""
from pathlib import Path
import shutil

def organize_data_files():
    """Di chuyển file dữ liệu vào thư mục data/ chung"""
    repo_root = Path(__file__).parent
    data_dir = repo_root / "data"
    data_file_name = "data_motobikes.xlsx - Sheet1.csv"
    
    # Tạo thư mục data nếu chưa có
    data_dir.mkdir(exist_ok=True)
    target_file = data_dir / data_file_name
    
    # Tìm file trong project1 và project2
    source_files = [
        repo_root / "project1" / data_file_name,
        repo_root / "project2" / data_file_name,
    ]
    
    # Kiểm tra file nào tồn tại
    existing_files = [f for f in source_files if f.exists()]
    
    if not existing_files:
        print(f"❌ Không tìm thấy file {data_file_name} trong project1/ hoặc project2/")
        return
    
    # Nếu file đã có trong data/, hỏi có muốn ghi đè không
    if target_file.exists():
        print(f"⚠️  File đã tồn tại trong {target_file}")
        response = input("Bạn có muốn ghi đè? (y/n): ")
        if response.lower() != 'y':
            print("Bỏ qua.")
            return
    
    # Copy file đầu tiên tìm thấy vào data/
    source_file = existing_files[0]
    print(f"📁 Di chuyển {source_file} → {target_file}")
    shutil.copy2(source_file, target_file)
    print(f"✅ Đã copy file vào {target_file}")
    
    # Xóa các file trùng lặp
    for file_path in existing_files:
        if file_path != source_file:  # Không xóa file đã dùng để copy
            print(f"🗑️  Xóa file trùng: {file_path}")
            file_path.unlink()
        elif target_file != source_file:  # Nếu đã copy, xóa file gốc
            print(f"🗑️  Xóa file gốc: {file_path}")
            file_path.unlink()
    
    print("\n✅ Hoàn thành! File dữ liệu đã được tổ chức vào data/")
    print(f"📂 Vị trí: {target_file.absolute()}")

if __name__ == "__main__":
    organize_data_files()

