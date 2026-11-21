"""
Safe Mathematical Expression Evaluator
Parses and evaluates expressions using Python's AST module without using unsafe eval().
Delegates math calculations directly to SmartCalculator methods.
"""

import ast
import math
import re
from typing import Union, Any
from .calculator import SmartCalculator


class SafeExpressionEvaluator:
    """Safely parses and evaluates mathematical expressions using AST."""

    # Allowed function names mapped to their evaluator callables
    ALLOWED_FUNCTIONS = {
        "sin": SmartCalculator.sin,
        "cos": SmartCalculator.cos,
        "tan": SmartCalculator.tan,
        "sqrt": SmartCalculator.square_root,
        "log": SmartCalculator.log10,
        "log10": SmartCalculator.log10,
        "ln": SmartCalculator.ln,
        "fact": SmartCalculator.factorial,
        "factorial": SmartCalculator.factorial,
        "sqr": SmartCalculator.square,
        "recip": SmartCalculator.reciprocal,
        "reciprocal": SmartCalculator.reciprocal,
    }

    # Allowed constants
    ALLOWED_CONSTANTS = {
        "pi": math.pi,
        "e": math.e,
    }

    @classmethod
    def sanitize_expression(cls, expr: str) -> str:
        """
        Normalizes human-facing symbols into AST-parsable Python expression.
        - Replaces Unicode multiplication, division, subtraction.
        - Replaces caret (^) with exponentiation (**).
        - Handles pi symbol (π) and square root symbol (√).
        - Handles implicit multiplication (e.g. '2(3)' -> '2*(3)', '5pi' -> '5*pi').
        - Auto-closes open parentheses.
        """
        if not expr:
            return ""

        s = expr.strip()

        # Unicode replacements
        s = s.replace("×", "*").replace("÷", "/").replace("−", "-").replace("–", "-")
        s = s.replace("π", "pi")
        s = s.replace("^", "**")

        # Replace √number or √(expr) with sqrt(...)
        # e.g., √(9) -> sqrt(9), √9 -> sqrt(9)
        s = re.sub(r"√\s*(\d+(?:\.\d+)?)", r"sqrt(\1)", s)
        s = re.sub(r"√\s*\(", "sqrt(", s)

        # Percentage handling: e.g. "50%" -> "(50*0.01)"
        s = re.sub(r"(\d+(?:\.\d+)?)\s*%", r"(\1*0.01)", s)

        # Implicit multiplication:
        # Number followed by parenthesis: '2(' -> '2*('
        s = re.sub(r"(\d)\s*\(", r"\1*(", s)
        # Closing parenthesis followed by opening: ')(' -> ')*('
        s = re.sub(r"\)\s*\(", r")*(", s)
        # Closing parenthesis followed by number: ')2' -> ')*2'
        s = re.sub(r"\)\s*(\d)", r")*\1", s)
        # Number followed by identifier: '5sin' -> '5*sin', '5pi' -> '5*pi'
        s = re.sub(r"(\d)\s*([a-zA-Z])", r"\1*\2", s)
        # Closing parenthesis followed by identifier: ')sin' -> ')*sin'
        s = re.sub(r"\)\s*([a-zA-Z])", r")*\1", s)

        # Auto-close unbalanced parentheses
        open_count = s.count("(")
        close_count = s.count(")")
        if open_count > close_count:
            s += ")" * (open_count - close_count)

        return s

    @classmethod
    def evaluate(cls, expression: str) -> Union[float, int]:
        """
        Evaluates a mathematical expression safely.

        :param expression: Mathematical expression string
        :return: Computed numeric result (float or int)
        :raises ValueError, ZeroDivisionError, OverflowError
        """
        cleaned = cls.sanitize_expression(expression)
        if not cleaned:
            raise ValueError("Expression is empty.")

        try:
            node = ast.parse(cleaned, mode="eval")
        except SyntaxError as exc:
            raise ValueError(f"Invalid expression syntax: {exc.msg}") from exc

        return cls._eval_node(node.body)

    @classmethod
    def _eval_node(cls, node: ast.AST) -> Union[float, int]:
        """Recursive AST node visitor evaluating allowed mathematical operations."""

        # Numeric constants (e.g. 42, 3.14)
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

        # Identifiers (e.g. pi, e)
        if isinstance(node, ast.Name):
            name_lower = node.id.lower()
            if name_lower in cls.ALLOWED_CONSTANTS:
                return cls.ALLOWED_CONSTANTS[name_lower]
            raise ValueError(f"Unknown variable or constant: '{node.id}'")

        # Unary operations (+x, -x)
        if isinstance(node, ast.UnaryOp):
            operand = cls._eval_node(node.operand)
            if isinstance(node.op, ast.UAdd):
                return +operand
            if isinstance(node.op, ast.USub):
                return -operand
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")

        # Binary operations (a + b, a - b, a * b, a / b, a ** b, a % b)
        if isinstance(node, ast.BinOp):
            left = cls._eval_node(node.left)
            right = cls._eval_node(node.right)

            if isinstance(node.op, ast.Add):
                return SmartCalculator.add(left, right)
            if isinstance(node.op, ast.Sub):
                return SmartCalculator.subtract(left, right)
            if isinstance(node.op, ast.Mult):
                return SmartCalculator.multiply(left, right)
            if isinstance(node.op, ast.Div):
                return SmartCalculator.divide(left, right)
            if isinstance(node.op, ast.Pow):
                return SmartCalculator.power(left, right)
            if isinstance(node.op, ast.Mod):
                if right == 0:
                    raise ZeroDivisionError("Modulo by zero is not allowed.")
                return left % right

            raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")

        # Function calls (sin(x), cos(x), sqrt(x), etc.)
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Dynamic or nested function calls are not allowed.")

            func_name = node.func.id.lower()
            if func_name not in cls.ALLOWED_FUNCTIONS:
                raise ValueError(f"Function '{node.func.id}' is not recognized or not allowed.")

            func = cls.ALLOWED_FUNCTIONS[func_name]

            # Evaluate arguments
            args = [cls._eval_node(arg) for arg in node.args]
            if len(args) != 1:
                raise ValueError(f"Function '{func_name}' expects 1 argument, got {len(args)}.")

            return func(args[0])

        raise ValueError(f"Unsupported expression syntax: {type(node).__name__}")
