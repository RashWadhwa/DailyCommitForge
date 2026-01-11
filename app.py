import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, session, g
from flask_session import Session  
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date, timedelta
from helpers import login_required 

app = Flask(__name__)
# Using your specific database name
app.config['DATABASE'] = os.path.join(app.root_path, 'habits.db') 

# Configure session to use filesystem 
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def calculate_streak(completion_dates, today): 
    if not completion_dates:
        return 0, 0, False, False

    dates = sorted(completion_dates)
    is_completed_today = (today in dates)
    current_streak = 0
    date_to_check = today
    
    if is_completed_today:
        current_streak = 1
        date_to_check = today - timedelta(days=1)
    elif today - timedelta(days=1) in dates:
        current_streak = 1
        date_to_check = today - timedelta(days=2) 
    
    while date_to_check in dates:
        current_streak += 1
        date_to_check -= timedelta(days=1)
        
    longest_streak = 0
    temp_streak = 0
    last_date = None
    
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

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        if not username or not email or not password or password != confirmation:
            return "Must provide valid username, email, and matching passwords", 400

        hash = generate_password_hash(password) # Securely hash password
        db = get_db()
        try:
            db.execute("INSERT INTO users (username, hash, email) VALUES (?, ?, ?)", (username, hash, email))
            db.commit()
        except sqlite3.IntegrityError:
            return "Username already exists", 400

        return redirect("/login")
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),)).fetchone()

        if user is None or not check_password_hash(user["hash"], request.form.get("password")):
            return "Invalid username/password", 403

        session["user_id"] = user["id"] # Save user ID in session
        return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# --- Updated INDEX for (Multi-user) ---

@app.route('/')
@login_required # Protecting the dashboard
def index():
    db = get_db()
    today = date.today()
    habits_data = []

    try:
        # Fetch habits ONLY for the logged-in user
        habits_rows = db.execute(
            "SELECT * FROM habits WHERE user_id = ? ORDER BY created_at DESC", 
            (session["user_id"],)
        ).fetchall()
        
        for habit in habits_rows:
            completions_rows = db.execute(
                "SELECT completion_date FROM completions WHERE habit_id = ? ORDER BY completion_date", 
                (habit['id'],)
            ).fetchall()
            
            completion_dates = [c['completion_date'] for c in completions_rows]
            current_streak, longest_streak, is_completed, is_due = calculate_streak(completion_dates, today)

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
        print(f"DB Error: {e}")
        habits_data = [] 

    return render_template("index.html", habits=habits_data)

@app.route('/add', methods=['POST'])
@login_required
def add_habit():
    name = request.form.get('name')
    description = request.form.get('description')
    
    if name:
        db = get_db()
        # Associate the new habit with the current user
        db.execute("INSERT INTO habits (name, description, user_id) VALUES (?, ?, ?)", 
                   (name, description, session["user_id"]))
        db.commit()
    return redirect(url_for('index'))

@app.route('/complete/<int:habit_id>', methods=['POST'])
@login_required
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
@login_required
def delete_habit(habit_id):
    db = get_db()
    try:
        # The ON DELETE CASCADE ensures related completion records are also deleted.
        db.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
        db.commit()
    except sqlite3.Error as e:
        print(f"Error deleting habit: {e}")

    return redirect(url_for('index'))
