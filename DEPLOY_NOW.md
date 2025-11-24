# 🚀 Deploy lên Streamlit Cloud - Hướng dẫn nhanh

## ⚠️ QUAN TRỌNG: Cần upload Models và Data lên GitHub

App cần có models và data để chạy đầy đủ. Hiện tại các file này đã bị gitignore.

## 📋 Bước 1: Cài Git LFS (để upload file lớn)

```bash
# Cài Git LFS
brew install git-lfs

# Khởi tạo
git lfs install

# Track các file lớn
git lfs track "*.joblib"
git lfs track "data/*.csv"

# Add .gitattributes
git add .gitattributes
git commit -m "Setup Git LFS"
git push origin main
```

## 📤 Bước 2: Upload Models và Data

```bash
# Update .gitignore để cho phép upload (tạm thời)
# Hoặc dùng git add -f để force add

# Add models và data
git add -f project1/models/*.joblib
git add -f project1/artifacts/*.joblib  
git add -f data/data_motobikes.xlsx*.csv

# Commit và push
git commit -m "Add models and data for deployment"
git push origin main
```

**Lưu ý:** File `price_model.joblib` (113MB) rất lớn. Nếu GitHub từ chối, cần dùng Git LFS.

## 🌐 Bước 3: Deploy lên Streamlit Cloud

1. **Truy cập:** https://share.streamlit.io
2. **Đăng nhập** bằng GitHub (teddyDn2001)
3. **Click "New app"** hoặc "Deploy an app"
4. **Điền thông tin:**
   - **Repository:** `teddyDn2001/ProjectChoTot`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL** (tùy chọn): `motorbike-analysis` → URL: `https://motorbike-analysis.streamlit.app`
5. **Click "Deploy"**
6. **Chờ 2-5 phút** để deploy xong

## ✅ Sau khi deploy

- App sẽ có URL: `https://[app-name].streamlit.app`
- Share link này để nộp bài
- Mỗi khi push code lên GitHub → tự động redeploy

## 🔧 Nếu có lỗi

**Lỗi: "Module not found"**
- Kiểm tra `requirements.txt` có đầy đủ dependencies

**Lỗi: "File not found" (models/data)**
- Đảm bảo đã upload models và data lên GitHub
- Kiểm tra paths trong `config.py`

**Lỗi: "Memory limit exceeded"**
- Models quá lớn, cần dùng Git LFS

---

**Link deploy:** https://share.streamlit.io  
**Repository:** https://github.com/teddyDn2001/ProjectChoTot

