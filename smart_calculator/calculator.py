"""
Smart Calculator Core Module
Contains the SmartCalculator class implementing basic, percentage, power, and scientific operations.
"""

import math
from typing import Union


class SmartCalculator:
    """A calculator class offering arithmetic, percentage, and scientific computations."""

    # ------------------ Basic Operations ------------------

    @staticmethod
    def add(a: float, b: float) -> float:
        """Adds two numbers."""
        return a + b

    @staticmethod
    def subtract(a: float, b: float) -> float:
        """Subtracts b from a."""
        return a - b

    @staticmethod
    def multiply(a: float, b: float) -> float:
        """Multiplies two numbers."""
        return a * b

    @staticmethod
    def divide(a: float, b: float) -> float:
        """
        Divides a by b.
        Raises ZeroDivisionError if denominator is 0.
        """
        if b == 0:
            raise ZeroDivisionError("Error: Division by zero is not allowed.")
        return a / b

    # ------------------ Percentage Operations ------------------

    @staticmethod
    def percentage(total: float, percent: float) -> float:
        """
        Calculates the percentage value of a total.
        Example: 20% of 150 = 30
        """
        return (percent / 100.0) * total

    @staticmethod
    def percentage_of(part: float, whole: float) -> float:
        """
        Calculates what percentage 'part' is of 'whole'.
        Example: 30 is what percent of 150? -> 20%
        """
        if whole == 0:
            raise ZeroDivisionError("Error: Cannot calculate percentage of whole = 0.")
        return (part / whole) * 100.0

    # ------------------ Power & Root Operations ------------------

    @staticmethod
    def power(base: float, exponent: float) -> float:
        """Raises base to the power of exponent (base ^ exponent)."""
        return math.pow(base, exponent)

    @staticmethod
    def square_root(x: float) -> float:
        """
        Calculates square root of x.
        Raises ValueError if x is negative.
        """
        if x < 0:
            raise ValueError("Error: Cannot calculate square root of a negative number in real numbers.")
        return math.sqrt(x)

    @staticmethod
    def square(x: float) -> float:
        """Calculates square of x (x^2)."""
        return x * x

    @staticmethod
    def reciprocal(x: float) -> float:
        """
        Calculates reciprocal of x (1/x).
        Raises ZeroDivisionError if x is 0.
        """
        if x == 0:
            raise ZeroDivisionError("Error: Cannot divide by zero for reciprocal (1/0).")
        return 1.0 / x

    # ------------------ Scientific Operations ------------------

    @staticmethod
    def sin(degrees: float) -> float:
        """Calculates sine of an angle given in degrees."""
        radians = math.radians(degrees)
        res = math.sin(radians)
        # Handle floating point inaccuracies (e.g. sin(180) should be 0)
        return round(res, 10)

    @staticmethod
    def cos(degrees: float) -> float:
        """Calculates cosine of an angle given in degrees."""
        radians = math.radians(degrees)
        res = math.cos(radians)
        # Handle floating point inaccuracies (e.g. cos(90) should be 0)
        return round(res, 10)

    @staticmethod
    def tan(degrees: float) -> float:
        """
        Calculates tangent of an angle given in degrees.
        Raises ValueError if tangent is undefined (e.g., 90°, 270°).
        """
        # Tangent is undefined at odd multiples of 90 degrees: 90, 270, -90, etc.
        normalized = degrees % 180
        if math.isclose(normalized, 90, abs_tol=1e-9):
            raise ValueError(f"Error: tan({degrees}°) is undefined (asymptote).")
        radians = math.radians(degrees)
        return round(math.tan(radians), 10)

    @staticmethod
    def log10(x: float) -> float:
        """
        Calculates base-10 logarithm.
        Raises ValueError if x <= 0.
        """
        if x <= 0:
            raise ValueError("Error: Logarithm is only defined for numbers greater than 0.")
        return math.log10(x)

    @staticmethod
    def ln(x: float) -> float:
        """
        Calculates natural logarithm (base e).
        Raises ValueError if x <= 0.
        """
        if x <= 0:
            raise ValueError("Error: Natural logarithm is only defined for numbers greater than 0.")
        return math.log(x)

    @staticmethod
    def factorial(n: int) -> int:
        """
        Calculates factorial of a non-negative integer n (n!).
        Raises ValueError if n is negative or not an integer.
        """
        if not isinstance(n, int):
            raise ValueError("Error: Factorial requires an integer input.")
        if n < 0:
            raise ValueError("Error: Factorial is not defined for negative integers.")
        return math.factorial(n)

    # ------------------ Helper Formatting ------------------

    @staticmethod
    def format_result(value: Union[float, int]) -> str:
        """Formats numbers cleanly (e.g. 5.0 becomes '5', 3.14159 retains decimals)."""
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        if isinstance(value, float):
            # Limit decimals to 6 places, strip trailing zeros
            return f"{value:.6f}".rstrip("0").rstrip(".")
        return str(value)
