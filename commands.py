import json
import os
import webbrowser
from datetime import datetime
from urllib.parse import quote

from config import ASSISTANT_NAME, NOTES_FILE, HISTORY_FILE


# --------------------------------------------------
# Website list
# --------------------------------------------------

WEBSITES = {
    "gemini": "https://gemini.google.com/",
    "chatgpt": "https://chatgpt.com/",
    "google": "https://www.google.com/",
    "youtube": "https://www.youtube.com/",
    "instagram": "https://www.instagram.com/",
    "facebook": "https://www.facebook.com/",
    "github": "https://github.com/",
    "gmail": "https://mail.google.com/",
    "whatsapp": "https://web.whatsapp.com/",
    "reddit": "https://www.reddit.com/",
    "linkedin": "https://www.linkedin.com/",
    "stackoverflow": "https://stackoverflow.com/",
    "wikipedia": "https://www.wikipedia.org/"
}


# --------------------------------------------------
# JSON file functions
# --------------------------------------------------

def load_json_file(filename, default_value):
    try:
        if not os.path.exists(filename):
            save_json_file(filename, default_value)
            return default_value

        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data

    except json.JSONDecodeError:
        save_json_file(filename, default_value)
        return default_value

    except Exception:
        return default_value


def save_json_file(filename, data):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    except Exception as error:
        print("Could not save file:", error)


# --------------------------------------------------
# History functions
# --------------------------------------------------

def add_to_history(command):
    history = load_json_file(HISTORY_FILE, [])

    if not isinstance(history, list):
        history = []

    history.append(command)
    save_json_file(HISTORY_FILE, history)


def show_history():
    history = load_json_file(HISTORY_FILE, [])

    if not history:
        return "Your command history is empty."

    result = "Command history:\n"

    for number, command in enumerate(history, start=1):
        result += f"{number}. {command}\n"

    return result.rstrip()


def clear_history():
    save_json_file(HISTORY_FILE, [])
    return "Command history cleared."


# --------------------------------------------------
# Notes functions
# --------------------------------------------------

def add_note(note):
    if not note:
        return "Please provide a note."

    notes = load_json_file(NOTES_FILE, [])

    if not isinstance(notes, list):
        notes = []

    notes.append(note)
    save_json_file(NOTES_FILE, notes)

    return "Note saved successfully."


def show_notes():
    notes = load_json_file(NOTES_FILE, [])

    if not notes:
        return "You do not have any saved notes."

    result = "Your notes:\n"

    for number, note in enumerate(notes, start=1):
        result += f"{number}. {note}\n"

    return result.rstrip()


def clear_notes():
    save_json_file(NOTES_FILE, [])
    return "All notes have been cleared."


# --------------------------------------------------
# Website functions
# --------------------------------------------------

def open_website(website_name):
    website_name = website_name.lower().strip()

    if not website_name:
        return "Please specify a website."

    if website_name in WEBSITES:
        webbrowser.open(WEBSITES[website_name])
        return f"Opening {website_name}."

    if "." in website_name:
        url = website_name

        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        webbrowser.open(url)
        return f"Opening {website_name}."

    return (
        f"I do not know the website '{website_name}'. "
        "Try using a complete domain such as example.com."
    )


def search_google(query):
    if not query:
        return "Please provide something to search."

    encoded_query = quote(query)
    url = "https://www.google.com/search?q=" + encoded_query

    webbrowser.open(url)

    return f"Opening Google search for: {query}"


def search_youtube(query):
    if not query:
        return "Please provide something to search on YouTube."

    encoded_query = quote(query)
    url = "https://www.youtube.com/results?search_query=" + encoded_query

    webbrowser.open(url)

    return f"Opening YouTube search for: {query}"


def search_gemini(query):
    if not query:
        return "Please provide a request for Gemini."

    encoded_query = quote(query)
    url = "https://gemini.google.com/app?q=" + encoded_query

    webbrowser.open(url)

    return (
        "Opening Gemini with your request. "
        "If it is not submitted automatically, press Send."
    )


def search_chatgpt(query):
    if not query:
        return "Please provide a request for ChatGPT."

    encoded_query = quote(query)
    url = "https://chatgpt.com/?q=" + encoded_query

    webbrowser.open(url)

    return (
        "Opening ChatGPT with your request. "
        "If it is not submitted automatically, press Send."
    )


# --------------------------------------------------
# Calculator
# --------------------------------------------------

def calculate(expression):
    if not expression:
        return "Please provide a mathematical expression."

    allowed_characters = "0123456789+-*/().% "

    for character in expression:
        if character not in allowed_characters:
            return "The calculator only supports basic arithmetic."

    try:
        result = eval(expression, {"__builtins__": None}, {})
        return f"Result: {result}"

    except ZeroDivisionError:
        return "You cannot divide by zero."

    except Exception:
        return "I could not calculate that expression."


# --------------------------------------------------
# Time and date
# --------------------------------------------------

def get_time():
    current_time = datetime.now().strftime("%I:%M %p")
    return f"The current time is {current_time}."


def get_date():
    current_date = datetime.now().strftime("%A, %d %B %Y")
    return f"Today is {current_date}."


# --------------------------------------------------
# Help
# --------------------------------------------------

def get_help():
    return """
Available commands:

General:
- hello
- hi
- how are you
- help
- exit
- quit
- stop

Time and date:
- what time is it
- time
- what is today's date
- date

Notes:
- add note Your note
- show notes
- clear notes

History:
- history
- clear history

Calculator:
- calculate 25 * 4
- calculate (10 + 5) / 3

Websites:
- open gemini
- open chatgpt
- open google
- open youtube
- open github
- open example.com

Search:
- search google for Python tutorials
- search youtube for Arduino projects
- search this in gemini explain nuclear fusion
- search this in chatgpt write a Python program
""".strip()


# --------------------------------------------------
# Main command processor
# --------------------------------------------------

def process_command(user_command):
    original_command = user_command.strip()
    command = original_command.lower()

    if not original_command:
        return "Please enter a command."

    add_to_history(original_command)

    # Greetings
    if command in ["hello", "hi", "hey", "hey friday"]:
        return "Hello sir. How can I help you?"

    if command in ["how are you", "how are you friday"]:
        return "I am functioning properly, sir."

    # Help
    if command in ["help", "commands", "what can you do"]:
        return get_help()

    # Exit
    if command in ["exit", "quit", "stop"]:
        return "Goodbye sir."

    # Time
    if command in ["time", "what time is it", "tell me the time"]:
        return get_time()

    # Date
    if command in [
        "date",
        "what is today's date",
        "what is todays date",
        "tell me the date"
    ]:
        return get_date()

    # Notes
    if command.startswith("add note "):
        note = original_command[len("add note "):].strip()
        return add_note(note)

    if command in ["show notes", "list notes", "read notes"]:
        return show_notes()

    if command in ["clear notes", "delete notes", "remove notes"]:
        return clear_notes()

    # History
    if command in ["history", "show history", "command history"]:
        return show_history()

    if command in ["clear history", "delete history"]:
        return clear_history()

    # Calculator
    if command.startswith("calculate "):
        expression = original_command[len("calculate "):].strip()
        return calculate(expression)

    if command.startswith("calculator "):
        expression = original_command[len("calculator "):].strip()
        return calculate(expression)

    # Gemini searches
    gemini_phrases = [
        "search this in gemini ",
        "search in gemini ",
        "ask gemini ",
        "search gemini for "
    ]

    for phrase in gemini_phrases:
        if command.startswith(phrase):
            query = original_command[len(phrase):].strip()
            return search_gemini(query)

    # ChatGPT searches
    chatgpt_phrases = [
        "search this in chatgpt ",
        "search in chatgpt ",
        "ask chatgpt ",
        "search chatgpt for "
    ]

    for phrase in chatgpt_phrases:
        if command.startswith(phrase):
            query = original_command[len(phrase):].strip()
            return search_chatgpt(query)

    # Google search
    if command.startswith("search google for "):
        query = original_command[len("search google for "):].strip()
        return search_google(query)

    # YouTube search
    if command.startswith("search youtube for "):
        query = original_command[len("search youtube for "):].strip()
        return search_youtube(query)

    # Open website
    if command.startswith("open "):
        website_name = original_command[len("open "):].strip()
        return open_website(website_name)

    # Unknown command
    return (
             "I do not understand that command. "
        "Type 'help' to see the available commands."
    )