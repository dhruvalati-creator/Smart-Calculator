"""
History Manager Module
Handles saving, reading, and clearing calculation history using a JSON file.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any


class HistoryManager:
    """Manages calculation history persistence and retrieval."""

    def __init__(self, filepath: str = "data/history.json") -> None:
        """
        Initialize the HistoryManager with a target file path.

        :param filepath: Path to the JSON file where history will be stored.
        """
        self.filepath = filepath
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Ensures the directory and file exist with valid JSON array structure."""
        dir_name = os.path.dirname(self.filepath)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)

        if not os.path.exists(self.filepath):
            self._write_records([])

    def _read_records(self) -> List[Dict[str, Any]]:
        """Reads records from the JSON file safely."""
        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, list):
                    return data
                return []
        except (json.JSONDecodeError, FileNotFoundError, OSError):
            return []

    def _write_records(self, records: List[Dict[str, Any]]) -> None:
        """Writes records to the JSON file."""
        with open(self.filepath, "w", encoding="utf-8") as file:
            json.dump(records, file, indent=4)

    def add_record(self, expression: str, result: Any) -> Dict[str, Any]:
        """
        Appends a calculation record with timestamp to history.

        :param expression: Text representation of calculation, e.g. '12 + 5'
        :param result: Calculation outcome, e.g. 17
        :return: The recorded dictionary
        """
        record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "expression": expression,
            "result": result,
        }
        records = self._read_records()
        records.append(record)
        self._write_records(records)
        return record

    def get_history(self) -> List[Dict[str, Any]]:
        """Returns all calculation history records."""
        return self._read_records()

    def clear_history(self) -> bool:
        """Clears all calculation records."""
        try:
            self._write_records([])
            return True
        except OSError:
            return False

    def delete_record(self, index: int) -> bool:
        """
        Deletes a specific calculation record by its 0-based index.

        :param index: 0-based index of record to delete
        :return: True if deleted successfully, False otherwise
        """
        records = self._read_records()
        if 0 <= index < len(records):
            records.pop(index)
            self._write_records(records)
            return True
        return False
