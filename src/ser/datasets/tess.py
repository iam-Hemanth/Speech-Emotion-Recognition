"""
TESS dataset processing utilities.
Handles the Toronto Emotional Speech Set (TESS) dataset organization and processing.
"""

import shutil
from pathlib import Path
from typing import List, Dict, Optional
import logging

from ..config import TESS_ORIGINAL_DIR, FEATURES_DIR, ensure_dirs_exist

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Emotion mapping for TESS dataset
TESS_EMOTION_MAP = {
    "angry": "angry",
    "disgust": "disgust", 
    "fear": "fear",
    "happy": "happy",
    "neutral": "neutral",
    "ps": "surprised",  # TESS uses 'ps' for 'pleasant surprise'
    "sad": "sad"
}

def process_tess_dataset(source_dir: Optional[Path] = None) -> None:
    """
    Process the TESS dataset and organize files into Actor_25 and Actor_26 folders.
    
    Args:
        source_dir: Source directory containing TESS files (optional)
    """
    if source_dir is None:
        source_dir = TESS_ORIGINAL_DIR
    
    if not source_dir.exists():
        logger.error(f"TESS source directory not found: {source_dir}")
        raise FileNotFoundError(f"TESS dataset not found at {source_dir}")
    
    ensure_dirs_exist()
    
    # Create Actor directories
    actor_25_dir = FEATURES_DIR / "Actor_25"
    actor_26_dir = FEATURES_DIR / "Actor_26"
    
    actor_25_dir.mkdir(parents=True, exist_ok=True)
    actor_26_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Processing TESS dataset from {source_dir}")
    
    # Find all audio files
    audio_files = list(source_dir.rglob("*.wav"))
    if not audio_files:
        logger.warning(f"No .wav files found in {source_dir}")
        return
    
    logger.info(f"Found {len(audio_files)} audio files")
    
    processed_count = 0
    skipped_count = 0
    
    for audio_file in audio_files:
        try:
            # Parse filename to extract information
            # Expected format: YAF_*_emotion.wav
            filename = audio_file.stem
            parts = filename.split('_')
            
            if len(parts) < 3:
                logger.warning(f"Skipping file with unexpected format: {filename}")
                skipped_count += 1
                continue
            
            # Extract emotion from filename
            emotion_part = parts[-1].lower()
            emotion = TESS_EMOTION_MAP.get(emotion_part)
            
            if emotion is None:
                logger.warning(f"Unknown emotion '{emotion_part}' in {filename}")
                skipped_count += 1
                continue
            
            # Determine actor (25 or 26) based on file characteristics
            # This is a simplified approach - you might need to adjust based on actual TESS structure
            actor_num = 25 if "YAF" in filename else 26
            
            # Create new filename in RAVDESS format
            # Format: modality-vocal_channel-emotion-intensity-statement-repetition-actor.wav
            new_filename = f"02-01-{get_emotion_code(emotion)}-01-01-01-{actor_num:02d}.wav"
            
            # Determine target directory
            target_dir = actor_25_dir if actor_num == 25 else actor_26_dir
            target_path = target_dir / new_filename
            
            # Copy file
            shutil.copy2(audio_file, target_path)
            processed_count += 1
            
            logger.debug(f"Processed {audio_file.name} -> {new_filename}")
            
        except Exception as e:
            logger.error(f"Error processing {audio_file}: {e}")
            skipped_count += 1
            continue
    
    logger.info(f"TESS processing complete:")
    logger.info(f"  ✅ Processed: {processed_count} files")
    logger.info(f"  ⚠️  Skipped: {skipped_count} files")
    logger.info(f"  📁 Actor_25: {len(list(actor_25_dir.glob('*.wav')))} files")
    logger.info(f"  📁 Actor_26: {len(list(actor_26_dir.glob('*.wav')))} files")

def get_emotion_code(emotion: str) -> int:
    """
    Get emotion code for RAVDESS format.
    
    Args:
        emotion: Emotion label
        
    Returns:
        Emotion code (1-8)
    """
    emotion_codes = {
        "neutral": 1,
        "calm": 2,
        "happy": 3,
        "sad": 4,
        "angry": 5,
        "fear": 6,
        "disgust": 7,
        "surprised": 8
    }
    
    return emotion_codes.get(emotion, 1)

def validate_tess_structure(source_dir: Optional[Path] = None) -> Dict[str, bool]:
    """
    Validate TESS dataset structure.
    
    Args:
        source_dir: Source directory to validate
        
    Returns:
        Dictionary with validation results
    """
    if source_dir is None:
        source_dir = TESS_ORIGINAL_DIR
    
    results = {
        "directory_exists": source_dir.exists(),
        "has_audio_files": False,
        "has_expected_structure": False
    }
    
    if not results["directory_exists"]:
        return results
    
    # Check for audio files
    audio_files = list(source_dir.rglob("*.wav"))
    results["has_audio_files"] = len(audio_files) > 0
    
    # Check structure (simplified)
    if audio_files:
        # Check if files follow expected naming pattern
        valid_files = 0
        for audio_file in audio_files:
            filename = audio_file.stem
            if '_' in filename and any(emotion in filename.lower() for emotion in TESS_EMOTION_MAP.keys()):
                valid_files += 1
        
        results["has_expected_structure"] = valid_files > 0
    
    return results

def cleanup_tess_processing() -> None:
    """
    Clean up temporary files from TESS processing.
    """
    # This function can be used to clean up any temporary files
    # created during TESS processing if needed
    logger.info("TESS processing cleanup complete")

if __name__ == "__main__":
    process_tess_dataset()
