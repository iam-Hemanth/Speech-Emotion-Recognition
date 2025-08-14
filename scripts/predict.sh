#!/bin/bash

# Speech Emotion Recognition - Prediction Script
# Usage: ./scripts/predict.sh [audio_file] or ./scripts/predict.sh -e for examples

set -e

# Activate virtual environment
source .venv/bin/activate

# Function to show usage
show_usage() {
    echo "🎵 Speech Emotion Recognition - Prediction Script"
    echo ""
    echo "Usage:"
    echo "  $0 <audio_file>     # Predict emotion for specific audio file"
    echo "  $0 -e               # Run predictions on all example files"
    echo "  $0 --help           # Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 data/examples/03-01-01-01-01-02-05.wav"
    echo "  $0 -e"
    echo ""
}

# Function to predict single file
predict_file() {
    local audio_file="$1"
    
    if [[ ! -f "$audio_file" ]]; then
        echo "❌ Error: Audio file '$audio_file' not found"
        exit 1
    fi
    
    echo "🎵 Analyzing: $audio_file"
    echo "----------------------------------------"
    
    python -m src.ser.inference "$audio_file"
}

# Function to predict all examples
predict_examples() {
    local examples_dir="data/examples"
    
    if [[ ! -d "$examples_dir" ]]; then
        echo "❌ Error: Examples directory '$examples_dir' not found"
        exit 1
    fi
    
    local example_files=($(find "$examples_dir" -name "*.wav" -type f))
    
    if [[ ${#example_files[@]} -eq 0 ]]; then
        echo "❌ No .wav files found in examples directory"
        exit 1
    fi
    
    echo "🎵 Found ${#example_files[@]} example files"
    echo "========================================"
    
    for file in "${example_files[@]}"; do
        echo ""
        predict_file "$file"
        echo ""
        echo "========================================"
    done
}

# Main script logic
case "${1:-}" in
    -h|--help|"")
        show_usage
        exit 0
        ;;
    -e|--examples)
        predict_examples
        ;;
    *)
        predict_file "$1"
        ;;
esac

