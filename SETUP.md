# Hướng dẫn Setup

## 1. Chuẩn bị dữ liệu

### Di chuyển file dữ liệu vào thư mục chung

Hiện tại có file dữ liệu trùng lặp trong cả `project1/` và `project2/`. Để tổ chức tốt hơn:

```bash
# Tạo thư mục data ở root
mkdir -p data

# Di chuyển file dữ liệu (chọn 1 trong 2)
mv "project1/data_motobikes.xlsx - Sheet1.csv" data/
# hoặc
mv "project2/data_motobikes.xlsx - Sheet1.csv" data/

# Xóa file trùng lặp còn lại
rm "project1/data_motobikes.xlsx - Sheet1.csv"  # nếu đã move từ project1
rm "project2/data_motobikes.xlsx - Sheet1.csv"  # nếu đã move từ project2
```

Sau khi di chuyển, các notebook và script sẽ tự động tìm file trong `data/` nhờ `config.py`.

## 2. Cài đặt môi trường

### Option 1: Môi trường chung cho cả 2 projects

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Cài tất cả dependencies
pip install -r project1/requirements.txt
pip install -r project2/requirements.txt
```

### Option 2: Môi trường riêng cho từng project

```bash
# Project 1
cd project1
python -m venv venv1
source venv1/bin/activate
pip install -r requirements.txt

# Project 2
cd project2
python -m venv venv2
source venv2/bin/activate
pip install -r requirements.txt
```

## 3. Cấu hình đường dẫn

Các file `config.py` đã được thiết lập để tự động tìm dữ liệu trong `data/`. Nếu bạn đặt file ở vị trí khác, chỉnh sửa:

- `project1/config.py` - cho Project 1
- `project2/config.py` - cho Project 2

## 4. Chạy thử

### Project 1 - Test preprocessing
```bash
cd project1
jupyter notebook preprocess_validate.ipynb
```

### Project 2 - Test analysis script
```bash
cd project2
python analysis.py
```

## 5. Chuẩn bị cho GitHub

Các file sau đã được gitignore (sẽ không được commit):
- Model files (`.joblib`, `.pkl`)
- Output CSV files (có thể regenerate)
- Plot images (`.png`, `.jpg`)
- Reports (`.html`)

Chỉ commit:
- Source code (`.py`, `.ipynb`)
- Configuration files (`config.py`, `requirements.txt`)
- README files
- `.gitignore`

## 6. Lưu ý khi deploy GUI

Khi triển khai GUI, cần:
1. **Models**: Copy các file từ `project1/models/` và `project1/artifacts/`
2. **Config**: Đảm bảo `config.py` trỏ đúng đường dẫn trong môi trường production
3. **Dependencies**: Cài đặt từ `requirements.txt`
4. **Data**: Đảm bảo có quyền truy cập file dữ liệu hoặc database

### Ví dụ structure cho GUI deployment:
```
gui_app/
├── app.py                 # Flask/FastAPI app
├── models/                # Copy từ project1/models/
├── artifacts/              # Copy từ project1/artifacts/
├── config.py              # Production config
├── templates/             # HTML templates
└── static/                # CSS, JS
```

