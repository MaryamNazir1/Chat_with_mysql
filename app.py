import os
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from streamlit_float import float_init
from dotenv import load_dotenv
from db_sql_module import init_database, get_response  # Import your DB functions
from utils import autoplay_audio, transcribe_audio, generate_speech

st.set_page_config(page_title="MySQL Database Assistant", page_icon="💬")

def load_env():
    load_dotenv()  # Load environment variables

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm here to assist you with your SQL queries."}]
    
    if "audio_query" not in st.session_state:
        st.session_state.audio_query = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []  # Initialize chat history

def clear_chat_history():
    st.session_state.messages = []  # Clear all messages
    st.session_state.messages.append({"role": "assistant", "content": "Hello! I'm here to assist you with your SQL queries."})  # Add initial message
    st.session_state.audio_query = None  # Clear the audio input history
    st.session_state.chat_history = []  # Clear the chat history

def user_input(user_question, db, chat_history):
    # Process the user question and get the response from the database
    response = get_response(user_question, db, chat_history)
    return response  # Return the response

def main():
    load_env()
    initialize_session_state()
    float_init()  # Initialize floating features

    st.title("MySQL Database Assistant 💬")  # Main title

    # Sidebar for database connection
    with st.sidebar:
        st.title("Database Connection")
        st.text_input("Host", value="localhost", key="Host")
        st.text_input("Port", value="3306", key="Port")
        st.text_input("User", value="root", key="User")
        st.text_input("Password", type="password", value="admin", key="Password")
        st.text_input("Database", value="onlinestore", key="Database")
        
        if st.button("Connect"):
            with st.spinner("Connecting to database..."):
                db = init_database(
                    st.session_state["User"],
                    st.session_state["Password"],
                    st.session_state["Host"],
                    st.session_state["Port"],
                    st.session_state["Database"]
                )
                st.session_state.db = db
                st.success("Connected to database!")

        st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

    # Create a footer container for the input
    footer_container = st.container()

    with footer_container:
        # Create columns for text input and audio recorder
        col1, col2 = st.columns([9, 1])
        
        with col1:
            # Text input for user question
            text_input = st.chat_input("Type your query here...")  # Use chat_input for text entry
        
        with col2:
            # Audio recorder for voice input
            audio_bytes = audio_recorder(text="", icon_size="2x", recording_color="#7C0A02", neutral_color="#FFFFFF")

    # Float the footer container at the bottom of the screen
    footer_container.float("bottom:20px;")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.write(message['content'])

    # Handle audio input (only process new audio)
    if audio_bytes and st.session_state.get('processed_audio_query') != audio_bytes:
        with st.chat_message("user"):
            with st.spinner("Transcribing..."):
                # Write the audio bytes to a temporary file
                webm_file_path = "temp_audio.wav"
                with open(webm_file_path, "wb") as f:
                    f.write(audio_bytes)

                # Convert the audio to text
                transcript = transcribe_audio(webm_file_path)
                os.remove(webm_file_path)
                if transcript:
                    st.session_state.messages.append({"role": "user", "content": transcript})
                    st.session_state.audio_query = transcript  # Store the processed audio query
                    st.session_state.processed_audio_query = audio_bytes  # Mark audio as processed
                    st.write(transcript)

    # Check if there is any user input (text or voice)
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        user_question = st.session_state.messages[-1]["content"]  # Get the last user input
        with st.chat_message("assistant"):
            with st.spinner("Thinking🤔..."):
                response = user_input(user_question, st.session_state.db, st.session_state.chat_history)  # Pass db and chat_history
                st.session_state.messages.append({"role": "assistant", "content": response})  # Append the assistant response

                # Display the response first
                st.write(response)  # Display the assistant's text response

                # Generate audio response after displaying text
            with st.spinner("Generating audio response..."):    
                audio_file = generate_speech(response)
                autoplay_audio(audio_file)  # Play the audio response
                os.remove(audio_file)  # Clean up the audio file after playing
            
    # Check if there is any text input
    if text_input:
        with st.chat_message("user"):
            st.write(text_input)  # Display the user's text input
            st.session_state.messages.append({"role": "user", "content": text_input})  

        # Handle text input search
        with st.chat_message("assistant"):
            with st.spinner("Thinking🤔..."):
                response = user_input(text_input, st.session_state.db, st.session_state.chat_history)  # Pass db and chat_history
                st.session_state.messages.append({"role": "assistant", "content": response})  # Append the assistant response
                # Display the response first
                st.write(response)  # Display the assistant's text response

                # Generate audio response after displaying text
            with st.spinner("Generating audio response..."):    
                audio_file = generate_speech(response)
                autoplay_audio(audio_file)  # Play the audio response
                os.remove(audio_file)  # Clean up the audio file after playing

if __name__ == "__main__":
    main()
