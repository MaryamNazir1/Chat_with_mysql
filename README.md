# MySQL Database Assistant

## Overview

The MySQL Database Assistant is a web application built using Streamlit that integrates voice and text input to interact with a MySQL database. Users can ask questions about the database, and the assistant responds with natural language answers. The app supports both text and voice inputs, transcribes voice queries, and generates audio responses for the answers.

## Features

- **Voice and Text Input**: Users can input queries either by typing or speaking.
- **Real-time Database Interaction**: Processes SQL queries based on user input and retrieves data from a MySQL database.
- **Natural Language Responses**: Converts SQL query results into human-readable answers.
- **Text-to-Speech**: Provides audio responses using Deepgram for text-to-speech conversion.

## Technologies Used

- **Streamlit**: For building the interactive web application.
- **Deepgram**: For text-to-speech conversion.
- **Groq**: For audio transcription.
- **MySQL**: For database operations.
- **Langchain**: For handling natural language processing and SQL queries.

## Setup Instructions

### Prerequisites

- Python 3.10
- MySQL server
- API keys for Deepgram and Groq (set up in a `.env` file)

### Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/maryamnazir1/mysql-database-assistant.git
    cd mysql-database-assistant
    ```

2. **Create a Virtual Environment**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Create a `.env` File**

    Create a `.env` file in the root directory of the project with the following content:

    ```env
    DG_API_KEY=your_deepgram_api_key
    GROQ_API_KEY=your_groq_api_key
    ```

5. **Run the Application**

    ```bash
    streamlit run app.py
    ```

## Usage

1. **Connect to Database**

   - Use the sidebar to input your MySQL database credentials (host, port, user, password, and database name).
   - Click "Connect" to establish a connection.

2. **Interact with the Assistant**

   - Type your query in the text input box or use the audio recorder to speak your query.
   - The assistant will process the query, interact with the database, and provide a response.
   - The response will be displayed as text, and an audio version will be generated and played automatically.

3. **Clear Chat History**

   - Click the "Clear Chat History" button in the sidebar to reset the conversation.

## File Descriptions

- **`app.py`**: The main application script that handles user interface and interactions.
- **`utils.py`**: Contains utility functions for audio handling, including playback, speech generation, and transcription.
- **`db_sql_module.py`**: Manages database connections and SQL query processing.

## Contributing

Feel free to open issues or submit pull requests. Contributions are welcome!
