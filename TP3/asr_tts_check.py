import time
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
    wav_path = "TP3/outputs/tts_reply_call_01.wav"
    model_id = "openai/whisper-base"

    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")
    torch_dtype = torch.float16 if use_cuda else torch.float32

    # Load audio
    wav, sr = load_wav_mono_16k(wav_path)

    # Load Whisper
    processor = AutoProcessor.from_pretrained(model_id)
    model = AutoModelForSpeechSeq2Seq.from_pretrained(model_id, torch_dtype=torch_dtype)
    model.to(device).eval()

    # Force English transcription
    forced_decoder_ids = processor.get_decoder_prompt_ids(language="en", task="transcribe")

    # Prepare input
    audio_np = wav.detach().cpu().numpy().astype("float32")
    inputs = processor(audio_np, sampling_rate=sr, return_tensors="pt")
    input_features = inputs["input_features"].to(device, dtype=torch_dtype)

    t0 = time.time()
    with torch.no_grad():
        generated_ids = model.generate(
            input_features,
            forced_decoder_ids=forced_decoder_ids
        )
    t1 = time.time()

    text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()

    print("model_id:", model_id)
    print("device:", "cuda" if use_cuda else "cpu")
    print("elapsed_s:", round(t1 - t0, 2))
    print("text:", text)

if __name__ == "__main__":
    main()