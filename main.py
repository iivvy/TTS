# app.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
from datetime import datetime
from model import tts_model, generate_speech

# ------------------ Title & Description ------------------
st.markdown("<h1 style='text-align: center; color: #4B0082;'>🎤 Custom TTS Demo</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>Type your text, select the language and the voice, then generate high-quality speech with visual feedback.</p>", unsafe_allow_html=True)

# ------------------ Dark / Light Mode ------------------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

st.session_state.dark_mode = st.checkbox("Dark mode", value=st.session_state.dark_mode)

if st.session_state.dark_mode:
    st.markdown(
        "<style>body{background-color:#1e1e1e; color:white;} .stButton>button{background-color:#4B0082;color:white;}</style>",
        unsafe_allow_html=True
    )
else:
    st.markdown(
        "<style>body{background-color:white; color:black;} .stButton>button{background-color:#4B0082;color:white;}</style>",
        unsafe_allow_html=True
    )

# ------------------ Language Selection ------------------
language_option = st.selectbox("Choose language:", ["English", "French"])
language_map = {"English": "en", "French": "fr"}

# ------------------ Voice Selection ------------------
if "voice_choice" not in st.session_state:
    st.session_state.voice_choice = None

st.markdown("### Choose a voice:")
col1, col2 = st.columns(2)

# Mapping voice names to audio files
voice_paths = {
    "Rekrouk Abdelmoumen": "sounds/voice1.wav",
    "Mehadji Raho Mohamed Hamza": "sounds/voice2.wav"
}

# Function to create clickable rectangle
def clickable_rectangle(name, color="#4B0082"):
    if st.button(name):
        st.session_state.voice_choice = name

# Circle + rectangle layout
with col1:
    st.markdown(
        "<div style='width:120px; height:120px; border-radius:75px; background-color:#4B0082; margin:auto;'></div>",
        unsafe_allow_html=True
    )
    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
    # Highlight selected rectangle
    rect_color = "#FFD700" if st.session_state.voice_choice == "Rekrouk Abdelmoumen" else "#4B0082"
    # st.markdown(
    #     f"<div style='width:140px; height:40px; background-color:{rect_color}; color:white; text-align:center; line-height:40px; margin:auto; border-radius:5px;'>{'Rekrouk Abdelmoumen'}</div>",
    #     unsafe_allow_html=True
    # )
    clickable_rectangle("Rekrouk Abdelmoumen")

with col2:
    st.markdown(
        "<div style='width:120px; height:120px; border-radius:75px; background-color:#FF0000; margin:auto;'></div>",
        unsafe_allow_html=True
    )
    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
    rect_color = "#FFD700" if st.session_state.voice_choice == "Mehadji Raho Mohamed Hamza" else "#FF0000"
    # st.markdown(
    #     f"<div style='width:140px; height:40px; background-color:{rect_color}; color:white; text-align:center; line-height:40px; margin:auto; border-radius:5px;'>{'Mehadji Raho Mohamed Hamza'}</div>",
    #     unsafe_allow_html=True
    # )
    clickable_rectangle("Mehadji Raho Mohamed Hamza")

st.write(f"Selected voice: {st.session_state.voice_choice}")

# ------------------ Text Input ------------------
text = st.text_area("Enter your text here:")

# ------------------ Generate Button ------------------
voice_option = st.session_state.voice_choice
if st.button("Generate Speech"):
    if not text.strip():
        st.warning("Please enter some text!")
    elif voice_option not in voice_paths:
        st.warning("Please select a voice!")
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"output/generated_{timestamp}.wav"

        # Generate TTS audio
        generate_speech(
            text=text,
            speaker_wav=voice_paths[voice_option],
            output_path=output_file,
            language=language_map[language_option],
        )

        st.success(f"Audio generated: {output_file}")

        # ------------------ Audio Playback ------------------
        st.audio(output_file)

        # ------------------ Download Button ------------------
        with open(output_file, "rb") as f:
            st.download_button(
                label="Download Audio",
                data=f,
                file_name=f"{output_file.split('/')[-1]}",
                mime="audio/wav"
            )

        # ------------------ Visualization ------------------
        data, samplerate = sf.read(output_file)
        viz_type = st.radio("Visualization type:", ["Spectrogram", "Waveform"])

        fig, ax = plt.subplots(figsize=(10,3))
        if viz_type == "Spectrogram":
            ax.specgram(data, Fs=samplerate, cmap="magma")
            ax.set_title("Spectrogram")
        else:
            ax.plot(np.linspace(0, len(data)/samplerate, num=len(data)), data)
            ax.set_title("Waveform")

        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude" if viz_type=="Waveform" else "Frequency")
        st.pyplot(fig)
