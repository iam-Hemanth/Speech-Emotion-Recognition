# 🎙️ Speech Emotion Recognition (SER)

A comprehensive Speech Emotion Recognition system using Machine Learning and Deep Learning techniques. This project provides both a web interface and command-line tools for analyzing emotions in speech audio.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- macOS (Apple Silicon recommended for best performance)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Speech-Emotion-Recognition-using-ML-and-DL
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install --upgrade pip setuptools wheel
   pip install -r requirements.txt
   ```

4. **For Apple Silicon Macs (M1/M2)**
   ```bash
   pip install tensorflow-macos tensorflow-metal
   ```

### Running the Application

#### Web Interface (Recommended)
```bash
# Option 1: Use the root-level entry point (recommended)
streamlit run app.py

# Option 2: Run the package directly
streamlit run src/ser/app.py
```
This opens a beautiful web interface where you can:
- Choose from example audio files
- Upload your own WAV files
- View predictions with emojis and confidence scores
- See audio visualizations (waveform and mel spectrogram)

#### Command Line Interface
```bash
# Predict a single file
python -m src.ser.inference data/examples/03-01-01-01-01-02-05.wav

# Predict all example files
python -m src.ser.inference --examples

# Use helper script
./scripts/predict.sh data/examples/03-01-01-01-01-02-05.wav

# Run all examples with helper script
./scripts/predict.sh -e
```

## 📁 Repository Structure

```
.
├── src/
│   └── ser/                    # Main package
│       ├── __init__.py
│       ├── config.py           # Configuration and paths
│       ├── features.py         # Feature extraction
│       ├── model.py            # Model loading and prediction
│       ├── inference.py        # CLI interface
│       ├── datasets/
│       │   └── tess.py         # TESS dataset processing
│       └── app.py              # Web interface
├── scripts/
│   ├── predict.sh              # Quick prediction script
│   ├── rebuild_features.sh     # Feature extraction script
│   └── restore_from_quarantine.py # File restore tool
├── models/
│   └── SER_model.h5            # Trained model
├── data/
│   ├── raw/                    # Raw datasets
│   │   └── tess/               # TESS dataset
│   ├── processed/              # Processed data
│   │   └── dataset_features/   # Feature files
│   └── examples/               # Example audio files
├── notebooks/                  # Jupyter notebooks
├── docs/                       # Documentation
├── assets/                     # Media files
├── .github/                    # GitHub workflows
├── .gitattributes              # Git LFS configuration
├── .gitignore                  # Git ignore rules
├── app.py                      # Main web app entry point
├── requirements.txt            # Dependencies
└── to_be_deleted/              # Quarantine for legacy files
```

## 🎯 Features

### Core Functionality
- **Emotion Recognition**: 8 emotion classes (neutral, calm, happy, sad, angry, fear, disgust, surprised)
- **MFCC Feature Extraction**: Mel-frequency cepstral coefficients for audio analysis
- **Deep Learning Model**: Conv1D neural network architecture
- **Cross-platform**: Works on macOS, Linux, and Windows

### Web Interface
- 🎨 **Beautiful UI**: Modern, responsive design with dark theme
- 📊 **Visualizations**: Waveform and mel spectrogram displays
- 📈 **Probability Charts**: Interactive bar charts showing emotion probabilities
- 🎵 **Audio Player**: Built-in audio playback
- 📁 **File Upload**: Drag-and-drop WAV file upload
- 📱 **Mobile Friendly**: Responsive design for all devices

### Command Line Tools
- **Single File Prediction**: Quick analysis of individual audio files
- **Batch Processing**: Process multiple files at once
- **Example Mode**: Test with included example files
- **Verbose Output**: Detailed logging and debugging

## 🔧 Usage Examples

### Web Interface
1. **Activate virtual environment first:**
   ```bash
   source .venv/bin/activate
   ```
2. **Run the web app:**
   ```bash
   streamlit run app.py
   ```
3. Choose "Choose example" to test with included files
4. Or choose "Upload file" to analyze your own audio
5. Click "Analyze Audio" to see results

**⚠️ Important:** Always activate the virtual environment before running the web app to avoid TensorFlow import errors.

### Command Line
```bash
# Basic prediction
python -m src.ser.inference audio.wav

# Verbose output
python -m src.ser.inference -v audio.wav

# Process all examples
python -m src.ser.inference --examples

# Use helper script
./scripts/predict.sh -e  # Examples
./scripts/predict.sh audio.wav  # Single file
```

### Feature Extraction
```bash
# Rebuild features from audio files
./scripts/rebuild_features.sh

# Or run directly
python -m src.ser.features
```

## 🧠 Model Architecture

The system uses a Conv1D neural network:
- **Input**: 40 MFCC features
- **Architecture**: 3 Conv1D layers with dropout and max pooling
- **Output**: 8 emotion classes with softmax activation
- **Training**: Adam optimizer with categorical crossentropy loss

## 📊 Supported Emotions

| Emotion | Emoji | Description |
|---------|-------|-------------|
| Neutral | 😐 | Calm, unemotional speech |
| Calm | 😌 | Relaxed, peaceful speech |
| Happy | 😊 | Joyful, positive speech |
| Sad | 😢 | Melancholic, sorrowful speech |
| Angry | 😠 | Hostile, aggressive speech |
| Fear | 😨 | Anxious, scared speech |
| Disgust | 🤢 | Repulsed, contemptuous speech |
| Surprised | 😮 | Astonished, shocked speech |

## 🔍 Troubleshooting

### Safety Net
If something breaks after cleanup, you can restore files from quarantine:
```bash
# Show what would be restored (dry run)
python scripts/restore_from_quarantine.py --dry-run

# Restore all files from quarantine
python scripts/restore_from_quarantine.py
```

### Common Issues

**Model Loading Error**
```bash
# Ensure model file exists
ls models/SER_model.h5
```

**Audio File Issues**
- Ensure files are in WAV format
- Check file permissions
- Verify audio is not corrupted

**Import Errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**macOS TensorFlow Issues**
```bash
# For Apple Silicon
pip install tensorflow-macos tensorflow-metal

# For Intel Macs
pip install tensorflow
```

### Environment Setup
```bash
# Check Python version
python --version  # Should be 3.8+

# Verify virtual environment
which python  # Should point to .venv/bin/python

# Test imports
python -c "import tensorflow, librosa, streamlit; print('All good!')"
```

## 📈 Performance

- **Accuracy**: ~85% on test set
- **Inference Time**: ~100ms per audio file
- **Memory Usage**: ~200MB for model loading
- **Supported Audio**: 16kHz, mono WAV files

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **RAVDESS Dataset**: Ryerson Audio-Visual Database of Emotional Speech and Song
- **TESS Dataset**: Toronto Emotional Speech Set
- **Librosa**: Audio and music signal processing library
- **Streamlit**: Web application framework
- **TensorFlow**: Deep learning framework

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the project documentation
3. Open an issue on GitHub

---

**Made with ❤️ for Speech Emotion Recognition**
