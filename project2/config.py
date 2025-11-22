"""
Configuration file for Project 2 - Recommendation & Clustering
Update DATA_DIR to point to your data location
"""
from pathlib import Path

# Project root (assuming this file is in project2/)
PROJECT_ROOT = Path(__file__).parent
REPO_ROOT = PROJECT_ROOT.parent

# Data directory - update this if your data is elsewhere
DATA_DIR = REPO_ROOT / "data"
RAW_DATA_FILE = DATA_DIR / "data_motobikes.xlsx - Sheet1.csv"

# Output directories
REPORTS_DIR = PROJECT_ROOT / "reports"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
FIGURES_DIR = PROJECT_ROOT / "figures"

# Create directories if they don't exist
for dir_path in [REPORTS_DIR, ARTIFACTS_DIR, FIGURES_DIR]:
    dir_path.mkdir(exist_ok=True)

# Random seed for reproducibility
RANDOM_SEED = 42

