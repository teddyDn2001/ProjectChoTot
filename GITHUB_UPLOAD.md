# Hướng dẫn Upload lên GitHub

## ⚠️ Lưu ý về giới hạn file

GitHub có giới hạn:
- **File đơn lẻ**: Tối đa 100MB (cảnh báo từ 50MB)
- **Khuyến nghị**: Giữ file < 25MB để tránh vấn đề

## 📋 Các file lớn đã được gitignore

Các file sau đã được loại bỏ khỏi git (theo `.gitignore`):
- ✅ `*.joblib` (models) - file `price_model.joblib` là 113MB
- ✅ `*.csv` (output files) - các file CSV kết quả
- ✅ `*.pdf` - file PDF 30MB
- ✅ `*.html` - reports
- ✅ `*.png`, `*.jpg` - plots/images

## 🚀 Các bước upload lên GitHub

### Bước 1: Khởi tạo Git repository

```bash
# Khởi tạo git repo
git init

# Thêm remote (thay YOUR_USERNAME và YOUR_REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

### Bước 2: Kiểm tra files sẽ được commit

```bash
# Xem các file sẽ được add
git status

# Xem kích thước các file sẽ commit
git ls-files | xargs ls -lh | awk '{print $5, $9}' | sort -hr | head -20
```

### Bước 3: Add và commit

```bash
# Add tất cả files (theo .gitignore)
git add .

# Commit
git commit -m "Initial commit: Motorbike analysis projects"
```

### Bước 4: Tạo branch main (nếu cần)

```bash
# Đổi tên branch thành main
git branch -M main
```

### Bước 5: Push lên GitHub

```bash
# Push lên GitHub
git push -u origin main
```

## 📦 Xử lý file lớn (nếu cần)

Nếu bạn muốn commit các file lớn (models, data), có 2 options:

### Option 1: Git LFS (Large File Storage)

```bash
# Cài Git LFS
brew install git-lfs  # macOS
# hoặc: https://git-lfs.github.com/

# Khởi tạo Git LFS
git lfs install

# Track các file lớn
git lfs track "*.joblib"
git lfs track "*.pdf"
git lfs track "data/*.csv"

# Add .gitattributes
git add .gitattributes
git commit -m "Add Git LFS tracking"
```

### Option 2: Loại bỏ file lớn (khuyến nghị)

Giữ file lớn ở local và chỉ commit code:
- Models có thể train lại từ notebooks
- Data files có thể lưu riêng hoặc dùng Google Drive/Dropbox
- Chỉ commit source code, config, và README

## ✅ Checklist trước khi push

- [ ] Đã kiểm tra `.gitignore` loại bỏ đúng files
- [ ] Không có file nào > 25MB trong git
- [ ] Đã test `git status` và thấy đúng files
- [ ] Đã tạo repo trên GitHub
- [ ] Đã có GitHub token/credentials

## 🔐 Xác thực GitHub

Nếu gặp lỗi authentication:

```bash
# Sử dụng Personal Access Token
# Tạo token tại: https://github.com/settings/tokens
git remote set-url origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/YOUR_REPO.git

# Hoặc dùng SSH
git remote set-url origin git@github.com:YOUR_USERNAME/YOUR_REPO.git
```

## 📝 Lệnh nhanh (copy-paste)

```bash
# 1. Init và add
git init
git add .

# 2. Commit
git commit -m "Initial commit: Motorbike analysis projects"

# 3. Đổi branch
git branch -M main

# 4. Add remote (THAY YOUR_USERNAME và REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# 5. Push
git push -u origin main
```

## 🎯 Kết quả mong đợi

Sau khi push thành công, trên GitHub sẽ có:
- ✅ Source code (Python scripts, notebooks)
- ✅ Configuration files (config.py, requirements.txt)
- ✅ Documentation (README.md, SETUP.md)
- ❌ Không có models, data files, output CSV (đã gitignore)

Người dùng khác có thể:
1. Clone repo
2. Cài dependencies từ `requirements.txt`
3. Chạy notebooks để generate lại models và outputs
