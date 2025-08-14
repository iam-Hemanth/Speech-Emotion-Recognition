"""
Command-line inference interface for Speech Emotion Recognition.
Provides a simple CLI for running predictions on audio files.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional
import logging

from .model import predict_path
from .config import get_model_path, EXAMPLES_DIR

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def predict_file(audio_path: Path, model_path: Optional[Path] = None) -> None:
    """
    Predict emotion for a single audio file and print results.
    
    Args:
        audio_path: Path to audio file
        model_path: Path to model file (optional)
    """
    try:
        result = predict_path(audio_path, model_path)
        
        print(f"\n🎵 File: {result['file']}")
        print(f"😊 Emotion: {result['pred_label']}")
        print(f"📊 Confidence: {result['confidence']:.2%}")
        print(f"🔢 Prediction Index: {result['pred_index']}")
        
        # Show all probabilities
        print("\n📈 All Probabilities:")
        for i, (emotion, prob) in enumerate(zip(result.get('emotions', []), result['probs'])):
            print(f"  {emotion}: {prob:.2%}")
            
    except Exception as e:
        logger.error(f"Error predicting {audio_path}: {e}")
        print(f"❌ Error: {e}")
        sys.exit(1)

def predict_directory(directory: Path, model_path: Optional[Path] = None) -> None:
    """
    Predict emotions for all audio files in a directory.
    
    Args:
        directory: Directory containing audio files
        model_path: Path to model file (optional)
    """
    if not directory.exists():
        print(f"❌ Directory not found: {directory}")
        sys.exit(1)
    
    audio_files = list(directory.glob("*.wav"))
    if not audio_files:
        print(f"❌ No .wav files found in {directory}")
        sys.exit(1)
    
    print(f"🎵 Processing {len(audio_files)} audio files...")
    
    results = []
    for audio_file in audio_files:
        try:
            result = predict_path(audio_file, model_path)
            results.append(result)
            
            print(f"✅ {audio_file.name}: {result['pred_label']} ({result['confidence']:.2%})")
            
        except Exception as e:
            logger.error(f"Error processing {audio_file}: {e}")
            print(f"❌ {audio_file.name}: Error - {e}")
    
    # Summary
    if results:
        print(f"\n📊 Summary: Processed {len(results)} files successfully")
        
        # Count emotions
        emotion_counts = {}
        for result in results:
            emotion = result['pred_label']
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        print("🎭 Emotion Distribution:")
        for emotion, count in sorted(emotion_counts.items()):
            percentage = (count / len(results)) * 100
            print(f"  {emotion}: {count} ({percentage:.1f}%)")

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Speech Emotion Recognition CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s audio.wav                    # Predict single file
  %(prog)s -d examples/                 # Predict all files in directory
  %(prog)s -m models/SER_model.h5 audio.wav  # Use specific model
        """
    )
    
    parser.add_argument(
        "input",
        nargs="?",
        help="Audio file or directory to process"
    )
    
    parser.add_argument(
        "-d", "--directory",
        action="store_true",
        help="Treat input as directory and process all .wav files"
    )
    
    parser.add_argument(
        "-m", "--model",
        type=Path,
        help="Path to model file (default: auto-detect)"
    )
    
    parser.add_argument(
        "--examples",
        action="store_true",
        help="Run predictions on example files"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Validate model path
    model_path = args.model
    if model_path and not model_path.exists():
        print(f"❌ Model file not found: {model_path}")
        sys.exit(1)
    
    try:
        # Handle examples mode
        if args.examples:
            if EXAMPLES_DIR.exists():
                predict_directory(EXAMPLES_DIR, model_path)
            else:
                print(f"❌ Examples directory not found: {EXAMPLES_DIR}")
                sys.exit(1)
            return
        
        # Handle input argument
        if not args.input:
            print("❌ No input specified. Use --help for usage information.")
            sys.exit(1)
        
        input_path = Path(args.input)
        
        if not input_path.exists():
            print(f"❌ Input not found: {input_path}")
            sys.exit(1)
        
        # Process based on type
        if args.directory or input_path.is_dir():
            predict_directory(input_path, model_path)
        else:
            predict_file(input_path, model_path)
            
    except KeyboardInterrupt:
        print("\n⏹️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
