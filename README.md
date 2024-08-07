# Habit Tracker

## Table of Contents
1. [Description](#Description)
2. [Installation](#Installation)
3. [Usage and main Functionalities](#Usage-and-main-Functionalities)
4. [Contributing](#Contributing)

## Description
'We first make our Habits that our Habits makes us.' -John Dryden. The Habit Tracker is meant to be used as a tool to 
introduce and maintain good habits in your life. It is possible to create habits with a certain periodicity, and category 
and complete them within the set periodicity. If done so a streak is formed which can be analyzed within the analyze menu. 
These streaks work as a motivating factor but also help to analyze where one struggles the most. It is also possible to 
analyze how often a habit was completed over all, how long the longest streak was, when a habit was created and when it 
was completed last. The user is also abled to order the Habits by Category, streak, longest streak, created at, name, id
and total completed to have an overview of witch habits come easier to him and with which he tends to struggle more.

## Installation

**Requirements:** 
Make sure you have Python 3.8+ installed on your computer. You can download the latest version of Python 
[here](https://www.python.org/downloads/). 

**Req Package**
Use the package manager to pip install Tkinter.
```bash
pip install tkinter
```

## Usage and main Functionalities

### Start the Habit Tracker
To start the Habit Tracker simply run the main.py and the Start Window will pop up. The Start Window has 5 Buttons.

#### Add Habit
If you press the Add Habit button the Add Habit window will pop up. Here you can type in a name, category and periodicity 
and insert a new habit to the database. A message Box will pop up to tell you your operation was succesfull.

#### Complete Habit
In the Complete Habit window you can enter the Habit ID of a habit to mark it as completed. A message Box will pop up 
to tell you your operation was succesfull.

#### Delete Habit
In the Delete Habit Window you can type in the Habit Id of a certain Habit to delete it from the database. A Massage Box 
will pop up to tell you your operation was succesfull.

#### Edit Habits
In the Edit Habit Window you can type in the Id of a Habit followed by the new information you would like to give the habit.

#### Analyze Habits
The Analyze Window is a tkinter Treeview. It shows all Habits in a table with the following information. ID, Name, Category,
Periodicity, current streak, longest streak, last completed at, created_at, total completed. You will be abled to order 
them in ascending or descending order depending on which header you will press.

#### Add Predefined Habits
IN the Predefined Habits Window a simple add Button will show up, if pressed it will add 5 Habits with Log Data of over 4 Weeks 
will be added to the Database. A message Box will pop up to tell you the data was inserted.


## Contributing
Please feel free to contribute pull requests or create issues for bugs and feature requests.



