"""
Streamlit App - Motorbike Analysis Platform
Ứng dụng web tích hợp các tính năng từ Project 1 và Project 2
"""
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add project paths to sys.path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT / "project1"))
sys.path.insert(0, str(PROJECT_ROOT / "project2"))

# Page config
st.set_page_config(
    page_title="Motorbike Analysis Platform",
    page_icon="🏍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'models_loaded' not in st.session_state:
    st.session_state.models_loaded = False

# Sidebar navigation
st.sidebar.title("🏍️ Motorbike Analysis")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Chọn chức năng:",
    ["🏠 Trang chủ", "💰 Dự đoán giá", "🚨 Phát hiện bất thường", "🔍 Gợi ý xe tương tự", "📊 Phân cụm dữ liệu"]
)

# Import modules (lazy loading)
@st.cache_resource
def load_price_model():
    """Load price prediction model"""
    try:
        from project1.config import PRICE_MODEL_PATH, PREPROCESSOR_PATH
        import joblib
        
        if not PRICE_MODEL_PATH.exists() or not PREPROCESSOR_PATH.exists():
            return None, None, "Models chưa được train. Vui lòng chạy notebooks trong project1/ để tạo models."
        
        model = joblib.load(PRICE_MODEL_PATH)
        preprocessor_data = joblib.load(PREPROCESSOR_PATH)
        preprocessor = preprocessor_data['preprocessor']
        return model, preprocessor, None
    except Exception as e:
        return None, None, f"Lỗi khi load model: {str(e)}"

@st.cache_resource
def load_anomaly_model():
    """Load anomaly detection model"""
    try:
        from project1.config import ISO_MODEL_PATH, PREPROCESSOR_PATH
        import joblib
        
        if not ISO_MODEL_PATH.exists() or not PREPROCESSOR_PATH.exists():
            return None, None, "Models chưa được train."
        
        iso_model = joblib.load(ISO_MODEL_PATH)
        preprocessor_data = joblib.load(PREPROCESSOR_PATH)
        preprocessor = preprocessor_data['preprocessor']
        return iso_model, preprocessor, None
    except Exception as e:
        return None, None, f"Lỗi khi load model: {str(e)}"

@st.cache_data
def load_sample_data():
    """Load sample data for recommendation"""
    try:
        from project2.config import RAW_DATA_FILE, DATA_DIR
        
        # Try multiple paths
        possible_paths = [
            RAW_DATA_FILE,  # data/data_motobikes.xlsx - Sheet1.csv
            PROJECT_ROOT / "data" / "data_motobikes.xlsx - Sheet1.csv",
            PROJECT_ROOT / "project2" / "data_motobikes.xlsx - Sheet1.csv",
            PROJECT_ROOT / "project1" / "data_motobikes.xlsx - Sheet1.csv",
        ]
        
        for path in possible_paths:
            if path.exists():
                df = pd.read_csv(path, nrows=1000, low_memory=False)  # Load sample
                return df, None
        
        return None, f"Không tìm thấy file dữ liệu. Đã thử: {[str(p) for p in possible_paths]}"
    except Exception as e:
        return None, f"Lỗi khi load dữ liệu: {str(e)}"

# Home page
if page == "🏠 Trang chủ":
    st.markdown('<div class="main-header">🏍️ Motorbike Analysis Platform</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 💰 Dự đoán giá")
        st.markdown("""
        Dự đoán giá xe máy dựa trên:
        - Thương hiệu, dòng xe
        - Năm đăng ký, số km
        - Tình trạng, dung tích
        """)
    
    with col2:
        st.markdown("### 🚨 Phát hiện bất thường")
        st.markdown("""
        Phát hiện các tin đăng có giá bất thường:
        - Residual-based detection
        - Isolation Forest
        """)
    
    with col3:
        st.markdown("### 🔍 Gợi ý")
        st.markdown("""
        Tìm xe máy tương tự:
        - KNN-based recommendation
        - Content-based filtering
        """)
    
    st.markdown("---")
    st.markdown("### 📊 Thống kê")
    
    # Check models status
    price_model, _, price_err = load_price_model()
    anomaly_model, _, anomaly_err = load_anomaly_model()
    sample_data, data_err = load_sample_data()
    
    status_col1, status_col2, status_col3 = st.columns(3)
    
    with status_col1:
        if price_model:
            st.success("✅ Price Model: Sẵn sàng")
        else:
            st.error(f"❌ Price Model: {price_err or 'Chưa load'}")
    
    with status_col2:
        if anomaly_model:
            st.success("✅ Anomaly Model: Sẵn sàng")
        else:
            st.error(f"❌ Anomaly Model: {anomaly_err or 'Chưa load'}")
    
    with status_col3:
        if sample_data is not None:
            st.success(f"✅ Data: {len(sample_data)} records")
        else:
            st.error(f"❌ Data: {data_err or 'Chưa load'}")

# Price Prediction page
elif page == "💰 Dự đoán giá":
    st.title("💰 Dự đoán giá xe máy")
    st.markdown("Nhập thông tin xe để dự đoán giá")
    
    model, preprocessor, error = load_price_model()
    
    if error:
        st.error(error)
        st.info("💡 Hướng dẫn: Chạy các notebooks trong project1/ để train models trước.")
    else:
        with st.form("price_prediction_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                thuong_hieu = st.selectbox("Thương hiệu", ["Honda", "Yamaha", "SYM", "Piaggio", "Vespa", "Khác"])
                dong_xe = st.text_input("Dòng xe", placeholder="Ví dụ: SH, Air Blade, Exciter")
                nam_dang_ky = st.number_input("Năm đăng ký", min_value=1990, max_value=2024, value=2020)
                so_km = st.number_input("Số km đã đi", min_value=0, value=10000)
            
            with col2:
                tinh_trang = st.selectbox("Tình trạng", ["Mới", "Đã sử dụng", "Cần sửa chữa"])
                loai_xe = st.selectbox("Loại xe", ["Tay ga", "Số", "Tay côn", "Khác"])
                xuat_xu = st.selectbox("Xuất xứ", ["Việt Nam", "Thái Lan", "Indonesia", "Nhật Bản", "Khác"])
                dung_tich_cc = st.number_input("Dung tích (cc)", min_value=50, max_value=1000, value=125)
            
            tinh_thanh = st.selectbox("Tỉnh/Thành", ["Hồ Chí Minh", "Hà Nội", "Đà Nẵng", "Khác"])
            quan = st.text_input("Quận/Huyện", placeholder="Ví dụ: Quận 1, Quận 7")
            
            submitted = st.form_submit_button("🔮 Dự đoán giá", use_container_width=True)
            
            if submitted:
                try:
                    # Prepare input data
                    input_data = pd.DataFrame({
                        'so_km': [so_km],
                        'nam_dang_ky': [nam_dang_ky],
                        'dung_tich_cc': [dung_tich_cc],
                        'trong_luong_kg': [np.nan],  # Will be imputed
                        'len_title': [len(dong_xe)],
                        'len_desc': [0],
                        'thuong_hieu': [thuong_hieu],
                        'dong_xe': [dong_xe],
                        'tinh_trang': [tinh_trang],
                        'loai_xe': [loai_xe],
                        'xuat_xu': [xuat_xu],
                        'tinh_thanh': [tinh_thanh],
                        'quan': [quan]
                    })
                    
                    # Transform and predict
                    X_transformed = preprocessor.transform(input_data)
                    prediction = model.predict(X_transformed)[0]
                    
                    # Display result
                    st.success(f"### 💰 Giá dự đoán: {prediction:,.0f} VNĐ")
                    st.info(f"≈ {prediction/1_000_000:.2f} triệu VNĐ")
                    
                except Exception as e:
                    st.error(f"Lỗi khi dự đoán: {str(e)}")

# Anomaly Detection page
elif page == "🚨 Phát hiện bất thường":
    st.title("🚨 Phát hiện giá bất thường")
    st.markdown("Kiểm tra xem giá xe có bất thường so với thị trường không")
    
    model, preprocessor, error = load_anomaly_model()
    
    if error:
        st.error(error)
    else:
        st.info("Nhập thông tin xe và giá để kiểm tra")
        
        with st.form("anomaly_detection_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                thuong_hieu = st.selectbox("Thương hiệu", ["Honda", "Yamaha", "SYM", "Piaggio", "Vespa"])
                dong_xe = st.text_input("Dòng xe")
                nam_dang_ky = st.number_input("Năm đăng ký", min_value=1990, max_value=2024)
                so_km = st.number_input("Số km", min_value=0)
            
            with col2:
                tinh_trang = st.selectbox("Tình trạng", ["Mới", "Đã sử dụng", "Cần sửa chữa"])
                loai_xe = st.selectbox("Loại xe", ["Tay ga", "Số", "Tay côn"])
                dung_tich_cc = st.number_input("Dung tích (cc)", min_value=50, max_value=1000)
                gia_vnd = st.number_input("Giá (VNĐ)", min_value=0, format="%d")
            
            submitted = st.form_submit_button("🔍 Kiểm tra", use_container_width=True)
            
            if submitted:
                try:
                    # Prepare input
                    input_data = pd.DataFrame({
                        'so_km': [so_km],
                        'nam_dang_ky': [nam_dang_ky],
                        'dung_tich_cc': [dung_tich_cc],
                        'trong_luong_kg': [np.nan],
                        'len_title': [len(dong_xe)],
                        'len_desc': [0],
                        'thuong_hieu': [thuong_hieu],
                        'dong_xe': [dong_xe],
                        'tinh_trang': [tinh_trang],
                        'loai_xe': [loai_xe],
                        'xuat_xu': ["Việt Nam"],
                        'tinh_thanh': ["Hồ Chí Minh"],
                        'quan': [""]
                    })
                    
                    # Transform
                    X_transformed = preprocessor.transform(input_data)
                    
                    # Predict anomaly
                    anomaly_score = model.decision_function(X_transformed)[0]
                    is_anomaly = model.predict(X_transformed)[0] == -1
                    
                    # Display result
                    if is_anomaly:
                        st.error("### ⚠️ Phát hiện giá BẤT THƯỜNG")
                        st.warning(f"Anomaly score: {anomaly_score:.4f}")
                        st.info("Giá này có vẻ không phù hợp với thị trường. Nên kiểm tra lại.")
                    else:
                        st.success("### ✅ Giá BÌNH THƯỜNG")
                        st.info(f"Anomaly score: {anomaly_score:.4f}")
                        
                except Exception as e:
                    st.error(f"Lỗi: {str(e)}")

# Recommendation page
elif page == "🔍 Gợi ý xe tương tự":
    st.title("🔍 Tìm xe máy tương tự")
    st.markdown("Nhập ID hoặc thông tin xe để tìm các xe tương tự")
    
    sample_data, error = load_sample_data()
    
    if error:
        st.error(error)
    else:
        st.info(f"📊 Đang load {len(sample_data)} records từ dữ liệu")
        
        # Import utils
        from utils import get_bike_info, find_similar_bikes, format_price, parse_price
        
        # Simple recommendation interface
        st.subheader("🔎 Tìm kiếm")
        search_option = st.radio("Tìm theo:", ["ID", "Thương hiệu", "Dòng xe", "Thông tin tùy chỉnh"], horizontal=True)
        
        if search_option == "ID":
            col1, col2 = st.columns([3, 1])
            with col1:
                bike_id = st.text_input("Nhập ID xe", placeholder="Ví dụ: 12345")
            with col2:
                top_n = st.number_input("Số kết quả", min_value=1, max_value=20, value=5)
            
            if bike_id and st.button("🔍 Tìm xe tương tự", use_container_width=True):
                bike_info = get_bike_info(sample_data, bike_id)
                if bike_info:
                    st.success(f"✅ Tìm thấy xe: {bike_info.get('Tiêu đề', bike_info.get('tieu_de', 'N/A'))}")
                    
                    # Show bike info
                    with st.expander("📋 Thông tin xe", expanded=False):
                        info_cols = st.columns(3)
                        with info_cols[0]:
                            st.metric("Thương hiệu", bike_info.get('Thương hiệu', bike_info.get('thuong_hieu', 'N/A')))
                        with info_cols[1]:
                            price = parse_price(bike_info.get('Giá', bike_info.get('gia_vnd', None)))
                            st.metric("Giá", format_price(price))
                        with info_cols[2]:
                            st.metric("Năm", bike_info.get('Năm đăng ký', bike_info.get('nam_dang_ky', 'N/A')))
                    
                    # Find similar
                    similar = find_similar_bikes(bike_info, sample_data, top_n=top_n)
                    
                    if similar:
                        st.subheader(f"🎯 {len(similar)} xe tương tự")
                        for i, bike in enumerate(similar, 1):
                            with st.container():
                                cols = st.columns([1, 2, 1, 1])
                                with cols[0]:
                                    st.write(f"**#{i}**")
                                with cols[1]:
                                    title = bike.get('Tiêu đề', bike.get('tieu_de', 'N/A'))
                                    st.write(f"**{title}**")
                                with cols[2]:
                                    price = parse_price(bike.get('Giá', bike.get('gia_vnd', None)))
                                    st.write(format_price(price))
                                with cols[3]:
                                    st.write(bike.get('Thương hiệu', bike.get('thuong_hieu', 'N/A')))
                                st.divider()
                    else:
                        st.warning("Không tìm thấy xe tương tự")
                else:
                    st.error(f"❌ Không tìm thấy xe với ID: {bike_id}")
                    st.info("💡 Thử tìm theo thương hiệu hoặc dòng xe")
        
        elif search_option == "Thương hiệu":
            brands = sorted(sample_data['Thương hiệu'].dropna().unique()) if 'Thương hiệu' in sample_data.columns else []
            if brands:
                selected_brand = st.selectbox("Chọn thương hiệu", brands)
                if st.button("🔍 Tìm", use_container_width=True):
                    filtered = sample_data[sample_data['Thương hiệu'] == selected_brand]
                    st.subheader(f"📊 Tìm thấy {len(filtered)} xe {selected_brand}")
                    st.dataframe(
                        filtered[['Tiêu đề', 'Giá', 'Năm đăng ký', 'Số Km đã đi']].head(20),
                        use_container_width=True,
                        hide_index=True
                    )
            else:
                st.warning("Không có cột 'Thương hiệu' trong dữ liệu")
        
        elif search_option == "Dòng xe":
            model_name = st.text_input("Nhập tên dòng xe", placeholder="Ví dụ: SH, Air Blade")
            if model_name and st.button("🔍 Tìm", use_container_width=True):
                if 'Dòng xe' in sample_data.columns:
                    filtered = sample_data[sample_data['Dòng xe'].str.contains(model_name, case=False, na=False)]
                    st.subheader(f"📊 Tìm thấy {len(filtered)} xe")
                    st.dataframe(
                        filtered[['Tiêu đề', 'Giá', 'Thương hiệu', 'Năm đăng ký']].head(20),
                        use_container_width=True,
                        hide_index=True
                    )
                else:
                    st.warning("Không có cột 'Dòng xe' trong dữ liệu")
        
        elif search_option == "Thông tin tùy chỉnh":
            st.subheader("🔧 Tìm kiếm nâng cao")
            col1, col2 = st.columns(2)
            with col1:
                brand = st.selectbox("Thương hiệu", ["Tất cả"] + sorted(sample_data['Thương hiệu'].dropna().unique().tolist()) if 'Thương hiệu' in sample_data.columns else ["Tất cả"])
                min_price = st.number_input("Giá tối thiểu (triệu)", min_value=0, value=0)
                max_price = st.number_input("Giá tối đa (triệu)", min_value=0, value=500)
            with col2:
                min_year = st.number_input("Năm tối thiểu", min_value=1990, max_value=2024, value=2010)
                max_year = st.number_input("Năm tối đa", min_value=1990, max_value=2024, value=2024)
            
            if st.button("🔍 Tìm kiếm", use_container_width=True):
                filtered = sample_data.copy()
                
                # Filter by brand
                if brand != "Tất cả" and 'Thương hiệu' in filtered.columns:
                    filtered = filtered[filtered['Thương hiệu'] == brand]
                
                # Filter by price
                if 'Giá' in filtered.columns:
                    from utils import parse_price
                    filtered['price_parsed'] = filtered['Giá'].apply(parse_price)
                    filtered = filtered[(filtered['price_parsed'] >= min_price) & (filtered['price_parsed'] <= max_price)]
                
                # Filter by year
                if 'Năm đăng ký' in filtered.columns:
                    filtered = filtered[(filtered['Năm đăng ký'] >= min_year) & (filtered['Năm đăng ký'] <= max_year)]
                
                st.subheader(f"📊 Tìm thấy {len(filtered)} xe phù hợp")
                if len(filtered) > 0:
                    display_cols = ['Tiêu đề', 'Giá', 'Thương hiệu', 'Năm đăng ký']
                    available_cols = [col for col in display_cols if col in filtered.columns]
                    st.dataframe(
                        filtered[available_cols].head(50),
                        use_container_width=True,
                        hide_index=True
                    )
                else:
                    st.info("Không tìm thấy xe phù hợp với tiêu chí")

# Clustering page
elif page == "📊 Phân cụm dữ liệu":
    st.title("📊 Phân cụm dữ liệu")
    st.markdown("Visualize clustering results từ project2")
    
    st.info("Tính năng này cần load clustering models từ project2.")
    st.markdown("""
    ### Các tính năng sẽ có:
    - KMeans clustering visualization
    - Gaussian Mixture Model
    - Agglomerative Clustering
    - PySpark clustering results
    """)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### 📚 Tài liệu")
st.sidebar.markdown("[GitHub Repository](https://github.com/teddyDn2001/ProjectChoTot)")
st.sidebar.markdown("[README](README.md)")

