import os
import time

import numpy as np
import torch
from transformers import pipeline
import torchaudio

def to_channels_first(audio: np.ndarray) -> np.ndarray:
    """
    Normalize audio to shape [C, T] (channels first).
    Handles common cases returned by HF TTS:
      - [T]
      - [1, T]
      - [T, 1]
      - [T, C]
      - [C, T]
    """
    if audio.ndim == 1:          # [T]
        return audio[None, :]    # [1, T]

    if audio.ndim == 2:
        # If one dimension is 1, it's mono: decide which one is channels
        if audio.shape[0] == 1:          # [1, T]
            return audio
        if audio.shape[1] == 1:          # [T, 1] -> [1, T]
            return audio.T

        # If both dims > 1, infer: most often [T, C] from some libs
        # Assume time is the larger dimension
        if audio.shape[0] >= audio.shape[1]:
            # [T, C] -> [C, T]
            return audio.T
        else:
            # [C, T] already
            return audio

    raise ValueError(f"Unexpected audio shape: {audio.shape}")

def main():
    os.makedirs("TP3/outputs", exist_ok=True)

    text = (
        "Thanks for calling. I am sorry your order arrived damaged. "
        "I can offer a replacement or a refund. "
        "Please confirm your preferred option."
    )

    # Modèle TTS léger (anglais)
    tts_model_id = "facebook/mms-tts-eng"

    device = 0 if torch.cuda.is_available() else -1
    tts = pipeline(
        task="text-to-speech",
        model=tts_model_id,
        device=device
    )

    t0 = time.time()
    out = tts(text)
    t1 = time.time()

    # Convert output audio to numpy float32
    audio = np.asarray(out["audio"], dtype=np.float32)
    sr = int(out["sampling_rate"])
    elapsed_s = t1 - t0

    # Normalize to [C, T]
    audio = to_channels_first(audio)

    # Duration (robust): last axis is time
    audio_dur_s = float(audio.shape[-1] / float(sr))
    rtf = elapsed_s / max(audio_dur_s, 1e-9)

    out_wav = "TP3/outputs/tts_reply_call_01.wav"

    wav_t = torch.from_numpy(audio)  # [C, T]
    torchaudio.save(out_wav, wav_t, sr)

    print("tts_model_id:", tts_model_id)
    print("device:", "cuda" if device == 0 else "cpu")
    print("sampling_rate:", sr)
    print("audio_shape:", tuple(audio.shape))
    print("audio_dur_s:", round(audio_dur_s, 2))
    print("elapsed_s:", round(elapsed_s, 2))
    print("rtf:", round(rtf, 3))
    print("saved:", out_wav)

if __name__ == "__main__":
    main()