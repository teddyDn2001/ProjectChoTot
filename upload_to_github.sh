#!/bin/bash
# Script để upload project lên GitHub
# Chạy: bash upload_to_github.sh

echo "🚀 Bắt đầu upload lên GitHub..."
echo ""

# Kiểm tra git đã được init chưa
if [ ! -d ".git" ]; then
    echo "📦 Khởi tạo Git repository..."
    git init
    echo "✅ Đã khởi tạo Git"
else
    echo "✅ Git repository đã tồn tại"
fi

# Kiểm tra files lớn
echo ""
echo "📊 Kiểm tra files lớn (>25MB)..."
large_files=$(find . -type f -size +25M -not -path "./.git/*" 2>/dev/null)
if [ -n "$large_files" ]; then
    echo "⚠️  Phát hiện files lớn:"
    echo "$large_files" | while read file; do
        size=$(du -h "$file" | cut -f1)
        echo "   - $file ($size)"
    done
    echo ""
    echo "💡 Các file này sẽ được gitignore theo .gitignore"
else
    echo "✅ Không có file nào > 25MB"
fi

# Kiểm tra git status
echo ""
echo "📋 Files sẽ được commit:"
git status --short | head -20

# Hỏi có muốn tiếp tục không
echo ""
read -p "Bạn có muốn tiếp tục? (y/n): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Đã hủy"
    exit 1
fi

# Add files
echo ""
echo "➕ Đang add files..."
git add .
echo "✅ Đã add files"

# Commit
echo ""
read -p "Nhập commit message (hoặc Enter để dùng mặc định): " commit_msg
if [ -z "$commit_msg" ]; then
    commit_msg="Initial commit: Motorbike analysis projects"
fi

echo "💾 Đang commit..."
git commit -m "$commit_msg"
echo "✅ Đã commit"

# Đổi branch thành main
echo ""
echo "🌿 Đổi branch thành main..."
git branch -M main
echo "✅ Đã đổi branch"

# Hướng dẫn add remote và push
echo ""
echo "📝 Bước tiếp theo:"
echo "1. Tạo repository mới trên GitHub (https://github.com/new)"
echo "2. Chạy lệnh sau (thay YOUR_USERNAME và REPO_NAME):"
echo ""
echo "   git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git"
echo "   git push -u origin main"
echo ""
echo "Hoặc nếu đã có remote, chạy:"
echo "   git push -u origin main"
echo ""

