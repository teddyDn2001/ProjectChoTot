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

# Enhanced Custom CSS with Modern UI
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@400;500;600;700;800&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Main Container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Main Header with Animation */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem 0;
        animation: gradient-shift 3s ease infinite;
        background-size: 200% 200%;
    }
    
    @keyframes gradient-shift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    /* Feature Cards with Glassmorphism */
    .feature-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        padding: 2.5rem;
        border-radius: 1.25rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(255, 255, 255, 0.8);
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s;
    }
    
    .feature-card:hover::before {
        left: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.2);
    }
    
    /* Status Cards Enhanced */
    .status-card {
        background: white;
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border-left: 5px solid #667eea;
        margin: 1rem 0;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .status-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 5px;
        height: 100%;
        background: linear-gradient(180deg, #667eea, #764ba2);
        border-radius: 0 5px 5px 0;
    }
    
    .status-card.success {
        border-left-color: #10b981;
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
    }
    
    .status-card.success::after {
        background: linear-gradient(180deg, #10b981, #059669);
    }
    
    .status-card.error {
        border-left-color: #ef4444;
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
    }
    
    .status-card.error::after {
        background: linear-gradient(180deg, #ef4444, #dc2626);
    }
    
    .status-card:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 25px rgba(0,0,0,0.12);
    }
    
    /* Enhanced Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        padding: 0.875rem 2rem;
        border-radius: 0.75rem;
        border: none;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton>button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
    }
    
    .stButton>button:active {
        transform: translateY(-1px);
    }
    
    /* Form Styling */
    .stSelectbox>div>div, .stTextInput>div>div>input {
        border-radius: 0.5rem;
        border: 2px solid #e5e7eb;
        transition: all 0.3s ease;
    }
    
    .stSelectbox>div>div:focus, .stTextInput>div>div>input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    
    .stError {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        border-left: 4px solid #ef4444;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    
    /* Enhanced Form Inputs */
    .stSelectbox>div>div, .stTextInput>div>div>input, .stNumberInput>div>div>input {
        border-radius: 0.75rem;
        border: 2px solid #e5e7eb;
        transition: all 0.3s ease;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        color: #1f2937 !important;
        background-color: white !important;
    }
    
    /* CRITICAL: Force selectbox selected value to be visible - highest specificity */
    /* Override any gradient or transparent text fill that might be applied */
    .stSelectbox [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"],
    .stSelectbox [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] *,
    .stSelectbox [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] div,
    .stSelectbox [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] span,
    .stSelectbox [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] p {
        color: #1f2937 !important;
        -webkit-text-fill-color: #1f2937 !important;
        -webkit-background-clip: unset !important;
        background: none !important;
        background-image: none !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    
    /* Ensure text is visible in selectbox */
    .stSelectbox>div>div>div, .stSelectbox select, .stSelectbox option {
        color: #1f2937 !important;
        background-color: white !important;
    }
    
    /* CRITICAL FIX: Override any transparent text in selectbox value display */
    .stSelectbox [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"],
    .stSelectbox [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] * {
        color: #1f2937 !important;
        -webkit-text-fill-color: #1f2937 !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    
    /* Also target any element that might be the displayed value */
    [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] {
        color: #1f2937 !important;
        -webkit-text-fill-color: #1f2937 !important;
    }
    
    /* Ensure text is visible in text inputs */
    .stTextInput>div>div>input, .stTextInput input {
        color: #1f2937 !important;
        background-color: white !important;
    }
    
    /* Ensure text is visible in number inputs */
    .stNumberInput>div>div>input, .stNumberInput input {
        color: #1f2937 !important;
        background-color: white !important;
    }
    
    /* Ensure labels are visible */
    label, .stSelectbox label, .stTextInput label, .stNumberInput label, .stSlider label {
        color: #374151 !important;
        font-weight: 500 !important;
    }
    
    .stSelectbox>div>div:hover, .stTextInput>div>div>input:hover, .stNumberInput>div>div>input:hover {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.05);
    }
    
    .stSelectbox>div>div:focus-within, .stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15);
        outline: none;
    }
    
    /* Ensure placeholder text is visible */
    .stTextInput input::placeholder, .stNumberInput input::placeholder {
        color: #9ca3af !important;
        opacity: 1 !important;
    }
    
    /* Ensure slider labels and values are visible */
    .stSlider label, .stSlider [data-testid="stMarkdownContainer"] {
        color: #374151 !important;
    }
    
    .stSlider [data-testid="stMarkdownContainer"] p {
        color: #1f2937 !important;
    }
    
    /* Ensure all Streamlit text elements are visible */
    [data-testid="stMarkdownContainer"], 
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3 {
        color: inherit !important;
    }
    
    /* Ensure selectbox dropdown text is visible */
    [data-baseweb="select"] {
        color: #1f2937 !important;
    }
    
    [data-baseweb="select"] [data-baseweb="select"] {
        color: #1f2937 !important;
    }
    
    /* Ensure selected value in selectbox is visible */
    [data-baseweb="select"] > div {
        color: #1f2937 !important;
    }
    
    [data-baseweb="select"] [data-baseweb="select"] > div {
        color: #1f2937 !important;
    }
    
    /* Selected value text in selectbox input */
    [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] {
        color: #1f2937 !important;
    }
    
    /* Single value display in selectbox */
    [data-baseweb="select"] [data-baseweb="select"] span,
    [data-baseweb="select"] span,
    .stSelectbox [data-baseweb="select"] span,
    .stSelectbox [data-baseweb="select"] [data-baseweb="select"] span {
        color: #1f2937 !important;
    }
    
    /* Selected value in selectbox - more specific selectors */
    .stSelectbox [data-baseweb="select"] > div > div,
    .stSelectbox [data-baseweb="select"] > div > div > div,
    .stSelectbox [data-baseweb="select"] > div > div > div > div {
        color: #1f2937 !important;
    }
    
    /* BaseWeb Select Value */
    [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] > div {
        color: #1f2937 !important;
    }
    
    /* All text inside selectbox container - but override for selected value */
    .stSelectbox * {
        color: inherit;
    }
    
    .stSelectbox [data-baseweb="select"] * {
        color: #1f2937 !important;
    }
    
    /* Force selected value to be visible - target the input value directly */
    [data-baseweb="select"] input,
    [data-baseweb="select"] [data-baseweb="select"] input,
    [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] input {
        color: #1f2937 !important;
        -webkit-text-fill-color: #1f2937 !important;
    }
    
    /* BaseWeb Select specific - ensure value is visible */
    [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] {
        color: #1f2937 !important;
        -webkit-text-fill-color: #1f2937 !important;
    }
    
    /* Target the value container in BaseWeb Select */
    [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] > div,
    [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] > div > div,
    [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] > div > div > div {
        color: #1f2937 !important;
        -webkit-text-fill-color: #1f2937 !important;
    }
    
    /* Target the value display area more aggressively */
    [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] {
        color: #1f2937 !important;
    }
    
    /* Ensure the displayed text in selectbox is visible */
    [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] > div > div,
    [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] > div > div > div,
    [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] > div > div > div > span {
        color: #1f2937 !important;
        -webkit-text-fill-color: #1f2937 !important;
    }
    
    /* More specific selectors for selected value display */
    div[data-baseweb="select"] > div > div,
    div[data-baseweb="select"] > div > div > div,
    div[data-baseweb="select"] > div > div > div > div,
    div[data-baseweb="select"] > div > div > div > div > span {
        color: #1f2937 !important;
    }
    
    /* Target the actual displayed value */
    [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] > div > div,
    [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] > div > div > div,
    [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] > div > div > div > span {
        color: #1f2937 !important;
    }
    
    /* Ensure all p tags and text nodes in selectbox are visible */
    .stSelectbox p,
    .stSelectbox [data-baseweb="select"] p,
    .stSelectbox [data-baseweb="select"] [data-baseweb="select"] p {
        color: #1f2937 !important;
    }
    
    /* Override any transparent or inherit colors */
    .stSelectbox [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] {
        -webkit-text-fill-color: #1f2937 !important;
        color: #1f2937 !important;
    }
    
    /* Selected value display - target the actual displayed text */
    [data-baseweb="select"] > div > div > div,
    [data-baseweb="select"] > div > div > div > div,
    [data-baseweb="select"] > div > div > div > div > div,
    [data-baseweb="select"] > div > div > div > div > div > span {
        color: #1f2937 !important;
        -webkit-text-fill-color: #1f2937 !important;
    }
    
    /* Ensure all text in selectbox value area is visible */
    .stSelectbox [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] > div > div > div,
    .stSelectbox [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] > div > div > div > div,
    .stSelectbox [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] > div > div > div > div > div {
        color: #1f2937 !important;
        -webkit-text-fill-color: #1f2937 !important;
    }
    
    /* Target the value container directly */
    [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] {
        color: #1f2937 !important;
    }
    
    /* All text nodes inside selectbox */
    .stSelectbox [data-baseweb="select"] * {
        color: #1f2937 !important;
    }
    
    /* Specific selector for the displayed value */
    [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] > div {
        color: #1f2937 !important;
    }
    
    /* Info Boxes Enhanced */
    .info-box {
        background: linear-gradient(135deg, rgba(239, 246, 255, 0.9) 0%, rgba(219, 234, 254, 0.9) 100%);
        backdrop-filter: blur(10px);
        border-left: 5px solid #3b82f6;
        padding: 2rem;
        border-radius: 1rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.1);
        transition: all 0.3s ease;
    }
    
    .info-box:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 30px rgba(59, 130, 246, 0.15);
    }
    
    /* Price Display with Animation */
    .price-display {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 50%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        padding: 1.5rem;
        animation: price-glow 2s ease-in-out infinite;
        background-size: 200% 200%;
    }
    
    @keyframes price-glow {
        0%, 100% { 
            background-position: 0% 50%;
            filter: drop-shadow(0 0 10px rgba(245, 87, 108, 0.3));
        }
        50% { 
            background-position: 100% 50%;
            filter: drop-shadow(0 0 20px rgba(245, 87, 108, 0.5));
        }
    }
    
    /* Enhanced Loading Animation */
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
            transform: scale(1);
        }
        50% {
            opacity: 0.7;
            transform: scale(1.05);
        }
    }
    
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .loading {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(102, 126, 234, 0.3);
        border-radius: 50%;
        border-top-color: #667eea;
        animation: spin 1s linear infinite;
    }
    
    /* Card Grid Enhanced */
    .card-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    
    /* Badge/Tag Styling */
    .badge {
        display: inline-block;
        padding: 0.375rem 0.875rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 600;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }
    
    .badge-success {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    }
    
    .badge-warning {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    }
    
    .badge-error {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    }
    
    /* Enhanced Divider */
    hr {
        border: none;
        height: 3px;
        background: linear-gradient(90deg, transparent, #667eea 20%, #764ba2 50%, #667eea 80%, transparent);
        margin: 3rem 0;
        border-radius: 2px;
        opacity: 0.6;
    }
    
    /* Tooltip Enhanced */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
    }
    
    .tooltip:hover::after {
        content: attr(data-tooltip);
        position: absolute;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        padding: 0.5rem 1rem;
        background: rgba(0, 0, 0, 0.9);
        color: white;
        border-radius: 0.5rem;
        font-size: 0.875rem;
        white-space: nowrap;
        z-index: 1000;
        animation: fadeIn 0.3s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateX(-50%) translateY(-5px); }
        to { opacity: 1; transform: translateX(-50%) translateY(0); }
    }
    
    /* Progress Bar Enhanced */
    .stProgress>div>div>div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
    }
    
    /* Table/Dataframe Styling */
    .dataframe {
        border-radius: 0.75rem;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    }
    
    .dataframe thead {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .dataframe tbody tr:hover {
        background: rgba(102, 126, 234, 0.05);
        transition: background 0.2s ease;
    }
    
    /* Sidebar Enhanced */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
    }
    
    section[data-testid="stSidebar"] .css-1d391kg {
        background: transparent;
    }
    
    /* Success/Error/Info Messages Enhanced */
    .stSuccess {
        background: linear-gradient(135deg, rgba(236, 253, 245, 0.95) 0%, rgba(209, 250, 229, 0.95) 100%);
        backdrop-filter: blur(10px);
        border-left: 5px solid #10b981;
        padding: 1.25rem;
        border-radius: 0.75rem;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.15);
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(254, 242, 242, 0.95) 0%, rgba(254, 226, 226, 0.95) 100%);
        backdrop-filter: blur(10px);
        border-left: 5px solid #ef4444;
        padding: 1.25rem;
        border-radius: 0.75rem;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.15);
    }
    
    .stInfo {
        background: linear-gradient(135deg, rgba(239, 246, 255, 0.95) 0%, rgba(219, 234, 254, 0.95) 100%);
        backdrop-filter: blur(10px);
        border-left: 5px solid #3b82f6;
        padding: 1.25rem;
        border-radius: 0.75rem;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.15);
    }
    
    .stWarning {
        background: linear-gradient(135deg, rgba(255, 251, 235, 0.95) 0%, rgba(254, 243, 199, 0.95) 100%);
        backdrop-filter: blur(10px);
        border-left: 5px solid #f59e0b;
        padding: 1.25rem;
        border-radius: 0.75rem;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.15);
    }
    
    /* Metrics Enhanced */
    [data-testid="stMetricValue"] {
        font-size: 2.25rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.95rem;
        font-weight: 500;
        color: #6b7280;
    }
    
    /* Expander Enhanced */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border-radius: 0.5rem;
        padding: 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
        transform: translateX(5px);
    }
    
    /* Tabs Enhanced */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 0.5rem 0.5rem 0 0;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(102, 126, 234, 0.1);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem;
        }
        
        .feature-card {
            padding: 1.5rem;
        }
        
        .price-display {
            font-size: 2.5rem;
        }
        
        .card-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
        }
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Hide Streamlit branding only - be careful not to hide content */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Ensure main content area is always visible */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Make sure all content is visible - no aggressive hiding */
    body, html {
        visibility: visible !important;
    }
    
    /* Ensure Streamlit elements are visible */
    [data-testid="stAppViewContainer"] {
        visibility: visible !important;
    }
    
    /* Smooth Scrolling */
    html {
        scroll-behavior: smooth;
    }
    
    /* Selection Color */
    ::selection {
        background: rgba(102, 126, 234, 0.3);
        color: #1f2937;
    }
    
    /* ULTIMATE FIX: Apply to ALL elements inside selectbox - highest priority */
    /* This must come AFTER all other CSS rules to override them */
    .stSelectbox [data-baseweb="select"] *,
    .stSelectbox [data-baseweb="select"] [data-baseweb="select"] *,
    .stSelectbox [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] *,
    .stSelectbox [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] *,
    .stSelectbox [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] *,
    .stSelectbox [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] *,
    .stSelectbox [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] * {
        color: #1f2937 !important;
        -webkit-text-fill-color: #1f2937 !important;
        -webkit-background-clip: unset !important;
        background: none !important;
        background-image: none !important;
        background-clip: unset !important;
    }
    
    /* EXTRA FIX: Target the actual input/display element more specifically */
    [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] {
        color: #1f2937 !important;
        -webkit-text-fill-color: #1f2937 !important;
        -webkit-background-clip: unset !important;
        background: none !important;
        background-image: none !important;
        background-clip: unset !important;
    }
    
    /* Also target any element that might be the displayed value */
    [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] [data-baseweb="select"] * {
        color: #1f2937 !important;
        -webkit-text-fill-color: #1f2937 !important;
        -webkit-background-clip: unset !important;
        background: none !important;
        background-image: none !important;
        background-clip: unset !important;
    }
    /* FINAL NUCLEAR OPTION: Inject style tag directly into selectbox elements */
    .stSelectbox {
        --selectbox-text-color: #1f2937 !important;
    }
    
    .stSelectbox * {
        --selectbox-text-color: #1f2937 !important;
    }
</style>
<script>
    // Inject a style tag directly into the page for maximum priority
    (function() {
        const style = document.createElement('style');
        style.textContent = `
            /* Fix for ALL selectbox elements */
            .stSelectbox [data-baseweb="select"],
            .stSelectbox [data-baseweb="select"] *,
            [data-baseweb="select"],
            [data-baseweb="select"] * {
                color: #1f2937 !important;
                -webkit-text-fill-color: #1f2937 !important;
                -webkit-background-clip: unset !important;
                background: none !important;
                background-image: none !important;
                background-clip: unset !important;
                opacity: 1 !important;
                visibility: visible !important;
            }
            /* Specifically target div and span elements that might contain text */
            .stSelectbox [data-baseweb="select"] div,
            .stSelectbox [data-baseweb="select"] span,
            .stSelectbox [data-baseweb="select"] p,
            [data-baseweb="select"] div,
            [data-baseweb="select"] span,
            [data-baseweb="select"] p {
                color: #1f2937 !important;
                -webkit-text-fill-color: #1f2937 !important;
                -webkit-background-clip: unset !important;
                background: none !important;
                background-image: none !important;
                background-clip: unset !important;
                opacity: 1 !important;
                visibility: visible !important;
            }
        `;
        document.head.appendChild(style);
    })();
    
    // ULTIMATE FIX: Force selected value in selectbox to be visible
    function fixSelectboxText() {
        // Find all selectboxes - use multiple selectors
        const selectboxes1 = document.querySelectorAll('[data-baseweb="select"]');
        const selectboxes2 = document.querySelectorAll('.stSelectbox [data-baseweb="select"]');
        const allSelectboxes = [...selectboxes1, ...selectboxes2];
        
        // Remove duplicates
        const uniqueSelectboxes = Array.from(new Set(allSelectboxes));
        
        uniqueSelectboxes.forEach(select => {
            // Get ALL elements inside selectbox including the select itself
            const allElements = select.querySelectorAll('*');
            
            // Also include the select element itself
            const allToFix = [select, ...Array.from(allElements)];
            
            allToFix.forEach(el => {
                // Skip script and style tags
                if (el.tagName === 'SCRIPT' || el.tagName === 'STYLE') return;
                
                // Force set ALL style properties for visibility
                el.style.setProperty('color', '#1f2937', 'important');
                el.style.setProperty('-webkit-text-fill-color', '#1f2937', 'important');
                el.style.setProperty('opacity', '1', 'important');
                el.style.setProperty('visibility', 'visible', 'important');
                el.style.setProperty('-webkit-background-clip', 'unset', 'important');
                el.style.setProperty('background', 'none', 'important');
                el.style.setProperty('background-image', 'none', 'important');
                el.style.setProperty('background-clip', 'unset', 'important');
                
                // Check computed style and force fix if needed
                try {
                    const computedStyle = window.getComputedStyle(el);
                    const fillColor = computedStyle.webkitTextFillColor;
                    const color = computedStyle.color;
                    
                    // If text is transparent or invisible, force fix
                    if (fillColor === 'transparent' || 
                        fillColor === 'rgba(0, 0, 0, 0)' ||
                        color === 'rgba(0, 0, 0, 0)' ||
                        color === 'transparent') {
                        el.style.setProperty('color', '#1f2937', 'important');
                        el.style.setProperty('-webkit-text-fill-color', '#1f2937', 'important');
                    }
                } catch(e) {
                    // Ignore errors
                }
            });
        });
        
        // Also find all stSelectbox containers and fix their children
        const stSelectboxes = document.querySelectorAll('.stSelectbox');
        stSelectboxes.forEach(container => {
            const allChildren = container.querySelectorAll('*');
            allChildren.forEach(el => {
                if (el.tagName === 'SCRIPT' || el.tagName === 'STYLE') return;
                el.style.setProperty('color', '#1f2937', 'important');
                el.style.setProperty('-webkit-text-fill-color', '#1f2937', 'important');
            });
        });
    }
    
    // Run on page load and after DOM updates
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', fixSelectboxText);
    } else {
        fixSelectboxText();
    }
    
    // Run multiple times to catch dynamically loaded elements
    setTimeout(fixSelectboxText, 100);
    setTimeout(fixSelectboxText, 300);
    setTimeout(fixSelectboxText, 500);
    setTimeout(fixSelectboxText, 1000);
    setTimeout(fixSelectboxText, 2000);
    
    // Use MutationObserver to watch for changes
    const observer = new MutationObserver(function(mutations) {
        fixSelectboxText();
    });
    observer.observe(document.body, { 
        childList: true, 
        subtree: true,
        attributes: true,
        attributeFilter: ['style', 'class']
    });
    
    // Also listen for click events on selectboxes
    document.addEventListener('click', function(e) {
        if (e.target.closest('[data-baseweb="select"]')) {
            setTimeout(fixSelectboxText, 50);
            setTimeout(fixSelectboxText, 100);
            setTimeout(fixSelectboxText, 300);
        }
    }, true);
    
    // Listen for change events (when value is selected)
    document.addEventListener('change', function(e) {
        if (e.target.closest('[data-baseweb="select"]')) {
            setTimeout(fixSelectboxText, 50);
            setTimeout(fixSelectboxText, 100);
            setTimeout(fixSelectboxText, 300);
        }
    }, true);
    
    // Also run periodically to catch any missed updates - very frequent
    setInterval(fixSelectboxText, 200);
    
    // Also run when window loads completely
    window.addEventListener('load', function() {
        setTimeout(fixSelectboxText, 50);
        setTimeout(fixSelectboxText, 100);
        setTimeout(fixSelectboxText, 300);
        setTimeout(fixSelectboxText, 500);
        setTimeout(fixSelectboxText, 1000);
        setTimeout(fixSelectboxText, 2000);
    });
    
    // Listen for Streamlit's custom events
    if (window.parent) {
        window.parent.addEventListener('message', function(event) {
            if (event.data && event.data.type === 'streamlit:render') {
                setTimeout(fixSelectboxText, 100);
                setTimeout(fixSelectboxText, 300);
            }
        });
    }
    
    // Use requestAnimationFrame for continuous checking
    function continuousFix() {
        fixSelectboxText();
        requestAnimationFrame(continuousFix);
    }
    // Start continuous fix after initial delay
    setTimeout(function() {
        requestAnimationFrame(continuousFix);
    }, 1000);
</script>
""", unsafe_allow_html=True)

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'models_loaded' not in st.session_state:
    st.session_state.models_loaded = False

# Enhanced Sidebar navigation
st.sidebar.markdown("""
<div style='text-align: center; padding: 1rem 0;'>
    <h1 style='font-size: 2rem; margin: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
        🏍️ Motorbike Analysis
    </h1>
    <p style='color: #6b7280; font-size: 0.9rem; margin-top: 0.5rem;'>Platform phân tích xe máy</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "📋 Chọn chức năng:",
    ["🏠 Trang chủ", "💰 Dự đoán giá", "🚨 Phát hiện bất thường", "🔍 Gợi ý xe tương tự", "📊 Phân cụm dữ liệu"],
    label_visibility="visible"
)

# Import modules (lazy loading)
@st.cache_resource
def load_price_model():
    """Load price prediction model"""
    try:
        from project1.config import PRICE_MODEL_PATH, PREPROCESSOR_PATH
        import joblib
        
        # Check if files exist with detailed error messages
        if not PRICE_MODEL_PATH.exists():
            return None, None, f"""❌ Không tìm thấy file model: `{PRICE_MODEL_PATH}`

**💡 Nguyên nhân có thể:**
1. File chưa được push lên GitHub (file này dùng Git LFS vì lớn 113MB)
2. Streamlit Cloud chưa pull Git LFS files
3. File path không đúng trên Streamlit Cloud

**🔧 Cách khắc phục:**
1. Kiểm tra file có trên GitHub: https://github.com/teddyDn2001/ProjectChoTot/tree/main/project1/models
2. Nếu file là pointer (text nhỏ) → Git LFS chưa được push đúng
3. Push lại Git LFS: `git lfs push origin main --all`
4. Reload app trên Streamlit Cloud (click "Relaunch to update")
5. Xem hướng dẫn chi tiết trong file `FIX_MODELS.md`"""
        
        if not PREPROCESSOR_PATH.exists():
            return None, None, f"""❌ Không tìm thấy file preprocessor: `{PREPROCESSOR_PATH}`

**💡 Nguyên nhân có thể:**
1. File chưa được push lên GitHub (file này dùng Git LFS)
2. Streamlit Cloud chưa pull Git LFS files
3. File path không đúng

**🔧 Cách khắc phục:**
1. Kiểm tra file có trên GitHub: https://github.com/teddyDn2001/ProjectChoTot/tree/main/project1/artifacts
2. Push lại Git LFS: `git lfs push origin main --all`
3. Reload app trên Streamlit Cloud"""
        
        # Load model - check if it's a dict or direct model
        try:
            model_data = joblib.load(PRICE_MODEL_PATH)
        except Exception as e:
            return None, None, f"❌ Lỗi khi đọc file model: {str(e)}\n\n💡 File có thể bị hỏng hoặc không tương thích."
        
        if isinstance(model_data, dict):
            # Extract model from dict (could be 'model', 'price_model', or direct)
            model = model_data.get('model', model_data.get('price_model', model_data))
            # If still a dict, try to get the actual model object
            if isinstance(model, dict):
                model = model.get('model', model)
        else:
            model = model_data
        
        # Load preprocessor
        try:
            preprocessor_data = joblib.load(PREPROCESSOR_PATH)
        except Exception as e:
            return None, None, f"❌ Lỗi khi đọc file preprocessor: {str(e)}\n\n💡 File có thể bị hỏng hoặc không tương thích."
        
        if isinstance(preprocessor_data, dict):
            preprocessor = preprocessor_data.get('preprocessor')
            if preprocessor is None:
                return None, None, "❌ Preprocessor không có trong file. Cấu trúc file không đúng."
        else:
            preprocessor = preprocessor_data
        
        return model, preprocessor, None
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return None, None, f"❌ Lỗi khi load model: {str(e)}\n\n<details><summary>Chi tiết lỗi</summary>\n\n```\n{error_details}\n```\n</details>"

@st.cache_resource
def load_anomaly_model():
    """Load anomaly detection model"""
    try:
        from project1.config import ISO_MODEL_PATH, PREPROCESSOR_PATH
        import joblib
        
        # Check if files exist with detailed error messages
        if not ISO_MODEL_PATH.exists():
            return None, None, f"❌ Không tìm thấy file model: {ISO_MODEL_PATH}\n\n💡 Có thể models chưa được upload lên GitHub. Vui lòng kiểm tra lại."
        
        if not PREPROCESSOR_PATH.exists():
            return None, None, f"❌ Không tìm thấy file preprocessor: {PREPROCESSOR_PATH}\n\n💡 Có thể preprocessor chưa được upload lên GitHub. Vui lòng kiểm tra lại."
        
        try:
            iso_data = joblib.load(ISO_MODEL_PATH)
        except Exception as e:
            return None, None, f"❌ Lỗi khi đọc file model: {str(e)}\n\n💡 File có thể bị hỏng hoặc không tương thích."
        
        # Check if it's a dict (saved with metadata) or direct model
        if isinstance(iso_data, dict):
            iso_model = iso_data.get('model', iso_data.get('iso_model', iso_data))
        else:
            iso_model = iso_data
        
        try:
            preprocessor_data = joblib.load(PREPROCESSOR_PATH)
        except Exception as e:
            return None, None, f"❌ Lỗi khi đọc file preprocessor: {str(e)}\n\n💡 File có thể bị hỏng hoặc không tương thích."
        
        if isinstance(preprocessor_data, dict):
            preprocessor = preprocessor_data.get('preprocessor')
            if preprocessor is None:
                return None, None, "❌ Preprocessor không có trong file. Cấu trúc file không đúng."
        else:
            preprocessor = preprocessor_data
        
        return iso_model, preprocessor, None
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return None, None, f"❌ Lỗi khi load model: {str(e)}\n\n<details><summary>Chi tiết lỗi</summary>\n\n```\n{error_details}\n```\n</details>"

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
                try:
                    # Load FULL dataset, not just sample
                    df = pd.read_csv(path, low_memory=False)
                    if len(df) == 0:
                        return None, f"❌ File dữ liệu rỗng: {path}"
                    return df, None
                except Exception as e:
                    return None, f"❌ Lỗi khi đọc file {path}: {str(e)}"
        
        paths_tried = "\n".join([f"  - {p}" for p in possible_paths])
        return None, f"❌ Không tìm thấy file dữ liệu.\n\nĐã thử các đường dẫn sau:\n{paths_tried}\n\n💡 Có thể file data chưa được upload lên GitHub. Vui lòng kiểm tra lại."
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return None, f"❌ Lỗi khi load dữ liệu: {str(e)}\n\n<details><summary>Chi tiết lỗi</summary>\n\n```\n{error_details}\n```\n</details>"

# Home page
if page == "🏠 Trang chủ":
    st.markdown('<div class="main-header">🏍️ Motorbike Analysis Platform</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; color: #6b7280; margin-bottom: 3rem; font-size: 1.15rem; line-height: 1.8;'>
        <p style='margin-bottom: 0.5rem;'>Nền tảng phân tích và dự đoán giá xe máy thông minh</p>
        <p style='margin: 0; font-size: 1rem;'>
            Dựa trên dữ liệu từ <strong style='color: #667eea;'>Chợ Tốt</strong> với 
            <span class="badge" style='display: inline-block; padding: 0.25rem 0.75rem; margin: 0 0.5rem;'>7,208+ tin đăng</span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature Cards with Enhanced Design
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div style='font-size: 3rem; margin-bottom: 1rem; text-align: center;'>💰</div>
            <h2 style='color: #667eea; margin-top: 0; text-align: center; font-size: 1.5rem;'>Dự đoán giá</h2>
            <p style='color: #4b5563; line-height: 1.8; text-align: center;'>
                Dự đoán giá xe máy chính xác dựa trên:
            </p>
            <ul style='color: #6b7280; line-height: 2;'>
                <li>✨ Thương hiệu, dòng xe</li>
                <li>📅 Năm đăng ký, số km</li>
                <li>🔧 Tình trạng, dung tích</li>
                <li>📍 Vị trí, xuất xứ</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h2 style='color: #f59e0b; margin-top: 0;'>🚨 Phát hiện bất thường</h2>
            <p style='color: #4b5563; line-height: 1.8;'>
                Phát hiện các tin đăng có giá bất thường:
            </p>
            <ul style='color: #6b7280; line-height: 2;'>
                <li>🔍 Residual-based detection</li>
                <li>🌲 Isolation Forest</li>
                <li>📊 So sánh với thị trường</li>
                <li>⚠️ Cảnh báo giá bất thường</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h2 style='color: #10b981; margin-top: 0;'>🔍 Gợi ý xe tương tự</h2>
            <p style='color: #4b5563; line-height: 1.8;'>
                Tìm xe máy tương tự thông minh:
            </p>
            <ul style='color: #6b7280; line-height: 2;'>
                <li>🎯 KNN-based recommendation</li>
                <li>📝 Content-based filtering</li>
                <li>🔎 Tìm kiếm đa tiêu chí</li>
                <li>💡 Gợi ý phù hợp nhất</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Status Section with better UI
    st.markdown("""
    <div style='text-align: center; margin: 2rem 0;'>
        <h2 style='color: #1f2937; margin-bottom: 1.5rem;'>📊 Trạng thái hệ thống</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Check models status
    price_model, _, price_err = load_price_model()
    anomaly_model, _, anomaly_err = load_anomaly_model()
    sample_data, data_err = load_sample_data()
    
    status_col1, status_col2, status_col3 = st.columns(3)
    
    with status_col1:
        if price_model:
            st.markdown("""
            <div class="status-card success">
                <h3 style='color: #10b981; margin-top: 0;'>💰 Price Model</h3>
                <p style='font-size: 1.2rem; font-weight: 600; color: #059669;'>✅ Sẵn sàng</p>
                <p style='color: #6b7280; font-size: 0.9rem;'>Model dự đoán giá đã được tải thành công</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="status-card error">
                <h3 style='color: #ef4444; margin-top: 0;'>💰 Price Model</h3>
                <p style='font-size: 1rem; font-weight: 600; color: #dc2626;'>❌ Chưa sẵn sàng</p>
                <p style='color: #6b7280; font-size: 0.85rem;'>{price_err or 'Chưa load'}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with status_col2:
        if anomaly_model:
            st.markdown("""
            <div class="status-card success">
                <h3 style='color: #10b981; margin-top: 0;'>🚨 Anomaly Model</h3>
                <p style='font-size: 1.2rem; font-weight: 600; color: #059669;'>✅ Sẵn sàng</p>
                <p style='color: #6b7280; font-size: 0.9rem;'>Model phát hiện bất thường đã được tải thành công</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="status-card error">
                <h3 style='color: #ef4444; margin-top: 0;'>🚨 Anomaly Model</h3>
                <p style='font-size: 1rem; font-weight: 600; color: #dc2626;'>❌ Chưa sẵn sàng</p>
                <p style='color: #6b7280; font-size: 0.85rem;'>{anomaly_err or 'Chưa load'}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with status_col3:
        if sample_data is not None:
            st.markdown(f"""
            <div class="status-card success">
                <h3 style='color: #10b981; margin-top: 0;'>📊 Dataset</h3>
                <p style='font-size: 1.2rem; font-weight: 600; color: #059669;'>✅ {len(sample_data):,} records</p>
                <p style='color: #6b7280; font-size: 0.9rem;'>Dữ liệu đã được tải thành công</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="status-card error">
                <h3 style='color: #ef4444; margin-top: 0;'>📊 Dataset</h3>
                <p style='font-size: 1rem; font-weight: 600; color: #dc2626;'>❌ Chưa sẵn sàng</p>
                <p style='color: #6b7280; font-size: 0.85rem;'>{data_err or 'Chưa load'}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Author Info Section
    st.markdown("""
    <div style='text-align: center; margin: 2rem 0;'>
        <h2 style='color: #1f2937; margin-bottom: 1.5rem;'>👤 Thông tin tác giả</h2>
    </div>
    """, unsafe_allow_html=True)
    
    author_col1, author_col2 = st.columns(2)
    
    with author_col1:
        st.markdown("""
        <div class="info-box">
            <h3 style='color: #667eea; margin-top: 0;'>👨‍💻 Thông tin cá nhân</h3>
            <p style='line-height: 2.5; color: #4b5563;'>
                <strong>👤 Tác giả:</strong> Đoàn Anh<br>
                <strong>📧 Email:</strong> <a href="mailto:anhwin01@gmail.com" style='color: #667eea; text-decoration: none;'>anhwin01@gmail.com</a><br>
                <strong>🔗 GitHub:</strong> <a href="https://github.com/teddyDn2001" target="_blank" style='color: #667eea; text-decoration: none;'>@teddyDn2001</a><br>
                <strong>📚 Repository:</strong> <a href="https://github.com/teddyDn2001/ProjectChoTot" target="_blank" style='color: #667eea; text-decoration: none;'>ProjectChoTot</a>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with author_col2:
        st.markdown("""
        <div class="info-box">
            <h3 style='color: #667eea; margin-top: 0;'>📊 Thông tin dự án</h3>
            <p style='line-height: 2.5; color: #4b5563;'>
                <strong>🎓 Đồ án:</strong> Data Science<br>
                <strong>📊 Dataset:</strong> Chợ Tốt - 7,208 tin rao<br>
                <strong>🏍️ Phạm vi:</strong> TP.HCM<br>
                <strong>📅 Năm:</strong> 2024
            </p>
        </div>
        """, unsafe_allow_html=True)

# Price Prediction page
elif page == "💰 Dự đoán giá":
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h1 style='font-size: 2.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem;'>
            💰 Dự đoán giá xe máy
        </h1>
        <p style='color: #6b7280; font-size: 1.1rem;'>Nhập thông tin xe để nhận dự đoán giá chính xác</p>
    </div>
    """, unsafe_allow_html=True)
    
    model, preprocessor, error = load_price_model()
    
    if error:
        st.error(error)
        st.markdown("---")
        st.warning("⚠️ **Lưu ý:** Form bên dưới vẫn có thể sử dụng để xem giao diện, nhưng sẽ không thể dự đoán giá cho đến khi models được load thành công.")
        st.info("""
        **💡 Hướng dẫn khắc phục:**
        1. Kiểm tra xem models đã được push lên GitHub chưa
        2. Đảm bảo files `project1/models/price_model.joblib` và `project1/artifacts/preprocessor.joblib` có trên GitHub
        3. Nếu files quá lớn (>100MB), cần dùng Git LFS
        4. Sau khi push, đợi vài phút để Streamlit Cloud sync lại
        5. Reload app trên Streamlit Cloud (click "Relaunch to update")
        """)
        st.markdown("---")
        # Don't stop - show form anyway so user can see the UI
        # st.stop()
    
    # Show form regardless of model status
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
                # Check if model is available
                if error or model is None or preprocessor is None:
                    st.error("❌ Không thể dự đoán vì model chưa được load. Vui lòng xem hướng dẫn khắc phục ở trên.")
                else:
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
                            # Display result with beautiful UI
                            st.markdown("---")
                            st.markdown("""
                            <div style='text-align: center; padding: 3rem 2rem; background: linear-gradient(135deg, rgba(245, 247, 250, 0.95) 0%, rgba(195, 207, 226, 0.95) 100%); backdrop-filter: blur(10px); border-radius: 1.5rem; margin: 2rem 0; box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2); border: 2px solid rgba(255, 255, 255, 0.5);'>
                                <div style='font-size: 4rem; margin-bottom: 1rem;'>💰</div>
                                <h3 style='color: #6b7280; margin-bottom: 1.5rem; font-size: 1.25rem; font-weight: 600;'>Giá dự đoán</h3>
                                <div class="price-display">{:,.0f} VNĐ</div>
                                <p style='font-size: 1.75rem; color: #667eea; font-weight: 700; margin-top: 1.5rem; padding: 1rem; background: rgba(255, 255, 255, 0.5); border-radius: 0.75rem; display: inline-block;'>
                                    ≈ {:.2f} triệu VNĐ
                                </p>
                            </div>
                            """.format(prediction, prediction/1_000_000), unsafe_allow_html=True)
                            
                            # Additional info
                            col_info1, col_info2, col_info3 = st.columns(3)
                            with col_info1:
                                st.metric("Thương hiệu", thuong_hieu)
                            with col_info2:
                                st.metric("Năm đăng ký", nam_dang_ky)
                            with col_info3:
                                st.metric("Số km", f"{so_km:,} km")
                    
                    except Exception as e:
                        st.error(f"Lỗi khi dự đoán: {str(e)}")
                        import traceback
                        with st.expander("Chi tiết lỗi"):
                            st.code(traceback.format_exc())

# Anomaly Detection page
elif page == "🚨 Phát hiện bất thường":
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h1 style='font-size: 2.5rem; background: linear-gradient(135deg, #f59e0b 0%, #ef4444 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem;'>
            🚨 Phát hiện giá bất thường
        </h1>
        <p style='color: #6b7280; font-size: 1.1rem;'>Kiểm tra xem giá xe có bất thường so với thị trường không</p>
    </div>
    """, unsafe_allow_html=True)
    
    model, preprocessor, error = load_anomaly_model()
    
    if error:
        st.error(error)
        st.markdown("---")
        st.warning("⚠️ **Lưu ý:** Form bên dưới vẫn có thể sử dụng để xem giao diện, nhưng sẽ không thể phát hiện bất thường cho đến khi models được load thành công.")
        st.info("""
        **💡 Hướng dẫn khắc phục:**
        1. Kiểm tra xem models đã được push lên GitHub chưa
        2. Đảm bảo files `project1/models/iso_model.joblib` và `project1/artifacts/preprocessor.joblib` có trên GitHub
        3. Nếu files quá lớn, cần dùng Git LFS
        4. Sau khi push, đợi vài phút để Streamlit Cloud sync lại
        5. Reload app trên Streamlit Cloud (click "Relaunch to update")
        """)
        st.markdown("---")
        # Don't stop - show form anyway
        # st.stop()
    
    # Show form regardless of model status
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
                # Check if model is available
                if error or model is None or preprocessor is None:
                    st.error("❌ Không thể phát hiện bất thường vì model chưa được load. Vui lòng xem hướng dẫn khắc phục ở trên.")
                else:
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
                        
                        # Transform features
                        X_transformed = preprocessor.transform(input_data)
                        
                        # CRITICAL: IsolationForest model was trained with log_price as additional feature
                        # Model expects 279 features: 278 from preprocessor + 1 log_price
                        # Add log_price feature (log of the price user entered)
                        from scipy import sparse
                        import scipy.sparse as sp
                        
                        # Calculate log_price (same as training: log1p of price)
                        price_for_iso = max(0, gia_vnd)  # Ensure non-negative
                        log_price = np.log1p(price_for_iso).reshape(-1, 1)
                        
                        # Concatenate transformed features with log_price
                        if sparse.issparse(X_transformed):
                            from scipy.sparse import hstack, csr_matrix
                            X_transformed_aug = hstack([X_transformed, csr_matrix(log_price)])
                        else:
                            X_transformed_aug = np.hstack([X_transformed, log_price])
                        
                        # Convert to dense if needed for prediction
                        if hasattr(X_transformed_aug, 'toarray'):
                            X_transformed_aug = X_transformed_aug.toarray()
                        
                        # Predict anomaly with augmented features (279 features)
                        anomaly_score = model.decision_function(X_transformed_aug)[0]
                        predictions = model.predict(X_transformed_aug)
                        is_anomaly = predictions[0] == -1
                        
                        # Validate scores
                        if np.isnan(anomaly_score) or np.isinf(anomaly_score):
                            st.warning("⚠️ Không thể tính anomaly score. Vui lòng kiểm tra lại thông tin.")
                        else:
                            # Display result with enhanced UI
                            if is_anomaly:
                                st.markdown("""
                                <div style='text-align: center; padding: 3rem 2rem; background: linear-gradient(135deg, rgba(254, 242, 242, 0.95) 0%, rgba(254, 226, 226, 0.95) 100%); backdrop-filter: blur(10px); border-radius: 1.5rem; margin: 2rem 0; box-shadow: 0 8px 32px rgba(239, 68, 68, 0.2); border: 3px solid #ef4444;'>
                                    <div style='font-size: 4rem; margin-bottom: 1rem;'>⚠️</div>
                                    <h2 style='color: #dc2626; margin-bottom: 1rem; font-size: 2.5rem; font-weight: 700;'>Phát hiện giá BẤT THƯỜNG</h2>
                                    <p style='font-size: 1.3rem; color: #991b1b; font-weight: 600; margin-bottom: 1.5rem;'>Anomaly Score: {:.4f}</p>
                                    <p style='color: #7f1d1d; margin-top: 1rem; font-size: 1.1rem; line-height: 1.6;'>Giá này có vẻ không phù hợp với thị trường. Nên kiểm tra lại thông tin và so sánh với các xe tương tự.</p>
                                </div>
                                """.format(anomaly_score), unsafe_allow_html=True)
                                
                                # Show predicted price for comparison
                                try:
                                    price_model, _, _ = load_price_model()
                                    if price_model is not None:
                                        # Use X_transformed (278 features) for price prediction, not X_transformed_aug
                                        if hasattr(X_transformed, 'toarray'):
                                            X_for_price = X_transformed.toarray()
                                        else:
                                            X_for_price = X_transformed
                                        
                                        price_pred = price_model.predict(X_for_price)[0]
                                        if price_pred > 0:
                                            st.markdown("---")
                                            col_comp1, col_comp2 = st.columns(2)
                                            with col_comp1:
                                                st.markdown("""
                                                <div style='padding: 1.5rem; background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); border-radius: 1rem; border-left: 4px solid #3b82f6;'>
                                                    <h3 style='color: #1e40af; margin-top: 0;'>💡 Giá dự đoán hợp lý</h3>
                                                    <p style='font-size: 1.5rem; font-weight: 700; color: #1e3a8a;'>{:.2f} triệu VNĐ</p>
                                                </div>
                                                """.format(price_pred/1_000_000), unsafe_allow_html=True)
                                            with col_comp2:
                                                st.markdown("""
                                                <div style='padding: 1.5rem; background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border-radius: 1rem; border-left: 4px solid #f59e0b;'>
                                                    <h3 style='color: #92400e; margin-top: 0;'>💰 Giá bạn nhập</h3>
                                                    <p style='font-size: 1.5rem; font-weight: 700; color: #78350f;'>{:.2f} triệu VNĐ</p>
                                                </div>
                                                """.format(gia_vnd/1_000_000), unsafe_allow_html=True)
                                            
                                            diff_pct = abs(price_pred - gia_vnd) / price_pred * 100
                                            if diff_pct > 30:
                                                st.warning(f"⚠️ **Chênh lệch {diff_pct:.1f}%** so với giá dự đoán - đây là lý do phát hiện bất thường")
                                except Exception as e:
                                    # Silently fail - not critical
                                    pass
                            else:
                                st.markdown("""
                                <div style='text-align: center; padding: 3rem 2rem; background: linear-gradient(135deg, rgba(236, 253, 245, 0.95) 0%, rgba(209, 250, 229, 0.95) 100%); backdrop-filter: blur(10px); border-radius: 1.5rem; margin: 2rem 0; box-shadow: 0 8px 32px rgba(16, 185, 129, 0.2); border: 3px solid #10b981;'>
                                    <div style='font-size: 4rem; margin-bottom: 1rem;'>✅</div>
                                    <h2 style='color: #059669; margin-bottom: 1rem; font-size: 2.5rem; font-weight: 700;'>Giá BÌNH THƯỜNG</h2>
                                    <p style='font-size: 1.3rem; color: #047857; font-weight: 600; margin-bottom: 1.5rem;'>Anomaly Score: {:.4f}</p>
                                    <p style='color: #065f46; margin-top: 1rem; font-size: 1.1rem; line-height: 1.6;'>Giá này phù hợp với thị trường. Bạn có thể yên tâm về mức giá này.</p>
                                </div>
                                """.format(anomaly_score), unsafe_allow_html=True)
                        
                    except Exception as e:
                        st.error(f"Lỗi: {str(e)}")
                        import traceback
                        with st.expander("Chi tiết lỗi"):
                            st.code(traceback.format_exc())

# Recommendation page
elif page == "🔍 Gợi ý xe tương tự":
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h1 style='font-size: 2.5rem; background: linear-gradient(135deg, #10b981 0%, #059669 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem;'>
            🔍 Tìm xe máy tương tự
        </h1>
        <p style='color: #6b7280; font-size: 1.1rem;'>Nhập ID hoặc thông tin xe để tìm các xe tương tự</p>
    </div>
    """, unsafe_allow_html=True)
    
    sample_data, error = load_sample_data()
    
    if error:
        st.error(error)
        st.markdown("---")
        st.info("""
        **💡 Hướng dẫn khắc phục:**
        1. Kiểm tra xem file data đã được push lên GitHub chưa
        2. Đảm bảo file `data/data_motobikes.xlsx - Sheet1.csv` có trên GitHub
        3. Nếu file quá lớn, cần dùng Git LFS
        4. Sau khi push, đợi vài phút để Streamlit Cloud sync lại
        """)
        st.stop()
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
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h1 style='font-size: 2.5rem; background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem;'>
            📊 Phân cụm dữ liệu
        </h1>
        <p style='color: #6b7280; font-size: 1.1rem;'>Phân khúc thị trường xe máy thông minh</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box" style='margin-bottom: 2rem;'>
        <h3 style='color: #3b82f6; margin-top: 0;'>💡 Phân cụm dữ liệu giúp:</h3>
        <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-top: 1rem;'>
            <div>
                <strong>🎯 Phân khúc thị trường</strong><br>
                <span style='color: #6b7280;'>Chia xe máy thành các nhóm có đặc điểm tương đồng</span>
            </div>
            <div>
                <strong>👥 Hiểu khách hàng</strong><br>
                <span style='color: #6b7280;'>Mỗi phân khúc đại diện cho một nhóm khách hàng khác nhau</span>
            </div>
            <div>
                <strong>💰 Định giá hợp lý</strong><br>
                <span style='color: #6b7280;'>Biết xe thuộc phân khúc nào để định giá phù hợp</span>
            </div>
            <div>
                <strong>🔍 Gợi ý sản phẩm</strong><br>
                <span style='color: #6b7280;'>Đề xuất xe tương tự trong cùng phân khúc</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
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
**📧 Email:** anhwin01@gmail.com  
**🎓 Đồ án:** Data Science  
**📊 Dataset:** Chợ Tốt  
**📈 Số lượng:** 7,208 records
""")
st.sidebar.markdown("### 📚 Tài liệu")
st.sidebar.markdown("[GitHub Repository](https://github.com/teddyDn2001/ProjectChoTot)")
st.sidebar.markdown("[README](README.md)")

