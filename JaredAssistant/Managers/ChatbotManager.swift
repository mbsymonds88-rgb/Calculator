//
//  ChatbotManager.swift
//  Jared Assistant
//
//  Manages chatbot conversations and OpenAI integration
//

import Foundation

@MainActor
class ChatbotManager: ObservableObject {
    @Published var messages: [ChatMessage] = []
    @Published var statusMessage = "Ready"
    @Published var isProcessing = false
    
    private let apiKey: String
    private let model = "gpt-4o-mini"
    private let maxHistoryMessages = 300
    
    private var conversationHistory: [[String: String]] = []
    
    init() {
        // Load API key from environment or UserDefaults
        self.apiKey = UserDefaults.standard.string(forKey: "openai_api_key") ?? ""
        loadHistory()
        
        // Add welcome message
        if messages.isEmpty {
            addMessage(sender: "Jared", text: "Hello! I'm Jared, your AI assistant. How can I help you today?")
        }
    }
    
    func sendMessage(_ text: String) async {
        // Add user message
        addMessage(sender: "You", text: text)
        
        // Check for local commands first
        if let response = handleLocalCommand(text) {
            addMessage(sender: "Jared", text: response)
            return
        }
        
        // Send to OpenAI
        isProcessing = true
        statusMessage = "Processing..."
        
        conversationHistory.append(["role": "user", "content": text])
        
        do {
            let response = try await sendToOpenAI()
            addMessage(sender: "Jared", text: response)
            conversationHistory.append(["role": "assistant", "content": response])
            
            // Trim history
            if conversationHistory.count > maxHistoryMessages {
                conversationHistory = Array(conversationHistory.suffix(maxHistoryMessages))
            }
            
            saveHistory()
        } catch {
            addMessage(sender: "System", text: "Error: \(error.localizedDescription)")
        }
        
        isProcessing = false
        statusMessage = "Ready"
    }
    
    private func sendToOpenAI() async throws -> String {
        guard !apiKey.isEmpty else {
            return "Please set your OpenAI API key in Settings."
        }
        
        let url = URL(string: "https://api.openai.com/v1/chat/completions")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let systemMessage = [
            "role": "system",
            "content": """
            You are Jared, a friendly, helpful, and concise AI assistant.
            
            Rules:
            - Answer questions naturally and clearly
            - Use previous conversation history when relevant
            - Remember useful details the user has told you
            - If a request is unclear, ask a helpful question
            - Keep responses reasonably short
            - Be friendly and conversational
            """
        ]
        
        let messages = [systemMessage] + conversationHistory
        
        let body: [String: Any] = [
            "model": model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 500
        ]
        
        request.httpBody = try JSONSerialization.data(withJSONObject: body)
        
        let (data, _) = try await URLSession.shared.data(for: request)
        let response = try JSONDecoder().decode(OpenAIResponse.self, from: data)
        
        return response.choices.first?.message.content ?? "I received an empty response."
    }
    
    private func handleLocalCommand(_ text: String) -> String? {
        let lowercased = text.lowercased().trimmingCharacters(in: .whitespaces)
        
        // Time
        if lowercased == "time" || lowercased == "what time is it" {
            let formatter = DateFormatter()
            formatter.timeStyle = .short
            return "The current time is \(formatter.string(from: Date()))."
        }
        
        // Date
        if lowercased == "date" || lowercased.contains("today's date") {
            let formatter = DateFormatter()
            formatter.dateStyle = .long
            return "Today's date is \(formatter.string(from: Date()))."
        }
        
        // Help
        if lowercased == "help" {
            return """
            I can help you with:
            • General questions and conversations
            • Setting reminders
            • Getting current time and date
            • Various tasks and queries
            
            Just ask me anything!
            """
        }
        
        // Clear history
        if lowercased.contains("clear") && (lowercased.contains("history") || lowercased.contains("chat")) {
            clearHistory()
            return "I've cleared our conversation history."
        }
        
        return nil
    }
    
    func showReminders() {
        // Implementation for showing reminders
        addMessage(sender: "System", text: "Reminders feature coming soon!")
    }
    
    func clearHistory() {
        messages.removeAll()
        conversationHistory.removeAll()
        saveHistory()
        addMessage(sender: "Jared", text: "Conversation history cleared. How can I help you?")
    }
    
    private func addMessage(sender: String, text: String) {
        let message = ChatMessage(sender: sender, text: text)
        messages.append(message)
    }
    
    private func loadHistory() {
        if let data = UserDefaults.standard.data(forKey: "chat_history"),
           let history = try? JSONDecoder().decode([ChatMessage].self, from: data) {
            messages = Array(history.suffix(50)) // Load last 50 messages
        }
    }
    
    private func saveHistory() {
        if let data = try? JSONEncoder().encode(messages) {
            UserDefaults.standard.set(data, forKey: "chat_history")
        }
    }
}

// OpenAI API Response Models
struct OpenAIResponse: Codable {
    let choices: [Choice]
    
    struct Choice: Codable {
        let message: Message
        
        struct Message: Codable {
            let content: String
        }
    }
}
