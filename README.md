# Jared Voice Assistant

A sophisticated Windows-based AI voice assistant with speech recognition, natural language processing, and a modern GUI interface.

## Features

- **Voice Recognition**: Wake-word activation with "Hey Jared"
- **Text-to-Speech**: Natural voice responses using Windows Speech API
- **AI-Powered Conversations**: Powered by OpenAI's GPT models
- **Smart Reminders**: Set and manage time-based reminders
- **System Integration**: 
  - Open folders and applications
  - Search for files and directories
  - Control approved Windows applications
- **Modern GUI**: Dark-themed interface built with PySide6
- **Conversation History**: Persistent chat history across sessions

## Requirements

- Windows 10/11 (for speech recognition and TTS)
- Python 3.8+
- OpenAI API key

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

Run the application:
```bash
python main.py
```

### Voice Commands

- **Wake phrase**: "Hey Jared" or variations
- **Reminders**: "Remind me to [task] at [time]"
- **Folders**: "Open downloads", "Find folder projects"
- **Applications**: "Open calculator", "Launch notepad"
- **Queries**: Ask general questions, get time/date, etc.

### GUI Features

- Type commands directly in the text input
- Start/pause/stop voice listening
- View conversation history
- Real-time status updates

## Configuration

Modify `main.py` to customize:

- `ALLOWED_APPLICATIONS`: Add/remove approved applications
- `SEARCH_ROOTS`: Change folder search locations
- `SPECIAL_FOLDERS`: Define quick-access folders
- Chatbot personality and model in the `Chatbot` class

## Security Note

The application only opens folders and applications explicitly allowed in the configuration. Review and modify `ALLOWED_APPLICATIONS` before use.

## License

See LICENSE file for details.