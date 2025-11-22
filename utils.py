"""
Utility functions for Streamlit app
"""
import pandas as pd
import numpy as np
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT / "project2"))

def parse_price(price_str):
    """Parse price string to float (millions VND)"""
    if pd.isna(price_str) or not price_str:
        return None
    
    price_str = str(price_str).lower().strip()
    if price_str in {"đang cập nhật", "liên hệ", "thỏa thuận"}:
        return None
    
    # Remove currency symbols
    price_str = price_str.replace("đ", "").replace("vnđ", "").replace("vnd", "")
    price_str = price_str.replace("triệu", "tr").replace("tỷ", "ty")
    price_str = price_str.replace(" ", "").replace(",", ".")
    
    # Parse
    if "tr" in price_str:
        try:
            return float(price_str.replace("tr", ""))
        except:
            return None
    elif "ty" in price_str:
        try:
            return float(price_str.replace("ty", "")) * 1000
        except:
            return None
    else:
        # Try to extract number
        import re
        match = re.search(r"([0-9]+(?:\.[0-9]+)?)", price_str)
        if match:
            try:
                num = float(match.group(1))
                # Assume it's in millions if > 1000
                if num > 1000:
                    return num / 1_000_000
                return num
            except:
                return None
    return None

def format_price(price_millions):
    """Format price in millions to display string"""
    if price_millions is None or pd.isna(price_millions):
        return "N/A"
    
    if price_millions >= 1000:
        return f"{price_millions/1000:.2f} tỷ VNĐ"
    else:
        return f"{price_millions:.2f} triệu VNĐ"

def get_bike_info(df, bike_id):
    """Get bike information by ID"""
    if 'id' in df.columns:
        bike = df[df['id'] == str(bike_id)]
    elif 'ID' in df.columns:
        bike = df[df['ID'] == str(bike_id)]
    else:
        return None
    
    if len(bike) == 0:
        return None
    
    return bike.iloc[0].to_dict()

def prepare_recommendation_input(bike_info, df):
    """Prepare input for recommendation"""
    # Simple feature extraction
    features = {}
    
    # Brand
    if 'Thương hiệu' in bike_info:
        features['brand'] = str(bike_info['Thương hiệu']).lower()
    elif 'thuong_hieu' in bike_info:
        features['brand'] = str(bike_info['thuong_hieu']).lower()
    
    # Price
    if 'Giá' in bike_info:
        features['price'] = parse_price(bike_info['Giá'])
    elif 'gia_vnd' in bike_info:
        features['price'] = bike_info['gia_vnd'] / 1_000_000 if bike_info.get('gia_vnd') else None
    
    # Year
    if 'Năm đăng ký' in bike_info:
        features['year'] = bike_info['Năm đăng ký']
    elif 'nam_dang_ky' in bike_info:
        features['year'] = bike_info['nam_dang_ky']
    
    # KM
    if 'Số Km đã đi' in bike_info:
        features['km'] = bike_info['Số Km đã đi']
    elif 'so_km' in bike_info:
        features['km'] = bike_info['so_km']
    
    return features

def find_similar_bikes(bike_info, df, top_n=5):
    """Find similar bikes using simple similarity"""
    if df is None or len(df) == 0:
        return []
    
    features = prepare_recommendation_input(bike_info, df)
    
    # Simple similarity scoring
    scores = []
    
    for idx, row in df.iterrows():
        score = 0
        
        # Brand match
        row_brand = str(row.get('Thương hiệu', row.get('thuong_hieu', ''))).lower()
        if features.get('brand') and row_brand == features['brand']:
            score += 10
        
        # Price similarity (within 20%)
        row_price = parse_price(row.get('Giá', row.get('gia_vnd', None)))
        if features.get('price') and row_price:
            price_diff = abs(row_price - features['price']) / features['price']
            if price_diff < 0.2:
                score += 5
        
        # Year similarity
        row_year = row.get('Năm đăng ký', row.get('nam_dang_ky', None))
        if features.get('year') and row_year:
            year_diff = abs(row_year - features['year'])
            if year_diff <= 2:
                score += 3
        
        scores.append((idx, score, row))
    
    # Sort by score and return top N
    scores.sort(key=lambda x: x[1], reverse=True)
    return [item[2] for item in scores[:top_n]]

