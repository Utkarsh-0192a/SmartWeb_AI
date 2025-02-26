# Question Answering System

This project is a question answering system built with Streamlit. It integrates web search, content extraction, and a language model to generate detailed responses to user questions.

## Features

- **Chat Interface:** Users ask questions via a Streamlit-based chat interface.
- **Web Search Toggle:** When enabled, the system enriches the user query by searching the web and extracting context.
- **LLM Integration:** Uses the Ollama API with the `llama3.2` model to generate responses.
- **Content Extraction:** Retrieves and extracts relevant content from selected URLs using `trafilatura`.
- **Logging:** Centralized logging is set up in `config.py` to track system activity and help with debugging.
  
## File Structure

- **`config.py`**: Configures shared logging.
- **`main.py`**: Contains the `websearch` class used for generating search queries, extracting content, and generating answers.
- **`app.py`**: The Streamlit application that provides the chat interface.
- **`requirements.txt`**: Lists all the required packages for the project.

## Setup and Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

## Author

Utkarsh Gautam

