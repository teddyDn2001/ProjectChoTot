# 🔧 Sửa lỗi: Models không tìm thấy trên Streamlit Cloud

## Vấn đề
File `price_model.joblib` (113MB) không được tìm thấy trên Streamlit Cloud mặc dù đã được commit với Git LFS.

## Nguyên nhân
Git LFS files cần được push riêng sau khi commit. Streamlit Cloud có thể không tự động pull Git LFS files.

## Giải pháp

### Option 1: Push Git LFS files (Khuyến nghị)

```bash
# 1. Đảm bảo Git LFS đã được cài và khởi tạo
git lfs install

# 2. Push tất cả Git LFS files
git lfs push origin main --all

# 3. Kiểm tra xem files đã được push
git lfs ls-files
```

### Option 2: Kiểm tra trên GitHub

1. Vào: https://github.com/teddyDn2001/ProjectChoTot
2. Kiểm tra file `project1/models/price_model.joblib`
3. Nếu thấy file là pointer (text file nhỏ) → Git LFS chưa được push đúng
4. Nếu thấy file lớn (113MB) → File đã có trên GitHub

### Option 3: Re-push với Git LFS

```bash
# 1. Đảm bảo .gitattributes đúng
cat .gitattributes
# Phải có: *.joblib filter=lfs diff=lfs merge=lfs -text

# 2. Re-track files
git lfs track "*.joblib"
git add .gitattributes

# 3. Re-add và commit
git add project1/models/price_model.joblib
git commit -m "Re-add price_model.joblib with Git LFS"

# 4. Push cả code và LFS
git push origin main
git lfs push origin main --all
```

### Option 4: Nếu Streamlit Cloud không hỗ trợ Git LFS tốt

Có thể cần upload models lên một storage service khác (Google Drive, S3) và download khi app khởi động.

## Kiểm tra sau khi fix

1. Vào Streamlit Cloud dashboard
2. Click "Relaunch to update"
3. Kiểm tra logs xem có lỗi gì không
4. Kiểm tra lại status cards trong app

## Lưu ý

- File `price_model.joblib` rất lớn (113MB) nên cần Git LFS
- Streamlit Cloud free tier có giới hạn về file size
- Nếu vẫn không được, có thể cần optimize model hoặc dùng cách khác

