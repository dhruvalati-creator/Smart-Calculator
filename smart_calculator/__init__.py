"""
Smart Calculator Package
A modular scientific calculator with history tracking and professional GUI.
"""

from .calculator import SmartCalculator
from .history import HistoryManager
from .evaluator import SafeExpressionEvaluator
from .gui import SmartCalculatorGUI, start_gui

__all__ = [
    "SmartCalculator",
    "HistoryManager",
    "SafeExpressionEvaluator",
    "SmartCalculatorGUI",
    "start_gui",
]
