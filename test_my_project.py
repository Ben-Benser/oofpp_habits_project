from myHabits import Habit
from db import get_db, create_table, insert_habit, show_habits, modify_habit, check_off_habit, check_habit_in_schedule, del_habit
import datetime
from analyse import get_all_habits_same_period, longest_streak, get_longest_streak_choose_habit, get_reason_and_failure_strategy
current_time = datetime.datetime.now()


class TestHabitTracker:

    def setup_method(self):
        self.db = get_db("test.db")

    def test_create_table(self):
        create_table(self.db)

    def test_habit(self, monkeypatch):
        inputs = iter(["hiking", "d", 20, "no", 45, current_time.isoweekday(), None, None, None])
        monkeypatch.setattr('typer.prompt', lambda _: next(inputs))
        habit = Habit("", "", "", "", "", "", "", "", "")
        habit.get_habit_name()
        habit.get_frequency()
        habit.get_duration()
        habit.get_habit_status()
        habit.get_times()
        insert_habit(self.db, habit.name, habit.frequency, habit.duration, habit.checked_status, habit.streak,
                     habit.check_date,habit.checked_timestamp)

    def test_show_habit(self):
        show_habits(self.db)

    def test_check_off_habit(self, monkeypatch):
        inputs = iter(['d', 'ausreichend schlafen'])
        monkeypatch.setattr('typer.prompt', lambda _: next(inputs))
        check_off_habit(self.db)

    def test_habit_checked_scheduled(self, monkeypatch):
        inputs = iter(['Ich war zu lange im Büro',
                       'Zukünftig früher mit der Arbeit beginnen, um rechtzeitig das Büro verlassen zu können'])
        monkeypatch.setattr('typer.prompt', lambda _: next(inputs))
        check_habit_in_schedule(self.db)

    def test_get_habits_same_period(self, monkeypatch):
        monkeypatch.setattr('typer.prompt', lambda _: "d")
        get_all_habits_same_period(self.db)

    def test_get_habit_longest_streak(self):
        longest_streak(self.db)

    def test_choose_habit_longest_streak(self, monkeypatch):
        monkeypatch.setattr('typer.prompt', lambda _: "hiking")
        get_longest_streak_choose_habit(self.db)

    def test_receive_reason_and_failure_strategy(self, monkeypatch):
        monkeypatch.setattr('typer.prompt', lambda _: "hiking")
        get_reason_and_failure_strategy(self.db)

    def test_edit_a__habit(self, monkeypatch):
        inputs = iter(['name', 'hiking', 'wandering'])
        monkeypatch.setattr('typer.prompt', lambda _: next(inputs))
        modify_habit(self.db)

    def test_del_a__habit(self, monkeypatch):
        monkeypatch.setattr('typer.prompt', lambda _: "running")
        del_habit(self.db)

