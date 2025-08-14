"""
Speech Emotion Recognition (SER) Package

A comprehensive package for emotion recognition from speech using
machine learning and deep learning techniques.
"""

__version__ = "1.0.0"
__author__ = "SER Team"

from .config import *
from .model import *
from .features import *
from .inference import *

__all__ = [
    "EMOTIONS",
    "extract_features", 
    "load_model_with_fallback",
    "predict_emotion",
    "predict_path",
    "BASE_DIR",
    "MODEL_PATH",
    "EXAMPLES_DIR"
]
