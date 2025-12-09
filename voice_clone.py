import streamlit as st
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
from datetime import datetime
from model import generate_speech

st.title("🎤 Live Voice Recording – Voice Cloning")
st.write("Record your voice, enter text, and generate cloned speech.")

# --- Record audio directly from microphone ----
audio_input = st.audio_input("Record a voice message")
if audio_input:
    st.audio(audio_input)

# --- Text to synthesize ---
text = st.text_area("Enter text to speak:")

# --- Language selection ---
language = st.selectbox("Language:", ["English", "French"])
language_map = {"English": "en", "French": "fr"}

# Initialize session_state to store generated file
if "cloned_audio" not in st.session_state:
    st.session_state.cloned_audio = None
if "audio_data" not in st.session_state:
    st.session_state.audio_data = None
if "samplerate" not in st.session_state:
    st.session_state.samplerate = None

# --- Generate button ---
if st.button("Clone Voice & Generate Speech"):
    if audio_input is None:
        st.warning("Please record your voice first.")
    elif not text.strip():
        st.warning("Please enter some text.")
    else:
        # Save recorded audio
        user_voice_path = "temp_recorded_voice.wav"
        with open(user_voice_path, "wb") as f:
            f.write(audio_input.getvalue())

        # Output path
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"output/cloned_{timestamp}.wav"

        # Generate speech
        generate_speech(
            text=text,
            speaker_wav=user_voice_path,
            output_path=output_path,
            language=language_map[language],
        )

        st.success("Cloned speech generated!")
        
        # Save to session_state
        st.session_state.cloned_audio = output_path
        data, samplerate = sf.read(output_path)
        st.session_state.audio_data = data
        st.session_state.samplerate = samplerate

# --- Playback and visualization ---
if st.session_state.cloned_audio:
    st.audio(st.session_state.cloned_audio)

    viz = st.radio("Visualization:", ["Waveform", "Spectrogram"], key="viz_radio")
    fig, ax = plt.subplots(figsize=(10, 3))
    data = st.session_state.audio_data
    samplerate = st.session_state.samplerate

    if viz == "Waveform":
        ax.plot(np.linspace(0, len(data)/samplerate, len(data)), data)
        ax.set_title("Waveform")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")
    else:
        ax.specgram(data, Fs=samplerate, cmap="magma")
        ax.set_title("Spectrogram")
        ax.set_xlabel("Time")
        ax.set_ylabel("Frequency")

    st.pyplot(fig)
