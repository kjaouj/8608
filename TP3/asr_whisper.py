import os
import json
import time
from typing import Dict, Any, List

import torch
import torchaudio
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq

def load_wav_mono_16k(path: str):
    wav, sr = torchaudio.load(path)          # [C, T]
    wav = wav.mean(dim=0, keepdim=True)      # mono [1, T]
    if sr != 16000:
        wav = torchaudio.functional.resample(wav, sr, 16000)
        sr = 16000
    return wav.squeeze(0), sr                # [T], sr

def main():
    audio_path = "TP3/data/call_01.wav"
    vad_path = "TP3/outputs/vad_segments_call_01.json"
    out_path = "TP3/outputs/asr_call_01.json"
    os.makedirs("TP3/outputs", exist_ok=True)

    wav, sr = load_wav_mono_16k(audio_path)
    audio_duration_s = wav.numel() / sr

    with open(vad_path, "r", encoding="utf-8") as f:
        vad_payload = json.load(f)
    segments = vad_payload["segments"]   # list of {start_s, end_s}

    # Whisper model on HF
    model_id = "openai/whisper-base"

    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")
    torch_dtype = torch.float16 if use_cuda else torch.float32

    processor = AutoProcessor.from_pretrained(model_id)
    model = AutoModelForSpeechSeq2Seq.from_pretrained(model_id, torch_dtype=torch_dtype)
    model.to(device).eval()

    # Force English decoding prompt
    forced_decoder_ids = processor.get_decoder_prompt_ids(language="en", task="transcribe")

    t0 = time.time()
    results: List[Dict[str, Any]] = []

    for i, seg in enumerate(segments):
        start_s = float(seg["start_s"])
        end_s = float(seg["end_s"])

        start = int(start_s * sr)
        end = int(end_s * sr)
        seg_wav = wav[start:end]

        # Processor expects float32 array
        audio_np = seg_wav.detach().cpu().numpy().astype("float32")

        inputs = processor(
            audio_np,
            sampling_rate=sr,
            return_tensors="pt"
        )

        input_features = inputs["input_features"].to(device, dtype=torch_dtype)

        with torch.no_grad():
            generated_ids = model.generate(
                input_features,
                forced_decoder_ids=forced_decoder_ids
            )

        text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()

        results.append({
            "segment_id": i,
            "start_s": start_s,
            "end_s": end_s,
            "text": text
        })

    t1 = time.time()
    elapsed_s = t1 - t0
    rtf = elapsed_s / max(audio_duration_s, 1e-9)

    full_text = " ".join([r["text"] for r in results]).strip()

    payload = {
        "audio_path": audio_path,
        "model_id": model_id,
        "device": "cuda" if use_cuda else "cpu",
        "audio_duration_s": audio_duration_s,
        "elapsed_s": elapsed_s,
        "rtf": rtf,
        "segments": results,
        "full_text": full_text
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print("model_id:", model_id)
    print("device:", payload["device"])
    print("audio_duration_s:", round(audio_duration_s, 2))
    print("elapsed_s:", round(elapsed_s, 2))
    print("rtf:", round(rtf, 3))
    print("saved:", out_path)

if __name__ == "__main__":
    main()