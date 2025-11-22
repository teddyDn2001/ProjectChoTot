# Đồ án Data Science - Motorbike Analysis Projects

Repository chứa 2 dự án phân tích dữ liệu xe máy từ Chotot:

## 📁 Cấu trúc dự án

```
.
├── data/                          # Dữ liệu chung (đặt file CSV vào đây)
│   └── data_motobikes.xlsx - Sheet1.csv
├── project1/                      # Dự án 1: Price Prediction & Anomaly Detection
│   ├── notebooks/                 # Jupyter notebooks
│   ├── models/                     # Model artifacts (gitignored)
│   ├── artifacts/                 # Preprocessing artifacts (gitignored)
│   ├── anomaly_outputs/           # Anomaly detection results (gitignored)
│   ├── plots/                     # Visualization outputs (gitignored)
│   └── requirements.txt
├── project2/                      # Dự án 2: Recommendation & Clustering
│   ├── notebooks/                 # Jupyter notebooks
│   ├── reports/                   # EDA reports (gitignored)
│   ├── analysis.py                # Standalone Python script
│   └── requirements.txt
└── .gitignore
```

## 🚀 Quick Start

### 1. Chuẩn bị môi trường

```bash
# Tạo virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Cài đặt dependencies cho project1
cd project1
pip install -r requirements.txt

# Hoặc cho project2
cd project2
pip install -r requirements.txt
```

### 2. Chuẩn bị dữ liệu

- Đặt file `data_motobikes.xlsx - Sheet1.csv` vào thư mục `data/` ở root
- Hoặc cập nhật đường dẫn trong các notebook/script

## 📊 Project 1: Price Prediction & Anomaly Detection

**Mục tiêu:**
- Dự đoán giá xe máy dựa trên metadata
- Phát hiện các tin đăng có giá bất thường

**Thứ tự chạy notebooks:**
1. `preprocess_validate.ipynb` - Làm sạch dữ liệu
2. `prep_preprocessor.ipynb` - Tạo preprocessing pipeline
3. `train_price_models.ipynb` - Huấn luyện mô hình dự đoán giá
4. `train_anomaly_models.ipynb` - Phát hiện bất thường
5. `explain_price_model.ipynb` - Giải thích mô hình
6. `evaluate_anomalies.ipynb` - Đánh giá kết quả anomaly
7. `eda_basic.ipynb`, `eda_visuals.ipynb` - EDA

Xem chi tiết trong [project1/README.md](project1/README.md)

## 🎯 Project 2: Recommendation & Clustering

**Mục tiêu:**
- Hệ thống gợi ý xe máy tương tự
- Phân cụm (clustering) các xe máy

**Cấu trúc notebooks:**
- `01_problem_understanding.ipynb` - Hiểu bài toán
- `02_libraries_overview.ipynb` - Tổng quan thư viện
- `03_data_loading.ipynb` - Load dữ liệu
- `04_eda_profile.ipynb` - EDA tự động
- `05_preprocessing.ipynb` - Tiền xử lý
- `06_visualization.ipynb` - Trực quan hóa
- `07_data_analysis.ipynb` - Phân tích dữ liệu
- `08_model_selection.ipynb` - Chọn mô hình
- `09_modeling_evaluation.ipynb` - Đánh giá mô hình
- `10_pyspark_clustering.ipynb` - Clustering với PySpark

**Hoặc chạy script Python:**
```bash
cd project2
python analysis.py
```

Xem chi tiết trong [project2/README.md](project2/README.md)

## 📝 Lưu ý

- Các file output (models, plots, CSV results) được gitignore để giữ repo gọn
- Chạy lại notebooks để regenerate các file output
- Đảm bảo đã cài đặt đầy đủ dependencies trước khi chạy

## 🔧 Development

### Thêm dependencies mới
```bash
pip install <package>
pip freeze > requirements.txt
```

### Cấu trúc cho GUI deployment
- Các model artifacts trong `project1/models/` và `project1/artifacts/`
- Script `project2/analysis.py` có thể được import như module
- Có thể tạo API wrapper (Flask/FastAPI) để deploy

## 📄 License

Dự án học tập - Đồ án Data Science

