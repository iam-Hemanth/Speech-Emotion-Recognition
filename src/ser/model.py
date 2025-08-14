"""
Model loading and prediction utilities for Speech Emotion Recognition.
Handles model loading with fallbacks and input shape adaptation.
"""

from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Any, Optional
import numpy as np
import librosa
import logging
from tensorflow import keras
from tensorflow.keras import layers, models

from .config import EMOTIONS, get_model_path
from .features import extract_features

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def adapt_input_shape(model: keras.Model, features: np.ndarray) -> np.ndarray:
    """
    Adapt input features to match the model's expected input shape.
    
    Args:
        model: The Keras model
        features: Input features array
        
    Returns:
        Reshaped features array
    """
    inp_shape = model.input_shape
    
    # Handle list of input shapes (multiple inputs)
    if isinstance(inp_shape, list):
        inp_shape = inp_shape[0]
    
    x = features.copy()
    
    # Add batch dimension if missing
    if x.ndim == 1:
        x = x[None, :]
    
    # Add channel dimension for Conv1D layers
    if len(inp_shape) == 3 and x.ndim == 2:
        x = x[:, :, None]
    
    logger.debug(f"Input shape: {inp_shape}, Features shape: {x.shape}")
    return x

def build_fallback_model() -> keras.Model:
    """
    Build the SER model architecture as a fallback when loading fails.
    
    Returns:
        Compiled Keras model
    """
    model = models.Sequential(name="ser_cnn")
    
    # First Conv1D block
    model.add(layers.Conv1D(64, 5, padding='same', input_shape=(40, 1), name='conv1d_1'))
    model.add(layers.Activation('relu', name='activation_1'))
    model.add(layers.Dropout(0.1, name='dropout_1'))
    model.add(layers.MaxPooling1D(pool_size=4, name='max_pooling1d_1'))
    
    # Second Conv1D block
    model.add(layers.Conv1D(128, 5, padding='same', name='conv1d_2'))
    model.add(layers.Activation('relu', name='activation_2'))
    model.add(layers.Dropout(0.1, name='dropout_2'))
    model.add(layers.MaxPooling1D(pool_size=4, name='max_pooling1d_2'))
    
    # Third Conv1D block
    model.add(layers.Conv1D(256, 5, padding='same', name='conv1d_3'))
    model.add(layers.Activation('relu', name='activation_3'))
    model.add(layers.Dropout(0.1, name='dropout_3'))
    
    # Flatten and dense layers
    model.add(layers.Flatten(name='flatten_1'))
    model.add(layers.Dense(8, name='dense_1'))
    model.add(layers.Activation('softmax', name='activation_4'))
    
    # Compile model
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    logger.info("Built fallback model architecture")
    return model

def load_model_with_fallback(model_path: Optional[Path] = None) -> keras.Model:
    """
    Load the SER model with fallback to rebuilding if loading fails.
    
    Args:
        model_path: Path to the model file (optional, uses config default)
        
    Returns:
        Loaded or rebuilt Keras model
        
    Raises:
        FileNotFoundError: If model file doesn't exist
        ValueError: If model cannot be loaded or rebuilt
    """
    if model_path is None:
        model_path = get_model_path()
    
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")
    
    try:
        # Try to load the model directly
        logger.info(f"Loading model from {model_path}")
        model = keras.models.load_model(model_path)
        logger.info("Model loaded successfully")
        return model
        
    except Exception as e:
        logger.warning(f"Failed to load model directly: {e}")
        logger.info("Attempting to rebuild model and load weights...")
        
        try:
            # Build the model architecture
            model = build_fallback_model()
            
            # Try to load weights by name
            model.load_weights(model_path, by_name=True)
            logger.info("Model rebuilt and weights loaded successfully")
            return model
            
        except Exception as e2:
            logger.error(f"Failed to rebuild model: {e2}")
            raise ValueError(
                f"Could not load or rebuild model from {model_path}. "
                f"Original error: {e}. Rebuild error: {e2}"
            )

def predict_emotion(model: keras.Model, audio_path: Path) -> Dict[str, Any]:
    """
    Predict emotion from an audio file.
    
    Args:
        model: Loaded Keras model
        audio_path: Path to audio file
        
    Returns:
        Dictionary with prediction results
        
    Raises:
        FileNotFoundError: If audio file doesn't exist
        ValueError: If prediction fails
    """
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    try:
        # Extract features
        features = extract_features(audio_path)
        
        # Adapt input shape
        x = adapt_input_shape(model, features)
        
        # Make prediction
        predictions = model.predict(x, verbose=0)
        probs = predictions[0]
        
        # Get top prediction
        top_idx = int(np.argmax(probs))
        top_prob = float(probs[top_idx])
        
        # Get emotion label
        if 0 <= top_idx < len(EMOTIONS):
            label = EMOTIONS[top_idx]
        else:
            label = f"unknown_{top_idx}"
        
        return {
            "file": str(audio_path),
            "pred_index": top_idx,
            "pred_label": label,
            "confidence": round(top_prob, 4),
            "probs": probs.tolist()
        }
        
    except Exception as e:
        logger.error(f"Error predicting emotion for {audio_path}: {e}")
        raise ValueError(f"Prediction failed for {audio_path}: {e}")

def predict_path(audio_path: Path, model_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    Convenience function to load model and predict emotion.
    
    Args:
        audio_path: Path to audio file
        model_path: Path to model file (optional)
        
    Returns:
        Dictionary with prediction results
    """
    model = load_model_with_fallback(model_path)
    return predict_emotion(model, audio_path)

# Backward compatibility
def load_model_with_fallback_legacy(model_path: Path) -> keras.Model:
    """Legacy function for backward compatibility."""
    return load_model_with_fallback(model_path)
