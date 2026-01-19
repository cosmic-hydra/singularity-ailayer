"""Tests for driver module."""
import pytest
from unittest.mock import patch, MagicMock


class TestActionParsing:
    """Tests for action parsing functionality."""

    def test_parse_json_actions(self, sample_action_json):
        """Test parsing of action JSON."""
        actions = sample_action_json["actions"]

        assert len(actions) == 3
        assert actions[0]["act"] == "click_element"
        assert actions[1]["act"] == "text_entry"
        assert actions[2]["act"] == "press_key"

    def test_keyboard_shortcut_parsing(self):
        """Test keyboard shortcut pattern matching."""
        import re

        keys_pattern = (
            r"\b(Win(?:dows)?|Ctrl|Alt|Shift|Enter|Space(?:\s*Bar)?|Tab|Esc(?:ape)?|"
            r"Backspace|Insert|Delete|Home|End|Page\s*Up|Page\s*Down|"
            r"(?:Arrow\s*)?(?:Up|Down|Left|Right)|F1|F2|F3|F4|F5|F6|F7|F8|F9|"
            r"F10|F11|F12|[A-Z0-9])\b"
        )

        test_input = "Ctrl + Shift + N"
        keys = re.findall(keys_pattern, test_input, re.IGNORECASE)

        assert "Ctrl" in keys
        assert "Shift" in keys
        assert "N" in keys


class TestDatabaseOperations:
    """Tests for database operations."""

    def test_create_database(self, tmp_path):
        """Test database creation."""
        import sqlite3

        db_path = tmp_path / "test_history.db"
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS app_cases (
                id INTEGER PRIMARY KEY,
                app_name TEXT NOT NULL,
                title TEXT NOT NULL,
                instructions TEXT NOT NULL,
                UNIQUE(app_name, title, instructions)
            )
        """
        )
        conn.commit()
        conn.close()

        assert db_path.exists()

    def test_add_case_to_database(self, tmp_path):
        """Test adding a case to the database."""
        import sqlite3
        import json

        db_path = tmp_path / "test_history.db"
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS app_cases (
                id INTEGER PRIMARY KEY,
                app_name TEXT NOT NULL,
                title TEXT NOT NULL,
                instructions TEXT NOT NULL,
                UNIQUE(app_name, title, instructions)
            )
        """
        )

        instructions = {"actions": [{"act": "click", "step": "button"}]}
        cursor.execute(
            "INSERT INTO app_cases (app_name, title, instructions) VALUES (?, ?, ?)",
            ("firefox", "test goal", json.dumps(instructions)),
        )
        conn.commit()

        cursor.execute("SELECT * FROM app_cases")
        rows = cursor.fetchall()
        conn.close()

        assert len(rows) == 1
        assert rows[0][1] == "firefox"
