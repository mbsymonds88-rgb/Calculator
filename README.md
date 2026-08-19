# Jared Voice Assistant

A sophisticated AI voice assistant with speech recognition, natural language processing, and modern interface. Available for **Windows** and **iOS**.

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

## Platforms

### 🪟 Windows Version
- **Technology**: Python, PySide6, Windows Speech API
- **File**: `main.py`
- **Documentation**: See sections below

### 📱 iOS Version
- **Technology**: Swift, SwiftUI, iOS Speech Framework
- **Folder**: `JaredAssistant/`
- **Documentation**: See [iOS-README.md](iOS-README.md) and [SETUP-IOS.md](SETUP-IOS.md)

---

## Windows Requirements

- Windows 10/11 (for speech recognition and TTS)
- Python 3.8+
- OpenAI API key

## iOS Requirements

- iOS 15.0+ (iPhone or iPad)
- Xcode 14.0+ (for development)
- Mac computer (for building)
- OpenAI API key

## Installation

### Windows Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
4. Run the application:
   ```bash
   python main.py
   ```

### iOS Installation

See detailed setup guide: **[SETUP-IOS.md](SETUP-IOS.md)**

Quick start:
1. Open Xcode
2. Create new iOS App project
3. Add files from `JaredAssistant/` folder
4. Build and run on simulator or device

## Usage

### Windows Usage

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

## Platform Comparison

| Feature | Windows | iOS |
|---------|---------|-----|
| Voice Recognition | ✅ Windows Speech API | ✅ Apple Speech Framework |
| Text-to-Speech | ✅ PowerShell TTS | ✅ AVSpeechSynthesizer |
| OpenAI Integration | ✅ GPT-4.1-mini | ✅ GPT-4o-mini |
| GUI Framework | PySide6 (Qt) | SwiftUI (Native) |
| Reminders | ✅ Full support | ⏳ Coming soon |
| Folder/App Control | ✅ Windows apps | ❌ iOS sandboxed |
| Conversation History | ✅ JSON files | ✅ UserDefaults |
| Wake Word | ✅ "Hey Jared" | ⏳ Tap to activate |

## Documentation

- **Main README**: This file (cross-platform overview)
- **iOS Guide**: [iOS-README.md](iOS-README.md) - iOS features and usage
- **iOS Setup**: [SETUP-IOS.md](SETUP-IOS.md) - Detailed iOS setup instructions
- **Windows**: Sections above cover Windows setup and usage

## License

See LICENSE file for details.