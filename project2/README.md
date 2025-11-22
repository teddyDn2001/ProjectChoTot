# Project 2 – Motorbike Recommendation & Segmentation

## Cấu trúc notebook
- `notebooks/01_problem_understanding.ipynb`: mô tả bối cảnh và mục tiêu bài toán.
- `notebooks/02_libraries_overview.ipynb`: liệt kê thư viện, cách cài đặt và sử dụng.
- `notebooks/03_data_loading.ipynb`: đọc dữ liệu CSV gốc, kiểm tra sơ bộ.
- `notebooks/04_eda_profile.ipynb`: sinh báo cáo EDA tự động (ydata_profiling, dataprep).
- `notebooks/05_preprocessing.ipynb`: làm sạch, chuẩn hóa, tạo ma trận đặc trưng cho mô hình.
- `notebooks/06_visualization.ipynb`: trực quan hóa phân phối và quan hệ giữa các biến.
- `notebooks/07_data_analysis.ipynb`: thống kê nâng cao, rút ra insight chính.
- `notebooks/08_model_selection.ipynb`: so sánh lựa chọn thuật toán cho recommendation & clustering (bao gồm thử nhiều giá trị k, chuẩn hóa dữ liệu đầu vào).
- `notebooks/09_modeling_evaluation.ipynb`: huấn luyện 5 mô hình gợi ý (KNN Full Features, KNN Numeric Only, KNN TF-IDF, Content-Based Cosine Matrix, Gensim Doc2Vec) và 3 mô hình phân cụm sklearn (KMeans, Gaussian Mixture, Agglomerative), đánh giá qua các chỉ số nội sinh.
- `notebooks/10_pyspark_clustering.ipynb`: huấn luyện 3 mô hình phân cụm PySpark (KMeans, GMM, Bisecting K-Means) theo yêu cầu đề bài, đánh giá qua silhouette score và WSSSE.

## Cấu hình đường dẫn

Trước khi chạy, cập nhật đường dẫn trong `config.py` hoặc đặt file dữ liệu vào thư mục `data/` ở root của repository.

```python
# Sử dụng config.py trong notebooks
from config import RAW_DATA_FILE, REPORTS_DIR, RANDOM_SEED
```

## Thiết lập môi trường
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt  # hoặc cài từng gói như hướng dẫn trong notebook 02
```

## Ghi chú quan trọng
- Trong môi trường làm việc hiện tại, việc import `pandas` gây lỗi segmentation fault nên các notebook chưa được chạy. Hãy tải về và chạy trên máy local.
- **Thư viện cần thiết**:
  - Cơ bản: `pandas`, `numpy`, `scikit-learn`, `matplotlib`, `seaborn`
  - EDA: `ydata_profiling`, `dataprep`
  - Recommendation: `gensim` (cho Doc2Vec)
  - Clustering PySpark: `pyspark` (cần Java JDK)
- Tạo sẵn các thư mục:
  - `reports/` cho output HTML từ EDA.
  - `artifacts/` nếu muốn lưu ma trận đặc trưng.
  - `figures/` cho hình ảnh trực quan hóa.
- Khi chạy các notebook có xử lý ma trận một-hot lớn (08, 09), cân nhắc máy có ≥8GB RAM.
- **Notebook 10 (PySpark)**: Cần cài đặt PySpark và Java JDK. Chạy trên máy có ≥8GB RAM để xử lý dữ liệu lớn.

## Đầu ra mong đợi
- Báo cáo EDA (`reports/*.html`).
- Ma trận đặc trưng cho modeling (`artifacts/features.npz`).
- **Notebook 09**: Bảng kết quả mô hình recommendation (5 mô hình: KNN Full Features, KNN Numeric Only, KNN TF-IDF, Content-Based Cosine Matrix, Gensim Doc2Vec) và clustering sklearn (3 mô hình: KMeans, GMM, Agglomerative) với các chỉ số đánh giá (silhouette, davies_bouldin, calinski_harabasz).
- **Notebook 10**: Bảng kết quả mô hình clustering PySpark (3 mô hình: PySpark KMeans, PySpark GMM, PySpark Bisecting K-Means) với silhouette score và WSSSE.

## Hướng phát triển tiếp theo
- Bổ sung embedding văn bản từ mô tả xe để cải thiện gợi ý.
- Áp dụng HDBSCAN hoặc Gaussian Mixture để so sánh với KMeans (đã có baseline GMM, có thể mở rộng thêm DBSCAN).
- Tích hợp giao diện web nhỏ (Streamlit) để demo tương tác.
