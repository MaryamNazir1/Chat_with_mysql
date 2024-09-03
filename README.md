# SQL Database Assistant Chat

This project is a Streamlit-based chat application that interacts with a MySQL database. It supports both text and voice input for querying the database, and provides responses in both text and synthesized speech formats. The app integrates SQL communication, voice transcription, and natural language processing to enhance user interaction with databases.

## Features

- **SQL Database Interaction**: Connect to a MySQL database and query it using natural language.
- **Voice Input**: Record voice queries which are transcribed into text.
- **Text-to-Speech**: Convert database query responses into speech.
- **Chat History**: Maintains a session-based history of interactions, including both text and audio responses.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/maryamnazir1/sql-database-assistant-chat.git
   cd sql-database-assistant-chat

2. **Install Dependencies**

   Ensure you have Python 3.7 or higher installed. Install the required Python packages using:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**

   Create a `.env` file in the root directory of the project with the following content:

   ```plaintext
   GROQ_API_KEY=your_groq_api_key
   DG_API_KEY=your_deepgram_api_key
   ```

   Replace `your_groq_api_key` and `your_deepgram_api_key` with your actual API keys from Groq and Deepgram.

## Usage

1. **Run the Application**

   Start the Streamlit application by running:

   ```bash
   streamlit run app.py
   ```

2. **Connect to Your MySQL Database**

   Use the sidebar in the Streamlit app to input your database credentials (host, port, user, password, database).

3. **Interact with the Assistant**

   - **Text Input**: Type your SQL-related questions into the input box.
   - **Voice Input**: Click the microphone button to record a question.
   - The assistant will respond with both text and an audio playback of the response.

## Project Structure

- **`app.py`**: The main application file that sets up the Streamlit interface and manages user interactions.
- **`db_sql_module.py`**: Contains functions for initializing and querying the MySQL database.
- **`stt_module.py`**: Handles voice recording, audio file saving, and transcription using the Groq API.
- **`tts_module.py`**: Converts text responses into speech using the Deepgram API.

## Dependencies

- `streamlit`
- `python-dotenv`
- `langchain-core`
- `langchain-community`
- `langchain-groq`
- `mysql-connector-python`
- `sounddevice`
- `groq`
- `deepgram-sdk`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an issue.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

- [Streamlit](https://streamlit.io/) for the framework to build this data app.
- [LangChain](https://www.langchain.com/) for enabling language model integration.
- [Deepgram](https://deepgram.com/) for providing the text-to-speech API.
- [Groq](https://www.groq.com/) for the speech-to-text API.
