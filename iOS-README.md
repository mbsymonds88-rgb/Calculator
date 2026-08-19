# Jared Assistant - iOS

A sophisticated iOS voice assistant application with speech recognition, natural language processing, and modern SwiftUI interface.

## Features

### 🎙️ Voice Integration
- **Speech Recognition**: Native iOS speech-to-text using Apple's Speech framework
- **Text-to-Speech**: Natural voice responses using AVSpeechSynthesizer
- **Wake-Free Operation**: Tap-to-talk interface for quick access
- **Real-time Recognition**: See your speech transcribed as you speak

### 🤖 AI-Powered Conversations
- **OpenAI GPT Integration**: Intelligent responses powered by GPT-4o-mini
- **Conversation Memory**: Maintains context across the conversation
- **Persistent History**: Chat history saved locally on device
- **Smart Commands**: Built-in handling for time, date, and utility commands

### 📱 Modern iOS Interface
- **SwiftUI Design**: Native iOS look and feel
- **Message Bubbles**: iMessage-style conversation interface
- **Dark Mode Support**: Automatically adapts to system theme
- **Smooth Animations**: Polished transitions and interactions
- **Status Indicators**: Real-time processing and listening states

### ⏰ Reminders (Coming Soon)
- Set time-based reminders with natural language
- Local notifications for scheduled reminders
- Manage and complete reminders in-app

## Requirements

- iOS 15.0 or later
- iPhone or iPad
- Microphone access for voice recognition
- OpenAI API key
- Internet connection for AI features

## Installation

### Option 1: Xcode (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd JaredAssistant
   ```

2. **Open in Xcode**
   - Double-click `JaredAssistant.xcodeproj` (or create using instructions below)
   - Or open Xcode and select "Open a project or file"

3. **Configure API Key**
   - First launch will prompt for OpenAI API key
   - Or set in UserDefaults with key `openai_api_key`

4. **Run on Device/Simulator**
   - Select your target device
   - Click Run (⌘R) or the play button
   - Grant microphone and speech recognition permissions when prompted

### Option 2: Manual Xcode Project Setup

If you don't have the `.xcodeproj` file:

1. Open Xcode
2. Create new project: File → New → Project
3. Choose "iOS" → "App"
4. Fill in:
   - Product Name: `JaredAssistant`
   - Interface: SwiftUI
   - Language: Swift
5. Add all `.swift` files from the `JaredAssistant/` folder
6. Replace `Info.plist` with the provided one
7. Add Assets.xcassets folder

## Project Structure

```
JaredAssistant/
├── JaredAssistantApp.swift      # App entry point
├── ContentView.swift             # Main UI view
├── Models/
│   ├── ChatMessage.swift         # Message data model
│   └── Reminder.swift            # Reminder data model
├── Managers/
│   ├── ChatbotManager.swift      # AI conversation logic
│   ├── SpeechManager.swift       # Speech recognition & TTS
│   └── ReminderManager.swift     # Reminder notifications
├── Assets.xcassets/              # App icons and assets
└── Info.plist                    # App permissions & config
```

## Usage

### Voice Commands

1. **Tap the microphone button** to start listening
2. **Speak your command** clearly
3. **Message appears** automatically when you stop speaking
4. **Jared responds** with voice and text

### Text Commands

- Type any message in the text field
- Press return or tap the send button
- Receive AI-powered responses

### Built-in Commands

- **"time"** or **"what time is it"** - Get current time
- **"date"** or **"today's date"** - Get current date
- **"help"** - Show available features
- **"clear history"** - Clear conversation

### Buttons

- **🎤 Listen**: Start/stop voice recognition
- **🔔 Reminders**: View and manage reminders
- **🗑️ Clear**: Clear conversation history
- **⚙️ Settings**: App configuration (coming soon)

## Configuration

### API Key

Store your OpenAI API key in UserDefaults:

```swift
UserDefaults.standard.set("your-api-key", forKey: "openai_api_key")
```

Or enter it when prompted on first launch.

### Customization

Edit `ChatbotManager.swift` to customize:
- AI personality and instructions
- Model selection (default: gpt-4o-mini)
- Response length and behavior
- History retention

## Permissions

The app requires these permissions (automatically requested):

- **Microphone**: For voice input
- **Speech Recognition**: For converting speech to text
- **Notifications**: For reminder alerts (optional)

## Privacy & Security

- All conversations stored locally on device
- API key stored securely in UserDefaults
- No data sent to third parties except OpenAI API
- Speech processed on-device when possible
- No analytics or tracking

## Troubleshooting

### Speech Recognition Not Working
- Check microphone permissions in Settings → Privacy
- Ensure Speech Recognition is enabled for the app
- Try restarting the app

### AI Responses Not Working
- Verify your OpenAI API key is valid
- Check internet connection
- Ensure you have API credits available
- Check Xcode console for error messages

### Build Errors
- Ensure deployment target is iOS 15.0+
- Update to latest Xcode version
- Clean build folder (⌘⇧K) and rebuild

## Future Enhancements

- [ ] Full reminder implementation with notifications
- [ ] Siri shortcuts integration
- [ ] Widget support for quick access
- [ ] iCloud sync for conversation history
- [ ] Custom voice selection
- [ ] Offline mode with local models
- [ ] Share conversations
- [ ] Export chat history

## Technical Details

### Frameworks Used
- **SwiftUI**: Modern declarative UI framework
- **Speech**: Apple's speech recognition framework
- **AVFoundation**: Audio and speech synthesis
- **UserNotifications**: Local reminder notifications
- **Foundation**: Core Swift utilities

### Architecture
- MVVM (Model-View-ViewModel) pattern
- ObservableObject for state management
- Async/await for API calls
- Codable for data persistence

## License

See LICENSE file for details.

## Credits

Developed for iOS using native Apple frameworks and OpenAI's GPT API.
