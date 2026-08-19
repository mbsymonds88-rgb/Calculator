# iOS Setup Guide for Jared Assistant

This guide will help you set up and run the Jared Assistant iOS application.

## Prerequisites

1. **Mac Computer**: Required for iOS development
2. **Xcode**: Download from Mac App Store (free)
   - Minimum version: Xcode 14.0+
   - macOS Monterey 12.0 or later recommended

3. **Apple Developer Account** (optional):
   - Free account: Run on your own device
   - Paid account ($99/year): Distribute to others

4. **OpenAI API Key**: Get from https://platform.openai.com/api-keys

## Step-by-Step Setup

### 1. Install Xcode

```bash
# Open Mac App Store
open -a "App Store"
# Search for "Xcode" and install
```

Or download directly from Apple Developer website.

### 2. Create Xcode Project

Since Git cannot store the `.xcodeproj` file properly, you'll need to create it:

**Method A: Using Xcode GUI**

1. Open Xcode
2. Click "Create New Project"
3. Select "iOS" → "App"
4. Enter project details:
   - Product Name: `JaredAssistant`
   - Team: (Select your Apple ID)
   - Organization Identifier: `com.yourname` (or any reverse domain)
   - Interface: **SwiftUI**
   - Language: **Swift**
   - Storage: None
5. Choose save location: Select the cloned repository folder
6. Click "Create"

**Method B: Using Command Line**

```bash
cd /workspace
# Xcode project can be created via GUI only
# Open Xcode and follow Method A above
```

### 3. Add Source Files to Project

1. In Xcode, right-click the project folder
2. Select "Add Files to JaredAssistant..."
3. Navigate to `JaredAssistant/` folder
4. Select all `.swift` files
5. Make sure "Copy items if needed" is **unchecked**
6. Click "Add"

### 4. Add Info.plist

1. Right-click project in Xcode
2. Select "Add Files to JaredAssistant..."
3. Add the `Info.plist` file
4. Ensure it's set as the project's Info.plist in Build Settings

### 5. Configure Project Settings

1. Select project in left sidebar
2. Select "JaredAssistant" target
3. Go to "Signing & Capabilities"
4. Select your Team (Apple ID)
5. Ensure "Automatically manage signing" is checked

### 6. Configure Deployment Target

1. In project settings, go to "General"
2. Set "Minimum Deployments" to iOS 15.0 or later

### 7. Add Required Capabilities

1. Go to "Signing & Capabilities" tab
2. Click "+ Capability"
3. Add:
   - Push Notifications (for reminders)
   - Background Modes → Audio (for TTS in background)

### 8. Build and Run

**On Simulator:**
```
1. Select a simulator from the device dropdown (e.g., iPhone 15 Pro)
2. Click the Play button (▶) or press ⌘R
3. Wait for build to complete
4. App will launch in simulator
```

**On Physical Device:**
```
1. Connect iPhone/iPad via USB
2. Unlock device and trust computer
3. Select your device from dropdown
4. Click Play button (▶) or press ⌘R
5. On device: Settings → General → Device Management
6. Trust your developer certificate
7. Launch app on device
```

## First Launch Configuration

### 1. Grant Permissions

When you first launch the app, grant these permissions:
- ✅ Microphone Access
- ✅ Speech Recognition
- ✅ Notifications (optional, for reminders)

### 2. Set OpenAI API Key

**Option A: On First Launch**
- App will prompt for API key
- Enter your key from OpenAI platform
- Tap Save

**Option B: Via Code**
- Open `ContentView.swift`
- Add this in `onAppear`:
```swift
UserDefaults.standard.set("your-api-key-here", forKey: "openai_api_key")
```

**Option C: Via Simulator/Device**
- Install and run the app
- Use Settings bundle (if implemented)
- Or hard-code temporarily in `ChatbotManager.swift`

## Testing the App

### Test Microphone
1. Tap the microphone button (🎤)
2. Speak: "What time is it?"
3. Should see transcription appear
4. Should receive spoken and text response

### Test AI Chat
1. Type a message: "Tell me a joke"
2. Press return or send button
3. Should receive AI-powered response

### Test Built-in Commands
```
- "time" → Current time
- "date" → Current date
- "help" → Feature list
- "clear history" → Clears chat
```

## Troubleshooting

### Build Fails

**Error: "No signing certificate found"**
```
Solution:
1. Go to Xcode → Settings → Accounts
2. Add your Apple ID
3. Select your account → Manage Certificates
4. Click + → iOS Development
5. Retry build
```

**Error: "Provisioning profile doesn't match"**
```
Solution:
1. Project settings → Signing & Capabilities
2. Change bundle identifier to something unique
3. Example: com.yourname.jaredassistant
4. Retry build
```

### Speech Recognition Not Working

**In Simulator:**
- Speech recognition has limited support in simulator
- Test on real device for best results

**On Device:**
- Settings → Privacy → Microphone → Enable for app
- Settings → Privacy → Speech Recognition → Enable for app
- Restart app

### OpenAI API Errors

**"API key not set"**
```swift
// Add to ChatbotManager.init() temporarily:
self.apiKey = "sk-your-key-here"
```

**"Rate limit exceeded"**
- Check your OpenAI account usage
- You may need to add billing info
- Or reached free tier limit

### App Crashes

1. Check Xcode console for errors
2. Common fixes:
   - Clean build folder (⌘⇧K)
   - Delete derived data
   - Restart Xcode
   - Restart device/simulator

## Project Structure Verification

Ensure your Xcode project looks like this:

```
JaredAssistant (folder - blue)
├── JaredAssistantApp.swift
├── ContentView.swift
├── Models (folder)
│   ├── ChatMessage.swift
│   └── Reminder.swift
├── Managers (folder)
│   ├── ChatbotManager.swift
│   ├── SpeechManager.swift
│   └── ReminderManager.swift
├── Assets.xcassets
└── Info.plist
```

## Advanced Configuration

### Change AI Model

Edit `ChatbotManager.swift`:
```swift
private let model = "gpt-4o-mini" // or "gpt-4o", "gpt-3.5-turbo"
```

### Customize Appearance

Edit `ContentView.swift`:
- Message bubble colors
- Button styles
- Font sizes
- Spacing and padding

### Add Custom Commands

Edit `ChatbotManager.swift` → `handleLocalCommand()`:
```swift
if lowercased.contains("your command") {
    return "Your response"
}
```

## Distribution (Optional)

### TestFlight (Beta Testing)
1. Need paid Apple Developer account
2. Archive app in Xcode
3. Upload to App Store Connect
4. Configure TestFlight
5. Invite testers via email

### App Store Release
1. Paid Apple Developer account required
2. Prepare app metadata and screenshots
3. Submit for review
4. Wait 1-3 days for approval

## Getting Help

- **Xcode Issues**: https://developer.apple.com/documentation/
- **Swift Questions**: https://stackoverflow.com/questions/tagged/swift
- **OpenAI API**: https://platform.openai.com/docs
- **Speech Framework**: https://developer.apple.com/documentation/speech

## Next Steps

Once running successfully:
1. ✅ Test all features
2. ✅ Customize for your needs
3. ✅ Add your own features
4. ✅ Share with friends (via TestFlight)

Happy coding! 🚀
