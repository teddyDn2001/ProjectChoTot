# 🏍️ Motorbike Analysis Platform - Streamlit App

Ứng dụng web tích hợp các tính năng từ Project 1 và Project 2.

## 🚀 Cài đặt và chạy

### 1. Cài đặt dependencies

```bash
pip install -r streamlit_requirements.txt
```

Hoặc cài đầy đủ từ cả 2 projects:

```bash
pip install -r project1/requirements.txt
pip install -r project2/requirements.txt
pip install streamlit
```

### 2. Chuẩn bị models (quan trọng!)

Trước khi chạy app, bạn cần train models:

```bash
# Chạy các notebooks trong project1/ để tạo models
cd project1
jupyter notebook

# Chạy theo thứ tự:
# 1. preprocess_validate.ipynb
# 2. prep_preprocessor.ipynb
# 3. train_price_models.ipynb
# 4. train_anomaly_models.ipynb
```

Sau khi train, các models sẽ được lưu trong:
- `project1/models/price_model.joblib`
- `project1/models/iso_model.joblib`
- `project1/artifacts/preprocessor.joblib`

### 3. Chuẩn bị dữ liệu

Đảm bảo file dữ liệu ở đúng vị trí:
- `data/data_motobikes.xlsx - Sheet1.csv` (cho recommendation)

Hoặc cập nhật đường dẫn trong `project2/config.py`.

### 4. Chạy ứng dụng

```bash
streamlit run app.py
```

App sẽ mở tự động tại: http://localhost:8501

## 📋 Các tính năng

### 💰 Dự đoán giá
- Nhập thông tin xe (thương hiệu, dòng xe, năm, km, ...)
- Dự đoán giá dựa trên RandomForest model
- Hiển thị kết quả dạng VNĐ và triệu VNĐ

### 🚨 Phát hiện bất thường
- Kiểm tra giá có bất thường so với thị trường
- Sử dụng Isolation Forest model
- Hiển thị anomaly score và cảnh báo

### 🔍 Gợi ý xe tương tự
- Tìm xe tương tự dựa trên thông tin
- Tìm kiếm theo ID, thương hiệu, hoặc dòng xe
- (Cần tích hợp recommendation models từ project2)

### 📊 Phân cụm dữ liệu
- Visualize clustering results
- (Cần tích hợp clustering models từ project2)

## 🏗️ Cấu trúc

```
.
├── app.py                      # Main Streamlit app
├── streamlit_requirements.txt  # Dependencies cho Streamlit
├── project1/                   # Price prediction & anomaly detection
│   ├── models/                 # Trained models (cần train trước)
│   └── artifacts/              # Preprocessor (cần train trước)
├── project2/                   # Recommendation & clustering
│   └── config.py               # Config paths
└── data/                       # Data files
```

## ⚠️ Lưu ý

1. **Models phải được train trước**: App cần models từ project1 để hoạt động
2. **Data files**: Đảm bảo file dữ liệu ở đúng vị trí hoặc cập nhật config
3. **Paths**: App sử dụng config từ project1 và project2, đảm bảo paths đúng

## 🔧 Troubleshooting

### Lỗi: "Models chưa được train"
- Chạy các notebooks trong project1/ để train models
- Đảm bảo models được lưu đúng vị trí

### Lỗi: "Không tìm thấy file dữ liệu"
- Kiểm tra file có trong `data/` không
- Hoặc cập nhật `project2/config.py`

### Lỗi import
- Đảm bảo đã cài đầy đủ dependencies
- Kiểm tra Python version (>= 3.8)

## 🚀 Deploy

### Deploy lên Streamlit Cloud

1. Push code lên GitHub (đã có)
2. Vào https://share.streamlit.io
3. Connect với repository: `teddyDn2001/ProjectChoTot`
4. Chọn file: `app.py`
5. Deploy!

**Lưu ý**: Cần upload models lên GitHub (có thể dùng Git LFS) hoặc train models trên cloud.

### Deploy local với Docker (tùy chọn)

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -r streamlit_requirements.txt
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 📝 TODO

- [ ] Tích hợp đầy đủ recommendation từ project2
- [ ] Tích hợp clustering visualization
- [ ] Thêm upload file CSV để batch prediction
- [ ] Thêm visualization charts
- [ ] Cải thiện UI/UX
- [ ] Thêm authentication (nếu cần)

## 📞 Support

Xem thêm:
- [README.md](README.md) - Tổng quan dự án
- [SETUP.md](SETUP.md) - Hướng dẫn setup
- [GitHub Repository](https://github.com/teddyDn2001/ProjectChoTot)

