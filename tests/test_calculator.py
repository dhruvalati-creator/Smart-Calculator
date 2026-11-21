"""
Unit Tests for Smart Calculator
Verifies basic arithmetic, percentages, powers, scientific functions, and history management.
"""

import os
import unittest
from smart_calculator.calculator import SmartCalculator
from smart_calculator.history import HistoryManager


class TestSmartCalculator(unittest.TestCase):
    """Test suite for the SmartCalculator class."""

    def setUp(self) -> None:
        self.calc = SmartCalculator()

    # --- Basic Operations ---
    def test_addition(self) -> None:
        self.assertEqual(self.calc.add(10, 5), 15)
        self.assertEqual(self.calc.add(-3, -7), -10)
        self.assertAlmostEqual(self.calc.add(0.1, 0.2), 0.3, places=7)

    def test_subtraction(self) -> None:
        self.assertEqual(self.calc.subtract(10, 4), 6)
        self.assertEqual(self.calc.subtract(3, 10), -7)

    def test_multiplication(self) -> None:
        self.assertEqual(self.calc.multiply(6, 7), 42)
        self.assertEqual(self.calc.multiply(-4, 5), -20)
        self.assertEqual(self.calc.multiply(10, 0), 0)

    def test_division(self) -> None:
        self.assertEqual(self.calc.divide(20, 4), 5)
        self.assertAlmostEqual(self.calc.divide(10, 3), 3.3333333, places=5)

    def test_division_by_zero(self) -> None:
        with self.assertRaises(ZeroDivisionError):
            self.calc.divide(10, 0)

    # --- Percentage Operations ---
    def test_percentage(self) -> None:
        self.assertEqual(self.calc.percentage(200, 15), 30)
        self.assertEqual(self.calc.percentage(50, 100), 50)

    def test_percentage_of(self) -> None:
        self.assertEqual(self.calc.percentage_of(50, 200), 25)
        with self.assertRaises(ZeroDivisionError):
            self.calc.percentage_of(50, 0)

    # --- Power & Root Operations ---
    def test_power(self) -> None:
        self.assertEqual(self.calc.power(2, 3), 8)
        self.assertEqual(self.calc.power(5, 0), 1)
        self.assertEqual(self.calc.power(4, 0.5), 2)

    def test_square_root(self) -> None:
        self.assertEqual(self.calc.square_root(16), 4)
        self.assertEqual(self.calc.square_root(0), 0)

    def test_square_root_negative_raises_error(self) -> None:
        with self.assertRaises(ValueError):
            self.calc.square_root(-9)

    # --- Scientific Operations ---
    def test_trigonometry(self) -> None:
        self.assertEqual(self.calc.sin(0), 0.0)
        self.assertEqual(self.calc.sin(90), 1.0)
        self.assertEqual(self.calc.cos(0), 1.0)
        self.assertEqual(self.calc.cos(90), 0.0)
        self.assertEqual(self.calc.tan(0), 0.0)
        self.assertEqual(self.calc.tan(45), 1.0)

    def test_tan_undefined(self) -> None:
        with self.assertRaises(ValueError):
            self.calc.tan(90)
        with self.assertRaises(ValueError):
            self.calc.tan(270)

    def test_logarithms(self) -> None:
        self.assertEqual(self.calc.log10(100), 2)
        self.assertEqual(self.calc.log10(1), 0)
        self.assertAlmostEqual(self.calc.ln(1), 0)

    def test_logarithm_invalid_input(self) -> None:
        with self.assertRaises(ValueError):
            self.calc.log10(0)
        with self.assertRaises(ValueError):
            self.calc.log10(-10)
        with self.assertRaises(ValueError):
            self.calc.ln(0)

    def test_factorial(self) -> None:
        self.assertEqual(self.calc.factorial(0), 1)
        self.assertEqual(self.calc.factorial(5), 120)

    def test_factorial_invalid_input(self) -> None:
        with self.assertRaises(ValueError):
            self.calc.factorial(-5)

    def test_format_result(self) -> None:
        self.assertEqual(self.calc.format_result(5.0), "5")
        self.assertEqual(self.calc.format_result(3.14), "3.14")

    def test_square(self) -> None:
        self.assertEqual(self.calc.square(5), 25)
        self.assertEqual(self.calc.square(-4), 16)

    def test_reciprocal(self) -> None:
        self.assertEqual(self.calc.reciprocal(4), 0.25)
        with self.assertRaises(ZeroDivisionError):
            self.calc.reciprocal(0)


class TestHistoryManager(unittest.TestCase):
    """Test suite for the HistoryManager persistence and clearing."""

    def setUp(self) -> None:
        self.test_filepath = "data/test_history.json"
        self.history = HistoryManager(filepath=self.test_filepath)

    def tearDown(self) -> None:
        if os.path.exists(self.test_filepath):
            os.remove(self.test_filepath)

    def test_add_and_get_history(self) -> None:
        self.history.add_record("5 + 5", "10")
        records = self.history.get_history()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["expression"], "5 + 5")
        self.assertEqual(records[0]["result"], "10")

    def test_clear_history(self) -> None:
        self.history.add_record("2 * 4", "8")
        self.history.clear_history()
        records = self.history.get_history()
        self.assertEqual(len(records), 0)

    def test_delete_individual_record(self) -> None:
        self.history.add_record("1 + 1", "2")
        self.history.add_record("2 + 2", "4")
        self.assertTrue(self.history.delete_record(0))
        records = self.history.get_history()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["expression"], "2 + 2")


class TestSafeExpressionEvaluator(unittest.TestCase):
    """Test suite for safe AST expression evaluator."""

    def test_basic_arithmetic(self) -> None:
        from smart_calculator.evaluator import SafeExpressionEvaluator
        self.assertEqual(SafeExpressionEvaluator.evaluate("10 + 5 * 2"), 20)
        self.assertEqual(SafeExpressionEvaluator.evaluate("(10 + 5) * 2"), 30)
        self.assertEqual(SafeExpressionEvaluator.evaluate("100 / 4 - 5"), 20)

    def test_decimals_and_negatives(self) -> None:
        from smart_calculator.evaluator import SafeExpressionEvaluator
        self.assertAlmostEqual(SafeExpressionEvaluator.evaluate("-5 + 12.5"), 7.5)
        self.assertEqual(SafeExpressionEvaluator.evaluate("(-3) * (-4)"), 12)

    def test_scientific_in_evaluator(self) -> None:
        from smart_calculator.evaluator import SafeExpressionEvaluator
        self.assertEqual(SafeExpressionEvaluator.evaluate("sqrt(25)"), 5)
        self.assertEqual(SafeExpressionEvaluator.evaluate("sin(90)"), 1)
        self.assertEqual(SafeExpressionEvaluator.evaluate("fact(4)"), 24)
        self.assertEqual(SafeExpressionEvaluator.evaluate("sqr(6)"), 36)
        self.assertEqual(SafeExpressionEvaluator.evaluate("recip(2)"), 0.5)

    def test_percentage_evaluator(self) -> None:
        from smart_calculator.evaluator import SafeExpressionEvaluator
        self.assertEqual(SafeExpressionEvaluator.evaluate("200 * 15%"), 30.0)

    def test_division_by_zero_evaluator(self) -> None:
        from smart_calculator.evaluator import SafeExpressionEvaluator
        with self.assertRaises(ZeroDivisionError):
            SafeExpressionEvaluator.evaluate("15 / 0")

    def test_security_rejection(self) -> None:
        from smart_calculator.evaluator import SafeExpressionEvaluator
        with self.assertRaises(ValueError):
            SafeExpressionEvaluator.evaluate("import os")
        with self.assertRaises(ValueError):
            SafeExpressionEvaluator.evaluate("open('data/history.json')")


if __name__ == "__main__":
    unittest.main()

