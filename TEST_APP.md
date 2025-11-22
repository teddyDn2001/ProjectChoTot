# ✅ App đã chạy thành công!

## 🌐 Truy cập app

**URL**: http://localhost:8501

Mở trình duyệt và vào link trên để xem app.

## 🧪 Test các tính năng

### 1. Trang chủ
- ✅ Kiểm tra models status
- ✅ Xem tổng quan

### 2. Dự đoán giá
**Test case:**
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
**Kỳ vọng**: Hiển thị giá dự đoán (triệu VNĐ)

### 3. Phát hiện bất thường
**Test case 1 - Giá bình thường:**
```
Giá: 80,000,000 VNĐ
(Các thông tin khác giống trên)
```
**Kỳ vọng**: "Giá BÌNH THƯỜNG"

**Test case 2 - Giá bất thường:**
```
Giá: 20,000,000 VNĐ (quá thấp)
```
**Kỳ vọng**: "Phát hiện giá BẤT THƯỜNG"

### 4. Gợi ý xe tương tự
**Test case:**
- Tìm theo ID: Nhập một ID bất kỳ từ data
- Tìm theo thương hiệu: Chọn "Honda"
- Tìm kiếm nâng cao: Filter theo giá 50-100 triệu, năm 2018-2022

**Kỳ vọng**: Hiển thị danh sách xe phù hợp

## 🐛 Nếu gặp lỗi

### Lỗi: "Models chưa được train"
- Kiểm tra: `ls project1/models/`
- Nếu thiếu, cần train models trước

### Lỗi: "Không tìm thấy file dữ liệu"
- Kiểm tra: `ls data/data_motobikes.xlsx*.csv`
- Hoặc cập nhật `project2/config.py`

### Lỗi import
- Chạy: `pip install -r streamlit_requirements.txt`

## 🛑 Dừng app

```bash
# Cách 1: Nhấn Ctrl+C trong terminal đang chạy streamlit

# Cách 2: Tìm và kill process
pkill -f streamlit

# Cách 3: Kill theo port
lsof -ti:8501 | xargs kill -9
```

## ✅ Checklist test

- [ ] App mở được trên trình duyệt
- [ ] Trang chủ hiển thị đúng
- [ ] Models status hiển thị "Sẵn sàng"
- [ ] Dự đoán giá hoạt động
- [ ] Phát hiện bất thường hoạt động
- [ ] Gợi ý xe hoạt động
- [ ] Không có lỗi trong console

## 🎉 Hoàn thành!

App đã sẵn sàng để demo cho cô giáo!

