# **DailyCommitForge 🔨
Daily Commit Forge is a web application designed to help users custom-build and maintain positive habits. It provides a clean and straightforward interface that allows users to define the habits they want to track. Users can then log their daily progress, and the application will visualise their consistency, focusing on streaks (How many days a habit is completed) to provide motivation. It creates a vibe of motivation, seriousness, action-oriented, and dynamic. It emphasises the accountability and the required daily action to maintain the progress. 

DailyCommitForge is a minimalist habit-tracking web application designed to help users build discipline through daily streaks. It features a secure authentication system and an automated offline reminder engine to ensure you never miss a commitment.

# **The Inspiration:**

The Inspiration Daily Commit Forge was born at the intersection of a **University Computing Technology Module** and a deep dive into **"Millionaire Mindset"** productivity podcasts watched on YouTube. I realised that the hardest part of adopting high-performance routines like **MOVERS** isn't the action itself—it's the consistency. I built this forge to serve as the digital accountability partner for anyone looking to master their morning routine.

# **Project Philosophy: The MOVERS Framework**

I developed this application after studying the psychological habits of high performers. The app is specifically designed to facilitate the **MOVERS** morning routine, a framework used by many to optimise mental and physical clarity:

**Meditation:** Quiet the mind to begin with a focused start.

**Oxygenation:** Deep breathing or hydration to revitalise the system.

**Visualisation:** Mentally rehearsing your goals for the day.

**Exercise:** Moving the body to spark energy.

**Reading:** Consuming positive or educational content.

**Scribbling:** Journaling or "brain dumping" to clear mental clutter.


## 🚀 Features
- **User Authentication**: Secure registration and login using Werkzeug password hashing.
- **Dynamic Habit Tracking**: Create, complete, and track streaks for custom habits.
- **Visual Progress**: Bootstrap-powered UI with colour-coded badges based on current streaks.
- **Offline Reminders**: A background Python script that sends email notifications if habits remain uncompleted.

## 🛠️ Tech Stack
- **Backend**: Python, Flask
- **Database**: SQLite3
- **Frontend**: Jinja2, Bootstrap 5
- **Automation**: SMTP with App Passwords and local Task Schedulers (Cron/Windows Task Scheduler)

## 🛡️ Security & Environment
This project uses environment variables to protect sensitive credentials. **Never commit your `.env` file.**

## **How to Get Started**
Clone & Install:
```
Bash

git clone <>
pip install -r requirements.txt
Environment Configuration:
Create a .env file in the root directory.
```

## Add your MAIL_USERNAME and MAIL_PASSWORD (Gmail App Password).

MAIL_USERNAME=your-email@gmail.com

MAIL_PASSWORD=your-16-digit-app-password

## **Database Setup:**

The schema is automatically handled by SQLite3. Ensure the habits.db file is present in the root directory.

## **Run the App:**
```
Bash

flask run
Navigate to http://127.0.0.1:5000 in your browser.
```

## 🧭 **Navigation Guide**

**Registration:** Create an account with a valid email to receive streak reminders.

**Dashboard:** Use the **"Add Habit"** card at the top to set your goals.

**Habit Cards:** Click **"Mark Complete"** daily to grow your streak. Cards change colour (Red → Yellow → Green) as your streak increases.

**Reminders:** To test the offline system, run python remind.py while you have uncompleted habits.

## **Navigating the App (MOVERS Example)**

**Morning Setup:** Create six habits in the dashboard named after the MOVERS pillars.

**The Feedback Loop:** As you finish your Meditation and Scribbling, mark them as "Complete" to see your streak badge turn green.

**The Safety Net:** If you get busy and forget to "Oxygenate" or "Exercise," the Remind.py engine will nudge you in the evening to help you avoid breaking your streak.
  
