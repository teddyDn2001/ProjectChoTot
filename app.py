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
    
    sample_data, data_error = load_sample_data()
    
    if data_error:
        st.error(data_error)
    else:
        st.info(f"📊 Đang load {len(sample_data)} records từ dữ liệu")
        
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
                        st.subheader("📊 Tóm tắt các cụm")
                        
                        cluster_summary = []
                        for cluster_id in range(n_clusters):
                            cluster_data = df_sample[df_sample['cluster'] == cluster_id]
                            if len(cluster_data) > 0:
                                price_col = 'price_parsed' if 'price_parsed' in cluster_data.columns else 'Giá'
                                year_col = 'Năm đăng ký' if 'Năm đăng ký' in cluster_data.columns else None
                                
                                prices = cluster_data[price_col].dropna()
                                years = cluster_data[year_col].dropna() if year_col else pd.Series()
                                
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
                        
                        # Show samples from each cluster
                        st.subheader("🔍 Mẫu từ các cụm")
                        selected_cluster = st.selectbox("Chọn cụm để xem", range(n_clusters))
                        cluster_samples = df_sample[df_sample['cluster'] == selected_cluster]
                        
                        display_cols = ['Tiêu đề', 'Giá', 'Thương hiệu', 'Năm đăng ký']
                        available_cols = [col for col in display_cols if col in cluster_samples.columns]
                        st.dataframe(
                            cluster_samples[available_cols].head(20),
                            use_container_width=True,
                            hide_index=True
                        )
            else:
                st.error("Không thể chuẩn bị dữ liệu cho clustering. Kiểm tra lại dữ liệu.")
        
        with tab2:
            st.subheader("📊 Content-Based Filtering")
            st.markdown("Tìm xe tương tự dựa trên nội dung (thương hiệu, giá, năm, mô tả)")
            
            if sample_data is not None and len(sample_data) > 0:
                # Select a bike
                st.markdown("### Chọn xe để tìm các xe tương tự")
                
                if 'Tiêu đề' in sample_data.columns:
                    bike_options = sample_data['Tiêu đề'].head(50).tolist()
                    selected_bike_title = st.selectbox("Chọn xe", bike_options)
                    selected_bike = sample_data[sample_data['Tiêu đề'] == selected_bike_title].iloc[0]
                else:
                    st.warning("Không có cột 'Tiêu đề' trong dữ liệu")
                    selected_bike = None
                
                if selected_bike is not None:
                    top_n = st.slider("Số xe tương tự", min_value=1, max_value=20, value=5)
                    
                    if st.button("🔍 Tìm xe tương tự", use_container_width=True):
                        with st.spinner("Đang tính toán similarity..."):
                            # Prepare features for content-based
                            def prepare_content_features(df):
                                features = []
                                for idx, row in df.iterrows():
                                    feature_vec = []
                                    
                                    # Brand (one-hot like)
                                    if 'Thương hiệu' in row:
                                        brand = str(row['Thương hiệu']).lower()
                                        feature_vec.append(hash(brand) % 1000 / 1000.0)
                                    else:
                                        feature_vec.append(0)
                                    
                                    # Price (normalized)
                                    from utils import parse_price
                                    price = parse_price(row.get('Giá', 0))
                                    if price:
                                        feature_vec.append(price / 100.0)  # Normalize
                                    else:
                                        feature_vec.append(0)
                                    
                                    # Year (normalized)
                                    year = row.get('Năm đăng ký', 0)
                                    if pd.notna(year) and year > 0:
                                        feature_vec.append((year - 2000) / 25.0)  # Normalize
                                    else:
                                        feature_vec.append(0)
                                    
                                    # KM (normalized)
                                    km = row.get('Số Km đã đi', 0)
                                    if pd.notna(km) and km > 0:
                                        feature_vec.append(km / 100000.0)  # Normalize
                                    else:
                                        feature_vec.append(0)
                                    
                                    features.append(feature_vec)
                                
                                return np.array(features)
                            
                            # Get features for all bikes
                            all_features = prepare_content_features(sample_data)
                            selected_idx = sample_data[sample_data['Tiêu đề'] == selected_bike_title].index[0]
                            selected_features = all_features[selected_idx:selected_idx+1]
                            
                            # Calculate cosine similarity
                            similarities = cosine_similarity(selected_features, all_features)[0]
                            
                            # Get top N similar (exclude itself)
                            similar_indices = np.argsort(similarities)[::-1][1:top_n+1]
                            
                            # Display results
                            st.success(f"✅ Tìm thấy {len(similar_indices)} xe tương tự")
                            
                            for i, idx in enumerate(similar_indices, 1):
                                similar_bike = sample_data.iloc[idx]
                                similarity = similarities[idx]
                                
                                with st.container():
                                    cols = st.columns([1, 3, 1, 1])
                                    with cols[0]:
                                        st.write(f"**#{i}**")
                                        st.progress(similarity)
                                    with cols[1]:
                                        title = similar_bike.get('Tiêu đề', 'N/A')
                                        st.write(f"**{title}**")
                                    with cols[2]:
                                        from utils import format_price, parse_price
                                        price = parse_price(similar_bike.get('Giá', 0))
                                        st.write(format_price(price))
                                    with cols[3]:
                                        st.write(f"Similarity: {similarity:.3f}")
                                    st.divider()
        
        with tab3:
            st.subheader("📈 Visualization")
            st.markdown("Biểu đồ phân cụm (cần chạy clustering trước)")
            
            if 'cluster' in st.session_state:
                st.info("Tính năng visualization đang phát triển. Sẽ hiển thị biểu đồ phân cụm 2D/3D.")
            else:
                st.info("💡 Chạy clustering ở tab 'Clustering' trước để xem visualization")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### 📚 Tài liệu")
st.sidebar.markdown("[GitHub Repository](https://github.com/teddyDn2001/ProjectChoTot)")
st.sidebar.markdown("[README](README.md)")

