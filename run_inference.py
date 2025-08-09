from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

import numpy as np
import librosa
from tensorflow import keras
from tensorflow.keras import layers, models
from ser_model import load_model_with_fallback, predict_path


EMOTIONS: List[str] = [
    "neutral",  # 0
    "calm",     # 1
    "happy",    # 2
    "sad",      # 3
    "angry",    # 4
    "fear",     # 5
    "disgust",  # 6
    "surprised" # 7 (pleasant surprise)
]


def extract_features(audio_path: Path) -> np.ndarray:
    x, sr = librosa.load(str(audio_path), res_type="kaiser_fast")
    mfcc = librosa.feature.mfcc(y=x, sr=sr, n_mfcc=40)
    mfcc_mean = np.mean(mfcc.T, axis=0)  # shape (40,)
    return mfcc_mean.astype(np.float32)


def adapt_input_shape(model: keras.Model, features: np.ndarray) -> np.ndarray:
    # Expected shapes examples: (None, 40) or (None, 40, 1)
    inp_shape = model.input_shape
    x = features
    if x.ndim == 1:
        x = x[None, :]  # (1, 40)
    # If model expects a channel dimension
    if isinstance(inp_shape, list):
        inp_shape = inp_shape[0]
    if len(inp_shape) == 3 and x.ndim == 2:
        x = x[:, :, None]  # (1, 40, 1)
    return x


def build_fallback_model() -> keras.Model:
    # Recreate the architecture used in the notebook, with explicit layer names
    model = models.Sequential(name="ser_cnn")
    model.add(layers.Conv1D(64, 5, padding='same', input_shape=(40,1), name='conv1d_1'))
    model.add(layers.Activation('relu', name='activation_1'))
    model.add(layers.Dropout(0.1, name='dropout_1'))
    model.add(layers.MaxPooling1D(pool_size=4, name='max_pooling1d_1'))
    model.add(layers.Conv1D(128, 5, padding='same', name='conv1d_2'))
    model.add(layers.Activation('relu', name='activation_2'))
    model.add(layers.Dropout(0.1, name='dropout_2'))
    model.add(layers.MaxPooling1D(pool_size=4, name='max_pooling1d_2'))
    model.add(layers.Conv1D(256, 5, padding='same', name='conv1d_3'))
    model.add(layers.Activation('relu', name='activation_3'))
    model.add(layers.Dropout(0.1, name='dropout_3'))
    model.add(layers.Flatten(name='flatten_1'))
    model.add(layers.Dense(8, name='dense_1'))
    model.add(layers.Activation('softmax', name='activation_4'))
    return model


def load_model_with_fallback(model_path: Path) -> keras.Model:
    print(f"Loading model: {model_path}")
    try:
        model = keras.models.load_model(str(model_path))
        print("Model loaded.")
        return model
    except Exception as e:
        print(f"Direct load failed: {e}\nRebuilding architecture and loading weights by name...")
        model = build_fallback_model()
        model.load_weights(str(model_path), by_name=True, skip_mismatch=True)
        print("Weights loaded into fallback model.")
        return model


def predict(model_path: Path, wav_path: Path) -> None:
    model = load_model_with_fallback(model_path)
    result = predict_path(model, wav_path)
    result["confidence"] = round(result["confidence"], 4)
    print(result)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=str(Path("Deep Learning") / "SER_model.h5"))
    parser.add_argument("--file", default=str(Path("examples") / "10-16-07-29-82-30-63.wav"))
    args = parser.parse_args()

    model_path = Path(args.model).resolve()
    wav_path = Path(args.file).resolve()

    if not model_path.exists():
        raise FileNotFoundError(f"Model not found at {model_path}")
    if not wav_path.exists():
        raise FileNotFoundError(f"Audio file not found at {wav_path}")

    predict(model_path, wav_path)


if __name__ == "__main__":
    main()


