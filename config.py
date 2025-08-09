"""
Cross-platform configuration for local paths used by the project.

All paths are derived relative to the repository root so the code runs on macOS,
Linux, and Windows without manual changes.
"""
from __future__ import annotations

import os
from pathlib import Path


# Repository root (directory that contains this file)
REPO_ROOT: Path = Path(__file__).resolve().parent

# Where to save/load precomputed feature matrices (X.joblib and y.joblib)
DATASET_FEATURES_DIR: Path = REPO_ROOT / "dataset_features"
DATASET_FEATURES_DIR.mkdir(parents=True, exist_ok=True)

# Where the combined RAVDESS (+ optional TESS) audio files live
# The pipeline will create Actor_25 and Actor_26 inside this directory if needed
FEATURES_DIR: Path = REPO_ROOT / "features"
FEATURES_DIR.mkdir(parents=True, exist_ok=True)

# Where the original TESS dataset is expected (place it here if you use tess_pipeline)
TESS_DIR: Path = REPO_ROOT / "TESS_Toronto_emotional_speech_set_data"


# Public constants consumed by scripts
SAVE_DIR_PATH: str = str(DATASET_FEATURES_DIR)
TRAINING_FILES_PATH: str = str(FEATURES_DIR)
TESS_ORIGINAL_FOLDER_PATH: str = str(TESS_DIR)


def ensure_actor_dirs_exist() -> None:
    """Create Actor_25 and Actor_26 inside the features directory if missing."""
    (FEATURES_DIR / "Actor_25").mkdir(parents=True, exist_ok=True)
    (FEATURES_DIR / "Actor_26").mkdir(parents=True, exist_ok=True)


__all__ = [
    "REPO_ROOT",
    "DATASET_FEATURES_DIR",
    "FEATURES_DIR",
    "TESS_DIR",
    "SAVE_DIR_PATH",
    "TRAINING_FILES_PATH",
    "TESS_ORIGINAL_FOLDER_PATH",
    "ensure_actor_dirs_exist",
]


