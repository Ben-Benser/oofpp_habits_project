# Object Oriented And Functional Programming With Python - Project:
## Habit Tracker 
An Application whose goal is to help the user acquire new habits. 

### How?
Successes are to be reinforced by means of positive reinforcement via the accumulation of a streak. 
Various functions are used to actively track the new habits, as well as specific, 
informative outputs about the user's own success and a few analysis outputs. 

## Database

### Overview
Data is created in a database using SQLite3. 
In order to use as little memory as possible and at the same time maintain simplicity, 
the data is overwritten per update - statement according to the actuality. 
Exceptions are losses of Streaks, which are not actively mapped but would be output 
via App-Command if desired. Relations between the tables are given by various FOREIGN KEY's.

The user creates various habits, specifying the frequency with which he wants to devote himself to them. 
If there is a failure to follow the set plan, the user is asked to explain how this failure occurred. 
Subsequently, the user must indicate his consideration or measure, 
which should contribute to avoid further fittings.

### Tables

#### Habits
The table within which all data about the respective habits are stored.
<table>
  <thead>
    <tr>
      <th>habits</th>
        <tr>
            <th>id</th>
            <th>name</th>
            <th>frequency</th>
            <th>duration</th>
            <th>checked_status</th>
            <th>streak</th>
            <th>reason_failure_id</th>
            <th>avoidance_strategy_id</th>
            <th>check_date</th>
            <th>checked_timestamp</th>
        </tr>
  </thead>
  <tbody>
    <tr>
      <td>INT</td>
      <td>TEXT</td>
      <td>TEXT</td>
      <td>INT</td>
      <td>INT</td>
      <td>INT</td>
      <td>INT</td>
      <td>INT</td>
      <td>INT</td>
      <td>DATETIME</td>
    </tr>
  </tbody>
</table>

The table within which the reason for each break of the streak is stored.
<table>
  <thead>
    <tr>
      <th>reason_for_failure</th>
        <tr>
            <th>id</th>
            <th>reason</th>
            <th>habit_id</th>
        </tr>
  </thead>
  <tbody>
    <tr>
      <td>INT</td>
      <td>TEXT</td>
      <td>INT</td>
    </tr>
  </tbody>
</table>

The table within which the strategy to avoid further streak breaks is stored. 
<table>
  <thead>
    <tr>
      <th>strategy_for_failure_elimination</th>
        <tr>
            <th>id</th>
            <th>strategy</th>
            <th>habit_id</th>
        </tr>
  </thead>
  <tbody>
    <tr>
      <td>INT</td>
      <td>TEXT</td>
      <td>INT</td>
    </tr>
  </tbody>
</table>

The table within which data for the respective break in the streak are stored
<table>
  <thead>
    <tr>
      <th>meta_information</th>
        <tr>
            <th>id</th>
            <th>frequency</th>
            <th>duration</th>
            <th>streak</th>
            <th>habit_id</th>
        </tr>
  </thead>
  <tbody>
    <tr>
      <td>INT</td>
      <td>TEXT</td>
      <td>INT</td>
      <td>INT</td>
      <td>INT</td>
    </tr>
  </tbody>
</table>

A linkage table between the reasons and the strategies
<table>
  <thead>
    <tr>
      <th>habit_reasons_strategies</th>
        <tr>
            <th>id</th>
            <th>habit_id</th>
            <th>reason_id</th>
            <th>strategy_id</th>
            <th>meta_information_id</th>
        </tr>
  </thead>
  <tbody>
    <tr>
      <td>INT</td>
      <td>INT</td>
      <td>INT</td>
      <td>INT</td>
      <td>INT</td>
    </tr>
  </tbody>
</table>

## Installation
```shell
pip install -r requirements.txt
```

## Usage
The CLI "Typer" serves as interface.  By means of simple app commands, the user can navigate through the app. 
Cosmetic adaptations of various outputs of the terminal were made with the library "rich". 

```shell
python main.py --help
```
Depending on whether you run the application via IDE or terminal, 
you open the IDE's terminal or use your computer's terminal and navigate to 
the application's directory. With the command "python main.py --help" you start 
the application and get an overview of all functions. Depending on which action 
is to be executed, further instructions are given to the user via the terminal.





## Tests
The pytest testing tool is used to test various functions within the app.
```shell
pytest .
```