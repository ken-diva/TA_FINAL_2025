#!/usr/bin/env python3
"""
Script to reset user passwords in the database
Run this after setting up your database to ensure passwords work
"""

import mysql.connector
from utils.database import hash_password
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
db_config = {
    "host": os.environ.get("MYSQL_HOST", "localhost"),
    "user": os.environ.get("MYSQL_USER", "root"),
    "password": os.environ.get("MYSQL_PASSWORD", ""),
    "database": os.environ.get("MYSQL_DB", "sport_room_booking"),
    "port": int(os.environ.get("MYSQL_PORT", 3306)),
}


def reset_user_passwords():
    """Reset all user passwords to 'password'"""
    try:
        # Connect to database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Hash the password "password"
        hashed_password = hash_password("password")
        print(f"Generated hash: {hashed_password}")

        # Update all users with the new password hash
        query = "UPDATE users SET password = %s"
        cursor.execute(query, (hashed_password,))

        # Commit changes
        conn.commit()

        print(f"Updated {cursor.rowcount} user passwords")
        print("All users now have password: 'password'")

        # Show all users
        cursor.execute("SELECT id, username, email, role FROM users")
        users = cursor.fetchall()

        print("\nAvailable users:")
        for user in users:
            print(f"- {user[1]} ({user[3]}) - {user[2]}")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error: {e}")
        print(
            "Make sure your database is running and .env file is configured correctly"
        )


if __name__ == "__main__":
    reset_user_passwords()
