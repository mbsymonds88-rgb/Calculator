//
//  ContentView.swift
//  Jared Assistant
//
//  Main view for the iOS voice assistant
//

import SwiftUI

struct ContentView: View {
    @StateObject private var chatbot = ChatbotManager()
    @StateObject private var speechManager = SpeechManager()
    @State private var userInput = ""
    @State private var isListening = false
    
    var body: some View {
        NavigationView {
            VStack(spacing: 0) {
                // Conversation transcript
                ScrollViewReader { proxy in
                    ScrollView {
                        LazyVStack(alignment: .leading, spacing: 12) {
                            ForEach(chatbot.messages) { message in
                                MessageBubble(message: message)
                                    .id(message.id)
                            }
                        }
                        .padding()
                    }
                    .onChange(of: chatbot.messages.count) { _ in
                        if let lastMessage = chatbot.messages.last {
                            withAnimation {
                                proxy.scrollTo(lastMessage.id, anchor: .bottom)
                            }
                        }
                    }
                }
                
                Divider()
                
                // Status bar
                HStack {
                    Image(systemName: chatbot.isProcessing ? "circle.fill" : "circle")
                        .foregroundColor(chatbot.isProcessing ? .yellow : .gray)
                    
                    Text(chatbot.statusMessage)
                        .font(.caption)
                        .foregroundColor(.secondary)
                    
                    Spacer()
                }
                .padding(.horizontal)
                .padding(.vertical, 8)
                .background(Color(.systemGray6))
                
                // Input area
                VStack(spacing: 12) {
                    HStack(spacing: 12) {
                        TextField("Type a message...", text: $userInput)
                            .textFieldStyle(RoundedBorderTextFieldStyle())
                            .onSubmit {
                                sendMessage()
                            }
                        
                        Button(action: sendMessage) {
                            Image(systemName: "paperplane.fill")
                                .foregroundColor(.white)
                                .frame(width: 36, height: 36)
                                .background(userInput.isEmpty ? Color.gray : Color.blue)
                                .cornerRadius(18)
                        }
                        .disabled(userInput.isEmpty)
                    }
                    
                    // Voice controls
                    HStack(spacing: 20) {
                        Button(action: toggleListening) {
                            VStack {
                                Image(systemName: isListening ? "mic.fill" : "mic")
                                    .font(.system(size: 24))
                                    .foregroundColor(.white)
                                    .frame(width: 60, height: 60)
                                    .background(isListening ? Color.red : Color.blue)
                                    .cornerRadius(30)
                                
                                Text(isListening ? "Stop" : "Listen")
                                    .font(.caption)
                                    .foregroundColor(.secondary)
                            }
                        }
                        
                        Button(action: showReminders) {
                            VStack {
                                Image(systemName: "bell.fill")
                                    .font(.system(size: 24))
                                    .foregroundColor(.white)
                                    .frame(width: 60, height: 60)
                                    .background(Color.orange)
                                    .cornerRadius(30)
                                
                                Text("Reminders")
                                    .font(.caption)
                                    .foregroundColor(.secondary)
                            }
                        }
                        
                        Button(action: clearHistory) {
                            VStack {
                                Image(systemName: "trash.fill")
                                    .font(.system(size: 24))
                                    .foregroundColor(.white)
                                    .frame(width: 60, height: 60)
                                    .background(Color.gray)
                                    .cornerRadius(30)
                                
                                Text("Clear")
                                    .font(.caption)
                                    .foregroundColor(.secondary)
                            }
                        }
                    }
                }
                .padding()
            }
            .navigationTitle("Jared Assistant")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: showSettings) {
                        Image(systemName: "gearshape.fill")
                    }
                }
            }
        }
        .onAppear {
            speechManager.chatbot = chatbot
            requestPermissions()
        }
    }
    
    private func sendMessage() {
        guard !userInput.isEmpty else { return }
        
        let message = userInput
        userInput = ""
        
        Task {
            await chatbot.sendMessage(message)
            if let response = chatbot.messages.last, response.sender != "You" {
                speechManager.speak(response.text)
            }
        }
    }
    
    private func toggleListening() {
        if isListening {
            speechManager.stopListening()
            isListening = false
        } else {
            isListening = true
            speechManager.startListening { recognizedText in
                if let text = recognizedText {
                    userInput = text
                    sendMessage()
                }
                isListening = false
            }
        }
    }
    
    private func showReminders() {
        chatbot.showReminders()
    }
    
    private func clearHistory() {
        chatbot.clearHistory()
    }
    
    private func showSettings() {
        // Settings implementation
    }
    
    private func requestPermissions() {
        speechManager.requestSpeechRecognitionPermission()
    }
}

struct MessageBubble: View {
    let message: ChatMessage
    
    var body: some View {
        HStack {
            if message.sender == "You" {
                Spacer()
            }
            
            VStack(alignment: message.sender == "You" ? .trailing : .leading, spacing: 4) {
                Text(message.sender)
                    .font(.caption)
                    .fontWeight(.bold)
                    .foregroundColor(.secondary)
                
                Text(message.text)
                    .padding(12)
                    .background(message.sender == "You" ? Color.blue : Color(.systemGray5))
                    .foregroundColor(message.sender == "You" ? .white : .primary)
                    .cornerRadius(16)
                
                Text(message.timestamp, style: .time)
                    .font(.caption2)
                    .foregroundColor(.secondary)
            }
            .frame(maxWidth: 280, alignment: message.sender == "You" ? .trailing : .leading)
            
            if message.sender != "You" {
                Spacer()
            }
        }
    }
}

#Preview {
    ContentView()
}
