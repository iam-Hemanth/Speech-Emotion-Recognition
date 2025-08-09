from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import numpy as np
import librosa
from tensorflow import keras
from tensorflow.keras import layers, models


EMOTIONS: List[str] = [
    "neutral",
    "calm",
    "happy",
    "sad",
    "angry",
    "fear",
    "disgust",
    "surprised",
]


def extract_features(audio_path: Path) -> np.ndarray:
    x, sr = librosa.load(str(audio_path), res_type="kaiser_fast")
    mfcc = librosa.feature.mfcc(y=x, sr=sr, n_mfcc=40)
    mfcc_mean = np.mean(mfcc.T, axis=0)  # shape (40,)
    return mfcc_mean.astype(np.float32)


def build_fallback_model() -> keras.Model:
    model = models.Sequential(name="ser_cnn")
    model.add(layers.Conv1D(64, 5, padding="same", input_shape=(40, 1), name="conv1d_1"))
    model.add(layers.Activation("relu", name="activation_1"))
    model.add(layers.Dropout(0.1, name="dropout_1"))
    model.add(layers.MaxPooling1D(pool_size=4, name="max_pooling1d_1"))
    model.add(layers.Conv1D(128, 5, padding="same", name="conv1d_2"))
    model.add(layers.Activation("relu", name="activation_2"))
    model.add(layers.Dropout(0.1, name="dropout_2"))
    model.add(layers.MaxPooling1D(pool_size=4, name="max_pooling1d_2"))
    model.add(layers.Conv1D(256, 5, padding="same", name="conv1d_3"))
    model.add(layers.Activation("relu", name="activation_3"))
    model.add(layers.Dropout(0.1, name="dropout_3"))
    model.add(layers.Flatten(name="flatten_1"))
    model.add(layers.Dense(8, name="dense_1"))
    model.add(layers.Activation("softmax", name="activation_4"))
    return model


def load_model_with_fallback(model_path: Path) -> keras.Model:
    try:
        return keras.models.load_model(str(model_path))
    except Exception:
        model = build_fallback_model()
        model.load_weights(str(model_path), by_name=True, skip_mismatch=True)
        return model


def adapt_input_shape(model: keras.Model, features: np.ndarray) -> np.ndarray:
    x = features
    if x.ndim == 1:
        x = x[None, :]  # (1, 40)
    inp_shape = model.input_shape
    if isinstance(inp_shape, list):
        inp_shape = inp_shape[0]
    if len(inp_shape) == 3 and x.ndim == 2:
        x = x[:, :, None]
    return x


def predict_path(model: keras.Model, wav_path: Path) -> Dict[str, object]:
    feats = extract_features(wav_path)
    x = adapt_input_shape(model, feats)
    probs = model.predict(x, verbose=0)[0]
    idx = int(np.argmax(probs))
    return {
        "file": str(wav_path),
        "pred_index": idx,
        "pred_label": EMOTIONS[idx] if 0 <= idx < len(EMOTIONS) else str(idx),
        "confidence": float(probs[idx]),
        "probs": probs.tolist(),
    }


