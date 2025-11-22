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
        
        # Load model - check if it's a dict or direct model
        model_data = joblib.load(PRICE_MODEL_PATH)
        if isinstance(model_data, dict):
            # Extract model from dict (could be 'model', 'price_model', or direct)
            model = model_data.get('model', model_data.get('price_model', model_data))
            # If still a dict, try to get the actual model object
            if isinstance(model, dict):
                model = model.get('model', model)
        else:
            model = model_data
        
        # Load preprocessor
        preprocessor_data = joblib.load(PREPROCESSOR_PATH)
        if isinstance(preprocessor_data, dict):
            preprocessor = preprocessor_data['preprocessor']
        else:
            preprocessor = preprocessor_data
        
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
        
        iso_data = joblib.load(ISO_MODEL_PATH)
        # Check if it's a dict (saved with metadata) or direct model
        if isinstance(iso_data, dict):
            iso_model = iso_data.get('model', iso_data.get('iso_model', iso_data))
        else:
            iso_model = iso_data
        
        preprocessor_data = joblib.load(PREPROCESSOR_PATH)
        preprocessor = preprocessor_data['preprocessor']
        return iso_model, preprocessor, None
    except Exception as e:
        return None, None, f"Lỗi khi load model: {str(e)}"

@st.cache_data
def load_sample_data():
    """Load full dataset for recommendation and clustering"""
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
                # Load FULL dataset, not just sample
                df = pd.read_csv(path, low_memory=False)
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
                    # Get feature names from preprocessor - MUST use exact order
                    from project1.config import PREPROCESSOR_PATH
                    import joblib
                    preprocessor_data = joblib.load(PREPROCESSOR_PATH)
                    if isinstance(preprocessor_data, dict):
                        numeric_features = preprocessor_data.get('numeric_features', [])
                        categorical_features = preprocessor_data.get('categorical_features', [])
                    else:
                        # Fallback: use default feature names
                        numeric_features = ['so_km', 'nam_dang_ky', 'dung_tich_cc', 'trong_luong_kg', 'len_title', 'len_desc']
                        categorical_features = ['thuong_hieu', 'dong_xe', 'tinh_trang', 'loai_xe', 'xuat_xu', 'tinh_thanh', 'quan']
                    
                    # CRITICAL: Use exact feature order that preprocessor expects
                    all_features = numeric_features + categorical_features
                    
                    # Prepare input data - must match exact column names and order
                    input_data = pd.DataFrame({
                        'so_km': [so_km],
                        'nam_dang_ky': [nam_dang_ky],
                        'dung_tich_cc': [dung_tich_cc],
                        'trong_luong_kg': [np.nan],
                        'len_title': [len(dong_xe) if dong_xe else 0],
                        'len_desc': [0],
                        'thuong_hieu': [thuong_hieu],
                        'dong_xe': [dong_xe if dong_xe else ""],
                        'tinh_trang': [tinh_trang],
                        'loai_xe': [loai_xe],
                        'xuat_xu': [xuat_xu],
                        'tinh_thanh': [tinh_thanh],
                        'quan': [quan if quan else ""]
                    }, columns=all_features)  # Ensure correct column order
                    
                    # Check if model is a Pipeline (contains preprocessor)
                    from sklearn.pipeline import Pipeline
                    is_pipeline = isinstance(model, Pipeline) or (hasattr(model, 'steps') and len(model.steps) > 0)
                    
                    if is_pipeline:
                        # Model already includes preprocessor, use raw input (13 features)
                        prediction = model.predict(input_data)[0]
                    else:
                        # Model needs transformed input (278 features)
                        X_transformed = preprocessor.transform(input_data)
                        
                        # Handle sparse matrix
                        if hasattr(X_transformed, 'toarray'):
                            X_transformed = X_transformed.toarray()
                        
                        prediction = model.predict(X_transformed)[0]
                    
                    # Validate prediction
                    if prediction <= 0 or np.isnan(prediction) or np.isinf(prediction):
                        st.warning("⚠️ Giá dự đoán không hợp lệ. Vui lòng kiểm tra lại thông tin đầu vào.")
                    else:
                        # Display result
                        st.success(f"### 💰 Giá dự đoán: {prediction:,.0f} VNĐ")
                        st.info(f"≈ {prediction/1_000_000:.2f} triệu VNĐ")
                    
                except Exception as e:
                    st.error(f"Lỗi khi dự đoán: {str(e)}")
                    import traceback
                    with st.expander("Chi tiết lỗi"):
                        st.code(traceback.format_exc())

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
                    # Get feature names - MUST use exact order
                    from project1.config import PREPROCESSOR_PATH
                    import joblib
                    preprocessor_data = joblib.load(PREPROCESSOR_PATH)
                    if isinstance(preprocessor_data, dict):
                        numeric_features = preprocessor_data.get('numeric_features', [])
                        categorical_features = preprocessor_data.get('categorical_features', [])
                    else:
                        numeric_features = ['so_km', 'nam_dang_ky', 'dung_tich_cc', 'trong_luong_kg', 'len_title', 'len_desc']
                        categorical_features = ['thuong_hieu', 'dong_xe', 'tinh_trang', 'loai_xe', 'xuat_xu', 'tinh_thanh', 'quan']
                    
                    # CRITICAL: Use exact feature order that preprocessor expects
                    all_features = numeric_features + categorical_features
                    
                    # Prepare input with correct columns and order
                    input_data = pd.DataFrame({
                        'so_km': [so_km],
                        'nam_dang_ky': [nam_dang_ky],
                        'dung_tich_cc': [dung_tich_cc],
                        'trong_luong_kg': [np.nan],
                        'len_title': [len(dong_xe) if dong_xe else 0],
                        'len_desc': [0],
                        'thuong_hieu': [thuong_hieu],
                        'dong_xe': [dong_xe if dong_xe else ""],
                        'tinh_trang': [tinh_trang],
                        'loai_xe': [loai_xe],
                        'xuat_xu': ["Việt Nam"],
                        'tinh_thanh': ["Hồ Chí Minh"],
                        'quan': [""]
                    }, columns=all_features)  # Ensure correct column order
                    
                    # Transform
                    X_transformed = preprocessor.transform(input_data)
                    
                    # Handle sparse matrix
                    if hasattr(X_transformed, 'toarray'):
                        X_transformed = X_transformed.toarray()
                    
                    # Predict anomaly
                    anomaly_score = model.decision_function(X_transformed)[0]
                    predictions = model.predict(X_transformed)
                    is_anomaly = predictions[0] == -1
                    
                    # Validate scores
                    if np.isnan(anomaly_score) or np.isinf(anomaly_score):
                        st.warning("⚠️ Không thể tính anomaly score. Vui lòng kiểm tra lại thông tin.")
                    else:
                        # Display result
                        if is_anomaly:
                            st.error("### ⚠️ Phát hiện giá BẤT THƯỜNG")
                            st.warning(f"Anomaly score: {anomaly_score:.4f}")
                            st.info("Giá này có vẻ không phù hợp với thị trường. Nên kiểm tra lại.")
                            
                            # Show predicted price for comparison
                            try:
                                price_model, _, _ = load_price_model()
                                if price_model is not None:
                                    price_pred = price_model.predict(X_transformed)[0]
                                    if price_pred > 0:
                                        st.info(f"💡 Giá dự đoán hợp lý: {price_pred/1_000_000:.2f} triệu VNĐ")
                                        st.info(f"💡 Giá bạn nhập: {gia_vnd/1_000_000:.2f} triệu VNĐ")
                                        diff_pct = abs(price_pred - gia_vnd) / price_pred * 100
                                        if diff_pct > 30:
                                            st.warning(f"⚠️ Chênh lệch {diff_pct:.1f}% so với giá dự đoán - đây là lý do phát hiện bất thường")
                            except Exception as e:
                                # Silently fail - not critical
                                pass
                        else:
                            st.success("### ✅ Giá BÌNH THƯỜNG")
                            st.info(f"Anomaly score: {anomaly_score:.4f}")
                            st.success("Giá này phù hợp với thị trường.")
                        
                except Exception as e:
                    st.error(f"Lỗi: {str(e)}")
                    import traceback
                    with st.expander("Chi tiết lỗi"):
                        st.code(traceback.format_exc())

# Recommendation page
elif page == "🔍 Gợi ý xe tương tự":
    st.title("🔍 Tìm xe máy tương tự")
    st.markdown("Nhập ID hoặc thông tin xe để tìm các xe tương tự")
    
    sample_data, error = load_sample_data()
    
    if error:
        st.error(error)
    else:
        st.success(f"📊 Đã load **{len(sample_data):,}** records từ dataset Chợ Tốt (toàn bộ dữ liệu)")
        
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
                
                # Filter by year - parse year first
                if 'Năm đăng ký' in filtered.columns:
                    def safe_parse_year_for_filter(value):
                        if pd.isna(value):
                            return None
                        try:
                            import re
                            value_str = str(value).strip()
                            year_match = re.search(r'\d{4}', value_str)
                            if year_match:
                                year = int(year_match.group())
                                if 1990 <= year <= 2025:
                                    return year
                            return None
                        except:
                            return None
                    
                    # Parse years and filter
                    filtered['year_parsed'] = filtered['Năm đăng ký'].apply(safe_parse_year_for_filter)
                    filtered = filtered[
                        (filtered['year_parsed'].notna()) & 
                        (filtered['year_parsed'] >= min_year) & 
                        (filtered['year_parsed'] <= max_year)
                    ]
                    # Drop temporary column
                    if 'year_parsed' in filtered.columns:
                        filtered = filtered.drop(columns=['year_parsed'])
                
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
    st.title("📊 Phân cụm dữ liệu - Phân khúc thị trường xe máy")
    st.markdown("""
    **Phân cụm dữ liệu giúp:**
    - 🎯 Phân khúc thị trường: Chia xe máy thành các nhóm có đặc điểm tương đồng
    - 👥 Hiểu khách hàng: Mỗi phân khúc đại diện cho một nhóm khách hàng khác nhau
    - 💰 Định giá hợp lý: Biết xe thuộc phân khúc nào để định giá phù hợp
    - 🔍 Gợi ý sản phẩm: Đề xuất xe tương tự trong cùng phân khúc
    """)
    
    sample_data, data_error = load_sample_data()
    
    if data_error:
        st.error(data_error)
    else:
        st.success(f"📊 Đã load **{len(sample_data):,}** records từ dataset Chợ Tốt (toàn bộ dữ liệu)")
        
        # Import clustering functions
        from sklearn.cluster import KMeans, AgglomerativeClustering
        from sklearn.mixture import GaussianMixture
        from sklearn.preprocessing import StandardScaler
        from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        import matplotlib.pyplot as plt
        import seaborn as sns
        
        tab1, tab2, tab3 = st.tabs(["🔍 Clustering", "📊 Content-Based Filtering", "📈 Visualization"])
        
        with tab1:
            st.subheader("🔍 Phân cụm dữ liệu")
            
            # Prepare data for clustering
            @st.cache_data
            def prepare_clustering_data(df):
                """Prepare numeric features for clustering"""
                try:
                    if df is None or len(df) == 0:
                        return None, None, None
                    
                    df_clean = df.copy()
                    numeric_cols = []
                    
                    # Parse price
                    from utils import parse_price
                    if 'Giá' in df_clean.columns:
                        df_clean['price_parsed'] = df_clean['Giá'].apply(lambda x: parse_price(x) if pd.notna(x) else 0)
                        numeric_cols.append('price_parsed')
                    elif 'gia_vnd' in df_clean.columns:
                        df_clean['price_parsed'] = df_clean['gia_vnd'] / 1_000_000
                        numeric_cols.append('price_parsed')
                    
                    # Year - parse carefully to handle strings like "2008 trước năm"
                    def parse_year(value):
                        if pd.isna(value):
                            return 0
                        try:
                            # Convert to string first
                            value_str = str(value).strip()
                            # Extract first 4 digits (year)
                            import re
                            year_match = re.search(r'\d{4}', value_str)
                            if year_match:
                                year = int(year_match.group())
                                # Validate year range
                                if 1990 <= year <= 2025:
                                    return year
                            return 0
                        except:
                            return 0
                    
                    if 'Năm đăng ký' in df_clean.columns:
                        df_clean['year_parsed'] = df_clean['Năm đăng ký'].apply(parse_year)
                        numeric_cols.append('year_parsed')
                    elif 'nam_dang_ky' in df_clean.columns:
                        df_clean['year_parsed'] = df_clean['nam_dang_ky'].apply(parse_year)
                        numeric_cols.append('year_parsed')
                    
                    # KM - parse carefully
                    def parse_km(value):
                        if pd.isna(value):
                            return 0
                        try:
                            # Convert to string and extract numbers
                            value_str = str(value).strip().lower()
                            # Remove common text
                            value_str = value_str.replace('km', '').replace(',', '').replace('.', '').strip()
                            # Extract numbers
                            import re
                            numbers = re.findall(r'\d+', value_str)
                            if numbers:
                                return float(''.join(numbers))
                            return 0
                        except:
                            return 0
                    
                    if 'Số Km đã đi' in df_clean.columns:
                        df_clean['km_parsed'] = df_clean['Số Km đã đi'].apply(parse_km)
                        numeric_cols.append('km_parsed')
                    elif 'so_km' in df_clean.columns:
                        df_clean['km_parsed'] = df_clean['so_km'].apply(parse_km)
                        numeric_cols.append('km_parsed')
                    
                    # One-hot encode brand
                    brand_col = None
                    if 'Thương hiệu' in df_clean.columns:
                        brand_col = 'Thương hiệu'
                    elif 'thuong_hieu' in df_clean.columns:
                        brand_col = 'thuong_hieu'
                    
                    if brand_col and df_clean[brand_col].notna().sum() > 0:
                        # Limit to top brands to avoid too many features
                        top_brands = df_clean[brand_col].value_counts().head(10).index.tolist()
                        for brand in top_brands:
                            col_name = f'brand_{brand}'
                            df_clean[col_name] = (df_clean[brand_col] == brand).astype(int)
                            numeric_cols.append(col_name)
                    
                    # Check if we have enough features
                    if len(numeric_cols) == 0:
                        st.warning("Không tìm thấy cột số phù hợp. Thêm các cột mặc định.")
                        # Add dummy features
                        df_clean['dummy_feature'] = 1
                        numeric_cols.append('dummy_feature')
                    
                    # Select and clean
                    available_cols = [col for col in numeric_cols if col in df_clean.columns]
                    if len(available_cols) == 0:
                        return None, None, None
                    
                    X = df_clean[available_cols].fillna(0)
                    
                    # Remove rows with all zeros
                    X = X[(X != 0).any(axis=1)]
                    if len(X) == 0:
                        return None, None, None
                    
                    # Scale
                    scaler = StandardScaler()
                    X_scaled = scaler.fit_transform(X)
                    
                    # Update df_clean to match X indices
                    df_clean = df_clean.loc[X.index].copy()
                    
                    return X_scaled, df_clean, scaler
                except Exception as e:
                    st.error(f"Lỗi khi chuẩn bị dữ liệu: {str(e)}")
                    import traceback
                    st.code(traceback.format_exc())
                    return None, None, None
            
            X_scaled, df_clean, scaler = prepare_clustering_data(sample_data)
            
            if X_scaled is not None:
                col1, col2 = st.columns(2)
                
                with col1:
                    n_clusters = st.slider("Số cụm (k)", min_value=2, max_value=10, value=5)
                    algorithm = st.selectbox(
                        "Thuật toán clustering",
                        ["KMeans", "Gaussian Mixture Model (GMM)", "Agglomerative Clustering"]
                    )
                
                with col2:
                    max_samples = st.slider("Số mẫu tối đa", min_value=100, max_value=min(1000, len(sample_data)), value=min(500, len(sample_data)))
                
                if st.button("🚀 Chạy Clustering", use_container_width=True):
                    with st.spinner("Đang chạy clustering..."):
                        # Sample data if too large
                        if len(X_scaled) > max_samples:
                            indices = np.random.choice(len(X_scaled), max_samples, replace=False)
                            X_sample = X_scaled[indices]
                            df_sample = df_clean.iloc[indices].copy()
                        else:
                            X_sample = X_scaled
                            df_sample = df_clean.copy()
                        
                        # Run clustering
                        if algorithm == "KMeans":
                            model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
                            labels = model.fit_predict(X_sample)
                        elif algorithm == "Gaussian Mixture Model (GMM)":
                            model = GaussianMixture(n_components=n_clusters, random_state=42)
                            labels = model.fit_predict(X_sample)
                        else:  # Agglomerative
                            model = AgglomerativeClustering(n_clusters=n_clusters, linkage='ward')
                            labels = model.fit_predict(X_sample)
                        
                        # Calculate metrics
                        if len(np.unique(labels)) >= 2:
                            sil_score = silhouette_score(X_sample, labels)
                            db_score = davies_bouldin_score(X_sample, labels)
                            ch_score = calinski_harabasz_score(X_sample, labels)
                        else:
                            sil_score = db_score = ch_score = np.nan
                        
                        # Display results
                        st.success(f"✅ Hoàn thành clustering với {algorithm}")
                        
                        # Metrics
                        metric_col1, metric_col2, metric_col3 = st.columns(3)
                        with metric_col1:
                            st.metric("Silhouette Score", f"{sil_score:.4f}" if not np.isnan(sil_score) else "N/A")
                        with metric_col2:
                            st.metric("Davies-Bouldin Score", f"{db_score:.4f}" if not np.isnan(db_score) else "N/A")
                        with metric_col3:
                            st.metric("Calinski-Harabasz Score", f"{ch_score:.4f}" if not np.isnan(ch_score) else "N/A")
                        
                        # Cluster summary
                        df_sample['cluster'] = labels
                        
                        # Store in session state for visualization
                        st.session_state['cluster_labels'] = labels
                        st.session_state['cluster_data'] = df_sample
                        st.session_state['cluster_X'] = X_sample
                        
                        st.subheader("📊 Tóm tắt các cụm")
                        
                        cluster_summary = []
                        for cluster_id in range(n_clusters):
                            cluster_data = df_sample[df_sample['cluster'] == cluster_id]
                            if len(cluster_data) > 0:
                                # Get prices
                                if 'price_parsed' in cluster_data.columns:
                                    prices = cluster_data['price_parsed'].dropna()
                                elif 'Giá' in cluster_data.columns:
                                    from utils import parse_price
                                    prices = cluster_data['Giá'].apply(parse_price).dropna()
                                else:
                                    prices = pd.Series()
                                
                                # Get years (use parsed year if available)
                                if 'year_parsed' in cluster_data.columns:
                                    years = cluster_data['year_parsed'].dropna()
                                    years = years[years > 0]  # Remove invalid years
                                elif 'Năm đăng ký' in cluster_data.columns:
                                    def safe_parse_year(v):
                                        try:
                                            import re
                                            if pd.isna(v):
                                                return None
                                            match = re.search(r'\d{4}', str(v))
                                            if match:
                                                y = int(match.group())
                                                return y if 1990 <= y <= 2025 else None
                                            return None
                                        except:
                                            return None
                                    years = cluster_data['Năm đăng ký'].apply(safe_parse_year).dropna()
                                else:
                                    years = pd.Series()
                                
                                # Get brands
                                brand_counts = cluster_data['Thương hiệu'].value_counts().head(3) if 'Thương hiệu' in cluster_data.columns else {}
                                
                                cluster_summary.append({
                                    'Cụm': cluster_id,
                                    'Số lượng': len(cluster_data),
                                    'Giá TB (triệu)': f"{prices.mean():.2f}" if len(prices) > 0 else "N/A",
                                    'Năm TB': f"{years.mean():.0f}" if len(years) > 0 else "N/A",
                                    'Thương hiệu phổ biến': ", ".join(brand_counts.index.tolist()[:3]) if len(brand_counts) > 0 else "N/A"
                                })
                        
                        summary_df = pd.DataFrame(cluster_summary)
                        st.dataframe(summary_df, use_container_width=True, hide_index=True)
                        
                        # Cluster insights and recommendations
                        st.subheader("💡 Phân tích và Gợi ý cho từng phân khúc")
                        
                        for cluster_id in range(n_clusters):
                            cluster_data = df_sample[df_sample['cluster'] == cluster_id]
                            if len(cluster_data) > 0:
                                with st.expander(f"📊 Phân khúc {cluster_id} - {len(cluster_data)} xe", expanded=(cluster_id == 0)):
                                    # Get statistics
                                    if 'price_parsed' in cluster_data.columns:
                                        prices = cluster_data['price_parsed'].dropna()
                                    elif 'Giá' in cluster_data.columns:
                                        from utils import parse_price
                                        prices = cluster_data['Giá'].apply(parse_price).dropna()
                                    else:
                                        prices = pd.Series()
                                    
                                    if 'year_parsed' in cluster_data.columns:
                                        years = cluster_data['year_parsed'].dropna()
                                        years = years[years > 0]
                                    elif 'Năm đăng ký' in cluster_data.columns:
                                        def safe_parse_year(v):
                                            try:
                                                import re
                                                if pd.isna(v):
                                                    return None
                                                match = re.search(r'\d{4}', str(v))
                                                if match:
                                                    y = int(match.group())
                                                    return y if 1990 <= y <= 2025 else None
                                                return None
                                            except:
                                                return None
                                        years = cluster_data['Năm đăng ký'].apply(safe_parse_year).dropna()
                                    else:
                                        years = pd.Series()
                                    
                                    brand_counts = cluster_data['Thương hiệu'].value_counts().head(5) if 'Thương hiệu' in cluster_data.columns else {}
                                    
                                    # Display insights
                                    col1, col2, col3 = st.columns(3)
                                    with col1:
                                        if len(prices) > 0:
                                            avg_price = prices.mean()
                                            st.metric("💰 Giá trung bình", f"{avg_price:.1f} triệu VNĐ")
                                            st.caption(f"Khoảng: {prices.min():.1f} - {prices.max():.1f} triệu")
                                    with col2:
                                        if len(years) > 0:
                                            avg_year = years.mean()
                                            st.metric("📅 Năm trung bình", f"{avg_year:.0f}")
                                            st.caption(f"Khoảng: {years.min():.0f} - {years.max():.0f}")
                                    with col3:
                                        st.metric("📊 Số lượng", f"{len(cluster_data)} xe")
                                        st.caption(f"Tỷ lệ: {len(cluster_data)/len(df_sample)*100:.1f}%")
                                    
                                    # Brand distribution
                                    if len(brand_counts) > 0:
                                        st.markdown("**🏍️ Thương hiệu phổ biến:**")
                                        brand_text = ", ".join([f"{brand} ({count})" for brand, count in brand_counts.items()])
                                        st.info(brand_text)
                                    
                                    # Characterize cluster
                                    st.markdown("**🎯 Đặc điểm phân khúc:**")
                                    if len(prices) > 0 and len(years) > 0:
                                        avg_price_val = prices.mean()
                                        avg_year_val = years.mean()
                                        
                                        # Determine segment
                                        if avg_price_val < 20:
                                            segment = "💰 **Phân khúc giá rẻ** - Phù hợp cho người mua có ngân sách hạn chế"
                                        elif avg_price_val < 40:
                                            segment = "🏠 **Phân khúc tầm trung** - Phù hợp cho người dùng phổ thông"
                                        elif avg_price_val < 70:
                                            segment = "⭐ **Phân khúc cao cấp** - Phù hợp cho người dùng có thu nhập tốt"
                                        else:
                                            segment = "💎 **Phân khúc siêu cao cấp** - Phù hợp cho người dùng cao cấp"
                                        
                                        st.markdown(segment)
                                        
                                        # Recommendations
                                        st.markdown("**💡 Gợi ý:**")
                                        if avg_year_val >= 2020:
                                            st.info("✅ Xe mới, phù hợp cho người muốn xe đời mới, ít phải sửa chữa")
                                        elif avg_year_val >= 2015:
                                            st.info("✅ Xe đời trung, cân bằng giữa giá và chất lượng")
                                        else:
                                            st.info("✅ Xe đời cũ, giá rẻ nhưng cần kiểm tra kỹ trước khi mua")
                                    
                                    # Show samples
                                    st.markdown("**🔍 Mẫu xe trong phân khúc:**")
                                    display_cols = ['Tiêu đề', 'Giá', 'Thương hiệu', 'Năm đăng ký']
                                    available_cols = [col for col in display_cols if col in cluster_data.columns]
                                    st.dataframe(
                                        cluster_data[available_cols].head(10),
                                        use_container_width=True,
                                        hide_index=True
                                    )
            else:
                st.error("Không thể chuẩn bị dữ liệu cho clustering. Kiểm tra lại dữ liệu.")
        
        with tab2:
            st.subheader("📊 Content-Based Filtering")
            st.markdown("Tìm xe tương tự dựa trên nội dung (thương hiệu, giá, năm, số km)")
            
            if sample_data is not None and len(sample_data) > 0:
                # Choose input method
                input_method = st.radio(
                    "Cách nhập thông tin:",
                    ["📝 Nhập thông tin trực tiếp", "🔍 Chọn từ danh sách xe"],
                    horizontal=True
                )
                
                selected_bike = None
                
                if input_method == "📝 Nhập thông tin trực tiếp":
                    st.markdown("### Nhập thông tin xe")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        cbf_thuong_hieu = st.selectbox(
                            "Thương hiệu",
                            ["Tất cả"] + sorted(sample_data['Thương hiệu'].dropna().unique().tolist()) if 'Thương hiệu' in sample_data.columns else ["Tất cả"],
                            key="cbf_brand"
                        )
                        cbf_gia = st.number_input(
                            "Giá (triệu VNĐ)",
                            min_value=0.0,
                            max_value=1000.0,
                            value=50.0,
                            step=1.0,
                            key="cbf_price"
                        )
                    
                    with col2:
                        cbf_nam = st.number_input(
                            "Năm sản xuất",
                            min_value=1990,
                            max_value=2024,
                            value=2020,
                            key="cbf_year"
                        )
                        cbf_km = st.number_input(
                            "Số km đã đi",
                            min_value=0,
                            value=10000,
                            key="cbf_km"
                        )
                    
                    # Create a dummy bike dict for similarity calculation
                    selected_bike = {
                        'Thương hiệu': cbf_thuong_hieu if cbf_thuong_hieu != "Tất cả" else "Honda",
                        'Giá': f"{cbf_gia} triệu",
                        'Năm đăng ký': cbf_nam,
                        'Số Km đã đi': cbf_km,
                        'Tiêu đề': f"Xe {cbf_thuong_hieu} {cbf_nam}"
                    }
                
                else:  # Chọn từ danh sách
                    st.markdown("### Chọn xe để tìm các xe tương tự")
                    
                    if 'Tiêu đề' in sample_data.columns:
                        bike_options = sample_data['Tiêu đề'].head(50).tolist()
                        selected_bike_title = st.selectbox("Chọn xe", bike_options, key="cbf_select_bike")
                        selected_bike = sample_data[sample_data['Tiêu đề'] == selected_bike_title].iloc[0].to_dict()
                    else:
                        st.warning("Không có cột 'Tiêu đề' trong dữ liệu")
                        selected_bike = None
                
                if selected_bike is not None:
                    top_n = st.slider("Số xe tương tự", min_value=1, max_value=20, value=5, key="cbf_top_n")
                    
                    if st.button("🔍 Tìm xe tương tự", use_container_width=True, key="cbf_search"):
                        with st.spinner("Đang tính toán similarity..."):
                            # Prepare features for content-based
                            def prepare_content_features(df):
                                features = []
                                
                                # Helper functions
                                def safe_parse_year(value):
                                    if pd.isna(value):
                                        return 0
                                    try:
                                        import re
                                        value_str = str(value).strip()
                                        year_match = re.search(r'\d{4}', value_str)
                                        if year_match:
                                            year = int(year_match.group())
                                            if 1990 <= year <= 2025:
                                                return year
                                        return 0
                                    except:
                                        return 0
                                
                                def safe_parse_km(value):
                                    if pd.isna(value):
                                        return 0
                                    try:
                                        import re
                                        value_str = str(value).strip().lower()
                                        value_str = value_str.replace('km', '').replace(',', '').replace('.', '').strip()
                                        numbers = re.findall(r'\d+', value_str)
                                        if numbers:
                                            return float(''.join(numbers))
                                        return 0
                                    except:
                                        return 0
                                
                                for idx, row in df.iterrows():
                                    feature_vec = []
                                    
                                    # Brand (one-hot like)
                                    if 'Thương hiệu' in row and pd.notna(row['Thương hiệu']):
                                        brand = str(row['Thương hiệu']).lower()
                                        feature_vec.append(hash(brand) % 1000 / 1000.0)
                                    else:
                                        feature_vec.append(0)
                                    
                                    # Price (normalized)
                                    from utils import parse_price
                                    price = parse_price(row.get('Giá', 0))
                                    if price and price > 0:
                                        feature_vec.append(price / 100.0)  # Normalize
                                    else:
                                        feature_vec.append(0)
                                    
                                    # Year (normalized) - handle string format
                                    year = safe_parse_year(row.get('Năm đăng ký', 0))
                                    if year > 0:
                                        feature_vec.append((year - 2000) / 25.0)  # Normalize
                                    else:
                                        feature_vec.append(0)
                                    
                                    # KM (normalized) - handle string format
                                    km = safe_parse_km(row.get('Số Km đã đi', 0))
                                    if km > 0:
                                        feature_vec.append(km / 100000.0)  # Normalize
                                    else:
                                        feature_vec.append(0)
                                    
                                    features.append(feature_vec)
                                
                                return np.array(features)
                            
                            # Get features for all bikes
                            all_features = prepare_content_features(sample_data)
                            
                            # Calculate features for selected bike
                            if input_method == "📝 Nhập thông tin trực tiếp":
                                # Create a temporary DataFrame with selected bike
                                temp_df = pd.DataFrame([selected_bike])
                                selected_features = prepare_content_features(temp_df)
                            else:
                                # Find index from selected bike title
                                if 'Tiêu đề' in sample_data.columns and 'Tiêu đề' in selected_bike:
                                    selected_bike_title = selected_bike.get('Tiêu đề', '')
                                    matching = sample_data[sample_data['Tiêu đề'] == selected_bike_title]
                                    if len(matching) > 0:
                                        selected_idx = matching.index[0]
                                        selected_features = all_features[selected_idx:selected_idx+1]
                                    else:
                                        st.error("Không tìm thấy xe trong dữ liệu")
                                        selected_features = None
                                else:
                                    st.error("Không có thông tin 'Tiêu đề'")
                                    selected_features = None
                            
                            if selected_features is not None and len(selected_features) > 0:
                                # Calculate cosine similarity
                                similarities = cosine_similarity(selected_features, all_features)[0]
                                
                                # Get top N similar
                                if input_method == "📝 Nhập thông tin trực tiếp":
                                    # Don't exclude any (no "itself" when input directly)
                                    similar_indices = np.argsort(similarities)[::-1][:top_n]
                                else:
                                    # Exclude itself when selecting from list
                                    similar_indices = np.argsort(similarities)[::-1][1:top_n+1]
                            else:
                                st.error("Không thể tính toán similarity")
                                similar_indices = []
                            
                            # Display results with better UX
                            st.success(f"✅ Tìm thấy {len(similar_indices)} xe tương tự")
                            
                            # Show selected bike info
                            if input_method == "📝 Nhập thông tin trực tiếp":
                                st.info(f"🔍 Đang tìm xe tương tự với: {selected_bike.get('Thương hiệu', 'N/A')}, {selected_bike.get('Giá', 'N/A')}, năm {selected_bike.get('Năm đăng ký', 'N/A')}")
                            else:
                                st.info(f"🔍 Đang tìm xe tương tự với: {selected_bike.get('Tiêu đề', 'N/A')}")
                            
                            st.markdown("### 🎯 Kết quả tìm kiếm")
                            
                            for i, idx in enumerate(similar_indices, 1):
                                similar_bike = sample_data.iloc[idx]
                                similarity = similarities[idx]
                                
                                # Create a card-like display
                                with st.container():
                                    # Header with rank and similarity
                                    header_cols = st.columns([1, 4, 1])
                                    with header_cols[0]:
                                        st.markdown(f"### #{i}")
                                    with header_cols[1]:
                                        title = similar_bike.get('Tiêu đề', 'N/A')
                                        st.markdown(f"**{title}**")
                                    with header_cols[2]:
                                        similarity_pct = similarity * 100
                                        st.metric("Độ tương đồng", f"{similarity_pct:.1f}%")
                                    
                                    # Details in columns
                                    detail_cols = st.columns(4)
                                    with detail_cols[0]:
                                        from utils import format_price, parse_price
                                        price = parse_price(similar_bike.get('Giá', 0))
                                        st.metric("💰 Giá", format_price(price))
                                    with detail_cols[1]:
                                        brand = similar_bike.get('Thương hiệu', 'N/A')
                                        st.metric("🏍️ Thương hiệu", brand)
                                    with detail_cols[2]:
                                        year = similar_bike.get('Năm đăng ký', 'N/A')
                                        st.metric("📅 Năm", str(year)[:4] if isinstance(year, (int, float)) else str(year)[:4] if len(str(year)) >= 4 else 'N/A')
                                    with detail_cols[3]:
                                        km = similar_bike.get('Số Km đã đi', 'N/A')
                                        st.metric("🛣️ Số km", f"{km:,}" if isinstance(km, (int, float)) else str(km))
                                    
                                    # Similarity bar
                                    st.progress(similarity)
                                    st.caption(f"Độ tương đồng: {similarity:.1%}")
                                    
                                    st.divider()
        
        with tab3:
            st.subheader("📈 Visualization - Trực quan hóa phân khúc")
            st.markdown("""
            **💡 Biểu đồ giúp bạn hiểu rõ:**
            - 📊 **Có bao nhiêu xe** trong mỗi phân khúc?
            - 💰 **Giá trung bình** của từng phân khúc là bao nhiêu?
            - 📅 **Xe đời nào** phổ biến trong mỗi phân khúc?
            - 🎯 **Các phân khúc khác nhau** như thế nào?
            
            > 💬 **Lưu ý:** Cần chạy clustering ở tab "Clustering" trước để xem visualization
            """)
            
            if 'cluster_labels' in st.session_state and 'cluster_data' in st.session_state:
                try:
                    cluster_labels = st.session_state['cluster_labels']
                    cluster_data = st.session_state['cluster_data']
                    X_vis = st.session_state.get('cluster_X', None)
                    
                    # Basic statistics with better explanations
                    st.markdown("### 📊 1. Số lượng xe trong mỗi phân khúc")
                    st.markdown("Biểu đồ này cho thấy **có bao nhiêu xe** trong mỗi phân khúc. Phân khúc nào có nhiều xe nhất?")
                    
                    cluster_counts = pd.Series(cluster_labels).value_counts().sort_index()
                    cluster_counts_df = pd.DataFrame({
                        'Phân khúc': [f'Phân khúc {i}' for i in cluster_counts.index],
                        'Số lượng xe': cluster_counts.values
                    })
                    
                    st.bar_chart(cluster_counts_df.set_index('Phân khúc'))
                    
                    # Add explanation
                    max_cluster = cluster_counts.idxmax()
                    max_count = cluster_counts.max()
                    st.info(f"💡 **Phân khúc {max_cluster}** có nhiều xe nhất với **{max_count} xe** ({max_count/len(cluster_data)*100:.1f}% tổng số xe)")
                    
                    st.markdown("---")
                    
                    # Price distribution
                    st.markdown("### 💰 2. Giá trung bình của từng phân khúc")
                    st.markdown("Biểu đồ này cho thấy **giá trung bình** của mỗi phân khúc. Phân khúc nào đắt nhất? Rẻ nhất?")
                    
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        # Price distribution by cluster
                        if 'price_parsed' in cluster_data.columns:
                            price_by_cluster = cluster_data.groupby('cluster')['price_parsed'].mean().sort_index()
                        elif 'Giá' in cluster_data.columns:
                            from utils import parse_price
                            cluster_data['price_temp'] = cluster_data['Giá'].apply(parse_price)
                            price_by_cluster = cluster_data.groupby('cluster')['price_temp'].mean().sort_index()
                        else:
                            price_by_cluster = pd.Series()
                        
                        if len(price_by_cluster) > 0:
                            price_df = pd.DataFrame({
                                'Phân khúc': [f'Phân khúc {i}' for i in price_by_cluster.index],
                                'Giá trung bình (triệu VNĐ)': price_by_cluster.values
                            })
                            st.bar_chart(price_df.set_index('Phân khúc'))
                            
                            # Add explanation
                            cheapest = price_by_cluster.idxmin()
                            most_expensive = price_by_cluster.idxmax()
                            with col2:
                                st.metric("💰 Rẻ nhất", f"Phân khúc {cheapest}", f"{price_by_cluster[cheapest]:.1f} triệu")
                                st.metric("💎 Đắt nhất", f"Phân khúc {most_expensive}", f"{price_by_cluster[most_expensive]:.1f} triệu")
                                st.caption(f"Chênh lệch: {price_by_cluster[most_expensive] - price_by_cluster[cheapest]:.1f} triệu")
                    
                    st.markdown("---")
                    
                    # Year distribution
                    st.markdown("### 📅 3. Năm sản xuất trung bình của từng phân khúc")
                    st.markdown("Biểu đồ này cho thấy **xe đời nào** phổ biến trong mỗi phân khúc. Phân khúc nào có xe mới nhất?")
                    
                    if 'year_parsed' in cluster_data.columns:
                        year_by_cluster = cluster_data.groupby('cluster')['year_parsed'].mean().sort_index()
                        year_df = pd.DataFrame({
                            'Phân khúc': [f'Phân khúc {i}' for i in year_by_cluster.index],
                            'Năm trung bình': year_by_cluster.values
                        })
                        st.bar_chart(year_df.set_index('Phân khúc'))
                        
                        # Add explanation
                        newest = year_by_cluster.idxmax()
                        oldest = year_by_cluster.idxmin()
                        col1, col2 = st.columns(2)
                        with col1:
                            st.info(f"🆕 **Phân khúc {newest}** có xe mới nhất (năm TB: {year_by_cluster[newest]:.0f})")
                        with col2:
                            st.info(f"📜 **Phân khúc {oldest}** có xe cũ nhất (năm TB: {year_by_cluster[oldest]:.0f})")
                    
                    st.markdown("---")
                    
                    # Brand distribution
                    if 'Thương hiệu' in cluster_data.columns:
                        st.markdown("### 🏍️ Thương hiệu phổ biến theo cụm")
                        for cluster_id in sorted(cluster_data['cluster'].unique()):
                            cluster_bikes = cluster_data[cluster_data['cluster'] == cluster_id]
                            if len(cluster_bikes) > 0:
                                brand_counts = cluster_bikes['Thương hiệu'].value_counts().head(5)
                                if len(brand_counts) > 0:
                                    st.write(f"**Cụm {cluster_id}:** {', '.join(brand_counts.index.tolist())}")
                    
                    # 2D visualization if we have features
                    if X_vis is not None and X_vis.shape[1] >= 2:
                        st.markdown("### 🎯 5. Bản đồ phân khúc (Biểu đồ 2D)")
                        st.markdown("""
                        **Biểu đồ này giúp bạn hiểu:**
                        - 🎯 **Vị trí** của từng phân khúc trong không gian 2 chiều
                        - 📍 **Khoảng cách** giữa các phân khúc (phân khúc gần nhau = tương đồng)
                        - 🔍 **Mật độ** xe trong mỗi phân khúc (điểm dày = nhiều xe)
                        
                        > 💡 **Cách đọc:** Mỗi chấm là một xe. Các chấm cùng màu = cùng phân khúc. Chấm gần nhau = đặc điểm tương đồng.
                        """)
                        
                        try:
                            from sklearn.decomposition import PCA
                            
                            # Reduce to 2D
                            pca = PCA(n_components=2, random_state=42)
                            X_2d = pca.fit_transform(X_vis)
                            
                            # Create plot with better styling
                            fig, ax = plt.subplots(figsize=(14, 10))
                            
                            # Use distinct colors for each cluster
                            colors_list = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E2']
                            
                            for cluster_id in np.unique(cluster_labels):
                                mask = cluster_labels == cluster_id
                                color = colors_list[cluster_id % len(colors_list)]
                                ax.scatter(
                                    X_2d[mask, 0], X_2d[mask, 1],
                                    c=color,
                                    label=f'Phân khúc {cluster_id} ({np.sum(mask)} xe)',
                                    alpha=0.7,
                                    s=80,
                                    edgecolors='white',
                                    linewidth=0.5
                                )
                            
                            # Better labels in Vietnamese
                            variance_pc1 = pca.explained_variance_ratio_[0] * 100
                            variance_pc2 = pca.explained_variance_ratio_[1] * 100
                            
                            ax.set_xlabel(f'Trục 1 - Giải thích {variance_pc1:.1f}% sự khác biệt', fontsize=12, fontweight='bold')
                            ax.set_ylabel(f'Trục 2 - Giải thích {variance_pc2:.1f}% sự khác biệt', fontsize=12, fontweight='bold')
                            ax.set_title('🗺️ Bản đồ các phân khúc xe máy', fontsize=14, fontweight='bold', pad=20)
                            ax.legend(title='📊 Phân khúc', title_fontsize=12, fontsize=10, 
                                    bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True, fancybox=True, shadow=True)
                            ax.grid(True, alpha=0.3, linestyle='--')
                            ax.set_facecolor('#f8f9fa')
                            plt.tight_layout()
                            st.pyplot(fig)
                            plt.close(fig)
                            
                            # Add explanation
                            st.success(f"""
                            ✅ **Biểu đồ đã được tạo thành công!**
                            
                            **Cách hiểu biểu đồ:**
                            - Mỗi chấm màu = một xe máy
                            - Chấm cùng màu = cùng phân khúc
                            - Chấm gần nhau = đặc điểm tương đồng (giá, năm, thương hiệu...)
                            - Chấm xa nhau = khác biệt nhiều
                            
                            **Ví dụ:** Nếu phân khúc 0 và phân khúc 1 gần nhau → hai phân khúc này có đặc điểm tương đồng, có thể gộp lại hoặc cần phân biệt rõ hơn.
                            """)
                        except Exception as e:
                            st.warning(f"Không thể tạo biểu đồ 2D: {str(e)}")
                            import traceback
                            with st.expander("Chi tiết lỗi"):
                                st.code(traceback.format_exc())
                    
                    # Summary insights - User-friendly
                    st.markdown("---")
                    st.subheader("💡 Tóm tắt - Những điều quan trọng cần biết")
                    st.markdown("Dựa trên kết quả phân cụm, đây là những **insights chính** giúp bạn hiểu thị trường:")
                    
                    # Price analysis
                    if 'price_parsed' in cluster_data.columns or 'Giá' in cluster_data.columns:
                        all_prices = []
                        for cluster_id in range(n_clusters):
                            cluster_subset = cluster_data[cluster_data['cluster'] == cluster_id]
                            if 'price_parsed' in cluster_subset.columns:
                                prices = cluster_subset['price_parsed'].dropna()
                            elif 'Giá' in cluster_subset.columns:
                                from utils import parse_price
                                prices = cluster_subset['Giá'].apply(parse_price).dropna()
                            else:
                                prices = pd.Series()
                            if len(prices) > 0:
                                all_prices.append((cluster_id, prices.mean(), prices.min(), prices.max(), len(cluster_subset)))
                        
                        if all_prices:
                            all_prices.sort(key=lambda x: x[1])
                            cheapest = all_prices[0]
                            most_expensive = all_prices[-1]
                            
                            # Display in cards
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown(f"""
                                #### 💰 Phân khúc giá rẻ nhất
                                **Phân khúc {cheapest[0]}**
                                - Giá trung bình: **{cheapest[1]:.1f} triệu VNĐ**
                                - Khoảng giá: {cheapest[2]:.1f} - {cheapest[3]:.1f} triệu
                                - Số lượng: {cheapest[4]} xe
                                
                                💡 **Phù hợp cho:** Người có ngân sách hạn chế, sinh viên, người mới bắt đầu
                                """)
                            
                            with col2:
                                st.markdown(f"""
                                #### 💎 Phân khúc giá cao nhất
                                **Phân khúc {most_expensive[0]}**
                                - Giá trung bình: **{most_expensive[1]:.1f} triệu VNĐ**
                                - Khoảng giá: {most_expensive[2]:.1f} - {most_expensive[3]:.1f} triệu
                                - Số lượng: {most_expensive[4]} xe
                                
                                💡 **Phù hợp cho:** Người có thu nhập cao, muốn xe cao cấp, đời mới
                                """)
                            
                            # Price difference
                            price_diff = most_expensive[1] - cheapest[1]
                            st.info(f"📊 **Chênh lệch giá:** Phân khúc đắt nhất cao hơn phân khúc rẻ nhất **{price_diff:.1f} triệu VNĐ** ({price_diff/cheapest[1]*100:.0f}%)")
                    
                    # Market share
                    st.markdown("### 📊 Thị phần các phân khúc")
                    cluster_counts = pd.Series(cluster_labels).value_counts().sort_index()
                    for cluster_id, count in cluster_counts.items():
                        percentage = count / len(cluster_data) * 100
                        st.progress(percentage / 100, text=f"Phân khúc {cluster_id}: {count} xe ({percentage:.1f}% thị trường)")
                    
                    # Final message
                    st.success("""
                    ✅ **Phân cụm hoàn tất!**
                    
                    **Bạn có thể sử dụng kết quả này để:**
                    - 🛒 **Người mua:** Tìm phân khúc phù hợp với ngân sách
                    - 💼 **Người bán:** Định giá hợp lý dựa trên phân khúc
                    - 📈 **Phân tích:** Hiểu cấu trúc và xu hướng thị trường
                    """)
                    
                except Exception as e:
                    st.error(f"Lỗi khi hiển thị visualization: {str(e)}")
                    import traceback
                    st.code(traceback.format_exc())
            else:
                st.info("💡 Chạy clustering ở tab 'Clustering' trước để xem visualization")
                st.markdown("""
                ### Các tính năng visualization sẽ có:
                - Biểu đồ số lượng xe trong mỗi cụm
                - Phân bố giá theo cụm
                - Phân bố năm theo cụm
                - Biểu đồ 2D/3D với PCA
                """)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### 👤 Thông tin")
st.sidebar.markdown("""
**👨‍💻 Tác giả:** Đoàn Anh  
**🎓 Đồ án:** Data Science  
**📊 Dataset:** Chợ Tốt  
**📈 Số lượng:** 7,200+ records
""")
st.sidebar.markdown("### 📚 Tài liệu")
st.sidebar.markdown("[GitHub Repository](https://github.com/teddyDn2001/ProjectChoTot)")
st.sidebar.markdown("[README](README.md)")

