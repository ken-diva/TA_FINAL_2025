from flask import current_app
from flask_mysqldb import MySQL
from datetime import datetime

# import bcrypt  # Commented out for testing

mysql = MySQL()


def init_db(app):
    """Initialize database connection with Flask app"""
    mysql.init_app(app)


def get_db_connection():
    """Get database connection"""
    return mysql.connection


def execute_query(query, params=None, fetch=False):
    """Execute a database query"""
    try:
        cur = mysql.connection.cursor()
        cur.execute(query, params or ())

        if fetch:
            if fetch == "one":
                result = cur.fetchone()
            else:
                result = cur.fetchall()
            cur.close()
            return result
        else:
            mysql.connection.commit()
            cur.close()
            return True
    except Exception as e:
        current_app.logger.error(f"Database error: {str(e)}")
        return False


def hash_password(password):
    """For testing - just return the password as is (no hashing)"""
    return password


def check_password(password, stored_password):
    """For testing - simple string comparison"""
    return password == stored_password


# User queries
def get_user_by_username(username):
    """Get user by username"""
    query = "SELECT * FROM users WHERE username = %s"
    return execute_query(query, (username,), fetch="one")


def get_user_by_id(user_id):
    """Get user by ID"""
    query = "SELECT * FROM users WHERE id = %s"
    return execute_query(query, (user_id,), fetch="one")


def create_user(username, password, email, role="user"):
    """Create a new user"""
    # For testing - store password as plain text
    query = """
        INSERT INTO users (username, password, email, role) 
        VALUES (%s, %s, %s, %s)
    """
    return execute_query(query, (username, password, email, role))


# Building queries
def get_all_buildings():
    """Get all buildings"""
    query = "SELECT * FROM building ORDER BY name"
    return execute_query(query, fetch=True)


def get_building_by_id(building_id):
    """Get building by ID"""
    query = "SELECT * FROM building WHERE id = %s"
    return execute_query(query, (building_id,), fetch="one")


# Sports room queries
def get_sports_rooms_by_building(building_id):
    """Get all sports rooms in a building"""
    query = """
        SELECT sr.*, b.name as building_name 
        FROM sports_room sr 
        JOIN building b ON sr.id_building = b.id 
        WHERE sr.id_building = %s
        ORDER BY sr.name
    """
    return execute_query(query, (building_id,), fetch=True)


def get_sports_room_by_id(room_id):
    """Get sports room by ID"""
    query = """
        SELECT sr.*, b.name as building_name 
        FROM sports_room sr 
        JOIN building b ON sr.id_building = b.id 
        WHERE sr.id = %s
    """
    return execute_query(query, (room_id,), fetch="one")


def get_all_sports_rooms():
    """Get all sports rooms"""
    query = """
        SELECT sr.*, b.name as building_name 
        FROM sports_room sr 
        JOIN building b ON sr.id_building = b.id 
        ORDER BY b.name, sr.name
    """
    return execute_query(query, fetch=True)


# Booking queries
def create_booking(user_id, sports_room_id, start_time, end_time):
    """Create a new booking"""
    query = """
        INSERT INTO booking_room (id_user, id_sports_room, start_time, end_time, status) 
        VALUES (%s, %s, %s, %s, 'Pending')
    """
    return execute_query(query, (user_id, sports_room_id, start_time, end_time))


def get_user_bookings(user_id):
    """Get all bookings for a user"""
    query = """
        SELECT br.*, sr.name as room_name, b.name as building_name
        FROM booking_room br
        JOIN sports_room sr ON br.id_sports_room = sr.id
        JOIN building b ON sr.id_building = b.id
        WHERE br.id_user = %s
        ORDER BY br.start_time DESC
    """
    return execute_query(query, (user_id,), fetch=True)


def get_all_bookings():
    """Get all bookings (for admin)"""
    query = """
        SELECT br.*, u.username, sr.name as room_name, b.name as building_name
        FROM booking_room br
        JOIN users u ON br.id_user = u.id
        JOIN sports_room sr ON br.id_sports_room = sr.id
        JOIN building b ON sr.id_building = b.id
        ORDER BY br.created_at DESC
    """
    return execute_query(query, fetch=True)


def update_booking_status(booking_id, status):
    """Update booking status"""
    query = "UPDATE booking_room SET status = %s WHERE id = %s"
    return execute_query(query, (status, booking_id))


def check_room_availability(room_id, start_time, end_time, exclude_booking_id=None):
    """Check if a room is available for the given time period"""
    query = """
        SELECT COUNT(*) as count FROM booking_room 
        WHERE id_sports_room = %s 
        AND status IN ('Pending', 'Approve')
        AND (
            (start_time <= %s AND end_time > %s) OR
            (start_time < %s AND end_time >= %s) OR
            (start_time >= %s AND end_time <= %s)
        )
    """
    params = [room_id, start_time, start_time, end_time, end_time, start_time, end_time]

    if exclude_booking_id:
        query += " AND id != %s"
        params.append(exclude_booking_id)

    result = execute_query(query, params, fetch="one")
    return result["count"] == 0 if result else False
