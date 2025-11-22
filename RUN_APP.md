# 🚀 Hướng dẫn chạy Streamlit App

## ⚡ Chạy nhanh

```bash
# 1. Cài đặt Streamlit và dependencies
pip install streamlit pandas numpy scikit-learn joblib

# 2. Chạy app
streamlit run app.py
```

App sẽ mở tự động tại: **http://localhost:8501**

## 📋 Các bước chi tiết

### Bước 1: Cài đặt dependencies

```bash
# Cài đặt từ file requirements
pip install -r streamlit_requirements.txt

# Hoặc cài đầy đủ từ cả 2 projects
pip install -r project1/requirements.txt
pip install -r project2/requirements.txt
pip install streamlit
```

### Bước 2: Chuẩn bị models (quan trọng!)

App cần models đã được train để hoạt động:

```bash
# Chạy notebooks trong project1/ để train models
cd project1

# Mở Jupyter và chạy theo thứ tự:
# 1. preprocess_validate.ipynb
# 2. prep_preprocessor.ipynb  
# 3. train_price_models.ipynb
# 4. train_anomaly_models.ipynb
```

Sau khi train, bạn sẽ có:
- ✅ `project1/models/price_model.joblib`
- ✅ `project1/models/iso_model.joblib`
- ✅ `project1/artifacts/preprocessor.joblib`

### Bước 3: Chuẩn bị dữ liệu (cho recommendation)

Đảm bảo file dữ liệu ở đúng vị trí:
- `data/data_motobikes.xlsx - Sheet1.csv`

Hoặc chạy script helper:
```bash
python organize_data.py
```

### Bước 4: Chạy app

```bash
streamlit run app.py
```

## 🎯 Các tính năng

### 💰 Dự đoán giá
- Nhập thông tin xe (thương hiệu, dòng, năm, km, ...)
- Dự đoán giá dựa trên RandomForest model
- Hiển thị kết quả

### 🚨 Phát hiện bất thường  
- Kiểm tra giá có bất thường
- Sử dụng Isolation Forest
- Hiển thị anomaly score

### 🔍 Gợi ý xe tương tự
- Tìm theo ID
- Tìm theo thương hiệu
- Tìm theo dòng xe
- Tìm kiếm nâng cao (filter theo giá, năm)

### 📊 Phân cụm (đang phát triển)
- Visualize clustering results

## ⚠️ Lưu ý

1. **Models phải được train trước** - App sẽ báo lỗi nếu không tìm thấy models
2. **Data files** - Cần file dữ liệu cho recommendation
3. **Paths** - Đảm bảo config paths đúng

## 🔧 Troubleshooting

### Lỗi: "Models chưa được train"
```bash
# Chạy notebooks trong project1/ để train
cd project1
jupyter notebook
```

### Lỗi: "Không tìm thấy file dữ liệu"
- Kiểm tra file có trong `data/` không
- Hoặc cập nhật `project2/config.py`

### Lỗi import
```bash
# Cài lại dependencies
pip install -r streamlit_requirements.txt
```

### App chạy chậm
- Lần đầu load models sẽ chậm (cache)
- Các lần sau sẽ nhanh hơn

## 🌐 Deploy lên Streamlit Cloud

1. Code đã có trên GitHub: `teddyDn2001/ProjectChoTot`
2. Vào https://share.streamlit.io
3. Sign in với GitHub
4. Click "New app"
5. Chọn repository: `teddyDn2001/ProjectChoTot`
6. Main file path: `app.py`
7. Click "Deploy"

**Lưu ý**: Cần upload models lên GitHub (dùng Git LFS) hoặc train models trên cloud.

## 📸 Screenshots

App có giao diện đẹp với:
- Sidebar navigation
- Form inputs cho prediction
- Results display với metrics
- Data tables cho recommendation

## 🎉 Hoàn thành!

App đã sẵn sàng để demo và deploy!

