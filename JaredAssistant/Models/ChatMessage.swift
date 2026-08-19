//
//  ChatMessage.swift
//  Jared Assistant
//
//  Message model for chat conversations
//

import Foundation

struct ChatMessage: Identifiable, Codable {
    let id: UUID
    let sender: String
    let text: String
    let timestamp: Date
    
    init(sender: String, text: String) {
        self.id = UUID()
        self.sender = sender
        self.text = text
        self.timestamp = Date()
    }
}
