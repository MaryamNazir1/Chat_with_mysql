# tts_module.py
import os
from dotenv import load_dotenv
import streamlit as st
from deepgram import DeepgramClient, SpeakOptions

# Load environment variables
load_dotenv()

# Filename for the output audio file
filename = "output.wav"

def generate_speech(text_input):
    """Generates speech from text and saves it to a file."""
    try:
        SPEAK_OPTIONS = {"text": text_input}

        # Create a Deepgram client using the API key from environment variables
        deepgram = DeepgramClient(api_key=os.getenv("DG_API_KEY"))

        # Configure the options (such as model choice, audio configuration, etc.)
        options = SpeakOptions(
            model="aura-asteria-en",
            encoding="linear16",
            container="wav"
        )

        # Call the save method on the speak property to generate the speech
        deepgram.speak.v("1").save(filename, SPEAK_OPTIONS, options)
        # st.success(f"Speech saved to {filename}")

        return filename

    except Exception as e:
        st.error(f"Exception: {e}")
        return None
