"""
Configuration file for Project 1 - Price Prediction & Anomaly Detection
Update DATA_DIR to point to your data location
"""
from pathlib import Path

# Project root (assuming this file is in project1/)
PROJECT_ROOT = Path(__file__).parent
REPO_ROOT = PROJECT_ROOT.parent

# Data directory - update this if your data is elsewhere
DATA_DIR = REPO_ROOT / "data"
RAW_DATA_FILE = DATA_DIR / "data_motobikes.xlsx - Sheet1.csv"
CLEAN_DATA_FILE = PROJECT_ROOT / "data_motobikes_clean.csv"

# Output directories
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
MODELS_DIR = PROJECT_ROOT / "models"
ANOMALY_OUTPUTS_DIR = PROJECT_ROOT / "anomaly_outputs"
PLOTS_DIR = PROJECT_ROOT / "plots"

# Create directories if they don't exist
for dir_path in [ARTIFACTS_DIR, MODELS_DIR, ANOMALY_OUTPUTS_DIR, PLOTS_DIR]:
    dir_path.mkdir(exist_ok=True)

# Model paths
PREPROCESSOR_PATH = ARTIFACTS_DIR / "preprocessor.joblib"
PRICE_MODEL_PATH = MODELS_DIR / "price_model.joblib"
ISO_MODEL_PATH = MODELS_DIR / "iso_model.joblib"

# Output file paths
VALIDATION_ISSUES_FILE = PROJECT_ROOT / "validation_issues.csv"
ANOMALY_SUMMARY_FILE = PROJECT_ROOT / "anomaly_summary.csv"
EXPLAIN_PERMUTATION_FILE = PROJECT_ROOT / "explain_permutation.csv"
PRICE_CV_RESULTS_FILE = MODELS_DIR / "price_cv_results.csv"

