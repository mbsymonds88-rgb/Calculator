# Jared Assistant - Platform Overview

## Quick Start Guide

### 🪟 Windows
```bash
git clone <repo>
cd <repo>
pip install -r requirements.txt
echo "OPENAI_API_KEY=your-key" > .env
python main.py
```

### 📱 iOS
```bash
git clone <repo>
cd <repo>
open Xcode
# Create new iOS App project
# Add files from JaredAssistant/ folder
# Run in simulator or device
```

---

## Feature Matrix

| Feature | Windows | iOS | Notes |
|---------|:-------:|:---:|-------|
| **Core Features** |
| Voice Input | ✅ | ✅ | Windows Speech API / Apple Speech |
| Voice Output | ✅ | ✅ | PowerShell TTS / AVSpeechSynthesizer |
| AI Chat | ✅ | ✅ | OpenAI GPT integration |
| Conversation History | ✅ | ✅ | JSON files / UserDefaults |
| Dark Mode | ✅ | ✅ | Custom theme / System adaptive |
| **Advanced Features** |
| Reminders | ✅ | 🚧 | Full support / Foundation ready |
| Wake Word | ✅ | ❌ | "Hey Jared" / Tap to activate |
| System Control | ✅ | ❌ | Open apps/folders / iOS sandboxed |
| Folder Search | ✅ | ❌ | Windows directories / N/A |
| **User Interface** |
| Modern GUI | ✅ | ✅ | PySide6 Qt / Native SwiftUI |
| Message Bubbles | ✅ | ✅ | Custom / iMessage-style |
| Real-time Status | ✅ | ✅ | Status bar / Indicators |
| Smooth Animations | ✅ | ✅ | Qt animations / SwiftUI |

**Legend:**
- ✅ Fully implemented
- 🚧 Foundation ready, coming soon
- ❌ Not applicable / Platform limitation

---

## Architecture Comparison

### Windows Architecture
```
┌─────────────────────────────────────┐
│         Main GUI (PySide6)          │
│  ┌──────────┐  ┌─────────────────┐ │
│  │ QTextEdit│  │  Control Buttons│ │
│  └──────────┘  └─────────────────┘ │
└─────────────────────────────────────┘
           │
    ┌──────┴────────┐
    ▼               ▼
┌─────────┐   ┌──────────────┐
│Chatbot  │   │ Speech I/O   │
│Manager  │   │ (Windows API)│
└─────────┘   └──────────────┘
    │               │
    └───────┬───────┘
            ▼
    ┌───────────────┐
    │   OpenAI API  │
    │   Reminders   │
    │ System Control│
    └───────────────┘
```

### iOS Architecture
```
┌─────────────────────────────────────┐
│      ContentView (SwiftUI)          │
│  ┌──────────┐  ┌─────────────────┐ │
│  │ScrollView│  │  Voice Controls │ │
│  └──────────┘  └─────────────────┘ │
└─────────────────────────────────────┘
           │
    ┌──────┴────────┐
    ▼               ▼
┌──────────────┐   ┌──────────────┐
│ChatbotManager│   │SpeechManager │
│@ObservableObj│   │(Speech+AVKit)│
└──────────────┘   └──────────────┘
    │                    │
    └────────┬───────────┘
             ▼
    ┌────────────────────┐
    │   OpenAI API       │
    │   UserDefaults     │
    │   UserNotifications│
    └────────────────────┘
```

---

## Technology Stack

### Windows Stack
```
┌─────────────────────────────┐
│         Python 3.8+         │
├─────────────────────────────┤
│ PySide6 (Qt GUI Framework)  │
│ python-dotenv (Config)      │
│ OpenAI SDK (AI)             │
│ pywinrt (Windows Runtime)   │
├─────────────────────────────┤
│   Windows Speech API        │
│   PowerShell TTS            │
│   Win32 APIs                │
└─────────────────────────────┘
```

### iOS Stack
```
┌─────────────────────────────┐
│         Swift 5.7+          │
├─────────────────────────────┤
│ SwiftUI (Native UI)         │
│ Combine (Reactive)          │
│ URLSession (Networking)     │
│ Foundation (Core)           │
├─────────────────────────────┤
│   Speech Framework          │
│   AVFoundation (TTS)        │
│   UserNotifications         │
└─────────────────────────────┘
```

---

## File Structure

### Windows Files
```
/workspace/
├── main.py                    # Complete app (1,877 lines)
├── requirements.txt           # Python dependencies
├── .env.example              # Config template
├── .gitignore                # Security exclusions
└── README.md                 # Documentation
```

### iOS Files
```
/workspace/JaredAssistant/
├── JaredAssistantApp.swift           # Entry point
├── ContentView.swift                 # Main UI
├── Models/
│   ├── ChatMessage.swift            # Message model
│   └── Reminder.swift               # Reminder model
├── Managers/
│   ├── ChatbotManager.swift         # AI logic
│   ├── SpeechManager.swift          # Voice I/O
│   └── ReminderManager.swift        # Notifications
├── Assets.xcassets/                 # Icons
├── Info.plist                       # Permissions
├── iOS-README.md                    # iOS docs
└── SETUP-IOS.md                     # Setup guide
```

---

## API Integration

### Both Platforms Use OpenAI

**Windows:**
```python
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
response = client.responses.create(
    model="gpt-4.1-mini",
    instructions=self.instructions,
    input=self.conversation
)
```

**iOS:**
```swift
let url = URL(string: "https://api.openai.com/v1/chat/completions")!
request.setValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")
let response = try await URLSession.shared.data(for: request)
```

---

## Speech Processing

### Windows
```python
# Speech Recognition (WinRT)
recognizer = SpeechRecognizer()
result = await recognizer.recognize_async()

# Text-to-Speech (PowerShell)
subprocess.run([
    "powershell", "-Command",
    "Add-Type -AssemblyName System.Speech; "
    "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
    "$s.Speak('text')"
])
```

### iOS
```swift
// Speech Recognition (Native)
let recognizer = SFSpeechRecognizer()
let request = SFSpeechAudioBufferRecognitionRequest()
recognizer.recognitionTask(with: request) { result, error in
    // Handle recognized text
}

// Text-to-Speech (AVFoundation)
let synthesizer = AVSpeechSynthesizer()
let utterance = AVSpeechUtterance(string: "text")
synthesizer.speak(utterance)
```

---

## Data Persistence

### Windows
```python
# JSON Files
with Path("chat_history.json").open("w") as f:
    json.dump(messages, f)
    
with Path("reminders.json").open("w") as f:
    json.dump(reminders, f)
```

### iOS
```swift
// UserDefaults
let data = try? JSONEncoder().encode(messages)
UserDefaults.standard.set(data, forKey: "chat_history")

let data = try? JSONEncoder().encode(reminders)
UserDefaults.standard.set(data, forKey: "reminders")
```

---

## Development Environment

### Windows Development
- **OS Required**: Windows 10/11
- **IDE**: VS Code, PyCharm, or any text editor
- **Runtime**: Python 3.8+
- **Testing**: Run directly on development machine
- **Distribution**: EXE (via PyInstaller) or Python script

### iOS Development
- **OS Required**: macOS 12.0+ (Monterey or later)
- **IDE**: Xcode 14.0+
- **Runtime**: iOS 15.0+ (iPhone/iPad)
- **Testing**: Simulator or physical device
- **Distribution**: TestFlight or App Store

---

## Deployment

### Windows
```bash
# Direct execution
python main.py

# Build executable (optional)
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

### iOS
```
1. Archive in Xcode
2. Upload to TestFlight (beta)
3. Submit to App Store (production)
4. Requires Apple Developer account ($99/year)
```

---

## Performance Characteristics

| Metric | Windows | iOS |
|--------|---------|-----|
| **Startup Time** | ~2-3 seconds | ~1 second |
| **Memory Usage** | ~100-150 MB | ~50-80 MB |
| **Speech Recognition** | Cloud-based | On-device capable |
| **TTS Quality** | Good (Microsoft voices) | Excellent (Apple voices) |
| **Offline Capability** | Limited | Speech can work offline |
| **Battery Impact** | N/A (Desktop) | Moderate (mobile) |

---

## Use Cases

### Best for Windows
- ✅ Desktop productivity
- ✅ System automation
- ✅ File management
- ✅ Multi-tasking
- ✅ Large screen work

### Best for iOS
- ✅ Mobile convenience
- ✅ On-the-go access
- ✅ Touch interface
- ✅ Notifications
- ✅ Quick queries

---

## Future Roadmap

### Cross-Platform
- [ ] Sync conversations via cloud
- [ ] Shared reminder system
- [ ] Common AI configuration
- [ ] Voice model selection

### Platform-Specific

**Windows:**
- [ ] System tray integration
- [ ] Global hotkeys
- [ ] Browser extension

**iOS:**
- [ ] Siri shortcuts
- [ ] Widgets
- [ ] Watch app
- [ ] Share extension

---

## Support Matrix

| OS Version | Windows | iOS |
|------------|---------|-----|
| **Minimum** | Windows 10 | iOS 15.0 |
| **Recommended** | Windows 11 | iOS 17.0 |
| **Tested** | Windows 11 | iOS 17.0 |

---

## Resources

### Windows
- [PySide6 Documentation](https://doc.qt.io/qtforpython/)
- [Windows Speech API](https://docs.microsoft.com/en-us/windows/win32/speech)
- [OpenAI Python SDK](https://github.com/openai/openai-python)

### iOS
- [SwiftUI Documentation](https://developer.apple.com/documentation/swiftui)
- [Speech Framework](https://developer.apple.com/documentation/speech)
- [OpenAI API Reference](https://platform.openai.com/docs)

---

Choose your platform and start building! 🚀
