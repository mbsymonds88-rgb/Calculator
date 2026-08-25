import asyncio
import base64
import datetime
import html
import threading
import uuid
from PySide6.QtCore import QTimer
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from winrt.windows.media.speechrecognition import (
    SpeechRecognizer,
    SpeechRecognitionResultStatus,
)

from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QTabWidget,
)

# Import Cherry's widget
from cherry_tab_widget import CherryWidget


# =========================================================
# Configuration
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


# Only these locations are searched for folders.
SEARCH_ROOTS = [
    Path.home() / "Desktop",
    Path.home() / "Documents",
    Path.home() / "Downloads",
    Path.home() / "Pictures",
    Path.home() / "Videos",
    Path.home() / "Music",
]


# Common Windows folders.
SPECIAL_FOLDERS = {
    "desktop": Path.home() / "Desktop",
    "documents": Path.home() / "Documents",
    "downloads": Path.home() / "Downloads",
    "pictures": Path.home() / "Pictures",
    "videos": Path.home() / "Videos",
    "music": Path.home() / "Music",
}


# Only applications in this list can be opened.
# Add applications carefully.
ALLOWED_APPLICATIONS = {
    "calculator": "calc.exe",
    "calc": "calc.exe",

    "notepad": "notepad.exe",
    "text editor": "notepad.exe",

    "paint": "mspaint.exe",
    "microsoft paint": "mspaint.exe",

    "task manager": "taskmgr.exe",

    "command prompt": "cmd.exe",
    "cmd": "cmd.exe",

    "powershell": "powershell.exe",

    "file explorer": "explorer.exe",
    "explorer": "explorer.exe",

    "settings": "ms-settings:",
}


# =========================================================
# Folder and application functions
# =========================================================

def search_for_folders(folder_name, maximum_results=10):
    """
    Search approved folders for directories matching folder_name.
    """
    folder_name = folder_name.lower().strip()

    if not folder_name:
        return []

    results = []

    for search_root in SEARCH_ROOTS:
        if not search_root.exists():
            continue

        try:
            for path in search_root.rglob("*"):
                if not path.is_dir():
                    continue

                if folder_name in path.name.lower():
                    results.append(path)

                    if len(results) >= maximum_results:
                        return results

        except (PermissionError, OSError):
            # Ignore folders that Windows does not allow us to access.
            continue

    return results


def open_folder(folder_path):
    """
    Open a folder in Windows File Explorer.
    """
    try:
        folder_path = Path(folder_path).expanduser().resolve()

        if not folder_path.exists():
            return f"I could not find the folder: {folder_path}"

        if not folder_path.is_dir():
            return f"This is not a folder: {folder_path}"

        os.startfile(str(folder_path))
        return f"Opening {folder_path.name}."

    except Exception as error:
        return f"I could not open that folder. Error: {error}"


def find_and_open_folder(folder_name):
    """
    Find a folder by name and open it if there is only one match.
    """
    folder_name = folder_name.lower().strip()

    # Open common folders directly.
    if folder_name in SPECIAL_FOLDERS:
        return open_folder(SPECIAL_FOLDERS[folder_name])

    matches = search_for_folders(folder_name)

    if not matches:
        return f"I could not find a folder named {folder_name}."

    if len(matches) == 1:
        return open_folder(matches[0])

    match_list = "\n".join(
        f"{index}. {path}"
        for index, path in enumerate(matches, start=1)
    )

    return (
        f"I found multiple folders matching '{folder_name}':\n"
        f"{match_list}\n\n"
        "Please say the full path of the folder you want to open."
    )


def open_application(application_name):
    """
    Open an application from ALLOWED_APPLICATIONS.
    """
    application_name = application_name.lower().strip()
    command = ALLOWED_APPLICATIONS.get(application_name)

    if not command:
        allowed_apps = ", ".join(
            sorted(ALLOWED_APPLICATIONS.keys())
        )

        return (
            f"I am not allowed to open '{application_name}'. "
            f"Approved applications include: {allowed_apps}."
        )

    try:
        # Handles Windows URI commands such as ms-settings:
        if command.endswith(":"):
            os.startfile(command)
            return f"Opening {application_name}."

        executable = shutil.which(command)

        # Also allow a full executable path.
        if not executable and Path(command).exists():
            executable = command

        if not executable:
            return (
                f"I could not find the application executable "
                f"'{command}'."
            )

        subprocess.Popen([executable])
        return f"Opening {application_name}."

    except Exception as error:
        return (
            f"I could not open {application_name}. "
            f"Error: {error}"
        )


def clean_folder_name(folder_name):
    """
    Remove words that are commonly included in spoken commands.
    """
    folder_name = folder_name.strip()

    folder_name = re.sub(
        r"^(the|my)\s+",
        "",
        folder_name,
        flags=re.IGNORECASE,
    )

    folder_name = re.sub(
        r"\s+folder$",
        "",
        folder_name,
        flags=re.IGNORECASE,
    )

    return folder_name.strip()


def clean_application_name(application_name):
    """
    Remove optional words such as 'app' or 'application'.
    """
    application_name = application_name.strip()

    application_name = re.sub(
        r"^(the)\s+",
        "",
        application_name,
        flags=re.IGNORECASE,
    )

    application_name = re.sub(
        r"\s+(application|app|program)$",
        "",
        application_name,
        flags=re.IGNORECASE,
    )

    return application_name.strip()


class ReminderManager:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.reminders = self.load_reminders()

    def load_reminders(self):
        if not self.file_path.exists():
            return []

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                reminders = json.load(file)

            if isinstance(reminders, list):
                return reminders

        except Exception as error:
            print(f"Could not load reminders: {error}")

        return []

    def save_reminders(self):
        try:
            temporary_path = self.file_path.with_suffix(".tmp")

            with temporary_path.open("w", encoding="utf-8") as file:
                json.dump(
                    self.reminders,
                    file,
                    ensure_ascii=False,
                    indent=2,
                )

            temporary_path.replace(self.file_path)

        except Exception as error:
            print(f"Could not save reminders: {error}")

    def add_reminder(self, text, reminder_time):
        reminder = {
            "id": str(uuid.uuid4())[:8],
            "text": text,
            "time": reminder_time.isoformat(timespec="seconds"),
            "completed": False,
        }

        self.reminders.append(reminder)
        self.save_reminders()

        return reminder

    def get_pending_reminders(self):
        now = datetime.datetime.now().replace(microsecond=0)
        due_reminders = []

        for reminder in self.reminders:
            if reminder.get("completed"):
                continue

            try:
                reminder_time = datetime.datetime.fromisoformat(
                    reminder["time"]
                )

                if reminder_time <= now:
                    due_reminders.append(reminder)

            except (KeyError, ValueError):
                continue

        return due_reminders

    def complete_reminder(self, reminder_id):
        for reminder in self.reminders:
            if reminder.get("id") == reminder_id:
                reminder["completed"] = True
                self.save_reminders()
                return True

        return False

    def list_reminders(self):
        active = [
            reminder
            for reminder in self.reminders
            if not reminder.get("completed")
        ]

        if not active:
            return "You have no active reminders."

        lines = []

        for index, reminder in enumerate(active, start=1):
            try:
                reminder_time = datetime.datetime.fromisoformat(
                    reminder["time"]
                ).strftime("%Y-%m-%d %H:%M")
            except (KeyError, ValueError):
                reminder_time = "unknown time"

            lines.append(
                f"{index}. {reminder['text']} — {reminder_time}"
            )

        return "\n".join(lines)

    def get_and_complete_due_reminders(self):
        due_reminders = self.get_pending_reminders()

        for reminder in due_reminders:
            reminder["completed"] = True

        if due_reminders:
            self.save_reminders()

        return due_reminders


# =========================================================
# Chatbot
# =========================================================

class Chatbot:
    def __init__(
        self,
        name="Jared",
        model="gpt-4.1-mini",
        history_file="chat_history.json",
        reminders_file="reminders.json",
        max_history_messages=300,
    ):
        self.name = name
        self.model = model
        self.max_history_messages = max_history_messages
        self.history_path = BASE_DIR / history_file

        self.reminder_manager = ReminderManager(
            BASE_DIR / reminders_file
        )

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key or not api_key.strip():
            raise RuntimeError(
                "OPENAI_API_KEY is not set."
            )


        if not api_key or not api_key.strip():
            raise RuntimeError(
                "OPENAI_API_KEY is not set."
            )


        if not api_key or not api_key.strip():
            raise RuntimeError(
                "OPENAI_API_KEY is not set. "
                "Add it to your .env file."
            )

        self.client = OpenAI(api_key=api_key.strip())

        self.instructions = f"""
You are {self.name}, a friendly, helpful, and concise AI chatbot.

Rules:
- Your name is {self.name}.
- Answer general questions naturally and clearly.
- Use previous conversation history when relevant.
- Remember useful details the user has told you.
- If a request is unclear, ask a helpful question.
- Do not claim to perform an action unless the program actually performed it.
- Keep casual responses reasonably short.
"""


        self.conversation = self.load_history()

    def load_history(self):
        if not self.history_path.exists():
            return []

        try:
            with self.history_path.open(
                "r",
                encoding="utf-8",
            ) as file:
                history = json.load(file)

            if not isinstance(history, list):
                return []

            valid_messages = []

            for message in history:
                if (
                    isinstance(message, dict)
                    and message.get("role")
                    in {"user", "assistant"}
                    and isinstance(message.get("content"), str)
                ):
                    valid_messages.append(
                        {
                            "role": message["role"],
                            "content": message["content"],
                        }
                    )

            valid_messages = valid_messages[
                -self.max_history_messages:
            ]

            print(
                f"Loaded {len(valid_messages)} previous messages.",
                flush=True,
            )

            return valid_messages

        except json.JSONDecodeError:
            print(
                "The chat history file is corrupted. "
                "Starting a new conversation.",
                flush=True,
            )
            return []

        except Exception as error:
            print(f"Could not load chat history: {error}", flush=True)
            return []

    def save_history(self):
        try:
            temporary_path = self.history_path.with_suffix(".tmp")

            history_to_save = self.conversation[
                -self.max_history_messages:
            ]

            with temporary_path.open(
                "w",
                encoding="utf-8",
            ) as file:
                json.dump(
                    history_to_save,
                    file,
                    ensure_ascii=False,
                    indent=2,
                )

            temporary_path.replace(self.history_path)

        except Exception as error:
            print(f"Could not save chat history: {error}", flush=True)

    def clear_history(self):
        self.conversation = []
        self.save_history()

    def _normalize_reminder_message(self, message):
        cleaned = message.strip().lower()
        cleaned = re.sub(r"[,.!?;]", "", cleaned)
        cleaned = re.sub(r"\s+", " ", cleaned)
        return cleaned

    def _word_to_int(self, value):
        value = value.strip().lower()

        if value.isdigit():
            return int(value)

        word_numbers = {
            "a": 1,
            "an": 1,
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
            "ten": 10,
            "eleven": 11,
            "twelve": 12,
            "fifteen": 15,
            "twenty": 20,
            "thirty": 30,
            "forty": 40,
            "forty five": 45,
            "forty-five": 45,
            "fortyfive": 45,
            "half": 30,
        }

        return word_numbers.get(value)

    def _parse_reminder_time(self, time_text):
        """Parse spoken reminder times into a datetime."""
        time_text = time_text.strip().lower()
        time_text = re.sub(r"[,.!?;]", "", time_text)
        time_text = re.sub(r"\s+", " ", time_text)
        now = datetime.datetime.now()

        match = re.match(
            r"^(?:in\s+)?(?:(\d+)|([a-z-]+))\s+minutes?$",
            time_text,
        )
        if match:
            minutes = self._word_to_int(
                match.group(1) or match.group(2)
            )
            if minutes is not None:
                return now + datetime.timedelta(minutes=minutes)

        match = re.match(
            r"^(?:in\s+)?(?:(\d+)|([a-z-]+))\s+hours?$",
            time_text,
        )
        if match:
            hours = self._word_to_int(
                match.group(1) or match.group(2)
            )
            if hours is not None:
                return now + datetime.timedelta(hours=hours)

        match = re.match(
            r"^(?:at\s+)?(\d{1,2})(?::(\d{2}))?\s*(am|pm)?$",
            time_text,
        )
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2) or 0)
            meridiem = match.group(3)

            if meridiem == "pm" and hour != 12:
                hour += 12
            elif meridiem == "am" and hour == 12:
                hour = 0

            reminder_time = now.replace(
                hour=hour,
                minute=minute,
                second=0,
                microsecond=0,
            )

            if reminder_time <= now:
                reminder_time += datetime.timedelta(days=1)

            return reminder_time

        match = re.match(
            r"^tomorrow\s+(?:at\s+)?(\d{1,2})(?::(\d{2}))?\s*(am|pm)?$",
            time_text,
        )
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2) or 0)
            meridiem = match.group(3)

            if meridiem == "pm" and hour != 12:
                hour += 12
            elif meridiem == "am" and hour == 12:
                hour = 0

            tomorrow = now.date() + datetime.timedelta(days=1)
            return datetime.datetime.combine(
                tomorrow,
                datetime.time(hour, minute),
            )

        return None

    def _save_reminder(self, reminder_text, reminder_time):
        reminder = self.reminder_manager.add_reminder(
            reminder_text,
            reminder_time,
        )

        formatted_time = reminder_time.strftime(
            "%Y-%m-%d %H:%M"
        )

        return (
            f"Reminder set: {reminder['text']} at {formatted_time}.",
            True,
        )

    def handle_reminder_command(self, message):
        """
        Handle reminder-related commands locally.

        Returns:
            response, handled
        """
        cleaned_message = message.strip().lower()

        if cleaned_message in {
            "list reminders",
            "show reminders",
            "my reminders",
            "what are my reminders",
        }:
            return self.reminder_manager.list_reminders(), True

        match = re.match(
            r"^(?:complete|dismiss|mark)\s+reminder\s+(\d+)$",
            cleaned_message,
        )
        if match:
            index = int(match.group(1))
            active = [
                reminder
                for reminder in self.reminder_manager.reminders
                if not reminder.get("completed")
            ]

            if index < 1 or index > len(active):
                return (
                    f"I could not find reminder number {index}.",
                    True,
                )

            reminder = active[index - 1]
            self.reminder_manager.complete_reminder(reminder["id"])
            return (
                f"Marked reminder '{reminder['text']}' as complete.",
                True,
            )

        match = re.match(
            r"^(?:remind me to|reminder to|schedule)\s+(.+?)\s+at "
            r"(\d{4}-\d{2}-\d{2})\s+(\d{1,2}):(\d{2})$",
            cleaned_message,
            flags=re.IGNORECASE,
        )
        if match:
            reminder_text = match.group(1).strip()
            date_text = match.group(2)
            hour = int(match.group(3))
            minute = int(match.group(4))

            try:
                reminder_time = datetime.datetime.strptime(
                    f"{date_text} {hour:02d}:{minute:02d}",
                    "%Y-%m-%d %H:%M",
                )
            except ValueError:
                return (
                    "I could not understand that reminder date and time.",
                    True,
                )

            if not reminder_text:
                return (
                    "Please tell me what you want to be reminded about.",
                    True,
                )

            reminder = self.reminder_manager.add_reminder(
                reminder_text,
                reminder_time,
            )

            formatted_time = reminder_time.strftime(
                "%Y-%m-%d %H:%M"
            )

            return (
                f"Reminder set: {reminder['text']} at {formatted_time}.",
                True,
            )

        match = re.match(
            r"^(?:remind me to|set a reminder to|set reminder to)\s+"
            r"(.+?)\s+(?:at|in|on|for)\s+(.+)$",
            cleaned_message,
        )
        if match:
            reminder_text = match.group(1).strip()
            time_text = match.group(2).strip()
            reminder_time = self._parse_reminder_time(time_text)

            if not reminder_text:
                return (
                    "Please tell me what you want to be reminded about.",
                    True,
                )

            if reminder_time is None:
                return (
                    "I could not understand that reminder time. "
                    "Try something like 'in 30 minutes' or 'at 5pm'.",
                    True,
                )

            reminder = self.reminder_manager.add_reminder(
                reminder_text,
                reminder_time,
            )

            formatted_time = reminder_time.strftime(
                "%Y-%m-%d %H:%M"
            )

            return (
                f"Reminder set: {reminder['text']} at {formatted_time}.",
                True,
            )

        match = re.match(
            r"^(?:delete|remove|cancel)\s+reminder\s+([a-zA-Z0-9]+)$",
            cleaned_message,
            flags=re.IGNORECASE,
        )
        if match:
            reminder_id = match.group(1)

            for reminder in self.reminder_manager.reminders:
                if reminder.get("id") == reminder_id:
                    reminder["completed"] = True
                    self.reminder_manager.save_reminders()

                    return (
                        f"Reminder {reminder_id} was cancelled.",
                        True,
                    )

            return (
                f"I could not find reminder {reminder_id}.",
                True,
            )

        return None, False

    def handle_local_command(self, message):
        """
        Handle commands that should be executed locally instead of
        being sent to the AI model.

        Returns:
            response, handled
        """
        original_message = message.strip()
        cleaned_message = original_message.lower()

        # -----------------------------------------------------
        # Find folder
        # Examples:
        # find folder projects
        # search for my projects folder
        # look for downloads
        # -----------------------------------------------------

        match = re.match(
            r"^(find|search for|look for)\s+"
            r"(?:the\s+)?(?:my\s+)?(?:folder\s+)?(.+)$",
            cleaned_message,
        )

        if match:
            folder_name = clean_folder_name(match.group(2))
            matches = search_for_folders(folder_name)

            if not matches:
                return (
                    f"I could not find a folder named "
                    f"{folder_name}.",
                    True,
                )

            results = "\n".join(
                f"{index}. {path}"
                for index, path in enumerate(matches, start=1)
            )

            return results, True

        # -----------------------------------------------------
        # Open a folder by full Windows path
        # Example:
        # open C:\Users\Mathew\Documents
        # -----------------------------------------------------

        match = re.match(
            r"^(open|launch)\s+([a-zA-Z]:\\.+)$",
            original_message,
            flags=re.IGNORECASE,
        )

        if match:
            folder_path = match.group(2).strip()
            return open_folder(folder_path), True

        # -----------------------------------------------------
        # Open a named folder
        # Examples:
        # open the Downloads folder
        # open my projects folder
        # launch documents
        # -----------------------------------------------------

        match = re.match(
            r"^(open|launch)\s+"
            r"(?:the\s+)?(?:my\s+)?(.+?)(?:\s+folder)?$",
            cleaned_message,
        )

        if match:
            requested_name = clean_folder_name(match.group(2))

            # If this is a known special folder, open it.
            if requested_name in SPECIAL_FOLDERS:
                return (
                    open_folder(
                        SPECIAL_FOLDERS[requested_name]
                    ),
                    True,
                )

            # If it is not an approved application, try it as a folder.
            if requested_name not in ALLOWED_APPLICATIONS:
                return (
                    find_and_open_folder(requested_name),
                    True,
                )

        # -----------------------------------------------------
        # Open an approved application
        # Examples:
        # open calculator
        # launch notepad
        # start task manager
        # -----------------------------------------------------

        match = re.match(
            r"^(open|launch|start)\s+"
            r"(?:the\s+)?(.+)$",
            cleaned_message,
        )

        if match:
            application_name = clean_application_name(match.group(2))

            if application_name in ALLOWED_APPLICATIONS:
                return (
                    open_application(application_name),
                    True,
                )

        return None, False

    def get_response(self, message):
        cleaned_message = message.lower().strip()

        # Handle reminders before sending the request to OpenAI.
        reminder_response, reminder_handled = (
            self.handle_reminder_command(message)
        )

        if reminder_handled:
            return reminder_response, False

        if cleaned_message in {
            "bye",
            "goodbye",
            "exit",
            "quit",
            "stop",
        }:
            return "Goodbye! Have a great day.", True


        if cleaned_message in {
            "time",
            "what time is it",
            "current time",
        }:
            current_time = datetime.datetime.now().strftime(
                "%H:%M:%S"
            )
            return f"The current time is {current_time}.", False

        if cleaned_message in {
            "date",
            "what is today's date",
            "what date is it",
            "today",
        }:
            current_date = datetime.datetime.now().strftime(
                "%Y-%m-%d"
            )
            return f"Today's date is {current_date}.", False

        if cleaned_message == "help":
            return (
                "You can ask me general questions, manage reminders, find folders, "
                "open folders, or open approved applications.\n\n"
                "Reminder examples:\n"
                "- remind me to take medicine at 2026-05-20 09:30\n"
                "- schedule team meeting at 2026-05-21 14:00\n"
                "- show reminders"
            ), False

        if cleaned_message in {
            "clear history",
            "clear chat",
            "forget everything",
            "reset conversation",
        }:
            self.clear_history()
            return (
                "I have forgotten the previous conversation.",
                False,
            )

        # Try local computer-control commands first.
        local_response, was_handled = self.handle_local_command(
            message
        )

        if was_handled:
            return local_response, False

        # Send other requests to OpenAI.
        self.conversation.append(
            {
                "role": "user",
                "content": message,
            }
        )

        self.conversation = self.conversation[
            -self.max_history_messages:
        ]

        try:
            response = self.client.responses.create(
                model=self.model,
                instructions=self.instructions,
                input=self.conversation,
            )

            response_text = response.output_text.strip()

            if not response_text:
                response_text = (
                    "I received an empty response from the AI service."
                )

            self.conversation.append(
                {
                    "role": "assistant",
                    "content": response_text,
                }
            )

            self.conversation = self.conversation[
                -self.max_history_messages:
            ]

            self.save_history()

            return response_text, False

        except Exception as error:
            # Remove the user message if the API request failed.
            if (
                self.conversation
                and self.conversation[-1]["role"] == "user"
                and self.conversation[-1]["content"] == message
            ):
                self.conversation.pop()

            return (
                "Sorry, I could not connect to the AI service. "
                f"Error: {error}"
            ), False


# =========================================================
# Windows speech recognition
# =========================================================

class WindowsSpeechInput:
    def __init__(self):
        self.recognizer = SpeechRecognizer()
        self.constraints_compiled = False

    async def ensure_ready(self):
        if not self.constraints_compiled:
            await self.recognizer.compile_constraints_async()
            self.constraints_compiled = True

    async def listen_async(self, prompt="Listening..."):
        print(prompt, flush=True)

        try:
            await self.ensure_ready()

            result = await self.recognizer.recognize_async()

            if result.status == SpeechRecognitionResultStatus.SUCCESS:
                text = result.text.strip()

                if text:
                    print(f"You: {text}", flush=True)
                    return text

                print("No speech was recognized.", flush=True)
                return None

            if (
                result.status
                == SpeechRecognitionResultStatus.USER_GAVE_UP
            ):
                print("No speech was detected.", flush=True)

            elif (
                result.status
                == SpeechRecognitionResultStatus.SPEECH_ERROR
            ):
                print(
                    "Windows could not understand the speech.",
                    flush=True,
                )

            else:
                print(
                    f"Speech recognition failed: {result.status}",
                    flush=True,
                )

            return None

        except Exception as error:
            print(f"Speech recognition error: {error}", flush=True)
            return None

    def listen(self, prompt="Listening..."):
        return asyncio.run(self.listen_async(prompt))

    @staticmethod
    def normalize_text(text):
        text = text.lower().strip()
        text = re.sub(r"[,.!?;:]", "", text)
        text = re.sub(r"\s+", " ", text)
        return text

    def is_wake_phrase(self, text, bot_name):
        normalized_text = self.normalize_text(text)
        normalized_name = self.normalize_text(bot_name)

        wake_phrases = {
            f"hey {normalized_name}",
            f"hi {normalized_name}",
            f"{normalized_name}",
            f"bud",
            f"jerrod",
            f"hey jerrod",
            normalized_name,
        }

        return normalized_text in wake_phrases

    def listen_for_wake_phrase(self, bot_name):
        while True:
            text = self.listen(
                f"Waiting for 'Hey {bot_name}'..."
            )

            if not text:
                continue

            if self.is_wake_phrase(text, bot_name):
                print(
                    "Wake phrase detected. "
                    "Listening for your request...",
                    flush=True,
                )
                return

            print(
                f"Wake phrase not detected. "
                f"Please say 'Hey {bot_name}'.",
                flush=True,
            )


# =========================================================
# Windows text-to-speech
# =========================================================

class VoiceOutput:
    def __init__(self):
        print(
            "Initializing Windows text-to-speech...",
            flush=True,
        )

        self.voice_name = ""
        self.voice_token = ""

        command = r"""
Add-Type -AssemblyName System.Speech

$s = New-Object System.Speech.Synthesis.SpeechSynthesizer

$Mark = $s.GetInstalledVoices() |
    Where-Object {
        $_.VoiceInfo.Name -like "*Mark*"
    } |
    Select-Object -First 1

if ($Mark) {
    Write-Output "VOICE_NAME=$($Mark.VoiceInfo.Name)"
    Write-Output "VOICE_TOKEN=$($Mark.VoiceInfo.Id)"
}
else {
    Write-Output "VOICE_NOT_FOUND"
}

$s.Dispose()
"""

        try:
            result = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-Command",
                    command,
                ],
                capture_output=True,
                text=True,
                timeout=100,
            )

            if result.returncode != 0:
                raise RuntimeError(
                    result.stderr.strip()
                    or "Could not inspect Windows voices."
                )

            for line in result.stdout.strip().splitlines():
                if line.startswith("VOICE_NAME="):
                    self.voice_name = line.split(
                        "=", 1
                    )[1].strip()

                elif line.startswith("VOICE_TOKEN="):
                    self.voice_token = line.split(
                        "=", 1
                    )[1].strip()

            if self.voice_token:
                print(
                    f"Selected voice: {self.voice_name}",
                    flush=True,
                )
            else:
                print(
                    "Microsoft Mark was not found. "
                    "Windows will use its default voice.",
                    flush=True,
                )

            print(
                "Windows text-to-speech initialized.",
                flush=True,
            )

        except Exception as error:
            print(
                f"Text-to-speech setup error: {error}",
                flush=True,
            )

    def speak(self, text):
        text = str(text).strip()

        if not text:
            return

        encoded_text = base64.b64encode(
            text.encode("utf-8")
        ).decode("ascii")

        encoded_token = ""

        if self.voice_token:
            encoded_token = base64.b64encode(
                self.voice_token.encode("utf-8")
            ).decode("ascii")

        command = f"""
Add-Type -AssemblyName System.Speech

$textBytes = [Convert]::FromBase64String("{encoded_text}")
$text = [System.Text.Encoding]::UTF8.GetString($textBytes)

$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
$s.Volume = 100
$s.Rate = 0
"""

        if encoded_token:
            command += f"""
$tokenBytes = [Convert]::FromBase64String("{encoded_token}")
$token = [System.Text.Encoding]::UTF8.GetString($tokenBytes)

$selectedVoice = $s.GetInstalledVoices() |
    Where-Object {{
        $_.VoiceInfo.Id -eq $token
    }} |
    Select-Object -First 1

if ($selectedVoice) {{
    $s.SelectVoice($selectedVoice.VoiceInfo.Name)
}}

$s.Speak($text)
$s.Dispose()
"""
        else:
            command += """
$s.Speak($text)
$s.Dispose()
"""

        try:
            result = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-Command",
                    command,
                ],
                capture_output=True,
                text=True,
                timeout=60,
            )

            if result.returncode != 0:
                print(
                    "Speech playback error: "
                    f"{result.stderr.strip()}",
                    flush=True,
                )

        except subprocess.TimeoutExpired:
            print("Speech playback timed out.", flush=True)

        except Exception as error:
            print(
                f"Speech playback error: {error}",
                flush=True,
            )


# =========================================================
# PySide6 background worker
# =========================================================

class BotWorker(QObject):
    """
    Runs speech recognition, chatbot processing, and text-to-speech
    outside the GUI thread.
    """

    message_received = Signal(str, str)
    status_changed = Signal(str)
    error_occurred = Signal(str)
    finished = Signal()

    # These signals ensure worker methods are called safely inside
    # the worker thread rather than directly from the GUI thread.
    stop_requested = Signal()
    pause_requested = Signal()
    typed_command_requested = Signal(str)

    def __init__(
        self,
        chatbot,
        voice_output,
        speech_input,
    ):
        super().__init__()

        self.chatbot = chatbot
        self.voice_output = voice_output
        self.speech_input = speech_input

        self.running = True
        self.paused = False

        self.stop_requested.connect(self.stop)
        self.pause_requested.connect(self.toggle_pause)
        self.typed_command_requested.connect(
            self.process_typed_command
        )

    @Slot()
    def run(self):
        try:
            greeting = (
                "Hello Mathew. All systems online. "
                f"Say Hey {self.chatbot.name} when you want my attention."
            )

            if self.chatbot.conversation:
                greeting += (
                    " I also remember our previous conversation."
                )

            self.send_bot_message(greeting)

            while self.running:
                if self.paused:
                    self.status_changed.emit("Paused")
                    asyncio.run(asyncio.sleep(0.2))
                    continue

                self.status_changed.emit(
                    f"Waiting for 'Hey {self.chatbot.name}'..."
                )

                self.speech_input.listen_for_wake_phrase(
                    self.chatbot.name
                )

                if not self.running:
                    break

                self.status_changed.emit(
                    "Listening for your request..."
                )

                user_input = self.speech_input.listen(
                    "Speak your request now."
                )

                if not user_input:
                    self.status_changed.emit(
                        "No request detected. "
                        "Waiting for wake phrase."
                    )
                    continue

                self.message_received.emit(
                    "You",
                    user_input,
                )

                self.status_changed.emit("Processing...")

                response, should_exit = (
                    self.chatbot.get_response(user_input)
                )

                self.send_bot_message(response)

                if should_exit:
                    self.running = False
                    break

        except Exception as error:
            self.error_occurred.emit(
                f"Unexpected worker error: {error}"
            )

        finally:
            self.finished.emit()

    @Slot(str)
    def process_typed_command(self, user_input):
        if not self.running:
            return

        user_input = str(user_input).strip()

        if not user_input:
            return

        try:
            self.status_changed.emit("Processing...")

            response, should_exit = (
                self.chatbot.get_response(user_input)
            )

            self.send_bot_message(response)

            if should_exit:
                self.running = False

        except Exception as error:
            self.error_occurred.emit(
                f"Command processing error: {error}"
            )

    @Slot()
    def stop(self):
        self.running = False
        self.status_changed.emit("Stopping...")

    @Slot()
    def toggle_pause(self):
        self.paused = not self.paused

        if self.paused:
            self.status_changed.emit("Paused")
        else:
            self.status_changed.emit("Resuming...")

    def send_bot_message(self, text):
        text = str(text).strip()

        if not text:
            return

        self.message_received.emit(
            self.chatbot.name,
            text,
        )

        # TTS runs in the worker thread and will not freeze the GUI.
        self.voice_output.speak(text)


# =========================================================
# PySide6 GUI
# =========================================================

class MainWindow(QMainWindow):
    typed_command = Signal(str)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Jared Assistant")
        self.resize(850, 650)

        # =====================================================
        # Jared dark-blue interface theme
        # =====================================================
        self.setStyleSheet("""
    QMainWindow {
        background-color: #210A0F;
    }

    QWidget {
        color: #FFE5E5;
        font-family: Segoe UI;
        font-size: 14px;
    }

    QLabel {
        color: #FFD1D1;
        background-color: transparent;
    }

    QTextEdit {
        background-color: rgba(80, 15, 25, 230);
        color: #FFE5E5;
        border: 2px solid #9E2638;
        border-radius: 10px;
        padding: 8px;
        selection-background-color: #C24155;
        selection-color: white;
    }

    QLineEdit {
        background-color: rgba(65, 12, 20, 235);
        color: #FFE5E5;
        border: 2px solid #9E2638;
        border-radius: 10px;
        padding: 10px;
        selection-background-color: #C24155;
        selection-color: white;
    }

    QPushButton {
        background-color: #8B1E2D;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 9px 16px;
        min-width: 110px;
    }

    QPushButton:hover {
        background-color: #A52A3A;
    }

    QPushButton:pressed {
        background-color: #641522;
    }

    QPushButton:disabled {
        background-color: #4A252B;
        color: #BFA5A8;
    }
""")


        self.chatbot = None
        self.voice_output = None
        self.speech_input = None

        self.thread = None
        self.worker = None

        self.build_ui()
        self.initialize_bot()

        self.reminder_timer = QTimer(self)
        self.reminder_timer.timeout.connect(self.check_reminders)
        self.reminder_timer.start(1000)  # Check every second

    def check_reminders(self):
        if not self.chatbot:
            return

        due_reminders = (
            self.chatbot.reminder_manager
            .get_and_complete_due_reminders()
        )

        for reminder in due_reminders:
            message = f"Reminder: {reminder['text']}"

            self.append_message("Reminder", message)
            self.status_label.setText(message)

            # Speak the reminder if voice output is available.
            if self.voice_output:
                threading.Thread(
                    target=self.voice_output.speak,
                    args=(message,),
                    daemon=True,
                ).start()

    def build_ui(self):
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #9E2638;
                border-radius: 5px;
            }
            QTabBar::tab {
                background-color: #4A252B;
                color: #FFE5E5;
                padding: 10px 20px;
                margin: 2px;
                border-radius: 5px;
            }
            QTabBar::tab:selected {
                background-color: #8B1E2D;
                color: white;
            }
            QTabBar::tab:hover {
                background-color: #641522;
            }
        """)
        
        # Create Jared Assistant tab
        jared_tab = QWidget()
        jared_layout = QVBoxLayout(jared_tab)
        
        self.transcript = QTextEdit()
        self.transcript.setReadOnly(True)

        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText(
            "Type a command and press Enter..."
        )
        self.command_input.returnPressed.connect(
            self.submit_typed_command
        )

        self.status_label = QLabel("Initializing...")

        self.start_button = QPushButton("Start Listening")
        self.pause_button = QPushButton("Pause")
        self.stop_button = QPushButton("Stop")

        self.start_button.clicked.connect(self.start_bot)
        self.pause_button.clicked.connect(self.pause_bot)
        self.stop_button.clicked.connect(self.stop_bot)

        self.pause_button.setEnabled(False)
        self.stop_button.setEnabled(False)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.stop_button)

        jared_layout.addWidget(QLabel("Conversation"))
        jared_layout.addWidget(self.transcript)
        jared_layout.addWidget(self.command_input)
        jared_layout.addWidget(self.status_label)
        jared_layout.addLayout(button_layout)
        
        # Create Cherry's widget tab
        cherry_tab = CherryWidget()
        
        # Add tabs to tab widget
        self.tab_widget.addTab(jared_tab, "🎙️ Jared Assistant")
        self.tab_widget.addTab(cherry_tab, "🍒 Cherry's Orchard")
        
        self.setCentralWidget(self.tab_widget)

    def initialize_bot(self):
        try:
            self.append_message(
                "System",
                "Starting chatbot...",
            )

            self.chatbot = Chatbot(name="Jared")

            self.append_message(
                "System",
                "Chatbot initialized.",
            )

            self.voice_output = VoiceOutput()

            self.append_message(
                "System",
                "Voice output initialized.",
            )

            self.speech_input = WindowsSpeechInput()

            self.append_message(
                "System",
                "Speech input initialized.",
            )

            self.status_label.setText("Ready")

        except Exception as error:
            self.append_message(
                "Error",
                f"Bot setup failed: {error}",
            )

            self.status_label.setText("Initialization failed")
            self.start_button.setEnabled(False)
            self.command_input.setEnabled(False)

    def start_bot(self):
        if self.worker is not None:
            return

        if not self.chatbot:
            self.append_message(
                "Error",
                "The chatbot has not been initialized.",
            )
            return

        self.thread = QThread()
        self.worker = BotWorker(
            chatbot=self.chatbot,
            voice_output=self.voice_output,
            speech_input=self.speech_input,
        )

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(
            self.worker.run
        )

        self.worker.message_received.connect(
            self.append_message
        )

        self.worker.status_changed.connect(
            self.status_label.setText
        )

        self.worker.error_occurred.connect(
            self.show_worker_error
        )

        self.worker.finished.connect(
            self.thread.quit
        )

        self.worker.finished.connect(
            self.worker.deleteLater
        )

        self.thread.finished.connect(
            self.thread.deleteLater
        )

        self.thread.finished.connect(
            self.worker_finished
        )

        self.thread.start()

        self.start_button.setEnabled(False)
        self.pause_button.setEnabled(True)
        self.stop_button.setEnabled(True)

        self.append_message(
            "System",
            "Voice assistant started.",
        )

    def pause_bot(self):
        if self.worker:
            self.worker.pause_requested.emit()

            if self.worker.paused:
                self.pause_button.setText("Resume")
            else:
                self.pause_button.setText("Pause")

    def stop_bot(self):
        if self.worker:
            self.worker.stop_requested.emit()

    def submit_typed_command(self):
        text = self.command_input.text().strip()

        if not text:
            return

        self.command_input.clear()

        self.append_message(
            "You",
            text,
        )

        if self.worker:
            self.worker.typed_command_requested.emit(text)
            return

        # Process typed commands before voice mode starts.
        try:
            response, should_exit = (
                self.chatbot.get_response(text)
            )

            self.append_message(
                self.chatbot.name,
                response,
            )

            self.voice_output.speak(response)

            if should_exit:
                self.close()

        except Exception as error:
            self.show_worker_error(str(error))

    @Slot(str, str)
    def append_message(self, sender, message):
        sender_html = html.escape(str(sender))
        message_html = html.escape(str(message))
        message_html = message_html.replace("\n", "<br>")

        self.transcript.append(
            f"<b>{sender_html}:</b><br>"
            f"{message_html}<br>"
        )

    @Slot(str)
    def show_worker_error(self, error):
        self.append_message(
            "Error",
            error,
        )

        self.status_label.setText("Error")

    @Slot()
    def worker_finished(self):
        self.append_message(
            "System",
            "Assistant stopped.",
        )

        self.worker = None
        self.thread = None

        self.start_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        self.pause_button.setText("Pause")

        self.status_label.setText("Stopped")

    def closeEvent(self, event):
        if self.worker:
            self.worker.stop_requested.emit()

        if self.thread and self.thread.isRunning():
            self.thread.quit()
            self.thread.wait(3000)

        event.accept()


# =========================================================
# Main program
# =========================================================

def main():
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
