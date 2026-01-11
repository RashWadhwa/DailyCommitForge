import sqlite3
import os
from datetime import date
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

# Establishing Database Connection
def check_reminders():
    db_path = os.path.join(os.path.dirname(__file__), 'habits.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    db = conn.cursor()

    today = date.today().isoformat()

    # Find users who haven't completed a habit today
    # Look for habits where no completion exists for 'today'
    query = """
        SELECT users.username, users.email, habits.name 
        FROM habits 
        JOIN users ON habits.user_id = users.id 
        WHERE habits.id NOT IN (
            SELECT habit_id FROM completions WHERE completion_date = ?
        )
    """
    rows = db.execute(query, (today,)).fetchall()

    for row in rows:
        if row['email']:
            send_email_notification(row['email'], row['name'], row['username'])
    
    conn.close()

# Setting up the Notification Engine
def send_email_notification(recipient, habit_name, username):
    # Fetch secrets from environment
    sender_email = os.getenv("MAIL_USERNAME")
    app_password = os.getenv("MAIL_PASSWORD")

    msg = EmailMessage()
    msg.set_content(f"Hi {username}, don't break your streak! You haven't forged your '{habit_name}' today.")
    msg['Subject'] = 'DailyCommitForge Reminder'
    msg['From'] = sender_email # Use the variable
    msg['To'] = recipient
    
    # Connecting to a free mail server (Gmail SMTP)
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)
            print(f"Reminder sent to {username} for {habit_name}")
    except Exception as e:
        print(f"Failed to send to {username}: {e}")

if __name__ == "__main__":
    check_reminders()