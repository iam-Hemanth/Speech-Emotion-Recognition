from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import streamlit as st
import numpy as np
import soundfile as sf
import altair as alt
import librosa
import matplotlib.pyplot as plt

from ser_model import (
    EMOTIONS,
    load_model_with_fallback,
    predict_path,
)


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


HERO_CSS = """
<style>
/* Full app background */
[data-testid="stAppViewContainer"] {
  background: linear-gradient(135deg, #0f172a 0%, #1d283a 40%, #0b1220 100%);
  color: #e5e7eb;
}
[data-testid="stSidebar"] {
  background: #0b1220;
}
.hero {
  padding: 36px 24px;
  border-radius: 16px;
  background: radial-gradient(800px circle at 20% 20%, rgba(99,102,241,0.25), transparent 40%),
              radial-gradient(800px circle at 80% 0%, rgba(16,185,129,0.20), transparent 35%),
              rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.08);
}
.title {
  font-size: 34px; font-weight: 800; margin: 0 0 6px 0;
}
.subtitle { opacity: 0.85; margin: 0; }
.card {
  padding: 20px; border-radius: 14px;
  background: rgba(17,24,39,0.65);
  border: 1px solid rgba(255,255,255,0.07);
}
.result-emoji { font-size: 72px; line-height: 1; }
.pill {
  display: inline-block; padding: 6px 12px; border-radius: 999px;
  background: rgba(99,102,241,0.18); border: 1px solid rgba(99,102,241,0.35);
}
.muted { opacity: 0.8; }
/* Buttons */
div.stButton > button {
  background: linear-gradient(135deg, #6366f1 0%, #22d3ee 100%);
  color: white; border: none; border-radius: 10px; padding: 10px 18px;
}
div.stButton > button:hover { filter: brightness(1.05); }
</style>
"""


@st.cache_resource
def get_model():
    model_path = Path("Deep Learning") / "SER_model.h5"
    return load_model_with_fallback(model_path)


def show_wave_and_melspec(path: Path) -> None:
    x, sr = librosa.load(str(path), res_type="kaiser_fast")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Waveform")
        fig, ax = plt.subplots(figsize=(5.5, 2.2))
        ax.plot(np.linspace(0, len(x)/sr, num=len(x)), x, color="#22d3ee")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")
        ax.grid(alpha=0.2)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    with col2:
        st.markdown("#### Mel spectrogram")
        S = librosa.feature.melspectrogram(y=x, sr=sr, n_mels=64)
        S_db = librosa.power_to_db(S, ref=np.max)
        fig, ax = plt.subplots(figsize=(5.5, 2.2))
        im = ax.imshow(S_db, aspect='auto', origin='lower', cmap='magma')
        ax.set_xlabel("Frames")
        ax.set_ylabel("Mel bins")
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)


def probs_chart(labels: List[str], probs: np.ndarray):
    data = [{"emotion": l, "prob": float(p)} for l, p in zip(labels, probs)]
    chart = (
        alt.Chart(alt.Data(values=data))
        .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
        .encode(
            x=alt.X("prob:Q", axis=alt.Axis(format=".0%"), title="Probability"),
            y=alt.Y("emotion:N", sort='-x', title=None),
            color=alt.value("#22d3ee"),
            tooltip=["emotion", alt.Tooltip("prob:Q", format=".2%")],
        )
        .properties(height=260)
    )
    st.altair_chart(chart, use_container_width=True)


def show_prediction(result: Dict[str, object]) -> None:
    label = str(result.get("pred_label", "?"))
    emoji = EMOJI_MAP.get(label, "❓")
    conf = float(result.get("confidence", 0.0))
    probs = np.array(result.get("probs", []), dtype=float)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown(f"<div class='result-emoji'>{emoji}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='pill'>{label}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='muted'>Confidence: <b>{conf:.2%}</b></div>", unsafe_allow_html=True)
    with c2:
        if probs.size:
            probs_chart(EMOTIONS, probs)
    st.markdown("</div>", unsafe_allow_html=True)


def main() -> None:
    st.set_page_config(page_title="Speech Emotion Recognition", page_icon="🎙️", layout="wide")
    st.markdown(HERO_CSS, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.header("Controls")
        mode = st.radio("Mode", ["Choose example", "Upload file"], index=0)
        st.caption("Tip: Examples live in the examples/ folder.")

    # Hero section
    st.markdown("""
    <div class="hero">
      <div class="title">🎙️ Speech Emotion Recognition</div>
      <p class="subtitle">Upload or pick an audio sample and get an emoji-powered emotion prediction.
      Powered by a Conv1D model over MFCC features.</p>
    </div>
    """, unsafe_allow_html=True)

    model = get_model()

    examples_dir = Path("examples")
    example_files = sorted([p for p in examples_dir.glob("*.wav")])

    st.markdown("\n")
    area = st.container()
    with area:
        if mode == "Choose example":
            if not example_files:
                st.info("No example .wav files found in the examples/ folder.")
            else:
                names = [p.name for p in example_files]
                choice = st.selectbox("Choose an audio sample", names)
                selected = examples_dir / choice

                st.audio(str(selected))
                show_wave_and_melspec(selected)
                if st.button("✨ Predict from example"):
                    result = predict_path(model, selected)
                    show_prediction(result)

        else:
            uploaded = st.file_uploader("Upload a .wav file", type=["wav"]) 
            if uploaded is not None:
                temp_path = Path("_uploaded_temp.wav")
                with open(temp_path, "wb") as f:
                    f.write(uploaded.getbuffer())
                st.audio(str(temp_path))
                show_wave_and_melspec(temp_path)
                if st.button("✨ Predict from upload"):
                    result = predict_path(model, temp_path)
                    show_prediction(result)


if __name__ == "__main__":
    main()


