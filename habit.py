import sqlite3
from datetime import datetime, timedelta, date


# set app

db = sqlite3.connect("Habittrack.db")

cr = db.cursor()


cr.execute("create table if not exists habit (id integer primary key autoincrement,name text , goal integer)")
cr.execute(
    "create table if not exists logs (log_id integer primary key autoincrement, habit_id integer,  date text, completed_status text , foreign key (habit_id) references habit(id))")


def commit_close():

    db.commit()

    db.close()


message = """
what do you want to do ?
'a' : add new habit
'l' : log
's' : show habits list
choose :
"""

user_input = input(message).strip().lower()


def add_habit():
    habit_name = input("Write a habit").strip().title()
    habit_goal = int(input("Enter your habit goal"))
    cr.execute(
        f"insert into habit  values (NULL,'{habit_name}','{habit_goal}')")
    commit_close()


def log_track():
    habit_id = int(input("Enter your habit ID"))
    habit_date = input(
        "Enter your habit full date .please follow this format (YYYY,MM,DD)").strip()

    habit_status = input(
        "Did you complete your habit? answer with : yes or no").strip().lower()
    cr.execute(
        f"insert into logs values (NULL,'{habit_id}','{habit_date}','{habit_status}')")

    commit_close()


def show_all_habits():

    cr.execute("select * from habit")


habit_list = cr.fetchall()

print(f"You have {len(habit_list)} habits :")

for hab in habit_list:

    print(f"{hab[0]}_ {hab[1]} => {hab[2]}%")


habit_id = int(input("Enter your habit ID"))

cr.execute(

    f"select date from logs where habit_id = ? order by date desc", (habit_id,))

date_db = cr.fetchall()

date_string = [row[0]for row in date_db]

dates = [datetime.strptime(d, "%Y-%m-%d").date() for d in date_string]

# Streak Calculation Logic

streak_count = 1

if len(dates) > 1:

    for i in range(len(dates) - 1):

        gap = dates[i]-dates[i+1]

        if gap.days == 1:

            streak_count += 1

        else:

            break


print(f"🔥 Current Streak for {habit_id}: {streak_count} days!")

commit_close()


command_list = ['a', 'l', 's']

if user_input in command_list:

    if user_input == 'a':

        add_habit()

    elif user_input == 'l':

        log_track()

    else:

        show_all_habits()

else:

    print("Invalid choice.")
