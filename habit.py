import sqlite3
from datetime import datetime

# 1. Connect once at the start
db = sqlite3.connect("Habit.db")
cr = db.cursor()

# Create tables
cr.execute("CREATE TABLE IF NOT EXISTS habit (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, goal INTEGER)")
cr.execute("""CREATE TABLE IF NOT EXISTS logs (
              log_id INTEGER PRIMARY KEY AUTOINCREMENT, 
              habit_id INTEGER,  
              date TEXT, 
              completed_status TEXT, 
              FOREIGN KEY (habit_id) REFERENCES habit(id))""")


def add_habit():
    habit_name = input("Write a habit: ").strip().title()
    habit_goal = int(input("Enter your weekly goal (days): "))
    # Use ? placeholders for security
    cr.execute("INSERT INTO habit VALUES (NULL, ?, ?)",
               (habit_name, habit_goal))
    db.commit()
    print("Habit added successfully!")


def log_track():
    habit_id = int(input("Enter habit ID: "))
    # Changed format to match the parser later
    habit_date = input("Enter date (YYYY-MM-DD): ").strip()
    habit_status = input("Completed? (yes/no): ").strip().lower()
    cr.execute("INSERT INTO logs VALUES (NULL, ?, ?, ?)",
               (habit_id, habit_date, habit_status))
    db.commit()
    print("Log saved!")


def show_all_habits():
    cr.execute("SELECT * FROM habit")
    habit_list = cr.fetchall()

    if not habit_list:
        print("No habits found.")
        return

    print("\n--- Your Habits ---")
    for hab in habit_list:
        print(f"ID: {hab[0]} | {hab[1]} (Goal: {hab[2]} days)")

    habit_id = int(input("\nEnter habit ID to see streak: "))
    cr.execute(
        "SELECT date FROM logs WHERE habit_id = ? AND completed_status = 'yes' ORDER BY date DESC", (habit_id,))

    date_db = cr.fetchall()
    if not date_db:
        print("No 'yes' logs found for this habit.")
        return

    date_strings = [row[0] for row in date_db]
    dates = [datetime.strptime(d, "%Y-%m-%d").date() for d in date_strings]

    streak_count = 1
    if len(dates) > 1:
        for i in range(len(dates) - 1):
            gap = dates[i] - dates[i+1]
            if gap.days == 1:
                streak_count += 1
            else:
                break

    print(f"🔥 Current Streak: {streak_count} days!")


# 2. Main Loop
while True:
    message = "\n'a': Add | 'l': Log | 's': Show | 'e': Exit\nChoose: "
    user_input = input(message).strip().lower()

    if user_input == 'a':
        add_habit()
    elif user_input == 'l':
        log_track()
    elif user_input == 's':
        show_all_habits()
    elif user_input == 'e':
        print("Goodbye!")
        break
    else:
        print("Invalid choice.")

# 3. Close once at the very end
db.close()
