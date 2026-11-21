"""
UI Module
Provides user interface menus, formatted outputs, and safe input handlers.
"""

from typing import List, Dict, Any


def display_banner() -> None:
    """Prints a friendly welcome banner."""
    print("=" * 60)
    print("             SMART CALCULATOR (Python Edition)             ")
    print("=" * 60)
    print(" Accurate calculations | Scientific operations | History ")
    print("=" * 60)


def display_main_menu() -> None:
    """Displays the main menu options."""
    print("\n--- MAIN MENU ---")
    print("1. Basic Arithmetic (+, -, *, /)")
    print("2. Percentage Calculations (%)")
    print("3. Power & Square Root (x^y, sqrt(x))")
    print("4. Scientific Operations (sin, cos, tan, log, n!)")
    print("5. View Calculation History")
    print("6. Clear Calculation History")
    print("7. Exit")
    print("-" * 25)


def get_float(prompt: str) -> float:
    """
    Safely prompts user for a floating-point number.
    Repeats prompt until valid input is given.
    """
    while True:
        user_input = input(prompt).strip()
        try:
            return float(user_input)
        except ValueError:
            print("  [!] Invalid number. Please enter a valid decimal or integer.")


def get_int(prompt: str) -> int:
    """
    Safely prompts user for an integer number.
    Repeats prompt until valid input is given.
    """
    while True:
        user_input = input(prompt).strip()
        try:
            return int(user_input)
        except ValueError:
            print("  [!] Invalid integer. Please enter a whole number.")


def display_history(records: List[Dict[str, Any]]) -> None:
    """Displays history records in a readable table format."""
    print("\n" + "=" * 60)
    print(f"{'#':<4} | {'TIMESTAMP':<19} | {'EXPRESSION':<20} | {'RESULT'}")
    print("-" * 60)

    if not records:
        print(" No calculation history found.")
    else:
        for idx, rec in enumerate(records, 1):
            ts = rec.get("timestamp", "-")
            expr = rec.get("expression", "-")
            res = rec.get("result", "-")
            print(f"{idx:<4} | {ts:<19} | {expr:<20} | {res}")

    print("=" * 60)


def prompt_continue() -> None:
    """Pauses execution so user can review the output."""
    input("\nPress [Enter] to return to menu...")
