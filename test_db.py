# test_main_db.py

import unittest
from unittest.mock import patch, Mock
from db import Main_Db

class TestMainDb(unittest.TestCase):

    @patch('db.sqlite3.connect')
    def setUp(self, mock_connect):
        """Set up mock database connection and cursor for each test."""
        # Create a mock connection and cursor
        self.mock_conn = Mock()
        self.mock_cursor = Mock()
        self.mock_conn.cursor.return_value = self.mock_cursor
        mock_connect.return_value = self.mock_conn

        # Initialize Main_Db with a mocked connection
        self.db = Main_Db()

    def test_create_table(self):
        """Test table creation in the database."""
        self.db.create_table()
        self.mock_cursor.execute.assert_any_call("""
        CREATE TABLE IF NOT EXISTS habits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        periodicity INTEGER,
        category TEXT,
        created_at DATETIME)
        """)
        self.mock_cursor.execute.assert_any_call("""
        CREATE TABLE IF NOT EXISTS habit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER,
        completed INTEGER,
        completed_at TEXT,
        FOREIGN KEY(habit_id) REFERENCES habits(id))
        """)
        self.assertEqual(self.mock_conn.commit.call_count, 2)

    def test_add_habits(self):
        """Test adding a habit to the database."""
        name = 'Exercise'
        periodicity = 1
        category = 'Health'
        created_at = '2023-08-05'

        self.db.add_habits(name, periodicity, category, created_at)
        self.mock_cursor.execute.assert_called_once_with(
            "INSERT INTO habits (name, periodicity, category, created_at) VALUES (?, ?, ?, ?)",
            (name, periodicity, category, created_at)
        )
        self.mock_conn.commit.assert_called_once()

    def test_delete_habits(self):
        """Test deleting a habit from the database."""
        habit_id = 1
        self.db.delete_habits(habit_id)
        self.mock_cursor.execute.assert_called_once_with(
            "DELETE FROM habits WHERE id = ?",
            (habit_id,)
        )
        self.mock_conn.commit.assert_called_once()

    def test_list_all_habits(self):
        """Test retrieving all habits from the database."""
        expected_result = [
            (1, 'Exercise', 1, 'Health', '2023-08-05'),
            (2, 'Read', 2, 'Education', '2023-08-06')
        ]
        self.mock_cursor.fetchall.return_value = expected_result

        result = self.db.list_all_habits()
        self.mock_cursor.execute.assert_called_once_with("SELECT * FROM habits")
        self.assertEqual(result, expected_result)

    def test_get_habits_id(self):
        """Test retrieving habit logs by habit ID."""
        habit_id = 1
        expected_result = [
            (1, 1, 1, '2023-08-03'),
            (2, 1, 1, '2023-08-02')
        ]
        self.mock_cursor.fetchall.return_value = expected_result

        result = self.db.get_habits_id(habit_id)
        self.mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM habit_logs WHERE habit_id = ?",
            (habit_id,)
        )
        self.assertEqual(result, expected_result)

    def test_add_habit_log(self):
        """Test adding a habit log entry."""
        habit_id = 1
        completed_at = '2023-08-05'

        self.db.add_habit_log(habit_id, completed_at)
        self.mock_cursor.execute.assert_called_once_with(
            "INSERT INTO habit_logs (habit_id, completed_at, completed) VALUES (?, ?, ?)",
            (habit_id, completed_at, 1)
        )
        self.mock_conn.commit.assert_called_once()

    def test_habit_exists_true(self):
        """Test checking if a habit exists (habit exists)."""
        self.db.list_all_habits = Mock(return_value=[(1, 'Exercise', 1, 'Health', '2023-08-05')])
        result = self.db.habit_exists('Exercise')
        self.assertTrue(result)

    def test_habit_exists_false(self):
        """Test checking if a habit exists (habit does not exist)."""
        self.db.list_all_habits = Mock(return_value=[(1, 'Exercise', 1, 'Health', '2023-08-05')])
        result = self.db.habit_exists('Reading')
        self.assertFalse(result)

    def test_complete_habits(self):
        """Test completing a habit."""
        habit_id = 1
        completed_at = '2023-08-05'

        self.db.update_habit_updated_at = Mock()  # Mock this function since it's not defined here
        self.db.complete_habits(habit_id, completed_at)

        self.mock_cursor.execute.assert_any_call(
            "UPDATE habit_logs SET completed = 1 WHERE completed_at = ? AND habit_id = ?",
            (completed_at, habit_id)
        )
        self.mock_conn.commit.assert_called_once()
        self.db.update_habit_updated_at.assert_called_once_with(habit_id)

    def test_get_habit_id_by_name(self):
        """Test getting habit ID by name."""
        habit_name = 'Exercise'
        self.mock_cursor.fetchone.return_value = (1,)

        result = self.db.get_habit_id_by_name(habit_name)
        self.mock_cursor.execute.assert_called_once_with(
            "SELECT id FROM habits WHERE name = ?",
            (habit_name,)
        )
        self.assertEqual(result, 1)

    def test_get_habit_id_by_name_not_found(self):
        """Test getting habit ID by name when habit is not found."""
        habit_name = 'Nonexistent'
        self.mock_cursor.fetchone.return_value = None

        result = self.db.get_habit_id_by_name(habit_name)
        self.mock_cursor.execute.assert_called_once_with(
            "SELECT id FROM habits WHERE name = ?",
            (habit_name,)
        )
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()

