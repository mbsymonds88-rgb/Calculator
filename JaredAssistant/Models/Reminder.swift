//
//  Reminder.swift
//  Jared Assistant
//
//  Reminder model for scheduled notifications
//

import Foundation

struct Reminder: Identifiable, Codable {
    let id: UUID
    var text: String
    var time: Date
    var completed: Bool
    
    init(text: String, time: Date) {
        self.id = UUID()
        self.text = text
        self.time = time
        self.completed = false
    }
}
