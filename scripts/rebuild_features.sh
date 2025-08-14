#!/bin/bash

# Speech Emotion Recognition - Feature Rebuild Script
# This script rebuilds the feature extraction pipeline

set -e

# Activate virtual environment
source .venv/bin/activate

echo "🔧 Speech Emotion Recognition - Feature Rebuild"
echo "=============================================="

# Check if we're in the right directory
if [[ ! -d "src/ser" ]]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

echo "📁 Project root: $(pwd)"
echo "🔍 Checking project structure..."

# Check if required directories exist
if [[ ! -d "data/raw" ]]; then
    echo "❌ Error: data/raw directory not found"
    echo "💡 Please ensure the project structure is correct"
    exit 1
fi

if [[ ! -d "data/processed" ]]; then
    echo "❌ Error: data/processed directory not found"
    echo "💡 Please ensure the project structure is correct"
    exit 1
fi

echo "✅ Project structure looks good"
echo ""

# Check if TESS dataset exists
if [[ -d "data/raw/tess" ]]; then
    echo "📊 Found TESS dataset in data/raw/tess"
    TESS_COUNT=$(find "data/raw/tess" -name "*.wav" | wc -l)
    echo "   - Found $TESS_COUNT .wav files"
else
    echo "⚠️  TESS dataset not found in data/raw/tess"
    echo "   - You may need to download it first"
fi

echo ""

# Run the TESS pipeline
echo "🚀 Running TESS dataset processing..."
python -m src.ser.datasets.tess

echo ""

# Run feature extraction
echo "🚀 Running feature extraction..."
python -m src.ser.features

echo ""
echo "✅ Feature rebuild complete!"
echo ""
echo "📊 Summary:"
echo "   - TESS dataset processed"
echo "   - Features extracted and saved"
echo "   - Ready for predictions"
echo ""
echo "💡 You can now run predictions with:"
echo "   ./scripts/predict.sh -e"
