import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from db_sql_module import init_database, get_response
from stt_module import save_audio_to_file, record_audio, transcribe_audio
from tts_module import generate_speech

# Load environment variables
load_dotenv()

# Streamlit page configuration
st.set_page_config(page_title="Database Assistant Chat", page_icon=":speech_balloon:")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello! I'm a SQL assistant. Ask me anything about your database."),
    ]

if "user_query" not in st.session_state:
    st.session_state.user_query = ""

if "last_query" not in st.session_state:
    st.session_state.last_query = ""

if "recording_complete" not in st.session_state:
    st.session_state.recording_complete = False

# Sidebar for database connection
with st.sidebar:
    st.subheader("Connect to Your SQL Database")
    st.write("This is a simple chat application using MySQL. Connect to the database and start chatting.")
    
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

# Chat history display
chat_container = st.container()  # Container for chat history

# Input section for user query
input_container = st.container()  # Container for input box and button

with input_container:
    # st.subheader("Ask a question about your database:")
    col1, col2 = st.columns([8, 1])
    
    with col1:
        # Show user query in the text input
        user_query = st.text_input("Type your query here...", value=st.session_state.user_query, key="input_query", 
                                   placeholder="Type your query here...")
    
    with col2:
        record_button = st.button("🎤", key="record_button")

    # Perform search if user manually enters text
    if user_query and user_query != st.session_state.last_query:
        st.session_state.last_query = user_query
        st.session_state.chat_history.append(HumanMessage(content=user_query))
        
        with st.spinner("Generating response..."):
            response = get_response(user_query, st.session_state.db, st.session_state.chat_history)
            st.session_state.chat_history.append(AIMessage(content=response))
            response_audio_file = generate_speech(response)  # Generate speech from response
            st.session_state.chat_history[-1].audio_file_path = response_audio_file
        
        # Clear the input box after processing the query
        st.session_state.user_query = ""
        st.experimental_rerun()  # Rerun the app to clear the input box

    # Check if the record button is clicked
    if record_button:
        st.session_state.recording_complete = False  # Reset recording state
        with st.spinner("Recording..."):
            duration = 10  # Fixed recording duration
            audio_data = record_audio(duration)  # Record audio
        st.session_state.recording_complete = True  # Set recording complete

        # Process the audio after recording
        temp_file_path = save_audio_to_file(audio_data)  # Save the recorded audio
        transcribed_text = transcribe_audio(temp_file_path)  # Get the text from the audio
        
        # Update the user query with the recognized text
        if transcribed_text and transcribed_text.strip() != "":
            st.session_state.user_query = transcribed_text  # Update session state with recognized text
            
            # Automatically perform the search if the query is different
            if st.session_state.user_query != st.session_state.last_query:
                st.session_state.last_query = st.session_state.user_query  # Update the last query

                # Store the user query in session state
                st.session_state.chat_history.append(HumanMessage(content=st.session_state.user_query, audio_file_path=temp_file_path))

                # AI response
                with st.spinner("Generating response..."):
                    response = get_response(st.session_state.user_query, st.session_state.db, st.session_state.chat_history)
                    st.session_state.chat_history.append(AIMessage(content=response))
                    response_audio_file = generate_speech(response)  # Generate speech from response
                    st.session_state.chat_history[-1].audio_file_path = response_audio_file

        # Clear the input box after processing the query
        st.session_state.user_query = ""
        st.experimental_rerun()  # Rerun the app to clear the input box


# Update chat history display after processing the input
with chat_container:
    st.subheader("Database Assistant Chat")
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.markdown(f"<div style='background-color: #1e1e1e; padding: 10px; border-radius: 5px; text-align: left; color: white;'>"
                            f"{message.content}</div>", unsafe_allow_html=True)
                if hasattr(message, 'audio_file_path') and message.audio_file_path:
                    st.audio(message.audio_file_path, format='audio/wav')

        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.markdown(f"<div style='background-color: #007acc; padding: 10px; border-radius: 5px; text-align: left; color: white;'>"
                            f"{message.content}</div>", unsafe_allow_html=True)
                if hasattr(message, 'audio_file_path') and message.audio_file_path:
                    st.audio(message.audio_file_path, format='audio/wav')
