# test_habit.py

import unittest
from unittest.mock import Mock
from habit import Habit

class TestHabit(unittest.TestCase):

    def setUp(self):
        """Set up test data and mock database for each test case."""
        self.mock_db = Mock()
        self.habit_id = 1
        self.name = 'Exercise'
        self.category = 'Health'
        self.periodicity = 1
        self.created_at = '2023-01-01'
        self.habit = Habit(self.habit_id, self.name, self.category, self.periodicity, self.created_at, self.mock_db)

    def test_calculate_current_streak_no_logs(self):
        """Test current streak calculation when there are no logs."""
        self.mock_db.get_habits_id.return_value = []
        self.assertEqual(self.habit.calculate_current_streak(), 0)

    def test_calculate_current_streak_with_logs(self):
        """Test current streak calculation with valid logs."""
        logs = [
            (1, 1, 1, '2023-08-03'),
            (2, 1, 1, '2023-08-02'),
            (3, 1, 1, '2023-08-01')
        ]
        self.mock_db.get_habits_id.return_value = logs
        self.assertEqual(self.habit.calculate_current_streak(), 3)

    def test_calculate_current_streak_with_break(self):
        """Test current streak calculation with a break in completion."""
        logs = [
            (1, 1, 1, '2023-08-03'),
            (2, 1, 1, '2023-07-31'),
            (3, 1, 1, '2023-07-30')
        ]
        self.mock_db.get_habits_id.return_value = logs
        self.assertEqual(self.habit.calculate_current_streak(), 1)

    def test_calculate_longest_streak_no_logs(self):
        """Test longest streak calculation when there are no logs."""
        self.mock_db.get_habits_id.return_value = []
        self.assertEqual(self.habit.calculate_longest_streak(), 0)

    def test_calculate_longest_streak_with_logs(self):
        """Test longest streak calculation with valid logs."""
        logs = [
            (1, 1, 1, '2023-08-01'),
            (2, 1, 1, '2023-08-02'),
            (3, 1, 1, '2023-08-03'),
            (4, 1, 0, '2023-08-04'),
            (5, 1, 1, '2023-08-05')
        ]
        self.mock_db.get_habits_id.return_value = logs
        self.assertEqual(self.habit.calculate_longest_streak(), 3)

    def test_calculate_longest_streak_with_break(self):
        """Test longest streak calculation with breaks."""
        logs = [
            (1, 1, 1, '2023-07-29'),
            (2, 1, 1, '2023-07-28'),
            (3, 1, 0, '2023-07-27'),
            (4, 1, 1, '2023-07-26'),
            (5, 1, 1, '2023-07-25')
        ]
        self.mock_db.get_habits_id.return_value = logs
        self.assertEqual(self.habit.calculate_longest_streak(), 2)

    def test_calculate_last_completed_no_logs(self):
        """Test last completed date when there are no logs."""
        self.mock_db.get_habits_id.return_value = []
        self.assertEqual(self.habit.calculate_last_completed(), "N/A")

    def test_calculate_last_completed_with_logs(self):
        """Test last completed date with valid logs."""
        logs = [
            (1, 1, 1, '2023-08-01'),
            (2, 1, 1, '2023-08-02'),
            (3, 1, 1, '2023-08-03')
        ]
        self.mock_db.get_habits_id.return_value = logs
        self.assertEqual(self.habit.calculate_last_completed(), '2023-08-03')

    def test_calculate_total_completed_no_logs(self):
        """Test total completed calculation when there are no logs."""
        self.mock_db.get_habits_id.return_value = []
        self.assertEqual(self.habit.calculate_total_completed(), 0)

    def test_calculate_total_completed_with_logs(self):
        """Test total completed calculation with valid logs."""
        logs = [
            (1, 1, 1, '2023-08-01'),
            (2, 1, 0, '2023-08-02'),
            (3, 1, 1, '2023-08-03')
        ]
        self.mock_db.get_habits_id.return_value = logs
        self.assertEqual(self.habit.calculate_total_completed(), 2)

if __name__ == '__main__':
    unittest.main()
