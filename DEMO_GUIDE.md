# 🎬 Hướng dẫn Demo cho Cô Giáo

## 📋 Checklist trước khi demo

### ✅ Bước 1: Kiểm tra models đã có chưa

```bash
# Kiểm tra models
ls project1/models/
ls project1/artifacts/
```

**Nếu chưa có models**, cần train trước:
```bash
cd project1
jupyter notebook
# Chạy theo thứ tự:
# 1. preprocess_validate.ipynb
# 2. prep_preprocessor.ipynb
# 3. train_price_models.ipynb
# 4. train_anomaly_models.ipynb
```

### ✅ Bước 2: Cài đặt Streamlit

```bash
pip install streamlit pandas numpy scikit-learn joblib
```

### ✅ Bước 3: Chuẩn bị dữ liệu (cho recommendation)

```bash
# Đảm bảo file dữ liệu ở đúng vị trí
ls data/data_motobikes.xlsx*.csv
# Hoặc chạy:
python organize_data.py
```

## 🚀 Cách chạy app

### Cách 1: Chạy trực tiếp (khuyến nghị)

```bash
streamlit run app.py
```

App sẽ tự động mở tại: **http://localhost:8501**

### Cách 2: Chạy với port tùy chỉnh

```bash
streamlit run app.py --server.port 8502
```

## 🎯 Script Demo cho Cô Giáo

### **Phần 1: Giới thiệu tổng quan (2 phút)**

1. **Mở trình duyệt** → http://localhost:8501
2. **Giới thiệu giao diện:**
   - "Đây là ứng dụng web tích hợp 2 projects của em"
   - "Bên trái là menu navigation với 4 tính năng chính"
   - "Trang chủ hiển thị trạng thái models và tổng quan"

3. **Chỉ vào trang chủ:**
   - "Em đã tích hợp Project 1 (Price Prediction & Anomaly Detection)"
   - "Và Project 2 (Recommendation & Clustering)"
   - "Các models đã được train và sẵn sàng sử dụng"

### **Phần 2: Demo Dự đoán giá (3 phút)**

1. **Click vào "💰 Dự đoán giá"** trong sidebar

2. **Điền form ví dụ:**
   ```
   Thương hiệu: Honda
   Dòng xe: SH 150i
   Năm đăng ký: 2020
   Số km: 15000
   Tình trạng: Đã sử dụng
   Loại xe: Tay ga
   Xuất xứ: Việt Nam
   Dung tích: 150
   Tỉnh/Thành: Hồ Chí Minh
   Quận: Quận 1
   ```

3. **Click "🔮 Dự đoán giá"**

4. **Giải thích kết quả:**
   - "Model RandomForest đã dự đoán giá là X triệu VNĐ"
   - "Dựa trên các features như thương hiệu, năm, km, tình trạng..."
   - "Model này đã được train với dữ liệu 7.2K tin rao"

### **Phần 3: Demo Phát hiện bất thường (3 phút)**

1. **Click vào "🚨 Phát hiện bất thường"**

2. **Điền form ví dụ:**
   ```
   Thương hiệu: Honda
   Dòng xe: SH 150i
   Năm đăng ký: 2020
   Số km: 15000
   Tình trạng: Đã sử dụng
   Loại xe: Tay ga
   Dung tích: 150
   Giá: 50,000,000 VNĐ (giá thấp bất thường)
   ```

3. **Click "🔍 Kiểm tra"**

4. **Giải thích kết quả:**
   - "Isolation Forest model đã phát hiện giá này BẤT THƯỜNG"
   - "Anomaly score cho biết mức độ bất thường"
   - "Có thể dùng để kiểm duyệt tin đăng tự động"

### **Phần 4: Demo Gợi ý xe tương tự (3 phút)**

1. **Click vào "🔍 Gợi ý xe tương tự"**

2. **Demo tìm theo ID:**
   - "Nhập ID của một xe bất kỳ"
   - "Hệ thống sẽ tìm các xe tương tự dựa trên thương hiệu, giá, năm..."
   - "Sử dụng similarity scoring"

3. **Demo tìm kiếm nâng cao:**
   - "Có thể filter theo thương hiệu, khoảng giá, năm sản xuất"
   - "Hữu ích cho người mua tìm xe phù hợp"

### **Phần 5: Tổng kết (2 phút)**

1. **Nhấn mạnh điểm mạnh:**
   - "Tích hợp được cả 2 projects thành 1 ứng dụng web"
   - "Giao diện thân thiện, dễ sử dụng"
   - "Có thể deploy lên cloud để nhiều người dùng"

2. **Hướng phát triển:**
   - "Có thể thêm authentication"
   - "Tích hợp database thay vì file CSV"
   - "Thêm visualization charts"
   - "Deploy production với Docker"

## 🎤 Script nói khi demo

### Mở đầu:
> "Em xin phép được demo ứng dụng web tích hợp 2 projects của em. Ứng dụng này được xây dựng bằng Streamlit, tích hợp các models từ Project 1 và Project 2."

### Khi demo từng tính năng:
> "Bây giờ em sẽ demo tính năng [tên tính năng]. Tính năng này sử dụng [model/algorithm] từ Project [1/2] để [mô tả chức năng]."

### Kết thúc:
> "Đây là ứng dụng web hoàn chỉnh tích hợp các models đã train. Em có thể deploy lên Streamlit Cloud hoặc server để nhiều người sử dụng. Em xin cảm ơn cô đã lắng nghe."

## 💡 Tips khi demo

1. **Chuẩn bị trước:**
   - Test app trước khi demo
   - Chuẩn bị data ví dụ
   - Đảm bảo models đã load

2. **Trong khi demo:**
   - Nói rõ ràng, không vội
   - Giải thích từng bước
   - Highlight các điểm mạnh

3. **Xử lý lỗi:**
   - Nếu app lỗi, bình tĩnh
   - Giải thích: "Có thể do models chưa được train hoặc thiếu dependencies"
   - Có thể show code để giải thích

## 🔧 Troubleshooting nhanh

### App không chạy:
```bash
# Kiểm tra Streamlit đã cài chưa
pip install streamlit

# Chạy lại
streamlit run app.py
```

### Models không load:
```bash
# Kiểm tra models có tồn tại không
ls project1/models/
ls project1/artifacts/

# Nếu chưa có, cần train trước
```

### Lỗi import:
```bash
# Cài lại dependencies
pip install -r streamlit_requirements.txt
```

## 📸 Screenshots để chuẩn bị

Nếu cần, có thể chụp screenshots các tính năng để backup:
- Trang chủ với status models
- Form dự đoán giá
- Kết quả dự đoán
- Phát hiện bất thường
- Gợi ý xe tương tự

## ✅ Checklist cuối cùng

- [ ] Models đã được train
- [ ] Streamlit đã cài đặt
- [ ] App đã test và chạy được
- [ ] Data files đã sẵn sàng
- [ ] Đã chuẩn bị script demo
- [ ] Đã test các tính năng trước

---

**Chúc bạn demo thành công! 🎉**

