# stt_module.py
import os
import wave
import sounddevice as sd
from groq import Groq
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

# Initialize the Groq client with the API key
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def record_audio(duration=5, fs=44100):
    """Records audio from the microphone."""
    # st.write("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    # st.write("Recording complete.")
    return recording

def save_audio_to_file(audio_data, filename="recorded_audio.wav", fs=44100):
    """Saves recorded audio data to a file."""
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)  # Mono
        wf.setsampwidth(2)  # 16 bits per sample
        wf.setframerate(fs)
        wf.writeframes(audio_data.tobytes())
    return filename

def transcribe_audio(file_path, prompt=""):
    """Transcribes the audio file to text using the Groq API."""
    try:
        with open(file_path, "rb") as file:
            # Create a translation of the audio file
            translation = client.audio.translations.create(
                file=(file_path, file.read()),  # Required audio file
                model="whisper-large-v3",  # Required model to use for translation
                prompt=prompt,  # Optional
                response_format="json",  # Optional
                temperature=0.0  # Optional
            )
            
        # Return the transcription text
        return translation.text if hasattr(translation, 'text') else "Transcription failed."
    
    except Exception as e:
        return f"An error occurred: {e}"