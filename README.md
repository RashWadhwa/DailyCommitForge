# Project Overview (A Personal Habit Tracker) 
# DailyCommitForge 🔨
Daily Commit Forge is a web application designed to help users custom-build and maintain positive habits. It provides a clean and straightforward interface that allows users to define the habits they want to track. Users can then log their daily progress, and the application will visualise their consistency, focusing on streaks (How many days a habit is completed) to provide motivation. It creates a vibe of motivation, seriousness, action-oriented, and dynamic. It emphasises the accountability and the required daily action to maintain the progress. 

DailyCommitForge is a minimalist habit-tracking web application designed to help users build discipline through daily streaks. It features a secure authentication system and an automated offline reminder engine to ensure you never miss a commitment.

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

1. Clone the repository.
2. Create a `.env` file in the root directory:
   ```text
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-16-digit-app-password
