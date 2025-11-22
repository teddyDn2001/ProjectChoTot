# 🚀 Hướng dẫn Push lên GitHub

## ✅ Đã sẵn sàng!

Code đã được commit và sẵn sàng push lên GitHub. Tất cả files lớn (>25MB) đã được gitignore.

## 📋 Các bước cuối cùng:

### Bước 1: Tạo repository trên GitHub

1. Vào https://github.com/new
2. Đặt tên repository (ví dụ: `motorbike-analysis` hoặc `do-an-data-science`)
3. **KHÔNG** tích "Initialize with README" (vì đã có sẵn)
4. Click "Create repository"

### Bước 2: Copy URL repository

Sau khi tạo, GitHub sẽ hiển thị URL, ví dụ:
- HTTPS: `https://github.com/YOUR_USERNAME/REPO_NAME.git`
- SSH: `git@github.com:YOUR_USERNAME/REPO_NAME.git`

### Bước 3: Thêm remote và push

Chạy các lệnh sau (thay `YOUR_USERNAME` và `REPO_NAME`):

```bash
# Thêm remote
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Push lên GitHub
git push -u origin main
```

## 🔐 Xác thực GitHub

### Nếu dùng HTTPS và được hỏi username/password:

1. **Username**: Tên GitHub của bạn
2. **Password**: Dùng **Personal Access Token** (không phải password GitHub)

**Cách tạo token:**
1. Vào https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Đặt tên token (ví dụ: "motorbike-project")
4. Chọn scope: ✅ `repo` (full control)
5. Click "Generate token"
6. **Copy token ngay** (chỉ hiện 1 lần)
7. Dán token khi được hỏi password

### Hoặc dùng SSH (khuyến nghị):

```bash
# Thay remote URL sang SSH
git remote set-url origin git@github.com:YOUR_USERNAME/REPO_NAME.git

# Push
git push -u origin main
```

## ✅ Kiểm tra sau khi push

Vào repository trên GitHub, bạn sẽ thấy:
- ✅ Tất cả notebooks
- ✅ Source code Python
- ✅ Configuration files
- ✅ Documentation (README, SETUP, etc.)
- ❌ Không có models, data files, outputs (đã gitignore)

## 🎯 Lệnh nhanh (copy-paste)

```bash
# 1. Thêm remote (THAY YOUR_USERNAME và REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# 2. Push
git push -u origin main
```

## 📝 Nếu đã có remote rồi

Nếu bạn đã thêm remote trước đó, chỉ cần:

```bash
git push -u origin main
```

## 🆘 Xử lý lỗi

### Lỗi: "remote origin already exists"
```bash
# Xóa remote cũ
git remote remove origin

# Thêm lại
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
```

### Lỗi: "Authentication failed"
- Kiểm tra lại username
- Dùng Personal Access Token thay vì password
- Hoặc chuyển sang SSH

### Lỗi: "file too large"
- Kiểm tra `.gitignore` đã loại bỏ đúng files chưa
- Xem file nào bị lỗi: `git ls-files | xargs ls -lh | grep -E "[0-9]+M"`

## 🎉 Hoàn thành!

Sau khi push thành công, bạn có thể:
- Share link repository
- Clone về máy khác
- Tiếp tục phát triển và push các thay đổi mới

