"""
Configuration and path management for Speech Emotion Recognition.
Handles cross-platform compatibility and ensures all required directories exist.
"""

from pathlib import Path
import os
import sys
from typing import Optional

# Base directory (project root)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Core directories
SRC_DIR = BASE_DIR / "src"
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
SCRIPTS_DIR = BASE_DIR / "scripts"
NOTEBOOKS_DIR = BASE_DIR / "notebooks"
DOCS_DIR = BASE_DIR / "docs"
ASSETS_DIR = BASE_DIR / "assets"

# Data subdirectories
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXAMPLES_DIR = DATA_DIR / "examples"

# Dataset directories
RAVDESS_DIR = RAW_DATA_DIR / "ravdess"
TESS_DIR = RAW_DATA_DIR / "tess"
TESS_ORIGINAL_DIR = BASE_DIR / "TESS_Toronto_emotional_speech_set_data"

# Feature directories
FEATURES_DIR = PROCESSED_DATA_DIR / "features"
DATASET_FEATURES_DIR = PROCESSED_DATA_DIR / "dataset_features"

# Model paths
MODEL_PATH = MODELS_DIR / "SER_model.h5"
MODEL_PATH_LEGACY = BASE_DIR / "Deep Learning" / "SER_model.h5"

# Emotion labels
EMOTIONS = [
    "neutral", "calm", "happy", "sad", "angry", "fear", "disgust", "surprised"
]

def ensure_dirs_exist() -> None:
    """Create all necessary directories if they don't exist."""
    directories = [
        SRC_DIR,
        DATA_DIR,
        MODELS_DIR,
        SCRIPTS_DIR,
        NOTEBOOKS_DIR,
        DOCS_DIR,
        ASSETS_DIR,
        RAW_DATA_DIR,
        PROCESSED_DATA_DIR,
        EXAMPLES_DIR,
        RAVDESS_DIR,
        TESS_DIR,
        FEATURES_DIR,
        DATASET_FEATURES_DIR,
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
    
    # Create Actor_25 and Actor_26 subdirectories within features
    (FEATURES_DIR / "Actor_25").mkdir(exist_ok=True)
    (FEATURES_DIR / "Actor_26").mkdir(exist_ok=True)

def get_model_path() -> Path:
    """Get the model path with fallback to legacy location."""
    if MODEL_PATH.exists():
        return MODEL_PATH
    elif MODEL_PATH_LEGACY.exists():
        return MODEL_PATH_LEGACY
    else:
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH} or {MODEL_PATH_LEGACY}. "
            "Please ensure the model file exists."
        )

def validate_paths() -> dict:
    """Validate all critical paths and return status."""
    status = {
        "base_dir": BASE_DIR.exists(),
        "model": get_model_path().exists(),
        "examples": EXAMPLES_DIR.exists() and any(EXAMPLES_DIR.glob("*.wav")),
        "features": FEATURES_DIR.exists(),
        "dataset_features": DATASET_FEATURES_DIR.exists(),
    }
    
    # Check for required data files
    if DATASET_FEATURES_DIR.exists():
        status["X_features"] = (DATASET_FEATURES_DIR / "X.joblib").exists()
        status["y_features"] = (DATASET_FEATURES_DIR / "y.joblib").exists()
    
    return status

def setup_environment() -> None:
    """Set up the complete environment with error handling."""
    try:
        ensure_dirs_exist()
        print("✅ All directories created successfully")
        
        # Validate critical components
        status = validate_paths()
        missing = [k for k, v in status.items() if not v]
        
        if missing:
            print(f"⚠️  Missing components: {', '.join(missing)}")
        else:
            print("✅ All critical components found")
            
    except Exception as e:
        print(f"❌ Error setting up environment: {e}")
        raise

# Auto-setup when imported
if __name__ != "__main__":
    ensure_dirs_exist()
