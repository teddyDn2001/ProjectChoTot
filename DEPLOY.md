# 🚀 Hướng dẫn Deploy lên Streamlit Cloud

## ✅ Trạng thái hiện tại

- ✅ Code đã trên GitHub: `teddyDn2001/ProjectChoTot`
- ✅ File `requirements.txt` đã có đầy đủ dependencies
- ✅ File `app.py` và `streamlit_app.py` sẵn sàng
- ✅ Models và data đã được upload (nếu có)

## 🚀 Bước 1: Deploy lên Streamlit Cloud

### Cách làm:

1. **Truy cập Streamlit Cloud:**
   - Vào: https://share.streamlit.io
   - Đăng nhập bằng GitHub account (teddyDn2001)

2. **Tạo app mới:**
   - Click nút **"New app"** hoặc **"Deploy an app"**
   - Điền thông tin:
     - **Repository:** `teddyDn2001/ProjectChoTot`
     - **Branch:** `main`
     - **Main file path:** `streamlit_app.py`
     - **App URL** (tùy chọn): `motorbike-analysis` → URL: `https://motorbike-analysis.streamlit.app`

3. **Click "Deploy"**

4. **Chờ deploy** (thường mất 2-5 phút)
   - Streamlit Cloud sẽ tự động:
     - Clone repository
     - Cài đặt dependencies từ `requirements.txt`
     - Chạy `streamlit run streamlit_app.py`

## ⚠️ Lưu ý quan trọng về Models và Data

### Vấn đề:
- Models (`.joblib` files) và data files (`.csv`) cần có trên GitHub
- Streamlit Cloud cần có models để app chạy đầy đủ

### Giải pháp:

**Option 1: Upload models lên GitHub với Git LFS (Khuyến nghị)**

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

## 🐛 Debug khi có lỗi

### Lỗi thường gặp:

**1. "Module not found"**
- Kiểm tra `requirements.txt` có đầy đủ dependencies
- Xem logs trong Streamlit Cloud dashboard

**2. "File not found" (models/data)**
- Upload files lên GitHub (dùng Git LFS)
- Kiểm tra paths trong `config.py`
- Đảm bảo files có trong repository

**3. "Memory limit exceeded"**
- Models quá lớn (>1GB)
- Cân nhắc optimize models hoặc dùng Git LFS

**4. "Feature mismatch" (X has 278 features, but model expects 279)**
- Đã được fix trong code mới nhất
- Đảm bảo đã pull code mới nhất

### Cách kiểm tra:

1. **Kiểm tra models/data có trên GitHub:**
   ```bash
   git ls-files project1/models/*.joblib
   git ls-files project1/artifacts/*.joblib
   git ls-files data/*.csv
   ```

2. **Xem logs trên Streamlit Cloud:**
   - Vào Streamlit Cloud dashboard
   - Click vào app của bạn
   - Xem tab "Logs" hoặc "Activity"

3. **Kiểm tra error messages trong app:**
   - App hiển thị lỗi chi tiết với hướng dẫn khắc phục

## 📋 Checklist trước khi deploy

- [x] Code đã push lên GitHub
- [x] `requirements.txt` đã có đầy đủ dependencies
- [x] `streamlit_app.py` là file chính
- [ ] Models đã được upload (hoặc có plan train)
- [ ] Data files đã sẵn sàng
- [x] Đã test app local trước
- [x] Email đã được thêm vào app

## 🌐 Sau khi deploy thành công

1. **URL của app:** `https://[app-name].streamlit.app`
2. **Share link** với cô giáo và mọi người
3. **Monitor** trong Streamlit Cloud dashboard
4. **Update** code → tự động redeploy (mỗi khi push lên GitHub)

## 💡 Tips

1. **Free tier:** Streamlit Cloud free có giới hạn, nhưng đủ cho demo
2. **Custom domain:** Có thể dùng domain riêng (paid plan)
3. **Secrets:** Dùng Streamlit secrets cho API keys (nếu cần)
4. **Auto-deploy:** Mỗi khi push code → tự động redeploy
5. **Logs:** Xem logs trong Streamlit Cloud dashboard để debug

## 🎉 Hoàn thành!

Sau khi deploy, bạn sẽ có:
- ✅ App chạy online 24/7
- ✅ Share được với mọi người
- ✅ Không cần server riêng
- ✅ Tự động update khi push code
- ✅ URL công khai để demo

---

**Link deploy:** https://share.streamlit.io  
**Repository:** https://github.com/teddyDn2001/ProjectChoTot  
**Email:** anhwin01@gmail.com

