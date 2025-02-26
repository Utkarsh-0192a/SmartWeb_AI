# Web-Enabled AI Question Answering System

This project is a question answering system built with Streamlit. It integrates web search, content extraction, and a language model to generate detailed responses to user questions. The system can answer questions on virtually any topic - from science and history to current events and technology - thanks to its combination of AI knowledge and real-time web search capabilities.

## Features

- **Chat Interface:** Users ask questions via a Streamlit-based chat interface.
- **Web Search Toggle:** When enabled, the system enriches the user query by searching the web and extracting context.
- **LLM Integration:** Uses the Ollama API with the `llama3.2` model to generate responses.
- **Content Extraction:** Retrieves and extracts relevant content from selected URLs using `trafilatura`.
- **Logging:** Centralized logging is set up in `config.py` to track system activity and help with debugging.

### Automatic Web Search Fallback
The system includes an intelligent fallback mechanism:
- When the AI model indicates it lacks knowledge about a query (responds with "false")
- It automatically triggers a web search to gather current information
- Uses the retrieved information to provide an informed response
- This ensures up-to-date and accurate answers for queries beyond the model's training data

### Manual Web Search Toggle
You can also manually enable web search:
- Toggle the "Enable Web Search" option before asking your question
- Forces the system to include web search results in its response
  
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

