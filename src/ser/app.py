"""
Streamlit web application for Speech Emotion Recognition.
Provides an interactive interface for testing the SER model with futuristic enterprise dashboard UI.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Any
import tempfile
import logging
import base64

import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import librosa
import matplotlib.pyplot as plt

# Handle both package and direct execution
try:
    from .model import predict_path, load_model_with_fallback
    from .config import EXAMPLES_DIR, get_model_path
except ImportError:
    # Fallback for direct execution
    from model import predict_path, load_model_with_fallback
    from config import EXAMPLES_DIR, get_model_path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Emotion to emoji mapping
EMOJI_MAP = {
    "neutral": "😐",
    "calm": "😌",
    "happy": "😊",
    "sad": "😢",
    "angry": "😠",
    "fear": "😨",
    "disgust": "🤢",
    "surprised": "😮",
}

# Emotion color mapping for dynamic theming
EMOTION_COLORS = {
    "neutral": "#48CAE4",
    "calm": "#00B4D8",
    "happy": "#00D4AA",
    "sad": "#0096C7",
    "angry": "#FF6B6B",
    "fear": "#6B5B95",
    "disgust": "#8B4513",
    "surprised": "#FFD700",
}

def load_css():
    """Load custom CSS for futuristic enterprise dashboard theme."""
    css_file = Path(__file__).parent / "assets" / "style.css"
    
    if css_file.exists():
        with open(css_file, 'r') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    else:
        # Fallback CSS if file doesn't exist
        st.markdown("""
        <style>
        .main .block-container {
            background: linear-gradient(135deg, #03045E 0%, #023E8A 25%, #0077B6 50%, #0096C7 75%, #00B4D8 100%);
            min-height: 100vh;
            padding: 0;
            max-width: 100%;
        }
        </style>
        """, unsafe_allow_html=True)

def get_logo_svg():
    """Get the custom logo SVG as base64 for embedding."""
    logo_file = Path(__file__).parent / "assets" / "logo.svg"
    
    if logo_file.exists():
        with open(logo_file, 'r') as f:
            svg_content = f.read()
            # Convert SVG to base64 for embedding
            svg_base64 = base64.b64encode(svg_content.encode()).decode()
            return f"data:image/svg+xml;base64,{svg_base64}"
    
    # Fallback to emoji if logo not found
    return "🎙️"

@st.cache_resource
def get_model():
    """Load and cache the model."""
    try:
        model_path = get_model_path()
        return load_model_with_fallback(model_path)
    except Exception as e:
        st.error(f"Failed to load model: {e}")
        return None

def show_wave_and_melspec(audio_path: Path) -> None:
    """Display waveform and mel spectrogram visualizations."""
    try:
        x, sr = librosa.load(str(audio_path), res_type="kaiser_fast")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Waveform")
            fig, ax = plt.subplots(figsize=(5.5, 2.2))
            ax.plot(np.linspace(0, len(x)/sr, num=len(x)), x, color="#48CAE4", linewidth=0.8)
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Amplitude")
            ax.grid(alpha=0.2)
            ax.set_facecolor('none')
            fig.patch.set_facecolor('none')
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
            
        with col2:
            st.markdown("#### 🎵 Mel Spectrogram")
            S = librosa.feature.melspectrogram(y=x, sr=sr, n_mels=64)
            S_db = librosa.power_to_db(S, ref=np.max)
            fig, ax = plt.subplots(figsize=(5.5, 2.2))
            im = ax.imshow(S_db, aspect='auto', origin='lower', cmap='viridis')
            ax.set_xlabel("Frames")
            ax.set_ylabel("Mel bins")
            fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
            ax.set_facecolor('none')
            fig.patch.set_facecolor('none')
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
            
    except Exception as e:
        st.error(f"Error creating visualizations: {e}")

def create_probability_chart(emotions: List[str], probabilities: List[float]) -> alt.Chart:
    """Create an Altair chart for emotion probabilities with Ocean Blue Serenity theme."""
    try:
        # Create DataFrame for Altair
        df = pd.DataFrame({
            'emotion': emotions,
            'probability': probabilities
        })
        
        # Create the chart with custom colors
        chart = alt.Chart(df).mark_bar(
            cornerRadiusTopLeft=8, 
            cornerRadiusTopRight=8,
            color=alt.Color('emotion:N', 
                          scale=alt.Scale(range=['#48CAE4', '#00B4D8', '#0096C7', '#0077B6', '#023E8A', '#03045E', '#90E0EF', '#CAF0F8']),
                          legend=None)
        ).encode(
            x=alt.X('probability:Q', 
                   axis=alt.Axis(format='.0%', 
                                titleColor='#CAF0F8',
                                labelColor='#90E0EF',
                                titleFontSize=14,
                                labelFontSize=12), 
                   title='Probability',
                   scale=alt.Scale(domain=[0, 1])),
            y=alt.Y('emotion:N', 
                   sort='-x', 
                   title=None,
                   axis=alt.Axis(labelColor='#CAF0F8', labelFontSize=12)),
            tooltip=[
                alt.Tooltip('emotion:N', title='Emotion'),
                alt.Tooltip('probability:Q', format='.2%', title='Probability')
            ]
        ).properties(
            height=300,
            title=alt.TitleParams(
                text='Emotion Probabilities',
                color='#CAF0F8',
                fontSize=18,
                fontWeight='bold'
            )
        ).configure_view(
            strokeWidth=0
        ).configure_axis(
            gridColor='rgba(72, 202, 228, 0.2)',
            gridOpacity=0.3
        )
        
        return chart
        
    except Exception as e:
        logger.error(f"Error creating probability chart: {e}")
        return None

def display_results(result: Dict[str, Any], audio_path: Path) -> None:
    """Display prediction results in a futuristic enterprise dashboard format."""
    try:
        label = str(result.get("pred_label", "?"))
        emoji = EMOJI_MAP.get(label, "❓")
        confidence = float(result.get("confidence", 0.0))
        probabilities = result.get("probs", [])
        emotion_color = EMOTION_COLORS.get(label, "#48CAE4")
        
        # Main result card with glassmorphism
        st.markdown(f"""
        <div class="prediction-card" style="border-color: {emotion_color};">
            <div class="emotion-emoji">{emoji}</div>
            <div class="emotion-text">{label.upper()}</div>
            <div class="confidence-score">Confidence: {confidence:.2%}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Probability chart
        if probabilities and len(probabilities) == len(EMOJI_MAP):
            st.markdown('<div class="probability-chart">', unsafe_allow_html=True)
            st.markdown("#### 📊 Emotion Probabilities")
            chart = create_probability_chart(list(EMOJI_MAP.keys()), probabilities)
            if chart:
                st.altair_chart(chart, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # File info
        st.markdown(f"**📁 File:** `{audio_path.name}`")
        
    except Exception as e:
        st.error(f"Error displaying results: {e}")

def main() -> None:
    """Main Streamlit application with futuristic enterprise dashboard UI."""
    st.set_page_config(
        page_title="Speech Emotion Recognition - Enterprise Dashboard", 
        page_icon="🎙️", 
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Load custom CSS
    load_css()
    
    # Custom header with logo and title
    logo_svg = get_logo_svg()
    
    st.markdown(f"""
    <header>
        <div class="logo-container">
            <img src="{logo_svg}" class="logo" alt="SER Logo">
            <div>
                <h1 class="hero-title">Speech Emotion Recognition</h1>
                <p class="hero-subtitle">AI-Powered Audio Emotion Analysis • Enterprise Dashboard</p>
            </div>
        </div>
    </header>
    """, unsafe_allow_html=True)
    
    # Load model
    model = get_model()
    if model is None:
        st.error("❌ Model failed to load. Please check the model file.")
        return
    
    # Sidebar controls with glassmorphism
    with st.sidebar:
        st.markdown('<div class="control-card">', unsafe_allow_html=True)
        st.markdown("### 🎛️ Analysis Mode")
        mode = st.radio(
            "Choose mode:", 
            ["Choose example", "Upload file"], 
            index=0,
            help="Select from example files or upload your own audio"
        )
        st.caption("💡 Tip: Examples are in the data/examples/ folder.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="control-card">', unsafe_allow_html=True)
        st.markdown("### 🔧 Model Information")
        st.markdown(f"✅ **Status:** Loaded successfully")
        st.markdown(f"📊 **Input shape:** {model.input_shape}")
        st.markdown(f"🎯 **Output classes:** {model.output_shape[-1]}")
        st.markdown(f"🚀 **Framework:** TensorFlow {model.__class__.__module__}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="control-card">', unsafe_allow_html=True)
        st.markdown("### 📚 Supported Emotions")
        for emotion, emoji in EMOJI_MAP.items():
            st.markdown(f"{emoji} **{emotion.title()}**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content area
    st.markdown("\n")
    
    if mode == "Choose example":
        # Example selection mode
        if not EXAMPLES_DIR.exists():
            st.warning(f"Examples directory not found: {EXAMPLES_DIR}")
            st.info("Please add some .wav files to the examples directory.")
        else:
            example_files = sorted([p for p in EXAMPLES_DIR.glob("*.wav")])
            
            if not example_files:
                st.info("No example .wav files found in the examples directory.")
            else:
                # File selection
                file_names = [p.name for p in example_files]
                selected_name = st.selectbox(
                    "Choose an audio sample:", 
                    file_names,
                    help="Select an audio file to analyze"
                )
                
                if selected_name:
                    selected_file = EXAMPLES_DIR / selected_name
                    
                    # Audio player
                    st.markdown('<div class="audio-viz">', unsafe_allow_html=True)
                    st.markdown("#### 🎵 Audio Preview")
                    st.audio(str(selected_file))
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Visualizations
                    st.markdown('<div class="audio-viz">', unsafe_allow_html=True)
                    st.markdown("#### 📊 Audio Analysis")
                    show_wave_and_melspec(selected_file)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Prediction button
                    if st.button("🚀 Analyze Audio", type="primary"):
                        with st.spinner("🔍 Analyzing audio with AI..."):
                            try:
                                result = predict_path(selected_file)
                                display_results(result, selected_file)
                            except Exception as e:
                                st.error(f"❌ Prediction failed: {e}")
    
    else:
        # File upload mode
        st.markdown('<div class="control-card">', unsafe_allow_html=True)
        st.markdown("#### 📁 Upload Audio File")
        uploaded_file = st.file_uploader(
            "Upload a .wav file", 
            type=["wav"],
            help="Upload an audio file in WAV format for emotion analysis"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        if uploaded_file is not None:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(uploaded_file.getbuffer())
                temp_path = Path(tmp_file.name)
            
            try:
                # Audio player
                st.markdown('<div class="audio-viz">', unsafe_allow_html=True)
                st.markdown("#### 🎵 Audio Preview")
                st.audio(uploaded_file)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Visualizations
                st.markdown('<div class="audio-viz">', unsafe_allow_html=True)
                st.markdown("#### 📊 Audio Analysis")
                show_wave_and_melspec(temp_path)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Prediction button
                if st.button("🚀 Analyze Audio", type="primary"):
                    with st.spinner("🔍 Analyzing audio with AI..."):
                        try:
                            result = predict_path(temp_path)
                            display_results(result, temp_path)
                        except Exception as e:
                            st.error(f"❌ Prediction failed: {e}")
                        finally:
                            # Clean up temp file
                            temp_path.unlink(missing_ok=True)
                            
            except Exception as e:
                st.error(f"❌ Error processing uploaded file: {e}")
                temp_path.unlink(missing_ok=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>🚀 Speech Emotion Recognition • Powered by AI & Deep Learning</p>
        <p>Built with ❤️ using Streamlit, TensorFlow, and Librosa</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
