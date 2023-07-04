import matplotlib.pyplot as plt
import sqlite3
import time
from helpers import get_input
from rich.table import Table
from rich.console import Console
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
progress_bar = Progress(
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    BarColumn(),
    MofNCompleteColumn(),
    TextColumn("•"),
    TimeElapsedColumn(),
    TextColumn("•"),
    TimeRemainingColumn(),
)


def get_db(name="main.db"):
    db = sqlite3.connect(name)
    return db


def get_all_habits_same_period(db):
    """
     Function to display all habits with its actual streak of a chosen frequency. Result will be printed as table in
     terminal and as a diagram.

     :param db: initialized sqlite3 database connection
     """

    chosen_frequency = str.lower(get_input('What is the periodicity of the habits you want to see? '
                                           'Please type in "d" or "daily, "w" or "weekly, "m" or "monthly"'))
    if chosen_frequency == "d" or chosen_frequency == "daily":
        chosen_frequency = 'd'
    elif chosen_frequency == "w" or chosen_frequency == "weekly":
        chosen_frequency = 'w'
    elif chosen_frequency == "m" or chosen_frequency == "monthly":
        chosen_frequency = 'm'
    else:
        print('No valid periodicity found')
        return
    cur = db.cursor()
    cur.execute('''SELECT name, frequency, duration, checked_status, streak FROM habits WHERE frequency =? ''', chosen_frequency)
    rows = cur.fetchall()
    if len(rows) == 0:
        print("No Habits found")
        return
    else:
        with progress_bar as p:
            for i in p.track(range(len(rows))):
                time.sleep(0.05)
                pass
        table = Table(title=f"[bold][red]A list of all your Habits with a periodicity of '{chosen_frequency}'", style="blue")
        table.add_column("Name", justify="center", style="bold cyan")
        table.add_column("Frequency", justify="right", style="red")
        table.add_column("Duration\n(min)", justify="right")
        table.add_column("Current streak", justify="right", style="bold green")
        habit_names = []
        streaks = []
        for row in rows:
            name, frequency, duration, checked_status, streak = row
            table.add_row(name, frequency, str(duration), str(streak))
            habit_names.append(row[0])
            streaks.append(row[4])

        console = Console()
        console.print(table)

        plt.figure(figsize=(13, 6))
        plt.bar(habit_names, streaks, width=0.3)
        plt.xlabel('Habits')
        plt.ylabel('Streaks')
        plt.title('Comparison of streaks for each habit in the given periodicity')
        plt.xticks(rotation=40)
        plt.tight_layout()
        plt.show()

    db.commit()


def longest_streak(db):
    """
        Function to display the habit with the longest streak, even if the streak is already lost.
        :param db: initialized sqlite3 database connection
        """
    cur = db.cursor()
    cur.execute('''SELECT name, MAX(streak) 
                    FROM(
                        SELECT h.name, h.streak FROM habits h
                        UNION
                        SELECT h.name, m.streak FROM habits h JOIN meta_information m ON h.id = m.habit_id
                        ) AS combined GROUP BY name ORDER BY streak DESC ''')
    result1 = cur.fetchone()
    cur.execute('''SELECT name, MAX(streak) FROM habits ORDER BY streak DESC''')
    result2 = cur.fetchone()
    if len(result1) == 0:
        print("No Habit with a Streak found")
        return
    else:
        if result2[1] == result1[1] or result2[1] >= result1[1]:
            print(f"Your actual highest Streak at the moment is '{result2[0]}' with a Streak of {result2[1]}")
        else:
            print(f"The Habit with the highest streak you've reached so far is '{result1[0]}' with a Streak of {result1[1]}")
            print(f"Your actual highest Streak at the moment is '{result2[0]}' with a Streak of {result2[1]}")

    db.commit()


def get_longest_streak_choose_habit(db):
    """
           Function to display a chosen habit with its actual streak.
           :param db: initialized sqlite3 database connection
           """
    cur = db.cursor()
    habit_chosen = str(get_input('For which Habit you want to display your actual longest Streak?'))
    cur.execute('''SELECT name, streak, frequency 
                        FROM habits WHERE name=? ORDER BY streak DESC LIMIT 1''', [habit_chosen])
    results = cur.fetchall()
    if len(results) == 0:
        print("Unfortunately you dont have that Habit in your schedule")
        return
    else:
        for result in results:
            name, streak, frequency = result
            if streak == 0:
                print(f"It seems like you didnt reach any streak so far for your Habit '{name}'")
            else:
                if frequency == "d" and streak == 1:
                    time = "day"
                elif frequency == "d" and streak != 1:
                    time = "days"
                elif frequency == "w" and streak == 1:
                    time = "week"
                elif frequency == "w" and streak != 1:
                    time = "weeks"
                elif frequency == "m" and streak == 1:
                    time = "month"
                elif frequency == "m" and streak != 1:
                    time = "months"
                print(
                    f"For the Habit '{name}' you've reached a Streak of {streak} so far. That means you accomplished "
                    f"to check off your Habit for {streak} {time} in a row. Well done, keep it up!")

    db.commit()


def get_reason_and_failure_strategy(db):
    """
           Function to return reason for failure and how you could prevent further failures regarding the habit.
           :param db: initialized sqlite3 database connection
           """
    cur = db.cursor()
    habit_chosen = str(get_input('For which Habit you want to display your Reasons for failure and their Strategies?'))
    cur.execute('''
        SELECT habits.name AS HabitName, reason_for_failure.reason AS FailureReason, strategy_for_failure_elimination.strategy 
        AS Strategy FROM habits
        JOIN habit_reasons_strategies on habits.id = habit_reasons_strategies.habit_id
        JOIN reason_for_failure ON habit_reasons_strategies.reason_id = reason_for_failure.id
        JOIN strategy_for_failure_elimination ON habit_reasons_strategies.strategy_id = strategy_for_failure_elimination.id
        WHERE habits.name=? ''', [habit_chosen])
    results = cur.fetchall()
    dict_of_habits = {}
    if len(results) == 0:
        print("Unfortunately you dont have that Habit in your schedule")
        return
    else:
        for result in results:
            habit_name, reason, strategy = result
            if habit_name in dict_of_habits:
                if reason is not None:
                    dict_of_habits[habit_name]["reasons"].add(reason)
                if strategy is not None:
                    dict_of_habits[habit_name]["strategies"].add(strategy)
            else:
                dict_of_habits[habit_name] = {"reasons": set(), "strategies": set()}
                if reason is not None:
                    dict_of_habits[habit_name]["reasons"].add(reason)
                if strategy is not None:
                    dict_of_habits[habit_name]["strategies"].add(strategy)
        for habit_name, details in dict_of_habits.items():
            print(f"Habit Name: {habit_name}")
            if len(dict_of_habits[habit_name]["reasons"]) > 1:
                print(f"Your Reasons for Failures regarding '{habit_name}' are:")
            else:
                print(f"Your Reason for Failure regarding '{habit_name}' is: ")
            for reason in details["reasons"]:
                print(f"- {reason}")
            if len(dict_of_habits[habit_name]["strategies"]) > 1:
                print(f"Your Strategies to avoid further Failures regarding '{habit_name}' are:")
            else:
                print(f"Your Strategy to avoid another Failure regarding '{habit_name}' is: ")
            for strategy in details["strategies"]:
                print(f"- {strategy}")
            print("\n")
    db.commit()
