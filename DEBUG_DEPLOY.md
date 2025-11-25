# 🐛 Hướng dẫn Debug khi Deploy lên Streamlit Cloud

## Vấn đề: Vào được trang chủ nhưng các chức năng không hoạt động

### Nguyên nhân có thể:

1. **Models/Data chưa được push lên GitHub**
   - Files quá lớn (>100MB) cần Git LFS
   - Files bị gitignore
   - Chưa commit/push

2. **Lỗi khi load models trên Streamlit Cloud**
   - Path không đúng
   - File format không tương thích
   - Memory limit

3. **Dependencies thiếu**
   - Package chưa có trong requirements.txt
   - Version không tương thích

## 🔍 Cách kiểm tra:

### 1. Kiểm tra models/data có trên GitHub:

```bash
# Kiểm tra xem files có được track không
git ls-files project1/models/*.joblib
git ls-files project1/artifacts/*.joblib
git ls-files data/*.csv

# Kiểm tra trên GitHub web
# Vào: https://github.com/teddyDn2001/ProjectChoTot
# Xem có files trong:
# - project1/models/
# - project1/artifacts/
# - data/
```

### 2. Kiểm tra logs trên Streamlit Cloud:

1. Vào Streamlit Cloud dashboard
2. Click vào app của bạn
3. Xem tab "Logs" hoặc "Activity"
4. Tìm các lỗi như:
   - `FileNotFoundError`
   - `ModuleNotFoundError`
   - `MemoryError`

### 3. Kiểm tra error messages trong app:

App đã được cải thiện để hiển thị lỗi chi tiết hơn:
- Nếu thiếu models → sẽ hiển thị đường dẫn file bị thiếu
- Nếu lỗi load → sẽ hiển thị chi tiết lỗi

## 🔧 Cách khắc phục:

### Nếu models/data chưa có trên GitHub:

#### Option 1: Dùng Git LFS (Khuyến nghị cho files >100MB)

```bash
# 1. Cài Git LFS (nếu chưa có)
brew install git-lfs  # macOS
# hoặc: https://git-lfs.github.com/

# 2. Khởi tạo Git LFS
git lfs install

# 3. Track các file lớn
git lfs track "*.joblib"
git lfs track "data/*.csv"

# 4. Add .gitattributes
git add .gitattributes

# 5. Add và commit files
git add project1/models/*.joblib
git add project1/artifacts/*.joblib
git add data/*.csv

# 6. Commit và push
git commit -m "Add models and data files with Git LFS"
git push origin main
```

#### Option 2: Push trực tiếp (nếu files <100MB)

```bash
# Force add files (bỏ qua .gitignore)
git add -f project1/models/*.joblib
git add -f project1/artifacts/*.joblib
git add -f data/*.csv

# Commit và push
git commit -m "Add models and data files"
git push origin main
```

### Nếu có lỗi khi load models:

1. **Kiểm tra file format:**
   ```python
   # Test local trước
   import joblib
   model = joblib.load('project1/models/price_model.joblib')
   print(type(model))
   ```

2. **Kiểm tra paths:**
   - Đảm bảo paths trong `config.py` đúng
   - Streamlit Cloud chạy từ root của repo

3. **Kiểm tra memory:**
   - File `price_model.joblib` (113MB) có thể gây vấn đề
   - Cân nhắc optimize model hoặc dùng Git LFS

## 📋 Checklist:

- [ ] Models đã được push lên GitHub
- [ ] Data files đã được push lên GitHub
- [ ] Git LFS đã được setup (nếu files >100MB)
- [ ] requirements.txt có đầy đủ dependencies
- [ ] Đã test app local trước
- [ ] Đã xem logs trên Streamlit Cloud
- [ ] Error messages hiển thị rõ ràng trong app

## 🚀 Sau khi fix:

1. **Commit và push code mới:**
   ```bash
   git add app.py streamlit_app.py
   git commit -m "Improve error handling for deployment"
   git push origin main
   ```

2. **Chờ Streamlit Cloud auto-redeploy** (2-5 phút)

3. **Kiểm tra lại app:**
   - Vào từng chức năng
   - Xem error messages (nếu có)
   - Kiểm tra logs

## 💡 Tips:

- Luôn test local trước khi deploy
- Kiểm tra file sizes trước khi push
- Dùng Git LFS cho files >100MB
- Xem logs trên Streamlit Cloud để debug
- Error messages trong app sẽ giúp identify vấn đề

---

**Nếu vẫn gặp vấn đề:**
1. Copy error message từ app
2. Copy logs từ Streamlit Cloud
3. Kiểm tra xem files có trên GitHub không
4. Thử reload app (click "Relaunch to update")

