from flask import redirect, session
from functools import wraps

def login_required(f):
   
    # Decorated routes to require login.
    # It acts as a security guard for the routes. It checks if a user_id exists in the session; if not, it sends the person back to the login page.
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function