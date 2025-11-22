# 🎤 Script Demo cho Cô Giáo (Chi tiết)

## ⏱️ Tổng thời gian: ~15 phút

---

## 📌 PHẦN 1: GIỚI THIỆU (2 phút)

### Mở đầu:
> "Em xin chào cô. Hôm nay em xin phép được trình bày về đồ án Data Science của em. Em đã xây dựng một ứng dụng web tích hợp 2 projects chính:
> 
> **Project 1**: Dự đoán giá xe máy và phát hiện giá bất thường
> **Project 2**: Hệ thống gợi ý xe tương tự và phân cụm dữ liệu
> 
> Em đã tích hợp cả 2 projects này thành một ứng dụng web sử dụng Streamlit, có thể chạy trên trình duyệt và dễ dàng deploy lên cloud."

### Giới thiệu giao diện:
> "Đây là giao diện chính của ứng dụng. Bên trái là menu navigation với 4 tính năng:
> - Trang chủ: Tổng quan và trạng thái hệ thống
> - Dự đoán giá: Sử dụng model RandomForest từ Project 1
> - Phát hiện bất thường: Sử dụng Isolation Forest
> - Gợi ý xe tương tự: Từ Project 2"

**Action**: Click vào "🏠 Trang chủ", chỉ vào các metrics

---

## 💰 PHẦN 2: DEMO DỰ ĐOÁN GIÁ (4 phút)

### Giới thiệu:
> "Bây giờ em sẽ demo tính năng đầu tiên: Dự đoán giá xe máy. Tính năng này sử dụng mô hình RandomForest đã được train trên dữ liệu 7.2K tin rao bán xe máy ở TP.HCM."

**Action**: Click "💰 Dự đoán giá"

### Điền form:
> "Em sẽ nhập thông tin một chiếc xe để dự đoán giá. Ví dụ: một chiếc Honda SH 150i năm 2020, đã đi 15,000 km, tình trạng đã sử dụng."

**Điền form:**
```
Thương hiệu: Honda
Dòng xe: SH 150i
Năm đăng ký: 2020
Số km đã đi: 15000
Tình trạng: Đã sử dụng
Loại xe: Tay ga
Xuất xứ: Việt Nam
Dung tích xe: 150
Tỉnh/Thành: Hồ Chí Minh
Quận/Huyện: Quận 1
```

### Giải thích kết quả:
> "Sau khi nhấn nút Dự đoán giá, model RandomForest sẽ xử lý thông tin và đưa ra dự đoán. 
> 
> Kết quả cho thấy giá dự đoán là [X] triệu VNĐ. Model này đã được đánh giá với các metrics như MAE, RMSE, R² trong quá trình cross-validation.
> 
> Tính năng này có thể giúp người bán định giá hợp lý, hoặc người mua ước lượng giá trước khi mua."

**Action**: Click "🔮 Dự đoán giá", chỉ vào kết quả

---

## 🚨 PHẦN 3: PHÁT HIỆN BẤT THƯỜNG (4 phút)

### Giới thiệu:
> "Tính năng thứ hai là Phát hiện giá bất thường. Đây là một phần quan trọng trong Project 1, giúp kiểm duyệt các tin đăng có giá không phù hợp với thị trường."

**Action**: Click "🚨 Phát hiện bất thường"

### Demo case bình thường:
> "Em sẽ nhập thông tin một chiếc xe với giá hợp lý trước."

**Điền form (giá hợp lý):**
```
Thương hiệu: Honda
Dòng xe: SH 150i
Năm đăng ký: 2020
Số km: 15000
Tình trạng: Đã sử dụng
Loại xe: Tay ga
Dung tích: 150
Giá: 80,000,000 VNĐ
```

> "Kết quả cho thấy: Giá BÌNH THƯỜNG. Anomaly score là [X], cho thấy giá này phù hợp với thị trường."

### Demo case bất thường:
> "Bây giờ em sẽ thử với một giá bất thường, ví dụ quá thấp so với thị trường."

**Điền lại form (giá thấp bất thường):**
```
Giá: 20,000,000 VNĐ (giữ nguyên các thông tin khác)
```

> "Kết quả: Phát hiện giá BẤT THƯỜNG! Anomaly score âm cho thấy giá này không phù hợp. 
> 
> Tính năng này sử dụng 2 phương pháp:
> 1. Residual-based: So sánh giá thực tế với giá dự đoán
> 2. Isolation Forest: Phát hiện outliers trong không gian features
> 
> Có thể ứng dụng để tự động gắn cờ các tin đăng đáng ngờ, hỗ trợ team kiểm duyệt."

**Action**: Click "🔍 Kiểm tra" cho cả 2 cases

---

## 🔍 PHẦN 4: GỢI Ý XE TƯƠNG TỰ (3 phút)

### Giới thiệu:
> "Tính năng thứ ba đến từ Project 2: Gợi ý xe tương tự. Tính năng này giúp người dùng tìm các xe máy tương tự dựa trên thông tin một xe cụ thể."

**Action**: Click "🔍 Gợi ý xe tương tự"

### Demo tìm theo ID:
> "Em có thể tìm theo ID của một xe. Hệ thống sẽ tìm các xe tương tự dựa trên similarity scoring, xét các yếu tố như thương hiệu, giá, năm sản xuất, số km."

**Action**: Nhập một ID bất kỳ từ data, click "Tìm"

### Demo tìm kiếm nâng cao:
> "Ngoài ra, có tính năng tìm kiếm nâng cao, cho phép filter theo nhiều tiêu chí: thương hiệu, khoảng giá, năm sản xuất. 
> 
> Ví dụ, tìm các xe Honda trong khoảng 50-100 triệu, từ năm 2018-2022."

**Action**: Chọn "Thông tin tùy chỉnh", điền filters, click "Tìm kiếm"

> "Kết quả hiển thị danh sách các xe phù hợp. Tính năng này hữu ích cho người mua muốn so sánh và tìm xe phù hợp với ngân sách."

---

## 📊 PHẦN 5: TỔNG KẾT (2 phút)

### Nhấn mạnh điểm mạnh:
> "Tóm lại, em đã xây dựng được một ứng dụng web hoàn chỉnh với các điểm mạnh:
> 
> 1. **Tích hợp thành công**: Gộp 2 projects thành 1 ứng dụng thống nhất
> 2. **Giao diện thân thiện**: Dễ sử dụng, không cần kiến thức kỹ thuật
> 3. **Sẵn sàng deploy**: Có thể deploy lên Streamlit Cloud hoặc server
> 4. **Mở rộng được**: Có thể thêm nhiều tính năng khác"

### Hướng phát triển:
> "Về hướng phát triển tiếp theo, em có thể:
> - Tích hợp database thay vì file CSV
> - Thêm authentication và user management
> - Thêm visualization charts cho phân tích
> - Deploy production với Docker và CI/CD
> - Tích hợp API để các ứng dụng khác có thể sử dụng"

### Kết thúc:
> "Em xin cảm ơn cô đã lắng nghe. Em sẵn sàng trả lời các câu hỏi của cô."

---

## 💡 Tips khi demo

1. **Nói chậm rãi, rõ ràng**
2. **Giải thích từng bước trước khi làm**
3. **Highlight các điểm kỹ thuật quan trọng**
4. **Chuẩn bị sẵn data ví dụ**
5. **Nếu có lỗi, bình tĩnh giải thích**

## 🎯 Checklist trước khi demo

- [ ] Models đã được train và load được
- [ ] App đã test và chạy mượt
- [ ] Đã chuẩn bị data ví dụ
- [ ] Đã đọc kỹ script này
- [ ] Đã test các tính năng trước

---

**Chúc bạn demo thành công! 🎉**

