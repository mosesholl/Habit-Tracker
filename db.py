import sqlite3
from datetime import datetime

class Main_Db:
    """
    A class to manage the database operations for habits and habit logs using SQLite.
    """

    def __init__(self, db_path="main.db"):
        """
        Initializes the database connection and cursor.

        Parameters:
        - db_path (str): Path to the SQLite database file. Defaults to "main.db".
        """
        # Connect to the SQLite database (or create it if it doesn't exist)
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()

    def create_table(self):
        """
        Creates the necessary tables in the database if they do not already exist.
        """
        # Create the 'habits' table if it does not exist
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS habits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        periodicity INTEGER,
        category TEXT,
        created_at DATETIME)
        """)
        self.conn.commit()

        # Create the 'habit_logs' table if it does not exist
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS habit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER,
        completed INTEGER,
        completed_at TEXT,
        FOREIGN KEY(habit_id) REFERENCES habits(id))
        """)
        self.conn.commit()

    def edit_habits(self, habit_id, name, periodicity, category):
        query="UPDATE habits SET name=?, periodicity=?, category=? WHERE id=?"
        self.cur.execute(query, (name, category, periodicity, habit_id))
        self.conn.commit()

    def habit_exists(self, habit_name):
        """
        Checks if a habit with the given name exists in the database.

        Parameters:
        - habit_name (str): The name of the habit to check.

        Returns:
        - bool: True if the habit exists, otherwise False.
        """
        # Retrieve all habits and check if any habit has the given name
        habits = self.list_all_habits()
        return any(habit[1] == habit_name for habit in habits)

    def add_habits(self, name, periodicity, category, created_at=datetime.now().strftime('%Y-%m-%d')):
        """
        Adds a new habit to the database.

        Parameters:
        - name (str): The name of the habit.
        - periodicity (int): The periodicity of the habit in days.
        - category (str): The category of the habit.
        - completed_at (int): The default value for completed_at, usually 0.
        """
        query = "INSERT INTO habits (name, periodicity, category, created_at) VALUES (?, ?, ?, ?)"
        self.cur.execute(query, (name, periodicity, category, created_at))
        self.conn.commit()

    def delete_habits(self, habit_id):
        """
        Deletes a habit from the database based on its ID.

        Parameters:
        - habit_id (int): The ID of the habit to delete.
        """
        query = "DELETE FROM habits WHERE id = ?"
        self.cur.execute(query, (habit_id,))
        self.conn.commit()

    def list_all_habits(self):
        """
        Retrieves all habits from the database.

        Returns:
        - list: A list of tuples representing all habits.
        """
        query = "SELECT * FROM habits"
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_habits_id(self, habit_id):
        """
        Retrieves all logs for a specific habit based on its ID.

        Parameters:
        - habit_id (int): The ID of the habit.

        Returns:
        - list: A list of tuples representing all logs for the specified habit.
        """
        query = "SELECT * FROM habit_logs WHERE habit_id = ?"
        self.cur.execute(query, (habit_id,))
        return self.cur.fetchall()

    def add_habit_log(self, habit_id, completed_at):
        """
        Adds a log entry for a habit completion.

        Parameters:
        - habit_id (int): The ID of the habit.
        - completed_at (str): The date and time when the habit was completed.
        """
        query = "INSERT INTO habit_logs (habit_id, completed_at, completed) VALUES (?, ?, ?)"
        self.cur.execute(query, (habit_id, completed_at, 1))  # 'completed' is set to 1 to mark completion
        self.conn.commit()


    def complete_habits(self, habit_id, completed_at):
        """
        Marks a habit as completed in the logs and updates the habit's updated_at field.

        Parameters:
        - habit_id (int): The ID of the habit.
        - completed_at (str): The date and time when the habit was completed.
        """
        # Update the habit_logs to mark the completion
        query = "UPDATE habit_logs SET completed = 1 WHERE completed_at = ? AND habit_id = ?"
        self.cur.execute(query, (completed_at, habit_id))
        self.conn.commit()

        # Update the updated_at field in the habits table
        self.update_habit_updated_at(habit_id)

    def get_habit_id_by_name(self, habit_name):
        """
        Retrieves the habit ID for a specific habit.
        :param habit_name:
        :return:
        """
        query = "SELECT id FROM habits WHERE name = ?"
        self.cur.execute(query, (habit_name,))
        result = self.cur.fetchone()
        return result[0] if result else None


