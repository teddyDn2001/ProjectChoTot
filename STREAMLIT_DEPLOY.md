# 🚀 Hướng dẫn Deploy lên Streamlit Cloud

## ✅ Đã chuẩn bị sẵn:
- ✅ Code đã trên GitHub: `teddyDn2001/ProjectChoTot`
- ✅ File `requirements.txt` đã được tạo đầy đủ
- ✅ File `app.py` là main app
- ✅ File `.streamlit/config.toml` đã có cấu hình

## 🚀 Bước 1: Deploy lên Streamlit Cloud

### Cách làm:

1. **Truy cập Streamlit Cloud:**
   - Vào: https://share.streamlit.io
   - Đăng nhập bằng GitHub account (teddyDn2001)

2. **Tạo app mới:**
   - Click nút **"New app"** hoặc **"Deploy an app"**
   - Chọn:
     - **Repository**: `teddyDn2001/ProjectChoTot`
     - **Branch**: `main`
     - **Main file path**: `app.py`
     - **App URL** (tùy chọn): Có thể đặt tên như `motorbike-analysis` → URL sẽ là `https://motorbike-analysis.streamlit.app`

3. **Click "Deploy"**

4. **Chờ deploy** (thường mất 2-5 phút)
   - Streamlit Cloud sẽ tự động:
     - Clone repository
     - Cài đặt dependencies từ `requirements.txt`
     - Chạy `streamlit run app.py`

## ⚠️ Lưu ý quan trọng về Models và Data

### Vấn đề:
- Models (`.joblib` files) và data files (`.csv`) đã bị gitignore
- Streamlit Cloud cần có models để app chạy đầy đủ

### Giải pháp:

**Option 1: Upload models lên GitHub (Khuyến nghị)**

```bash
# 1. Cài Git LFS (nếu chưa có)
brew install git-lfs  # macOS
# hoặc tải từ: https://git-lfs.github.com/

# 2. Khởi tạo Git LFS
git lfs install

# 3. Track các file lớn
git lfs track "*.joblib"
git lfs track "data/*.csv"

# 4. Tạo file .gitattributes
git add .gitattributes

# 5. Add models và data
git add -f project1/models/*.joblib
git add -f project1/artifacts/*.joblib
git add -f data/data_motobikes.xlsx*.csv

# 6. Commit và push
git commit -m "Add models and data files with Git LFS"
git push origin main
```

**Option 2: Train models khi deploy (Nếu models quá lớn)**

Tạo file `setup.py` hoặc thêm logic train models trong app startup (không khuyến nghị vì chậm).

## 🔧 Sau khi deploy

### Kiểm tra app:
1. Truy cập URL được cung cấp (ví dụ: `https://motorbike-analysis.streamlit.app`)
2. Kiểm tra các chức năng:
   - ✅ Dự đoán giá
   - ✅ Phát hiện bất thường
   - ✅ Gợi ý xe tương tự
   - ✅ Phân cụm dữ liệu

### Nếu có lỗi:

**Lỗi: "Module not found"**
- Kiểm tra `requirements.txt` có đầy đủ dependencies
- Xem logs trong Streamlit Cloud dashboard

**Lỗi: "File not found" (models/data)**
- Upload files lên GitHub (dùng Git LFS)
- Hoặc kiểm tra paths trong `config.py`

**Lỗi: "Memory limit exceeded"**
- Models quá lớn (>1GB)
- Cân nhắc optimize models hoặc dùng Git LFS

## 📝 Checklist trước khi deploy

- [x] Code đã push lên GitHub
- [x] `requirements.txt` đã có đầy đủ dependencies
- [x] `app.py` là file chính
- [ ] Models đã được upload (hoặc có plan train)
- [ ] Data files đã sẵn sàng
- [x] Đã test app local trước
- [x] Email đã được thêm vào app

## 🌐 Sau khi deploy thành công

1. **URL của app**: `https://[app-name].streamlit.app`
2. **Share link** với cô giáo và mọi người
3. **Monitor** trong Streamlit Cloud dashboard
4. **Update** code → tự động redeploy (mỗi khi push lên GitHub)

## 💡 Tips

1. **Free tier**: Streamlit Cloud free có giới hạn, nhưng đủ cho demo
2. **Custom domain**: Có thể dùng domain riêng (paid plan)
3. **Secrets**: Dùng Streamlit secrets cho API keys (nếu cần)
4. **Auto-deploy**: Mỗi khi push code → tự động redeploy
5. **Logs**: Xem logs trong Streamlit Cloud dashboard để debug

## 🎉 Hoàn thành!

Sau khi deploy, bạn sẽ có:
- ✅ App chạy online 24/7
- ✅ Share được với mọi người
- ✅ Không cần server riêng
- ✅ Tự động update khi push code
- ✅ URL công khai để demo

---

**Link deploy**: https://share.streamlit.io

**Repository**: https://github.com/teddyDn2001/ProjectChoTot

**Email**: anhwin01@gmail.com

