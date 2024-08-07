from tkinter import *
from tkinter import Tk, Toplevel, Label, Entry, Button, messagebox, END
from tkinter import ttk
import datetime

from db import Main_Db
from habit import Habit


class GUI:
    """
    A graphical user interface class for managing habits using Tkinter.
    """

    def __init__(self):
        """
        Initializes the main window and sets up the GUI components.
        """
        # Create the main window
        self.root = Tk()
        self.root.geometry('600x600')  # Set the window size
        self.root.title('Habit Tracker')  # Set the window title

        # Create and initialize the database instance
        self.habit_db = Main_Db()

        # Set up the headline label
        headline_label = Label(self.root, text='The Habit Tracker', font=('Arial', 60))
        headline_label.pack(pady=(10, 0))  # Add some padding to the top

        # Set up the description label
        hl_descr_label = Label(self.root, text='Become the master of your Habits', font=('Arial', 20))
        hl_descr_label.pack(pady=(10, 0))  # Add some padding to the top

        # Create and configure the "Add Habit" button
        add_habit_button = Button(
            self.root, text='Add Habit', font=('Arial', 30), command=self.open_add_habit_window
        )
        add_habit_button.pack(pady=(40, 0))  # Add some padding to the top

        # Create and configure the "Delete Habit" button
        delete_habit_button = Button(
            self.root, text='Delete Habit', font=('Arial', 30), command=self.open_delete_habit_window
        )
        delete_habit_button.pack(pady=(20, 0))  # Add some padding to the top

        # Create and configure the "Complete Habit" button
        complete_habit_button = Button(
            self.root, text='Complete Habit', font=('Arial', 30), command=self.open_complete_habit_window
        )
        complete_habit_button.pack(pady=(20, 0))  # Add some padding to the top

        # Create and configure the "Edit Habit" button
        edit_habit_button = Button(
            self.root, text='Edit Habit', font=('Arial', 30), command=self.open_edit_habit_window
        )
        edit_habit_button.pack(pady=(20, 0))  # Add some padding to the top

        # Create and configure the "Analyze Habits" button
        analyze_habit_button = Button(
            self.root, text='Analyze Habits', font=('Arial', 30), command=self.open_analyze_habit_window
        )
        analyze_habit_button.pack(pady=(20, 0))  # Add some padding to the top

        # Create and configure the "Add Predefined Habits" button
        pre_def_habit_button = Button(
            self.root, text='Add Predefined Habits', font=('Arial', 30), command=self.open_pre_def_habit_window
        )
        pre_def_habit_button.pack(pady=(20, 0))  # Add some padding to the top

        self.current_sort_col = None  # Keep track of the currently sorted column

        # Set up styles for the Treeview headings
        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", background="lightgray")  # Default heading style
        self.style.map("Treeview.Heading", background=[("active", "lightblue")])  # Style when active
        self.style.configure("Treeview.Highlighted", background="darkgray")  # Highlighted style for sorted column

    def open_edit_habit_window(self):
        """
        Opens a new Window to edit Habit
        """
        edit_habit_window = Toplevel(self.root) # Create a new top-level window
        edit_habit_window.title('Edit Habit') # set window title
        edit_habit_window.geometry('500x600') # Set Window size

        # Set up Headline label in the edit window
        headline_label = Label(edit_habit_window, text='Edit Habit', font=('Arial', 50))
        headline_label.pack(pady=(10, 0))

        # Set up the description label
        hl_descr_label = Label(edit_habit_window, text='Type in Habit ID and the updated Information. \n Press Edit to edit the Habit.', font=('Arial', 20))
        hl_descr_label.pack()

        # Create and configure the input fields and labels
        id_label = Label(edit_habit_window, text='ID: ', font=('Arial', 30))
        id_label.pack()
        id_entry = Entry(edit_habit_window, font=('Arial', 30))
        id_entry.pack()

        name_label = Label(edit_habit_window, text='Name: ', font=('Arial', 30))
        name_label.pack()
        name_entry = Entry(edit_habit_window, font=('Arial', 30))
        name_entry.pack()

        category_label = Label(edit_habit_window, text='Category: ', font=('Arial', 30))
        category_label.pack()
        category_entry = Entry(edit_habit_window, font=('Arial', 30))
        category_entry.pack()

        periodicity_label = Label(edit_habit_window, text='Periodicity: ', font=('Arial', 30))
        periodicity_label.pack()
        periodicity_entry = Entry(edit_habit_window, font=('Arial', 30))
        periodicity_entry.pack()
        periodicity_sublabel = Label(edit_habit_window, text='Enter the habit periodicity in days \n e.g., 1 = every day | 2 = every other day | 7 = every week ', font=('Arial', 10))
        periodicity_sublabel.pack()

        def edit_habit():
            habit_name = name_entry.get().strip()
            if self.habit_db.habit_exists(habit_name):
                # Show an error message if the habit already exists
                messagebox.showerror('Error', 'Habit with this name already exists!')
                return

            # update the habit in the database
            self.habit_db.edit_habits(id_entry.get(), habit_name,  periodicity_entry.get(), category_entry.get())

            # Clear the input fields
            id_entry.delete(0, END)
            name_entry.delete(0, END)
            category_entry.delete(0, END)
            periodicity_entry.delete(0, END)
            # Show a success message
            messagebox.showinfo('It worked!', 'Habit Edited')

        edit_button = Button(
            edit_habit_window, text='Edit', font=('Arial', 30), command=edit_habit
        )
        edit_button.pack(pady=(10, 0))




    def open_add_habit_window(self):
        """
        Opens a new window to add a habit.
        """
        add_habit_window = Toplevel(self.root)  # Create a new top-level window
        add_habit_window.title('Add Habit')  # Set window title
        add_habit_window.geometry('500x500')  # Set window size

        # Set up the headline label in the add habit window
        headline_label = Label(add_habit_window, text='Add Habit', font=('Arial', 50))
        headline_label.pack()

        # Set up the description label
        hl_descr_label = Label(add_habit_window, text='Type in Habit information and submit to the database', font=('Arial', 20))
        hl_descr_label.pack()

        # Create and configure the input fields and labels
        name_label = Label(add_habit_window, text='Name: ', font=('Arial', 30))
        name_label.pack()
        name_entry = Entry(add_habit_window, font=('Arial', 30))
        name_entry.pack()

        category_label = Label(add_habit_window, text='Category: ', font=('Arial', 30))
        category_label.pack()
        category_entry = Entry(add_habit_window, font=('Arial', 30))
        category_entry.pack()

        periodicity_label = Label(add_habit_window, text='Periodicity: ', font=('Arial', 30))
        periodicity_label.pack()
        periodicity_entry = Entry(add_habit_window, font=('Arial', 30))
        periodicity_entry.pack()
        periodicity_sublabel = Label(add_habit_window, text='Enter the habit periodicity in days \n e.g., 1 = every day | 2 = every other day | 7 = every week ', font=('Arial', 10))
        periodicity_sublabel.pack()

        def submit_habit():
            """
            Submits the new habit to the database.
            """
            habit_name = name_entry.get().strip()
            if self.habit_db.habit_exists(habit_name):
                # Show an error message if the habit already exists
                messagebox.showerror('Error', 'Habit with this name already exists!')
                return

            # Add the new habit to the database
            self.habit_db.add_habits(habit_name, category_entry.get(), periodicity_entry.get())
            # Clear the input fields
            name_entry.delete(0, END)
            category_entry.delete(0, END)
            periodicity_entry.delete(0, END)
            # Show a success message
            messagebox.showinfo('It worked!', 'Habit Submitted')

        # Create and configure the submit button
        submit_button = Button(add_habit_window, text='Submit', font=('Arial', 30), command=submit_habit)
        submit_button.pack()

    def open_delete_habit_window(self):
        """
        Opens a new window to delete a habit.
        """
        delete_habit_window = Toplevel(self.root)  # Create a new top-level window
        delete_habit_window.title('Delete Habit')  # Set window title
        delete_habit_window.geometry('500x500')  # Set window size

        # Set up the headline label in the delete habit window
        headline_label = Label(delete_habit_window, text='Delete Habit', font=('Arial', 50))
        headline_label.pack()

        # Set up the description label
        hl_descr_label = Label(delete_habit_window, text='Type in Habit ID to delete from database', font=('Arial', 20))
        hl_descr_label.pack()

        # Create and configure the input fields and labels
        delete_label = Label(delete_habit_window, text='Delete Habit with ID: ', font=('Arial', 30))
        delete_label.pack(pady=(50, 0))
        delete_entry = Entry(delete_habit_window, font=('Arial', 30))
        delete_entry.pack()

        def delete_habit():
            """
            Deletes the habit with the specified ID from the database.
            """
            self.habit_db.delete_habits(delete_entry.get())
            # Clear the entry after deletion
            delete_entry.delete(0, END)
            # Show a success message
            messagebox.showinfo('It worked!', 'Habit Deleted')

        # Create and configure the delete button
        delete_button = Button(delete_habit_window, text='Delete', font=('Arial', 30), command=delete_habit)
        delete_button.pack(pady=(20, 0))

    def open_complete_habit_window(self):
        """
        Opens a new window to mark a habit as completed.
        """
        complete_habit_window = Toplevel(self.root)  # Create a new top-level window
        complete_habit_window.title('Complete Habit')  # Set window title
        complete_habit_window.geometry('500x500')  # Set window size

        # Set up the headline label in the complete habit window
        headline_label = Label(complete_habit_window, text='Complete Habit', font=('Arial', 50))
        headline_label.pack()

        # Set up the description label
        hl_descr_label = Label(complete_habit_window, text='Type in Habit ID to complete', font=('Arial', 30))
        hl_descr_label.pack()

        # Create and configure the input fields and labels
        complete_label = Label(complete_habit_window, text='Complete Habit with ID: ', font=('Arial', 30))
        complete_label.pack(pady=(50, 0))
        complete_entry = Entry(complete_habit_window, font=('Arial', 30))
        complete_entry.pack()

        def complete_habit():
            """
            Marks the habit with the specified ID as completed.
            """
            habit_id = complete_entry.get()
            try:
                habit_id = int(habit_id)  # Convert the ID to an integer
                habits = self.habit_db.list_all_habits()
                habit = next((h for h in habits if h[0] == habit_id), None)
                if habit:
                    # Log the habit completion
                    completed_at = datetime.datetime.now().strftime('%Y-%m-%d')
                    self.habit_db.add_habit_log(habit_id, completed_at)

                    # Update streak calculations
                    habit_instance = Habit(*habit, self.habit_db)
                    current_streak = habit_instance.calculate_current_streak()
                    longest_streak = habit_instance.calculate_longest_streak()

                    # Show a success message
                    messagebox.showinfo("Success", "Habit completed successfully!")
                else:
                    # Show an error message if the habit ID is not found
                    messagebox.showerror("Error", "Habit ID not found.")
            except ValueError:
                # Show an error message if the input is not a valid number
                messagebox.showerror("Error", "Invalid Habit ID. Please enter a number.")

            # Clear the entry after the completion attempt
            complete_entry.delete(0, END)

        # Create and configure the complete button
        complete_button = Button(complete_habit_window, text='Complete', font=('Arial', 30), command=complete_habit)
        complete_button.pack(pady=(20, 0))

    def open_analyze_habit_window(self):
        """
        Opens a new window to analyze all habits.
        """
        analyze_habit_window = Toplevel(self.root)  # Create a new top-level window
        analyze_habit_window.title('Analyze Habits')  # Set window title
        analyze_habit_window.geometry('900x600')  # Set window size

        # Create and configure the Treeview widget
        tree = ttk.Treeview(analyze_habit_window)
        tree["columns"] = (
            "name", "category", "periodicity", "created_at", "current_streak", "longest_streak",
            "last_completed", "total_completed")

        # Configure the Treeview columns
        tree.heading("#0", text="Habit ID", anchor="w", command=lambda: self.sort_by_column(tree, "#0", False))
        tree.column("#0", anchor="w", width=80)

        for col in tree["columns"]:
            tree.heading(col, text=col, anchor="w", command=lambda c=col: self.sort_by_column(tree, c, False))
            tree.column(col, anchor="w", width=100)

        # Retrieve and display habit data in the Treeview
        habits = self.habit_db.list_all_habits()
        for habit in habits:
            habit_instance = Habit(*habit, self.habit_db)
            current_streak = habit_instance.calculate_current_streak()
            longest_streak = habit_instance.calculate_longest_streak()
            last_completed = habit_instance.calculate_last_completed()
            total_completed = habit_instance.calculate_total_completed()
            created_at_str = habit_instance.created_at.split()[0]  # Extract date part

            # Insert data into the Treeview
            tree.insert("", "end", text=habit_instance.habit_id, values=(habit_instance.name, habit_instance.category,
                                                                         habit_instance.periodicity, created_at_str,
                                                                         current_streak, longest_streak, last_completed,
                                                                         total_completed))
        tree.pack(expand=True, fill=BOTH)  # Expand Treeview to fill the window

    def open_pre_def_habit_window(self):
        """
        Opens a new window to mark a habit as completed.
        """
        pre_def_habit_window = Toplevel(self.root)  # Create a new top-level window
        pre_def_habit_window.title('Add Predefined Habits')  # Set window title
        pre_def_habit_window.geometry('500x500')  # Set window size

        # Set up the headline label in the complete habit window
        headline_label = Label(pre_def_habit_window, text='Add Predefined Habits', font=('Arial', 50))
        headline_label.pack()

        def add_pre_def_habit():
            """
            Inserts predefined habit into the database.
            """
            self.habit_db.add_habits("running", "sport", 1, created_at='2024-07-04')
            self.habit_db.add_habits("swimming", "sport", 7, created_at='2024-07-04')
            self.habit_db.add_habits("programming", "university", 2, created_at='2024-07-04')
            self.habit_db.add_habits("reading", "university", 7, created_at='2024-07-04')
            self.habit_db.add_habits("3L Water", "nutrition", 1, created_at='2024-07-04')

            # Inserts habit logs in to the database and retrieves habit ID
            habit_id = self.habit_db.get_habit_id_by_name("running")
            self.habit_db.add_habit_log(habit_id, '2024-07-05')
            self.habit_db.add_habit_log(habit_id, '2024-07-06')
            self.habit_db.add_habit_log(habit_id, '2024-07-07')
            self.habit_db.add_habit_log(habit_id, '2024-07-10')
            self.habit_db.add_habit_log(habit_id, '2024-07-12')
            self.habit_db.add_habit_log(habit_id, '2024-07-14')
            self.habit_db.add_habit_log(habit_id, '2024-07-15')
            self.habit_db.add_habit_log(habit_id, '2024-07-16')
            self.habit_db.add_habit_log(habit_id, '2024-07-17')
            self.habit_db.add_habit_log(habit_id, '2024-07-18')
            self.habit_db.add_habit_log(habit_id, '2024-07-19')
            self.habit_db.add_habit_log(habit_id, '2024-07-20')
            self.habit_db.add_habit_log(habit_id, '2024-07-22')
            self.habit_db.add_habit_log(habit_id, '2024-07-23')
            self.habit_db.add_habit_log(habit_id, '2024-07-24')
            self.habit_db.add_habit_log(habit_id, '2024-07-25')
            self.habit_db.add_habit_log(habit_id, '2024-07-26')
            self.habit_db.add_habit_log(habit_id, '2024-07-27')
            self.habit_db.add_habit_log(habit_id, '2024-07-28')
            self.habit_db.add_habit_log(habit_id, '2024-08-02')
            self.habit_db.add_habit_log(habit_id, '2024-08-03')

            habit_id = self.habit_db.get_habit_id_by_name("swimming")
            self.habit_db.add_habit_log(habit_id, '2024-07-10')
            self.habit_db.add_habit_log(habit_id, '2024-07-16')

            habit_id = self.habit_db.get_habit_id_by_name("programming")
            self.habit_db.add_habit_log(habit_id, '2024-07-06')
            self.habit_db.add_habit_log(habit_id, '2024-07-08')
            self.habit_db.add_habit_log(habit_id, '2024-07-10')
            self.habit_db.add_habit_log(habit_id, '2024-07-16')
            self.habit_db.add_habit_log(habit_id, '2024-07-17')
            self.habit_db.add_habit_log(habit_id, '2024-07-19')
            self.habit_db.add_habit_log(habit_id, '2024-07-21')
            self.habit_db.add_habit_log(habit_id, '2024-07-23')
            self.habit_db.add_habit_log(habit_id, '2024-07-25')
            self.habit_db.add_habit_log(habit_id, '2024-08-01')
            self.habit_db.add_habit_log(habit_id, '2024-08-02')
            self.habit_db.add_habit_log(habit_id, '2024-08-03')

            habit_id = self.habit_db.get_habit_id_by_name("reading")
            self.habit_db.add_habit_log(habit_id, '2024-07-10')
            self.habit_db.add_habit_log(habit_id, '2024-07-20')
            self.habit_db.add_habit_log(habit_id, '2024-07-26')

            habit_id = self.habit_db.get_habit_id_by_name("3L Water")
            self.habit_db.add_habit_log(habit_id, '2024-07-05')
            self.habit_db.add_habit_log(habit_id, '2024-07-06')
            self.habit_db.add_habit_log(habit_id, '2024-07-07')
            self.habit_db.add_habit_log(habit_id, '2024-07-10')
            self.habit_db.add_habit_log(habit_id, '2024-07-12')
            self.habit_db.add_habit_log(habit_id, '2024-07-14')
            self.habit_db.add_habit_log(habit_id, '2024-07-15')
            self.habit_db.add_habit_log(habit_id, '2024-07-16')
            self.habit_db.add_habit_log(habit_id, '2024-07-17')
            self.habit_db.add_habit_log(habit_id, '2024-07-27')
            self.habit_db.add_habit_log(habit_id, '2024-08-01')
            self.habit_db.add_habit_log(habit_id, '2024-08-02')
            self.habit_db.add_habit_log(habit_id, '2024-08-03')


            # Shows a success message
            messagebox.showinfo('It worked!', 'Predefined Habits Added')

        add_button = Button(pre_def_habit_window,  text='Add', font=('Arial', 30), command=add_pre_def_habit)
        add_button.pack(pady=(50, 0))



    def sort_by_column(self, tree, col, descending):
        """
        Sorts the Treeview by the specified column.

        Parameters:
        - tree (ttk.Treeview): The Treeview widget to sort.
        - col (str): The column to sort by.
        - descending (bool): Whether to sort in descending order.
        """
        # Retrieve and sort data
        data_list = [(tree.set(child, col) if col != "#0" else tree.item(child, "text"), child) for child in
                     tree.get_children('')]

        if col in ["current_streak", "longest_streak", "total_completed", "Habit ID", "#0"]:
            data_list.sort(key=lambda t: int(t[0]), reverse=descending)
        else:
            data_list.sort(reverse=descending, key=lambda x: x[0])

        for index, (_, child) in enumerate(data_list):
            tree.move(child, '', index)

        # Update column heading to reflect the current sort state
        tree.heading(col, command=lambda: self.sort_by_column(tree, col, not descending))

        # Remove highlight from the previous sorted column
        if self.current_sort_col is not None:
            self.style.configure(f"Treeview.Heading.{self.current_sort_col}", background="lightgray")

        # Highlight the new sorted column
        self.style.configure(f"Treeview.Heading.{col}", background="darkgray")

        # Update the current sort column
        self.current_sort_col = col

    def run(self):
        """
        Starts the Tkinter main loop.
        """
        self.root.mainloop()
