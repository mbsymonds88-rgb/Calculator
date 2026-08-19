//
//  ReminderManager.swift
//  Jared Assistant
//
//  Manages reminders and notifications
//

import Foundation
import UserNotifications

class ReminderManager: ObservableObject {
    @Published var reminders: [Reminder] = []
    
    init() {
        loadReminders()
        requestNotificationPermission()
    }
    
    func requestNotificationPermission() {
        UNUserNotificationCenter.current().requestAuthorization(options: [.alert, .sound, .badge]) { granted, error in
            if granted {
                print("Notification permission granted")
            } else if let error = error {
                print("Notification permission error: \(error)")
            }
        }
    }
    
    func addReminder(text: String, time: Date) {
        let reminder = Reminder(text: text, time: time)
        reminders.append(reminder)
        scheduleNotification(for: reminder)
        saveReminders()
    }
    
    func completeReminder(_ reminder: Reminder) {
        if let index = reminders.firstIndex(where: { $0.id == reminder.id }) {
            reminders[index].completed = true
            cancelNotification(for: reminder)
            saveReminders()
        }
    }
    
    func deleteReminder(_ reminder: Reminder) {
        reminders.removeAll { $0.id == reminder.id }
        cancelNotification(for: reminder)
        saveReminders()
    }
    
    func getPendingReminders() -> [Reminder] {
        return reminders.filter { !$0.completed && $0.time > Date() }
    }
    
    private func scheduleNotification(for reminder: Reminder) {
        let content = UNMutableNotificationContent()
        content.title = "Reminder"
        content.body = reminder.text
        content.sound = .default
        
        let triggerDate = Calendar.current.dateComponents([.year, .month, .day, .hour, .minute], from: reminder.time)
        let trigger = UNCalendarNotificationTrigger(dateMatching: triggerDate, repeats: false)
        
        let request = UNNotificationRequest(identifier: reminder.id.uuidString, content: content, trigger: trigger)
        
        UNUserNotificationCenter.current().add(request) { error in
            if let error = error {
                print("Error scheduling notification: \(error)")
            }
        }
    }
    
    private func cancelNotification(for reminder: Reminder) {
        UNUserNotificationCenter.current().removePendingNotificationRequests(withIdentifiers: [reminder.id.uuidString])
    }
    
    private func loadReminders() {
        if let data = UserDefaults.standard.data(forKey: "reminders"),
           let savedReminders = try? JSONDecoder().decode([Reminder].self, from: data) {
            reminders = savedReminders
        }
    }
    
    private func saveReminders() {
        if let data = try? JSONEncoder().encode(reminders) {
            UserDefaults.standard.set(data, forKey: "reminders")
        }
    }
}
