import sqlite3
import os
from datetime import date

# Define the path to the database file
DATABASE_PATH = 'habits.db'

def check_db_content():
    # Connects to habits.db and prints the contents of the habits and completions tables.
    if not os.path.exists(DATABASE_PATH):
        print(f"Error: Database file '{DATABASE_PATH}' not found.")
        print("Please ensure you have run 'flask --app app initdb' first.")
        return

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row  # Set row factory to access columns by name
        cursor = conn.cursor()

        # Check Habits Table 
        print("\n--- Habits in the Database ---")
        habits = cursor.execute(
            "SELECT id, name, description, created_at FROM habits ORDER BY id"
        ).fetchall()

        if habits:
            print(f"Found {len(habits)} habit(s):")
            for habit in habits:
                print(f"| ID: {habit['id']} | Name: {habit['name']} | Description: {habit['description'] or 'N/A'} | Created: {habit['created_at']}")
        else:
            print("No habits found in the 'habits' table.")

        # Check Completions Table
        print("\n--- Completions Log in the Database ---")
        completions = cursor.execute(
            "SELECT habit_id, completion_date FROM completions ORDER BY habit_id, completion_date"
        ).fetchall()
        
        if completions:
            print(f"Found {len(completions)} completion log entries:")
            for comp in completions:
                print(f"| Habit ID: {comp['habit_id']} | Date: {comp['completion_date']}")
        else:
            print("No completion entries found in the 'completions' table.")

    except sqlite3.Error as e:
        print(f"\n Failed to read database: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    check_db_content()
