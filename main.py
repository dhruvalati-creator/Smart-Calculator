"""
Smart Calculator Application Entry Point
Orchestrates user interface, mathematical operations, and history logging.
"""

import sys
from smart_calculator.calculator import SmartCalculator
from smart_calculator.history import HistoryManager
from smart_calculator import ui


def handle_basic_arithmetic(calc: SmartCalculator, history: HistoryManager) -> None:
    """Handles basic arithmetic operations."""
    print("\n--- Basic Arithmetic ---")
    print("Select operator:")
    print("  1. Addition (+)")
    print("  2. Subtraction (-)")
    print("  3. Multiplication (*)")
    print("  4. Division (/)")
    print("  5. Back to Main Menu")

    choice = input("Enter choice (1-5): ").strip()
    if choice == "5":
        return

    op_map = {"1": "+", "2": "-", "3": "*", "4": "/"}
    if choice not in op_map:
        print("[!] Invalid operator choice.")
        ui.prompt_continue()
        return

    num1 = ui.get_float("Enter first number: ")
    num2 = ui.get_float("Enter second number: ")

    try:
        if choice == "1":
            result = calc.add(num1, num2)
        elif choice == "2":
            result = calc.subtract(num1, num2)
        elif choice == "3":
            result = calc.multiply(num1, num2)
        elif choice == "4":
            result = calc.divide(num1, num2)

        formatted_res = calc.format_result(result)
        num1_str = calc.format_result(num1)
        num2_str = calc.format_result(num2)
        op_symbol = op_map[choice]
        expression = f"{num1_str} {op_symbol} {num2_str}"

        print(f"\n--> Result: {expression} = {formatted_res}")
        history.add_record(expression, formatted_res)
    except ZeroDivisionError as err:
        print(f"\n[!] Calculation Error: {err}")

    ui.prompt_continue()


def handle_percentage(calc: SmartCalculator, history: HistoryManager) -> None:
    """Handles percentage calculations."""
    print("\n--- Percentage Calculations ---")
    print("  1. Find X% of a Total (e.g., 15% of 200)")
    print("  2. Find what % Part is of Whole (e.g., 40 of 200)")
    print("  3. Back to Main Menu")

    choice = input("Enter choice (1-3): ").strip()
    if choice == "3":
        return

    if choice == "1":
        percent = ui.get_float("Enter percentage (%): ")
        total = ui.get_float("Enter total amount: ")
        result = calc.percentage(total, percent)
        formatted_res = calc.format_result(result)
        expression = f"{calc.format_result(percent)}% of {calc.format_result(total)}"
        print(f"\n--> Result: {expression} = {formatted_res}")
        history.add_record(expression, formatted_res)

    elif choice == "2":
        part = ui.get_float("Enter part value: ")
        whole = ui.get_float("Enter whole total: ")
        try:
            result = calc.percentage_of(part, whole)
            formatted_res = calc.format_result(result)
            expression = f"{calc.format_result(part)} as % of {calc.format_result(whole)}"
            print(f"\n--> Result: {expression} = {formatted_res}%")
            history.add_record(expression, f"{formatted_res}%")
        except ZeroDivisionError as err:
            print(f"\n[!] Calculation Error: {err}")
    else:
        print("[!] Invalid option.")

    ui.prompt_continue()


def handle_power_and_root(calc: SmartCalculator, history: HistoryManager) -> None:
    """Handles exponentiation and square root calculations."""
    print("\n--- Power & Square Root ---")
    print("  1. Power (x ^ y)")
    print("  2. Square Root (sqrt(x))")
    print("  3. Back to Main Menu")

    choice = input("Enter choice (1-3): ").strip()
    if choice == "3":
        return

    if choice == "1":
        base = ui.get_float("Enter base (x): ")
        exponent = ui.get_float("Enter exponent (y): ")
        try:
            result = calc.power(base, exponent)
            formatted_res = calc.format_result(result)
            expression = f"{calc.format_result(base)} ^ {calc.format_result(exponent)}"
            print(f"\n--> Result: {expression} = {formatted_res}")
            history.add_record(expression, formatted_res)
        except OverflowError:
            print("\n[!] Calculation Error: The result is too large to represent.")

    elif choice == "2":
        val = ui.get_float("Enter number (x): ")
        try:
            result = calc.square_root(val)
            formatted_res = calc.format_result(result)
            expression = f"sqrt({calc.format_result(val)})"
            print(f"\n--> Result: {expression} = {formatted_res}")
            history.add_record(expression, formatted_res)
        except ValueError as err:
            print(f"\n[!] Calculation Error: {err}")
    else:
        print("[!] Invalid option.")

    ui.prompt_continue()


def handle_scientific(calc: SmartCalculator, history: HistoryManager) -> None:
    """Handles scientific calculations."""
    print("\n--- Scientific Operations ---")
    print("  1. Sine: sin(angle deg)")
    print("  2. Cosine: cos(angle deg)")
    print("  3. Tangent: tan(angle deg)")
    print("  4. Logarithm (base 10): log10(x)")
    print("  5. Natural Logarithm: ln(x)")
    print("  6. Factorial: n!")
    print("  7. Back to Main Menu")

    choice = input("Enter choice (1-7): ").strip()
    if choice == "7":
        return

    try:
        if choice in ["1", "2", "3"]:
            angle = ui.get_float("Enter angle in degrees: ")
            if choice == "1":
                res = calc.sin(angle)
                expr = f"sin({calc.format_result(angle)} deg)"
            elif choice == "2":
                res = calc.cos(angle)
                expr = f"cos({calc.format_result(angle)} deg)"
            else:
                res = calc.tan(angle)
                expr = f"tan({calc.format_result(angle)} deg)"

            formatted_res = calc.format_result(res)
            print(f"\n--> Result: {expr} = {formatted_res}")
            history.add_record(expr, formatted_res)

        elif choice == "4":
            val = ui.get_float("Enter number (x > 0): ")
            res = calc.log10(val)
            formatted_res = calc.format_result(res)
            expr = f"log10({calc.format_result(val)})"
            print(f"\n--> Result: {expr} = {formatted_res}")
            history.add_record(expr, formatted_res)

        elif choice == "5":
            val = ui.get_float("Enter number (x > 0): ")
            res = calc.ln(val)
            formatted_res = calc.format_result(res)
            expr = f"ln({calc.format_result(val)})"
            print(f"\n--> Result: {expr} = {formatted_res}")
            history.add_record(expr, formatted_res)

        elif choice == "6":
            n = ui.get_int("Enter non-negative integer (n): ")
            res = calc.factorial(n)
            formatted_res = str(res)
            expr = f"{n}!"
            print(f"\n--> Result: {expr} = {formatted_res}")
            history.add_record(expr, formatted_res)

        else:
            print("[!] Invalid scientific choice.")

    except (ValueError, OverflowError) as err:
        print(f"\n[!] Calculation Error: {err}")

    ui.prompt_continue()


def handle_view_history(history: HistoryManager) -> None:
    """Displays the history records."""
    records = history.get_history()
    ui.display_history(records)
    ui.prompt_continue()


def handle_clear_history(history: HistoryManager) -> None:
    """Asks for confirmation and clears the calculation history."""
    confirm = input("Are you sure you want to clear all history? (y/N): ").strip().lower()
    if confirm in ["y", "yes"]:
        success = history.clear_history()
        if success:
            print("[OK] Calculation history has been cleared successfully.")
        else:
            print("[!] Failed to clear history file.")
    else:
        print("[-] Operation cancelled.")
    ui.prompt_continue()


def start_cli() -> None:
    """Original command-line interactive interface loop."""
    calc = SmartCalculator()
    history = HistoryManager(filepath="data/history.json")

    ui.display_banner()

    while True:
        try:
            ui.display_main_menu()
            choice = input("Enter your choice (1-7): ").strip()

            if choice == "1":
                handle_basic_arithmetic(calc, history)
            elif choice == "2":
                handle_percentage(calc, history)
            elif choice == "3":
                handle_power_and_root(calc, history)
            elif choice == "4":
                handle_scientific(calc, history)
            elif choice == "5":
                handle_view_history(history)
            elif choice == "6":
                handle_clear_history(history)
            elif choice == "7":
                print("\nThank you for using Smart Calculator. Goodbye!")
                sys.exit(0)
            else:
                print("[!] Invalid option. Please enter a number between 1 and 7.")
                ui.prompt_continue()

        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user. Exiting...")
            sys.exit(0)


def main() -> None:
    """Application entry point: launches GUI by default or CLI with --cli flag."""
    if "--cli" in sys.argv:
        start_cli()
        return

    try:
        from smart_calculator.gui import start_gui
        start_gui()
    except Exception as exc:
        print(f"[!] Unable to launch graphical interface: {exc}")
        print("[*] Falling back to terminal interface...")
        start_cli()


if __name__ == "__main__":
    main()

