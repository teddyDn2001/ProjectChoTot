# 🚀 Deploy lên Streamlit Cloud

## 📋 Bước 1: Chuẩn bị

### ✅ Đã có sẵn:
- ✅ Code đã trên GitHub: `teddyDn2001/ProjectChoTot`
- ✅ File `requirements.txt` đã được tạo
- ✅ File `app.py` là main app

### ⚠️ Lưu ý quan trọng:

**Models và Data files:**
- Models (`.joblib` files) đã được gitignore
- Có 2 options:
  1. **Upload models lên GitHub** (dùng Git LFS cho file lớn)
  2. **Train models trên Streamlit Cloud** (chạy notebooks)

## 🚀 Bước 2: Deploy lên Streamlit Cloud

### Cách 1: Deploy từ GitHub (Khuyến nghị)

1. **Vào Streamlit Cloud:**
   - Truy cập: https://share.streamlit.io
   - Sign in với GitHub account

2. **Tạo app mới:**
   - Click "New app"
   - Chọn repository: `teddyDn2001/ProjectChoTot`
   - Branch: `main`
   - Main file path: `app.py`

3. **Click "Deploy"**

4. **Chờ deploy** (thường mất 2-5 phút)

### Cách 2: Deploy từ local (nếu có Streamlit CLI)

```bash
streamlit deploy
```

## ⚙️ Cấu hình sau khi deploy

### Nếu thiếu models:

**Option A: Upload models lên GitHub (Git LFS)**

```bash
# Cài Git LFS
brew install git-lfs  # macOS
# hoặc: https://git-lfs.github.com/

# Khởi tạo
git lfs install

# Track các file lớn
git lfs track "*.joblib"
git lfs track "data/*.csv"

# Add và commit
git add .gitattributes
git add project1/models/*.joblib
git add project1/artifacts/*.joblib
git commit -m "Add models with Git LFS"
git push origin main
```

**Option B: Train models trên Streamlit Cloud**

1. Tạo file `setup.py` để train models khi deploy
2. Hoặc tạo notebook riêng để train
3. Chạy training script trong app startup

### Nếu thiếu data files:

```bash
# Upload data file (nếu cần)
git add -f "data/data_motobikes.xlsx - Sheet1.csv"
git commit -m "Add data file"
git push origin main
```

## 🔧 Troubleshooting

### Lỗi: "Module not found"
- Kiểm tra `requirements.txt` có đầy đủ dependencies
- Đảm bảo tất cả imports đều có trong requirements

### Lỗi: "File not found" (models/data)
- Upload files lên GitHub
- Hoặc cập nhật paths trong config để tạo files mới

### Lỗi: "Memory limit exceeded"
- Models quá lớn (>1GB)
- Cân nhắc dùng Git LFS hoặc optimize models

### App chạy chậm
- Lần đầu load models sẽ chậm
- Streamlit Cloud có cache, lần sau sẽ nhanh hơn

## 📝 Checklist trước khi deploy

- [ ] Code đã push lên GitHub
- [ ] `requirements.txt` đã có đầy đủ dependencies
- [ ] `app.py` là file chính
- [ ] Models đã được upload (hoặc có plan train)
- [ ] Data files đã sẵn sàng (nếu cần)
- [ ] Đã test app local trước

## 🌐 Sau khi deploy thành công

1. **URL của app**: `https://[app-name].streamlit.app`
2. **Share link** với cô giáo và mọi người
3. **Monitor** trong Streamlit Cloud dashboard
4. **Update** code → tự động redeploy

## 💡 Tips

1. **Free tier**: Streamlit Cloud free có giới hạn, nhưng đủ cho demo
2. **Custom domain**: Có thể dùng domain riêng (paid)
3. **Secrets**: Dùng Streamlit secrets cho API keys (nếu cần)
4. **Auto-deploy**: Mỗi khi push code → tự động redeploy

## 🎉 Hoàn thành!

Sau khi deploy, bạn sẽ có:
- ✅ App chạy online 24/7
- ✅ Share được với mọi người
- ✅ Không cần server riêng
- ✅ Tự động update khi push code

---

**Link deploy**: https://share.streamlit.io

**Repository**: https://github.com/teddyDn2001/ProjectChoTot

