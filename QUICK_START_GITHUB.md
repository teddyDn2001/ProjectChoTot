# 🚀 Upload nhanh lên GitHub

## Bước 1: Tạo repository trên GitHub

1. Vào https://github.com/new
2. Đặt tên repository (ví dụ: `motorbike-analysis`)
3. **KHÔNG** tích "Initialize with README" (vì đã có sẵn)
4. Click "Create repository"

## Bước 2: Chạy các lệnh sau

```bash
# Commit code (nếu chưa commit)
git commit -m "Initial commit: Motorbike analysis projects"

# Đổi branch thành main
git branch -M main

# Thêm remote (THAY YOUR_USERNAME và REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Push lên GitHub
git push -u origin main
```

## ✅ Hoặc dùng script tự động

```bash
bash upload_to_github.sh
```

Sau đó làm theo hướng dẫn trên màn hình.

## 🔐 Nếu gặp lỗi authentication

### Cách 1: Dùng Personal Access Token
1. Tạo token tại: https://github.com/settings/tokens
2. Chọn scope: `repo`
3. Copy token
4. Khi push, nhập username và dán token làm password

### Cách 2: Dùng SSH
```bash
# Thay remote URL
git remote set-url origin git@github.com:YOUR_USERNAME/REPO_NAME.git
git push -u origin main
```

## 📊 Kiểm tra trước khi push

```bash
# Xem files sẽ được commit
git status

# Xem kích thước (không có file nào > 25MB)
git ls-files | xargs ls -lh | awk '{if ($5 ~ /M/ && $5+0 > 25) print "⚠️", $5, $9}'
```

## ✨ Sau khi push thành công

Repository sẽ có:
- ✅ Source code (notebooks, Python scripts)
- ✅ Configuration files
- ✅ Documentation
- ❌ Không có models, data files (đã gitignore)

Người khác có thể clone và chạy notebooks để generate lại outputs!

