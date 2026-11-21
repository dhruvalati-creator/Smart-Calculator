"""
Smart Calculator Modern GUI Application
Professional CustomTkinter-based interface with Standard and Scientific modes,
theme toggling, persistent history panel, and keyboard shortcut support.
"""

import sys
import tkinter as tk
from typing import Optional, List, Dict, Any
import customtkinter as ctk

from .calculator import SmartCalculator
from .history import HistoryManager
from .evaluator import SafeExpressionEvaluator
from .gui_theme import THEMES, ThemeColors, DARK_THEME, LIGHT_THEME


class SmartCalculatorGUI(ctk.CTk):
    """Main application window for Smart Calculator."""

    def __init__(self, history_manager: Optional[HistoryManager] = None) -> None:
        super().__init__()

        self.history = history_manager or HistoryManager(filepath="data/history.json")
        self.current_theme_name = "dark"
        self.theme: ThemeColors = DARK_THEME
        self.is_scientific_mode = False
        self.is_history_open = False

        # State tracking
        self.expression_text = ""
        self.result_text = "0"
        self.just_evaluated = False

        # Configure Window
        self.title("Smart Calculator")
        self.minsize(440, 680)
        self.geometry("460, 700")

        # Set default CustomTkinter appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Container setup
        self._setup_layout()
        self._create_header()
        self._create_display()
        self._create_main_content()
        self._create_history_sidebar()

        # Keyboard shortcuts
        self._bind_keyboard_events()

        # Apply initial theme
        self.apply_theme("dark")

    # ------------------ Layout & Structure ------------------

    def _setup_layout(self) -> None:
        """Sets up the primary grid and frames."""
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def _create_header(self) -> None:
        """Creates the top header bar with mode switch, theme switch, and history toggle."""
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent", height=45)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=18, pady=(14, 6))
        self.header_frame.grid_columnconfigure(1, weight=1)

        # Title
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="SMART CALCULATOR",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            text_color=self.theme.text_primary,
        )
        self.title_label.grid(row=0, column=0, sticky="w")

        # Controls container
        controls_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        controls_frame.grid(row=0, column=2, sticky="e")

        # Mode Selector (Standard / Scientific)
        self.mode_button = ctk.CTkButton(
            controls_frame,
            text="Scientific",
            width=88,
            height=28,
            corner_radius=8,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.toggle_scientific_mode,
        )
        self.mode_button.pack(side="left", padx=4)

        # Theme Switch Button
        self.theme_button = ctk.CTkButton(
            controls_frame,
            text="☀️ Light",
            width=76,
            height=28,
            corner_radius=8,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.toggle_theme,
        )
        self.theme_button.pack(side="left", padx=4)

        # History Button
        self.history_button = ctk.CTkButton(
            controls_frame,
            text="🕒 History",
            width=76,
            height=28,
            corner_radius=8,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.toggle_history_panel,
        )
        self.history_button.pack(side="left", padx=4)

    def _create_display(self) -> None:
        """Creates the display section with expression and current result."""
        self.display_card = ctk.CTkFrame(self, corner_radius=14)
        self.display_card.grid(row=1, column=0, sticky="ew", padx=18, pady=(4, 12))
        self.display_card.grid_columnconfigure(0, weight=1)

        # Expression Label (small top line)
        self.expression_label = ctk.CTkLabel(
            self.display_card,
            text="",
            anchor="e",
            font=ctk.CTkFont(family="Consolas", size=16),
            height=26,
        )
        self.expression_label.grid(row=0, column=0, sticky="ew", padx=16, pady=(12, 0))

        # Main Value / Result Label (large bottom line)
        self.result_label = ctk.CTkLabel(
            self.display_card,
            text="0",
            anchor="e",
            font=ctk.CTkFont(family="Segoe UI", size=36, weight="bold"),
            height=54,
        )
        self.result_label.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 12))

    def _create_main_content(self) -> None:
        """Creates the container holding the keypad and collapsible history."""
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=2, column=0, sticky="nsew", padx=18, pady=(0, 18))
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        # Keypad container
        self.keypad_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.keypad_frame.grid(row=0, column=0, sticky="nsew")

        self._build_keypad()

    def _build_keypad(self) -> None:
        """Constructs both scientific and standard keypads."""
        # Clear existing buttons if any
        for widget in self.keypad_frame.winfo_children():
            widget.destroy()

        self.buttons_dict = {}

        if self.is_scientific_mode:
            # 6 columns: [Sci1, Sci2, Std1, Std2, Std3, Std4]
            for col in range(6):
                self.keypad_frame.grid_columnconfigure(col, weight=1, uniform="keypad_col")
            for row in range(5):
                self.keypad_frame.grid_rowconfigure(row, weight=1, uniform="keypad_row")

            # Scientific buttons layout: (text, row, col, type)
            sci_buttons = [
                ("sin", 0, 0, "sci"), ("cos", 0, 1, "sci"),
                ("tan", 1, 0, "sci"), ("log", 1, 1, "sci"),
                ("ln", 2, 0, "sci"),  ("n!", 2, 1, "sci"),
                ("√", 3, 0, "sci"),   ("x²", 3, 1, "sci"),
                ("x^y", 4, 0, "sci"), ("1/x", 4, 1, "sci"),
            ]

            # Standard buttons layout in 6-col mode (cols 2, 3, 4, 5)
            std_buttons = [
                ("AC", 0, 2, "action"), ("DEL", 0, 3, "action"), ("(", 0, 4, "op"), (")", 0, 5, "op"),
                ("7", 1, 2, "num"),    ("8", 1, 3, "num"),     ("9", 1, 4, "num"), ("÷", 1, 5, "op"),
                ("4", 2, 2, "num"),    ("5", 2, 3, "num"),     ("6", 2, 4, "num"), ("×", 2, 5, "op"),
                ("1", 3, 2, "num"),    ("2", 3, 4, "num"),     ("3", 3, 4, "num"), ("−", 3, 5, "op"),
                ("π", 4, 2, "sci"),    ("0", 4, 3, "num"),     (".", 4, 4, "num"), ("+", 4, 5, "op"),
            ]
            # Fix 1, 2, 3 row column indices:
            std_buttons[8] = ("1", 3, 2, "num")
            std_buttons[9] = ("2", 3, 3, "num")
            std_buttons[10] = ("3", 3, 4, "num")

            all_buttons = sci_buttons + std_buttons

            # Extra row for Equal & Percentage in Scientific Mode
            self.keypad_frame.grid_rowconfigure(5, weight=1, uniform="keypad_row")
            all_buttons.append(("%", 5, 0, "sci"))
            all_buttons.append(("±", 5, 1, "sci"))

            for text, r, c, b_type in all_buttons:
                btn = self._create_keypad_button(text, b_type)
                btn.grid(row=r, column=c, padx=3, pady=3, sticky="nsew")
                self.buttons_dict[text] = btn

            # Equal button spans remaining columns on bottom row
            eq_btn = self._create_keypad_button("=", "equal")
            eq_btn.grid(row=5, column=2, columnspan=4, padx=3, pady=3, sticky="nsew")
            self.buttons_dict["="] = eq_btn

        else:
            # Standard Mode: 4 columns x 6 rows
            for col in range(4):
                self.keypad_frame.grid_columnconfigure(col, weight=1, uniform="keypad_col")
            for row in range(6):
                self.keypad_frame.grid_rowconfigure(row, weight=1, uniform="keypad_row")

            std_buttons = [
                ("AC", 0, 0, "action"), ("DEL", 0, 1, "action"), ("%", 0, 2, "op"), ("÷", 0, 3, "op"),
                ("(", 1, 0, "op"),     (")", 1, 1, "op"),       ("√", 1, 2, "op"), ("×", 1, 3, "op"),
                ("7", 2, 0, "num"),    ("8", 2, 1, "num"),      ("9", 2, 2, "num"), ("−", 2, 3, "op"),
                ("4", 3, 0, "num"),    ("5", 3, 1, "num"),      ("6", 3, 2, "num"), ("+", 3, 3, "op"),
                ("1", 4, 0, "num"),    ("2", 4, 1, "num"),      ("3", 4, 2, "num"), ("^", 4, 3, "op"),
                ("±", 5, 0, "num"),    ("0", 5, 1, "num"),      (".", 5, 2, "num"), ("=", 5, 3, "equal"),
            ]

            for text, r, c, b_type in std_buttons:
                btn = self._create_keypad_button(text, b_type)
                btn.grid(row=r, column=c, padx=3, pady=3, sticky="nsew")
                self.buttons_dict[text] = btn

    def _create_keypad_button(self, text: str, b_type: str) -> ctk.CTkButton:
        """Instantiates a styled CustomTkinter button."""
        font_size = 18 if len(text) <= 2 else 15
        weight = "bold" if b_type in ["action", "equal", "op"] else "normal"

        btn = ctk.CTkButton(
            self.keypad_frame,
            text=text,
            corner_radius=10,
            font=ctk.CTkFont(family="Segoe UI", size=font_size, weight=weight),
            command=lambda t=text: self._on_button_click(t),
        )
        btn._button_type = b_type
        return btn

    def _create_history_sidebar(self) -> None:
        """Constructs the collapsible history sidebar."""
        self.history_frame = ctk.CTkFrame(self.content_frame, corner_radius=12, width=280)
        self.history_frame.grid_rowconfigure(1, weight=1)
        self.history_frame.grid_columnconfigure(0, weight=1)

        # Header with close and clear
        top_bar = ctk.CTkFrame(self.history_frame, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 6))
        top_bar.grid_columnconfigure(0, weight=1)

        lbl = ctk.CTkLabel(
            top_bar,
            text="History",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            anchor="w",
        )
        lbl.grid(row=0, column=0, sticky="w")

        close_btn = ctk.CTkButton(
            top_bar,
            text="✕",
            width=26,
            height=26,
            corner_radius=6,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.toggle_history_panel,
        )
        close_btn.grid(row=0, column=1, sticky="e")

        # Scrollable list of entries
        self.history_scroll = ctk.CTkScrollableFrame(self.history_frame, corner_radius=8)
        self.history_scroll.grid(row=1, column=0, sticky="nsew", padx=8, pady=4)
        self.history_scroll.grid_columnconfigure(0, weight=1)

        # Bottom clear history button
        self.clear_history_btn = ctk.CTkButton(
            self.history_frame,
            text="Clear All History",
            height=32,
            corner_radius=8,
            command=self._clear_all_history,
        )
        self.clear_history_btn.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

    # ------------------ Button Actions & Math Logic ------------------

    def _on_button_click(self, text: str) -> None:
        """Dispatches button actions."""
        if text.isdigit() or text == ".":
            self._handle_number(text)
        elif text in ["+", "−", "×", "÷", "^"]:
            self._handle_operator(text)
        elif text == "=":
            self._calculate_result()
        elif text == "AC":
            self._clear_all()
        elif text == "DEL":
            self._delete_char()
        elif text == "±":
            self._toggle_sign()
        elif text == "%":
            self._append_to_expression("%")
        elif text in ["(", ")"]:
            self._append_to_expression(text)
        elif text == "π":
            self._append_to_expression("π")
        elif text == "√":
            self._append_function("√(")
        elif text == "x²":
            self._append_to_expression("^2")
        elif text == "x^y":
            self._append_to_expression("^")
        elif text == "1/x":
            self._handle_reciprocal()
        elif text == "n!":
            self._handle_factorial()
        elif text in ["sin", "cos", "tan", "log", "ln"]:
            self._append_function(f"{text}(")

    def _handle_number(self, digit: str) -> None:
        """Handles numeric digit and decimal input."""
        if self.just_evaluated:
            # Start a new expression if entering a fresh number after '='
            self.expression_text = ""
            self.just_evaluated = False

        if digit == "." and self.expression_text.endswith("."):
            return

        self.expression_text += digit
        self._update_display()

    def _handle_operator(self, op: str) -> None:
        """Handles binary math operators."""
        if self.just_evaluated:
            self.just_evaluated = False

        if not self.expression_text:
            if op == "−":
                self.expression_text = "-"
                self._update_display()
            elif self.result_text != "0" and self.result_text != "Error":
                self.expression_text = f"{self.result_text} {op} "
                self._update_display()
            return

        # If previous character is already an operator, replace it
        stripped = self.expression_text.rstrip()
        if stripped and stripped[-1] in ["+", "−", "×", "÷", "^", "-"]:
            self.expression_text = stripped[:-1] + op + " "
        else:
            self.expression_text += f" {op} "

        self._update_display()

    def _append_to_expression(self, text: str) -> None:
        """Appends arbitrary token to expression."""
        if self.just_evaluated:
            self.just_evaluated = False
        self.expression_text += text
        self._update_display()

    def _append_function(self, func_prefix: str) -> None:
        """Appends a scientific function call (e.g. sin(), sqrt())."""
        if self.just_evaluated:
            self.expression_text = ""
            self.just_evaluated = False
        self.expression_text += func_prefix
        self._update_display()

    def _handle_reciprocal(self) -> None:
        """Applies 1/x to the current expression or wraps it."""
        if not self.expression_text:
            if self.result_text not in ["0", "Error"]:
                self.expression_text = f"1/({self.result_text})"
            else:
                self.expression_text = "1/("
        else:
            self.expression_text = f"1/({self.expression_text})"
        self.just_evaluated = False
        self._update_display()

    def _handle_factorial(self) -> None:
        """Applies factorial function."""
        if not self.expression_text:
            if self.result_text not in ["0", "Error"]:
                self.expression_text = f"fact({self.result_text})"
            else:
                self.expression_text = "fact("
        else:
            self.expression_text = f"fact({self.expression_text})"
        self.just_evaluated = False
        self._update_display()

    def _toggle_sign(self) -> None:
        """Toggles negation of the current number or expression."""
        if not self.expression_text:
            self.expression_text = "-"
        elif self.expression_text.startswith("-("):
            self.expression_text = self.expression_text[2:-1]
        elif self.expression_text.startswith("-"):
            self.expression_text = self.expression_text[1:]
        else:
            self.expression_text = f"-({self.expression_text})"
        self._update_display()

    def _clear_all(self) -> None:
        """Resets calculator state (AC)."""
        self.expression_text = ""
        self.result_text = "0"
        self.just_evaluated = False
        self._update_display()

    def _delete_char(self) -> None:
        """Deletes the last character (DEL)."""
        if self.just_evaluated:
            self.just_evaluated = False

        if self.expression_text:
            # Handle trailing spaces around operators
            if self.expression_text.endswith(" "):
                self.expression_text = self.expression_text.rstrip()
            else:
                self.expression_text = self.expression_text[:-1]

        self._update_display()

    def _calculate_result(self) -> None:
        """Safely parses and evaluates the current expression."""
        if not self.expression_text.strip():
            return

        raw_expression = self.expression_text.strip()

        try:
            val = SafeExpressionEvaluator.evaluate(raw_expression)
            formatted = SmartCalculator.format_result(val)

            # Update display
            self.result_text = formatted
            self.expression_label.configure(text=f"{raw_expression} =")
            self.result_label.configure(text=self.result_text, text_color=self.theme.text_primary)

            # Save to persistent history
            self.history.add_record(raw_expression, formatted)
            self._refresh_history_ui()

            # Carry result forward
            self.expression_text = formatted
            self.just_evaluated = True

        except (ZeroDivisionError, ValueError, OverflowError) as err:
            error_msg = str(err)
            if "division by zero" in error_msg.lower():
                display_err = "Cannot divide by zero"
            elif "negative number" in error_msg.lower():
                display_err = "Invalid input (neg sqrt)"
            else:
                display_err = "Invalid Input"

            self.expression_label.configure(text=f"{raw_expression} =")
            self.result_label.configure(text=display_err, text_color="#ef4444")
            self.just_evaluated = True

    def _update_display(self) -> None:
        """Updates display labels to reflect current state."""
        self.expression_label.configure(text=self.expression_text)
        preview_text = self.expression_text if self.expression_text else "0"
        self.result_label.configure(text=preview_text, text_color=self.theme.text_primary)

    # ------------------ History Functionality ------------------

    def toggle_history_panel(self) -> None:
        """Toggles visibility of the history drawer."""
        self.is_history_open = not self.is_history_open

        if self.is_history_open:
            # Show history on the right
            self.content_frame.grid_columnconfigure(1, weight=0)
            self.history_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
            self.history_button.configure(fg_color=self.theme.btn_equal_bg, text_color="#ffffff")
            self._refresh_history_ui()
            # Expand window width if needed
            current_w = self.winfo_width()
            current_h = self.winfo_height()
            self.geometry(f"{max(current_w, 680)}x{current_h}")
        else:
            self.history_frame.grid_forget()
            self.history_button.configure(
                fg_color=self.theme.btn_op_bg,
                text_color=self.theme.btn_op_text,
            )

    def _refresh_history_ui(self) -> None:
        """Populates history sidebar with records."""
        for widget in self.history_scroll.winfo_children():
            widget.destroy()

        records = self.history.get_history()
        if not records:
            lbl = ctk.CTkLabel(
                self.history_scroll,
                text="No calculations yet.\nPerform operations to see them here.",
                font=ctk.CTkFont(size=12),
                text_color=self.theme.text_secondary,
                justify="center",
            )
            lbl.pack(pady=30)
            return

        # Display records in reverse chronological order
        for idx in range(len(records) - 1, -1, -1):
            rec = records[idx]
            item_frame = ctk.CTkFrame(
                self.history_scroll,
                fg_color=self.theme.history_item_bg,
                corner_radius=8,
            )
            item_frame.pack(fill="x", pady=4, padx=2)
            item_frame.grid_columnconfigure(0, weight=1)

            # Expression and Result
            expr_text = rec.get("expression", "")
            res_text = str(rec.get("result", ""))
            ts_text = rec.get("timestamp", "")

            # Clickable content area to reuse calculation
            btn_use = ctk.CTkButton(
                item_frame,
                text=f"{expr_text}\n= {res_text}",
                anchor="w",
                fg_color="transparent",
                hover_color=self.theme.history_item_hover,
                text_color=self.theme.text_primary,
                font=ctk.CTkFont(family="Consolas", size=13),
                command=lambda r=res_text: self._reuse_history_result(r),
            )
            btn_use.grid(row=0, column=0, sticky="ew", padx=(8, 4), pady=4)

            # Delete single entry button
            btn_del = ctk.CTkButton(
                item_frame,
                text="🗑",
                width=24,
                height=24,
                corner_radius=6,
                fg_color="transparent",
                hover_color="#ef4444",
                text_color=self.theme.text_secondary,
                font=ctk.CTkFont(size=12),
                command=lambda i=idx: self._delete_history_item(i),
            )
            btn_del.grid(row=0, column=1, padx=(0, 6), pady=4)

    def _reuse_history_result(self, result: str) -> None:
        """Puts a past result into the active calculation."""
        self.expression_text = result
        self.result_text = result
        self.just_evaluated = False
        self._update_display()

    def _delete_history_item(self, index: int) -> None:
        """Removes a single history record and updates UI."""
        self.history.delete_record(index)
        self._refresh_history_ui()

    def _clear_all_history(self) -> None:
        """Clears all history records."""
        self.history.clear_history()
        self._refresh_history_ui()

    # ------------------ Mode & Theme Toggling ------------------

    def toggle_scientific_mode(self) -> None:
        """Toggles between Standard and Scientific layouts."""
        self.is_scientific_mode = not self.is_scientific_mode

        if self.is_scientific_mode:
            self.mode_button.configure(text="Standard", fg_color=self.theme.btn_equal_bg, text_color="#ffffff")
            self.title_label.configure(text="SMART CALCULATOR • SCIENTIFIC")
            # Expand window width for scientific columns
            cur_w = self.winfo_width()
            cur_h = self.winfo_height()
            target_w = 660 if not self.is_history_open else 920
            self.geometry(f"{max(cur_w, target_w)}x{max(cur_h, 700)}")
            self.minsize(620, 680)
        else:
            self.mode_button.configure(
                text="Scientific",
                fg_color=self.theme.btn_op_bg,
                text_color=self.theme.btn_op_text,
            )
            self.title_label.configure(text="SMART CALCULATOR")
            self.minsize(440, 680)
            if not self.is_history_open:
                self.geometry("460x700")

        self._build_keypad()
        self.apply_theme(self.current_theme_name)

    def toggle_theme(self) -> None:
        """Switches between Dark and Light mode."""
        new_theme = "light" if self.current_theme_name == "dark" else "dark"
        self.apply_theme(new_theme)

    def apply_theme(self, theme_name: str) -> None:
        """Applies theme colors to the entire interface."""
        self.current_theme_name = theme_name
        self.theme = THEMES.get(theme_name, DARK_THEME)

        ctk.set_appearance_mode(theme_name)
        self.configure(fg_color=self.theme.bg_window)

        # Update theme toggle button text
        theme_btn_text = "🌙 Dark" if theme_name == "light" else "☀️ Light"
        self.theme_button.configure(
            text=theme_btn_text,
            fg_color=self.theme.btn_op_bg,
            hover_color=self.theme.btn_op_hover,
            text_color=self.theme.btn_op_text,
        )

        # Mode button styling
        if not self.is_scientific_mode:
            self.mode_button.configure(
                fg_color=self.theme.btn_op_bg,
                hover_color=self.theme.btn_op_hover,
                text_color=self.theme.btn_op_text,
            )

        # History button styling
        if not self.is_history_open:
            self.history_button.configure(
                fg_color=self.theme.btn_op_bg,
                hover_color=self.theme.btn_op_hover,
                text_color=self.theme.btn_op_text,
            )

        # Display card
        self.display_card.configure(fg_color=self.theme.bg_card)
        self.expression_label.configure(text_color=self.theme.text_secondary)
        self.result_label.configure(text_color=self.theme.text_primary)
        self.title_label.configure(text_color=self.theme.text_primary)

        # History Sidebar
        self.history_frame.configure(fg_color=self.theme.history_bg)
        self.history_scroll.configure(fg_color=self.theme.history_bg)
        self.clear_history_btn.configure(
            fg_color=self.theme.btn_action_bg,
            hover_color=self.theme.btn_action_hover,
            text_color=self.theme.btn_action_text,
        )

        # Keypad buttons styling
        for btn in self.buttons_dict.values():
            b_type = getattr(btn, "_button_type", "num")
            if b_type == "num":
                btn.configure(
                    fg_color=self.theme.btn_num_bg,
                    hover_color=self.theme.btn_num_hover,
                    text_color=self.theme.btn_num_text,
                )
            elif b_type in ["op", "sci"]:
                btn.configure(
                    fg_color=self.theme.btn_op_bg,
                    hover_color=self.theme.btn_op_hover,
                    text_color=self.theme.btn_op_text,
                )
            elif b_type == "action":
                btn.configure(
                    fg_color=self.theme.btn_action_bg,
                    hover_color=self.theme.btn_action_hover,
                    text_color=self.theme.btn_action_text,
                )
            elif b_type == "equal":
                btn.configure(
                    fg_color=self.theme.btn_equal_bg,
                    hover_color=self.theme.btn_equal_hover,
                    text_color=self.theme.btn_equal_text,
                )

        if self.is_history_open:
            self._refresh_history_ui()

    # ------------------ Keyboard Support ------------------

    def _bind_keyboard_events(self) -> None:
        """Binds hardware keyboard events to calculator actions."""
        self.bind("<Key>", self._on_key_press)

    def _on_key_press(self, event: tk.Event) -> None:
        """Handles physical keypresses."""
        char = event.char
        keysym = event.keysym

        # Numbers
        if char in "0123456789.":
            self._handle_number(char)
        # Operators
        elif char == "+":
            self._handle_operator("+")
        elif char == "-":
            self._handle_operator("−")
        elif char == "*":
            self._handle_operator("×")
        elif char == "/":
            self._handle_operator("÷")
        elif char == "^":
            self._handle_operator("^")
        elif char == "%":
            self._append_to_expression("%")
        elif char in ["(", ")"]:
            self._append_to_expression(char)
        # Calculate
        elif keysym in ["Return", "KP_Enter"] or char == "=":
            self._calculate_result()
        # Backspace / DEL
        elif keysym == "BackSpace":
            self._delete_char()
        # Clear / AC
        elif keysym == "Escape" or char in ["c", "C"]:
            self._clear_all()


def start_gui() -> None:
    """Launches the Smart Calculator GUI application."""
    app = SmartCalculatorGUI()
    app.mainloop()


if __name__ == "__main__":
    start_gui()
