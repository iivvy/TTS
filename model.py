import torch
import soundfile as sf
from TTS.api import TTS


device = "cuda" if torch.cuda.is_available() else "cpu"
tts_model = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2").to(device)



def generate_speech(text, speaker_wav, output_path="output.wav",language='en'):
    audio = tts_model.tts(text=text, speaker_wav=speaker_wav,language=language)
    sf.write(output_path, audio, samplerate=tts_model.synthesizer.output_sample_rate)
    return output_path