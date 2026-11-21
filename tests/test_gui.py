"""
GUI Automated Component Tests
Tests initialization, theme switching, mode toggling, button click simulation,
and history interaction without manual user input.
"""

import unittest
from smart_calculator.gui import SmartCalculatorGUI
from smart_calculator.history import HistoryManager


class TestCalculatorGUI(unittest.TestCase):
    """Test suite for SmartCalculatorGUI components and events."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_hist_path = "data/test_gui_history.json"

    def setUp(self) -> None:
        self.history = HistoryManager(filepath=self.test_hist_path)
        self.history.clear_history()
        self.app = SmartCalculatorGUI(history_manager=self.history)
        # Avoid hanging on mainloop
        self.app.withdraw()

    def tearDown(self) -> None:
        self.app.destroy()
        self.history.clear_history()

    def test_gui_initial_state(self) -> None:
        self.assertEqual(self.app.current_theme_name, "dark")
        self.assertFalse(self.app.is_scientific_mode)
        self.assertFalse(self.app.is_history_open)
        self.assertEqual(self.app.result_text, "0")

    def test_theme_toggle(self) -> None:
        self.app.toggle_theme()
        self.assertEqual(self.app.current_theme_name, "light")
        self.app.toggle_theme()
        self.assertEqual(self.app.current_theme_name, "dark")

    def test_scientific_mode_toggle(self) -> None:
        self.app.toggle_scientific_mode()
        self.assertTrue(self.app.is_scientific_mode)
        self.assertIn("sin", self.app.buttons_dict)
        self.assertIn("cos", self.app.buttons_dict)
        self.app.toggle_scientific_mode()
        self.assertFalse(self.app.is_scientific_mode)

    def test_button_clicks_and_calculation(self) -> None:
        # Simulate: 1 2 + 8 =
        self.app._on_button_click("1")
        self.app._on_button_click("2")
        self.app._on_button_click("+")
        self.app._on_button_click("8")
        self.app._on_button_click("=")
        self.assertEqual(self.app.result_text, "20")

        # Verify recorded into history
        records = self.history.get_history()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["result"], "20")

    def test_scientific_calculation(self) -> None:
        self.app._clear_all()
        self.app._on_button_click("sin")
        self.app._on_button_click("3")
        self.app._on_button_click("0")
        self.app._on_button_click(")")
        self.app._on_button_click("=")
        self.assertEqual(self.app.result_text, "0.5")

    def test_clear_and_delete(self) -> None:
        self.app._clear_all()
        self.app._on_button_click("9")
        self.app._on_button_click("8")
        self.app._on_button_click("DEL")
        self.assertEqual(self.app.expression_text, "9")
        self.app._on_button_click("AC")
        self.assertEqual(self.app.expression_text, "")

    def test_division_by_zero_handling(self) -> None:
        self.app._clear_all()
        self.app._on_button_click("5")
        self.app._on_button_click("÷")
        self.app._on_button_click("0")
        self.app._on_button_click("=")
        self.assertIn("zero", self.app.result_label.cget("text").lower())

    def test_history_toggle_and_reuse(self) -> None:
        self.app.toggle_history_panel()
        self.assertTrue(self.app.is_history_open)
        self.app._reuse_history_result("99")
        self.assertEqual(self.app.result_text, "99")
        self.app.toggle_history_panel()
        self.assertFalse(self.app.is_history_open)


if __name__ == "__main__":
    unittest.main()
