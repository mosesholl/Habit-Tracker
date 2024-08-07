from datetime import datetime


class Habit:
    """
    Represents a habit with associated methods to track its completion and streaks.
    """

    def __init__(self, habit_id, name, category, periodicity, created_at, habit_db):
        """
        Initializes a new Habit instance.

        Parameters:
        - habit_id (int): The unique identifier for the habit.
        - name (str): The name of the habit.
        - category (str): The category of the habit.
        - periodicity (int): The frequency (in days) at which the habit should be completed.
        - completed_at (str): The date the habit was last completed.
        - created_at (str): The date the habit was created.
        - updated_at (str): The date the habit was last updated.
        - habit_db: The database instance used to track the habit.
        """
        self.habit_id = habit_id
        self.name = name
        self.category = category
        self.periodicity = int(periodicity)  # Ensure periodicity is an integer
        self.created_at = created_at
        self.db = habit_db

    def calculate_current_streak(self):
        """
        Calculates the current streak of consecutive completions for the habit.

        Returns:
        int: The current streak of completions.
        """
        # Retrieve all logs for this habit from the database
        logs = self.db.get_habits_id(self.habit_id)

        # If no logs are found, the streak is zero
        if not logs:
            return 0

        # Filter logs to only include completed ones and sort by date in descending order
        logs = sorted([datetime.strptime(log[3], '%Y-%m-%d') for log in logs if log[2] == 1], reverse=True)

        # Initialize streak counter
        streak = 1
        for i in range(1, len(logs)):
            # Check if the difference between consecutive dates is within the periodicity
            if (logs[i - 1] - logs[i]).days <= self.periodicity:
                streak += 1  # Increment streak
            else:
                break  # Stop streak calculation if the gap is too long

        return streak

    def calculate_longest_streak(self):
        """
        Calculates the longest streak of consecutive completions for the habit.

        Returns:
        int: The longest streak of completions.
        """
        # Retrieve all logs for this habit from the database
        logs = self.db.get_habits_id(self.habit_id)

        # If no logs are found, the longest streak is zero
        if not logs:
            return 0

        # Filter logs to only include completed ones and sort by date in ascending order
        logs = sorted([datetime.strptime(log[3], '%Y-%m-%d') for log in logs if log[2] == 1])

        # Initialize counters for the longest and current streaks
        longest_streak = 1
        current_streak = 1

        for i in range(1, len(logs)):
            # Check if the difference between consecutive dates is within the periodicity
            if (logs[i] - logs[i - 1]).days <= self.periodicity:
                current_streak += 1  # Increment current streak
                longest_streak = max(longest_streak, current_streak)  # Update longest streak
            else:
                current_streak = 1  # Reset current streak if the gap is too long

        return longest_streak

    def calculate_last_completed(self):
        """
        Determines the last date the habit was completed.

        Returns:
        str: The last completion date as a string in 'YYYY-MM-DD' format, or "N/A" if no completion exists.
        """
        # Retrieve all logs for this habit from the database
        logs = self.db.get_habits_id(self.habit_id)

        # If no logs are found, return "N/A"
        if not logs:
            return "N/A"

        # Filter logs to only include completed ones
        logs = [datetime.strptime(log[3], '%Y-%m-%d') for log in logs if log[2] == 1]

        # Determine the most recent completion date
        last_completed = max(logs).strftime('%Y-%m-%d') if logs else "N/A"
        return last_completed

    def calculate_total_completed(self):
        """
        Calculates the total number of times the habit has been completed.

        Returns:
        int: The total number of completions.
        """
        # Retrieve all logs for this habit from the database
        logs = self.db.get_habits_id(self.habit_id)

        # If no logs are found, the total completions are zero
        if not logs:
            return 0

        # Sum up the completion status (assuming a status of 1 indicates completion)
        return sum(log[2] for log in logs)  # Count the number of completions