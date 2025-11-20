import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, g
from datetime import date, timedelta

app = Flask(__name__)
# Define the path to the database file (habits.db)
app.config['DATABASE'] = os.path.join(app.root_path, 'habits.db') 
app.secret_key = 'super_secret_key' # Needed for flash messages (optional)

def get_db():
    # Opens a new database connection 
    if 'db' not in g:
        g.db = sqlite3.connect(
            app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # Set row factory to sqlite3.Row to access columns by name 
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    # Closes the database again at the end of the request.
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    # Initializes the database using the schema.sql file.
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    # Flask command to initialize the database: flask --app app initdb
    init_db()
    print('Initialized the database.')

def calculate_streak(completion_dates, today): 
    # completion_dates must be a list of date objects, not strings/rows
    
    # If no dates, streaks are 0.
    if not completion_dates:
        return 0, 0, False, False

    dates = sorted(completion_dates)
    
    # Check for completion today 
    is_completed_today = (today in dates)

    current_streak = 0
    date_to_check = today
    
    # If completed today, start the streak count at 1 and check backward from yesterday.
    if is_completed_today:
        current_streak = 1
        date_to_check = today - timedelta(days=1)
    
    # If not completed today, but was completed yesterday, the streak is 1 
    # and we check backward from the day before yesterday.
    elif today - timedelta(days=1) in dates:
        current_streak = 1
        date_to_check = today - timedelta(days=2) 
    
    else:
        # If neither today nor yesterday was completed, the current streak is 0.
        pass
        
    # Iteratively count backwards 
    while date_to_check in dates:
        current_streak += 1
        date_to_check -= timedelta(days=1)
        
    longest_streak = 0
    temp_streak = 0
    last_date = None
    
    # This loop finds the longest run of consecutive dates
    for d in dates:
        if last_date is None or d == last_date + timedelta(days=1):
            temp_streak += 1
        else:
            longest_streak = max(longest_streak, temp_streak)
            temp_streak = 1
        last_date = d

    longest_streak = max(longest_streak, temp_streak)
    
    is_due_today = not is_completed_today

    return current_streak, longest_streak, is_completed_today, is_due_today

@app.route('/')
def index():
    db = get_db()
    today = date.today()
    habits_data = []

    try:
        # Get all habits
        habits_rows = db.execute(
            "SELECT * FROM habits ORDER BY created_at DESC"
        ).fetchall()
        
        # Process each habit to calculate its streaks
        for habit in habits_rows:
            # Get all completion dates for this habit
            completions_rows = db.execute(
                "SELECT completion_date FROM completions WHERE habit_id = ? ORDER BY completion_date", 
                (habit['id'],)
            ).fetchall()
            
            # It parsing the date string into a date object
            # because we set 'detect_types'. We just need to extract the date objects.
            completion_dates = [c['completion_date'] for c in completions_rows]

            # Calculate the streaks
            current_streak, longest_streak, is_completed, is_due = calculate_streak(completion_dates, today)

            # Store the final habit data
            habits_data.append({
                'id': habit['id'],
                'name': habit['name'],
                'description': habit['description'],
                'created_at': habit['created_at'],
                'current_streak': current_streak,
                'longest_streak': longest_streak,
                'completed_today': is_completed, 
                'is_due': is_due,
            })
            
    except sqlite3.Error as e:
        print(f"Database Error during index route: {e}")
        # Return an empty list to prevent a server crash
        habits_data = [] 

    # Return the template with the processed data
    return render_template("index.html", habits=habits_data)


@app.route('/add', methods=['POST'])
def add_habit():
    name = request.form.get('name')
    description = request.form.get('description')
    
    if not name:
        return redirect(url_for('index'))

    db = get_db()
    try:
        db.execute(
            "INSERT INTO habits (name, description) VALUES (?, ?)",
            (name, description)
        )
        db.commit()
    except sqlite3.Error as e:
        print(f"Error adding habit: {e}")
        # Return a redirect even if an error occurs.
        return redirect(url_for('index'))
        
    return redirect(url_for('index'))


@app.route('/complete/<int:habit_id>', methods=['POST'])
def complete_habit(habit_id):
    db = get_db()
    today_str = date.today().isoformat()
    
    try:
        # Insert the completion log for today.
        db.execute(
            "INSERT INTO completions (habit_id, completion_date) VALUES (?, ?)",
            (habit_id, today_str)
        )
        db.commit()
    except sqlite3.IntegrityError:
        # Handles the case where the habit was already completed today (UNIQUE constraint).
        pass
    except sqlite3.Error as e:
        print(f"Error completing habit: {e}")

    # Redirect back to the index page to refresh the view, after processing. 
    return redirect(url_for('index'))


@app.route('/delete/<int:habit_id>', methods=['POST'])
def delete_habit(habit_id):
    db = get_db()
    try:
        # The ON DELETE CASCADE ensures related completion records are also deleted.
        db.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
        db.commit()
    except sqlite3.Error as e:
        print(f"Error deleting habit: {e}")

    return redirect(url_for('index'))
