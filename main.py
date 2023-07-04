import typer
from myHabits import Habit
from db import get_db, create_table, insert_habit, show_habits, modify_habit, check_off_habit, check_habit_in_schedule, check_db_exists, del_habit
from analyse import get_all_habits_same_period, longest_streak, get_longest_streak_choose_habit, get_reason_and_failure_strategy

app = typer.Typer(add_completion=False, help="""
This is an App to track your Habits based on a fixed Schedule.\n
Keep in mind that you can cancel any process, that asks you for an input.\n
To do so, just type in 'CANCEL'. Enjoy!
""")


def habit_name_check(db, habit_name):
    cur = db.cursor()
    cur.execute('SELECT name FROM habits WHERE name =?', [habit_name])
    return cur.fetchone() is not None
# Checks if the habit is already in the DB, before entering all other values.


@app.command()
def create_habit():
    db = get_db()
    create_table(db)
    habit = Habit("", "", "", "", "", "", "", "", "")
    habit.get_habit_name()
    while habit_name_check(db, habit.name):
        typer.echo("You already got that Habit in your List. Please choose another Habit, which you want to add.")
        habit.get_habit_name()
    habit.get_frequency()
    habit.get_duration()
    habit.get_habit_status()
    habit.get_times()
    insert_habit(db, habit.name, habit.frequency, habit.duration, habit.checked_status, habit.streak, habit.check_date,
                 habit.checked_timestamp)
    typer.echo("Good Job, you added a new Habit!")


@app.command()
def show_all_habits():
    db = get_db()
    check_db_exists(db)
    show_habits(db)

@app.command()
def edit_habit():
    db = get_db()
    check_db_exists(db)
    modify_habit(db)


@app.command()
def delete_habit():
    db = get_db()
    check_db_exists(db)
    del_habit(db)


@app.command()
def check_habit():
    db = get_db()
    check_db_exists(db)
    check_off_habit(db)


@app.command()
def get_longest_streak():
    db = get_db()
    check_db_exists(db)
    longest_streak(db)


@app.command()
def choose_habit_for_longest_streak():
    db = get_db()
    check_db_exists(db)
    get_longest_streak_choose_habit(db)


@app.command()
def all_habits_same_period():
    db = get_db()
    check_db_exists(db)
    get_all_habits_same_period(db)


@app.command()
def get_reason_and_strategy():
    db = get_db()
    check_db_exists(db)
    show_habits(db)
    get_reason_and_failure_strategy(db)


check_habit_in_schedule(get_db())
if __name__ == "__main__":
    app()

