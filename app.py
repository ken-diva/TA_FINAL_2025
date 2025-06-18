from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from mysql.connector import Error
from functools import wraps
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")


# Database connection function
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", ""),
            database=os.getenv("MYSQL_DB", "sport_room_booking"),
            port=int(os.getenv("MYSQL_PORT", 3306)),
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login first.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login first.", "warning")
            return redirect(url_for("login"))
        if session.get("role") != "admin":
            flash("Admin access required.", "danger")
            return redirect(url_for("index"))
        return f(*args, **kwargs)

    return decorated_function


# Homepage route
@app.route("/")
def index():
    return render_template("index.html")


# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Please enter both username and password.", "danger")
            return render_template("login.html")

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            try:
                # Query user from database
                query = "SELECT id, username, email, role FROM users WHERE username = %s AND password = %s"
                cursor.execute(query, (username, password))
                user = cursor.fetchone()

                if user:
                    # Store user info in session
                    session["user_id"] = user["id"]
                    session["username"] = user["username"]
                    session["email"] = user["email"]
                    session["role"] = user["role"]

                    flash(f'Welcome back, {user["username"]}!', "success")
                    return redirect(url_for("index"))
                else:
                    flash("Invalid username or password.", "danger")
            except Error as e:
                flash(f"Database error: {e}", "danger")
            finally:
                cursor.close()
                conn.close()
        else:
            flash("Database connection failed.", "danger")

    return render_template("login.html")


# Register route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        email = request.form.get("email")

        # Validation
        if not all([username, password, confirm_password, email]):
            flash("All fields are required.", "danger")
            return render_template("register.html")

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("register.html")

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "danger")
            return render_template("register.html")

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                # Check if username or email already exists
                check_query = "SELECT id FROM users WHERE username = %s OR email = %s"
                cursor.execute(check_query, (username, email))
                existing_user = cursor.fetchone()

                if existing_user:
                    flash("Username or email already exists.", "danger")
                else:
                    # Insert new user
                    insert_query = """
                        INSERT INTO users (username, password, email, role) 
                        VALUES (%s, %s, %s, 'user')
                    """
                    cursor.execute(insert_query, (username, password, email))
                    conn.commit()

                    flash("Registration successful! Please login.", "success")
                    return redirect(url_for("login"))
            except Error as e:
                flash(f"Database error: {e}", "danger")
            finally:
                cursor.close()
                conn.close()
        else:
            flash("Database connection failed.", "danger")

    return render_template("register.html")


# Logout route
@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))


# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=True)
