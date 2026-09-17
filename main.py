from commands import process_command
from datetime import datetime
import os
import shutil
import time


# =====================================
# Terminal Colors and Text Styles
# =====================================

RESET = "\033[0m"
BOLD = "\033[1m"

CYAN = "\033[96m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"
GRAY = "\033[90m"


# =====================================
# Terminal Layout Functions
# =====================================

def terminal_width():
    return shutil.get_terminal_size((80, 24)).columns


def center_text(text):
    width = terminal_width()
    return text.center(width)


def print_center(text="", color=WHITE, bold=False):
    style = BOLD if bold else ""
    print(style + color + center_text(text) + RESET)


def print_centered_box(lines, color=CYAN):
    width = max(len(line) for line in lines) + 8
    screen_width = terminal_width()

    width = min(width, screen_width)

    print(color + BOLD + center_text("╔" + "═" * (width - 2) + "╗") + RESET)

    for line in lines:
        available_width = width - 4
        shortened_line = line[:available_width]
        inside = shortened_line.center(available_width)

        box_line = "║ " + inside + " ║"
        print(color + BOLD + center_text(box_line) + RESET)

    print(color + BOLD + center_text("╚" + "═" * (width - 2) + "╝") + RESET)


def clear_screen():
    os.system("clear")


def print_separator():
    print_center("─" * min(60, terminal_width()), GRAY)


# =====================================
# Friday Interface
# =====================================

def print_banner():
    print()
    print_centered_box(
        [
            "F R I D A Y",
            "PERSONAL ANDROID ASSISTANT",
            "SYSTEM ONLINE"
        ],
        CYAN
    )

    print()
    print_center(
        "How are you sir, and how can I help you today?",
        GREEN,
        True
    )

    print()
    print_center("Type 'help' to view commands.", GRAY)
    print_center("Type 'exit' to close Friday.", GRAY)
    print()


def print_status():
    current_time = datetime.now().strftime("%I:%M:%S %p")
    current_date = datetime.now().strftime("%d %B %Y")

    print_separator()

    print_center(
        "DATE: " + current_date + "    TIME: " + current_time,
        BLUE,
        True
    )

    print_separator()
    print()


def print_response(response):
    print()
    print_center("┌────────────── FRIDAY ──────────────┐", MAGENTA, True)

    for line in str(response).splitlines():
        print_center("│ " + line, WHITE)

    print_center("└────────────────────────────────────┘", MAGENTA, True)
    print()


def print_goodbye():
    print()
    print_separator()
    print_center("Goodbye sir. Have a great day.", GREEN, True)
    print_separator()
    print()


# =====================================
# Main Program
# =====================================

def main():
    clear_screen()
    print_banner()
    print_status()

    while True:
        try:
            prompt = center_text("YOU ❯ ")
            user_command = input(
                CYAN + BOLD + prompt + RESET
            ).strip()

            if not user_command:
                print_center(
                    "Friday: Please enter a command.",
                    YELLOW
                )
                print()
                continue

            if user_command.lower() in ["exit", "quit", "stop"]:
                print_goodbye()
                break

            response = process_command(user_command)
            print_response(response)

        except KeyboardInterrupt:
            print_goodbye()
            break

        except EOFError:
            print_goodbye()
            break

        except Exception as error:
            print()
            print_center(
                "Friday: An unexpected error occurred.",
                RED,
                True
            )
            print_center("Details: " + str(error), RED)
            print()


if __name__ == "__main__":
    main()