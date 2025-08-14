"""
Feature extraction utilities for Speech Emotion Recognition.
Extracts MFCC features from audio files and manages feature persistence.
"""

from pathlib import Path
import numpy as np
import librosa
import joblib
from typing import List, Tuple, Optional
import logging

from .config import FEATURES_DIR, DATASET_FEATURES_DIR, ensure_dirs_exist

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_features(audio_path: Path) -> np.ndarray:
    """
    Extract MFCC features from an audio file.
    
    Args:
        audio_path: Path to the audio file
        
    Returns:
        MFCC features as numpy array
        
    Raises:
        FileNotFoundError: If audio file doesn't exist
        ValueError: If audio file cannot be loaded
    """
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    try:
        # Load audio with resampling
        x, sr = librosa.load(str(audio_path), res_type="kaiser_fast")
        
        # Extract MFCC features
        mfcc = librosa.feature.mfcc(y=x, sr=sr, n_mfcc=40)
        mfcc_mean = np.mean(mfcc.T, axis=0)
        
        return mfcc_mean.astype(np.float32)
        
    except Exception as e:
        logger.error(f"Error extracting features from {audio_path}: {e}")
        raise ValueError(f"Failed to extract features from {audio_path}: {e}")

def process_audio_directory(audio_dir: Path, output_dir: Path) -> None:
    """
    Process all audio files in a directory and save features.
    
    Args:
        audio_dir: Directory containing audio files
        output_dir: Directory to save extracted features
    """
    if not audio_dir.exists():
        logger.warning(f"Audio directory not found: {audio_dir}")
        return
    
    ensure_dirs_exist()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    audio_files = list(audio_dir.glob("*.wav"))
    if not audio_files:
        logger.warning(f"No .wav files found in {audio_dir}")
        return
    
    logger.info(f"Processing {len(audio_files)} audio files from {audio_dir}")
    
    features_list = []
    labels_list = []
    
    for audio_file in audio_files:
        try:
            # Extract emotion label from filename
            # Expected format: modality-vocal_channel-emotion-intensity-statement-repetition-actor.wav
            filename = audio_file.stem
            parts = filename.split('-')
            
            if len(parts) >= 3:
                emotion_code = int(parts[2])
                # Map emotion codes to labels
                emotion_map = {
                    1: "neutral", 2: "calm", 3: "happy", 4: "sad",
                    5: "angry", 6: "fear", 7: "disgust", 8: "surprised"
                }
                emotion_label = emotion_map.get(emotion_code, "unknown")
            else:
                emotion_label = "unknown"
            
            # Extract features
            features = extract_features(audio_file)
            
            features_list.append(features)
            labels_list.append(emotion_label)
            
            logger.debug(f"Processed {audio_file.name} -> {emotion_label}")
            
        except Exception as e:
            logger.error(f"Error processing {audio_file}: {e}")
            continue
    
    if features_list:
        # Convert to numpy arrays
        X = np.array(features_list)
        y = np.array(labels_list)
        
        # Save features
        features_path = output_dir / "X.joblib"
        labels_path = output_dir / "y.joblib"
        
        joblib.dump(X, features_path)
        joblib.dump(y, labels_path)
        
        logger.info(f"Saved {len(features_list)} feature vectors to {output_dir}")
        logger.info(f"Feature shape: {X.shape}")
        logger.info(f"Label distribution: {np.bincount(np.unique(y, return_inverse=True)[1])}")
    else:
        logger.warning("No features extracted successfully")

def create_all_features() -> None:
    """
    Create features for all audio directories (Actor_25 and Actor_26).
    """
    ensure_dirs_exist()
    
    # Process Actor_25 and Actor_26 directories
    for actor in ["Actor_25", "Actor_26"]:
        actor_dir = FEATURES_DIR / actor
        if actor_dir.exists():
            logger.info(f"Processing {actor}...")
            process_audio_directory(actor_dir, DATASET_FEATURES_DIR)
        else:
            logger.warning(f"Directory not found: {actor_dir}")

def load_features() -> Tuple[np.ndarray, np.ndarray]:
    """
    Load pre-computed features from disk.
    
    Returns:
        Tuple of (X, y) where X is features and y is labels
        
    Raises:
        FileNotFoundError: If feature files don't exist
    """
    X_path = DATASET_FEATURES_DIR / "X.joblib"
    y_path = DATASET_FEATURES_DIR / "y.joblib"
    
    if not X_path.exists() or not y_path.exists():
        raise FileNotFoundError(
            f"Feature files not found. Expected: {X_path}, {y_path}. "
            "Run create_all_features() first."
        )
    
    X = joblib.load(X_path)
    y = joblib.load(y_path)
    
    logger.info(f"Loaded features: X={X.shape}, y={y.shape}")
    return X, y

if __name__ == "__main__":
    create_all_features()
