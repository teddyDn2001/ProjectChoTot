#!/bin/bash
# Script nhanh để chạy app Streamlit

echo "🚀 Khởi động Motorbike Analysis Platform..."
echo ""

# Kiểm tra Streamlit
if ! command -v streamlit &> /dev/null; then
    echo "⚠️  Streamlit chưa được cài đặt"
    echo "📦 Đang cài đặt Streamlit..."
    pip install streamlit pandas numpy scikit-learn joblib
    echo "✅ Đã cài đặt Streamlit"
fi

# Kiểm tra models
echo "🔍 Kiểm tra models..."
if [ -f "project1/models/price_model.joblib" ] && [ -f "project1/artifacts/preprocessor.joblib" ]; then
    echo "✅ Models đã sẵn sàng"
else
    echo "⚠️  Models chưa được train"
    echo "💡 Cần chạy notebooks trong project1/ để train models trước"
    echo ""
    read -p "Bạn có muốn tiếp tục không? (y/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Đã hủy"
        exit 1
    fi
fi

# Chạy app
echo ""
echo "🌐 Đang khởi động app..."
echo "📍 App sẽ mở tại: http://localhost:8501"
echo ""
streamlit run app.py

