import typer
import datetime
from helpers import get_input


class Habit:
    def __init__(self, name="", frequency="", duration=0, checked_status=1,  streak=0, check_date = None, checked_timestamp=None, reason_failure=None, avoidance_strategy=None):
        """
        Habit class to track and save habits

        :param name: name of the Habit
        :param frequency: frequency of the Habit
        :param duration: Duration of the Habit
        :param checked_status: checked_status of the Habit. Clarifies, whether a habit has already been done, before
        entering the habit into the DB
        :param streak: Streak for the Habit
        :param check_date: Defines the integer of isocalender-date as periodicity - rule
        :param checked_timestamp: Datetime that stands for the last Check Off
        :param reason_failure: reason why a habit didn't get checked off
        :param avoidance_strategy: strategy of how to avoid further failure
        """
        self.name = name
        self.frequency = frequency
        self.duration = duration
        self.checked_status = checked_status
        self.streak = streak
        self.check_date = check_date
        self.checked_timestamp = checked_timestamp
        self.reason_failure = reason_failure
        self.avoidance_strategy = avoidance_strategy

    def get_habit_name(self):
        habit_name = get_input("What's the Habit you want to pass in?")
        self.name = habit_name

    def get_frequency(self):
        while True:
            habit_frequency = str.lower(get_input('Type in "d" for daily, "w" for weekly or "m" for monthly '))
            if habit_frequency in ['d', 'daily', 'w', 'weekly', 'm', 'monthly']:
                self.frequency = habit_frequency
                break
            else:
                typer.echo("Invalid input. Please enter 'd', 'daily', 'w', 'weekly', 'm', 'monthly'.")

    def get_duration(self):
        while True:
            habit_duration = get_input("Do you have a specific time you want to spend on the habit? "
                                       "If not, type in '0'. Otherwise type in the amount of minutes.")
            try:
                self.duration = int(habit_duration)
                break
            except ValueError:
                typer.echo("Invalid input. Please enter a number which represents "
                           "the amount of minutes you want to spend on the specific Habit.")

    def get_habit_status(self):
        current_time = datetime.datetime.now()
        while True:
            habit_status = str.lower(get_input("Did you already accomplish the habit so far? Type in 'Yes', 'Y' or 'No', 'N'"))
            if habit_status in ['yes', 'y', 'no', 'n']:
                if habit_status == "yes" or habit_status == "y":
                    self.streak = 0
                    self.checked_status = 2
                    self.streak = self.streak + 1
                    self.checked_timestamp = current_time
                    break
                elif habit_status == "no" or habit_status == "n":
                    self.checked_status = 1
                    self.streak = 0
                    break
            else:
                typer.echo(f"Invalid input. Please enter 'Yes', 'Y' or 'No', 'N'.")

    def get_times(self):
        current_time = datetime.datetime.now()
        if self.frequency == "d" or self.frequency == "daily":
            self.check_date = current_time.isoweekday()
        elif self.frequency == "w" or self.frequency == "weekly":
            self.check_date = current_time.isocalendar().week
        elif self.frequency == "m" or self.frequency == "monthly":
            self.check_date = (current_time.year + current_time.month)

    def get_habit_checked_timestamp(self):
        current_time = datetime.datetime.now()
        self.checked_timestamp = current_time
        return self.checked_timestamp

    def get_habit_reason_for_failure(self):
        habit_reason_failure = str.lower(get_input("Please explain in a short sentence why you couldn't stick to your scheduled check off."))
        self.reason_failure = habit_reason_failure
        return habit_reason_failure

    def get_habit_failure_avoidance_strategy(self):
        habit_avoidance_strategy = str.lower(get_input("Try to wrap your mind about "))
        self.avoidance_strategy = habit_avoidance_strategy
        return habit_avoidance_strategy

    def __repr__(self):
        return f"Your Habit: {self.name}, Frequency: {self.frequency}, Duration: {self.duration}, Status: {self.checked_status}"







