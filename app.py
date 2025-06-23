from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    jsonify,
)
import mysql.connector, os
from mysql.connector import Error
from functools import wraps
from datetime import datetime, timedelta
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

# Set upload directory and allowed extensions
UPLOAD_FOLDER = os.path.join("static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure upload folder exists
if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


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


@app.route("/api/sports_rooms/<building_code>")
def api_sports_rooms(building_code):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT sr.id, sr.name, sr.capacity, sr.image_url
                FROM sports_room sr
                JOIN building b ON sr.id_building = b.id
                WHERE b.code = %s
            """
            cursor.execute(query, (building_code,))
            rooms = cursor.fetchall()
            return jsonify(rooms)
        except Error as e:
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            conn.close()
    return jsonify({"error": "Database connection failed"}), 500


# @app.route("/book", methods=["POST"])
# @login_required
# def book_room():
#     if session.get("role") == "admin":
#         flash("Admins are not allowed to book rooms.", "danger")
#         return redirect(url_for("index"))

#     sports_room_id = request.form.get("sports_room_id")
#     start_time = request.form.get("start_time")
#     end_time = request.form.get("end_time")

#     if not all([sports_room_id, start_time, end_time]):
#         flash("All booking fields are required.", "danger")
#         return redirect(url_for("index"))

#     try:
#         start_dt = datetime.fromisoformat(start_time)
#         end_dt = datetime.fromisoformat(end_time)
#         if start_dt >= end_dt:
#             flash("Start time must be before end time.", "danger")
#             return redirect(url_for("index"))
#     except ValueError:
#         flash("Invalid datetime format.", "danger")
#         return redirect(url_for("index"))

#     conn = get_db_connection()
#     if conn:
#         cursor = conn.cursor()
#         try:
#             query = """
#                 INSERT INTO booking_room (id_user, id_sports_room, start_time, end_time)
#                 VALUES (%s, %s, %s, %s)
#             """
#             cursor.execute(
#                 query, (session["user_id"], sports_room_id, start_time, end_time)
#             )
#             conn.commit()
#             flash("Booking submitted and pending approval.", "success")
#         except Error as e:
#             flash(f"Error booking room: {e}", "danger")
#         finally:
#             cursor.close()
#             conn.close()
#     else:
#         flash("Database connection failed.", "danger")

#     return redirect(url_for("index"))


@app.route("/book", methods=["POST"])
@login_required
def book_room():
    if session.get("role") == "admin":
        flash("Admins are not allowed to book rooms.", "danger")
        return redirect(url_for("index"))

    sports_room_id = request.form.get("sports_room_id")
    booking_date = request.form.get("booking_date")  # e.g. "2025-06-23"
    start_time = request.form.get("start_time")  # e.g. "09:00"
    end_time = request.form.get("end_time")  # e.g. "11:00"

    if not all([sports_room_id, booking_date, start_time, end_time]):
        flash("Semua kolom peminjaman harus diisi.", "danger")
        return redirect(url_for("index"))

    try:
        start_dt = datetime.fromisoformat(f"{booking_date}T{start_time}")
        end_dt = datetime.fromisoformat(f"{booking_date}T{end_time}")

        if start_dt >= end_dt:
            flash("Jam mulai harus sebelum jam selesai.", "danger")
            return redirect(url_for("index"))
    except ValueError:
        flash("Format tanggal atau jam tidak valid.", "danger")
        return redirect(url_for("index"))

    conn = get_db_connection()
    if not conn:
        flash("Koneksi database gagal.", "danger")
        return redirect(url_for("index"))

    cursor = conn.cursor(dictionary=True)
    try:
        # Cek apakah ada konflik peminjaman (selain yang sudah Reject)
        cursor.execute(
            """
            SELECT * FROM booking_room
            WHERE id_sports_room = %s
              AND booking_date = %s
              AND status != 'Reject'
              AND (
                  (start_time < %s AND end_time > %s)  -- overlap
              )
        """,
            (sports_room_id, booking_date, end_time, start_time),
        )

        conflict = cursor.fetchone()
        if conflict:
            flash(
                "Ruangan sudah dipesan pada waktu tersebut. Silakan pilih jam lain.",
                "warning",
            )
            return redirect(url_for("index"))

        # Simpan peminjaman baru
        cursor.execute(
            """
            INSERT INTO booking_room (id_user, id_sports_room, booking_date, start_time, end_time)
            VALUES (%s, %s, %s, %s, %s)
        """,
            (session["user_id"], sports_room_id, booking_date, start_time, end_time),
        )
        conn.commit()
        flash("Peminjaman berhasil diajukan dan menunggu persetujuan.", "success")

    except Error as e:
        flash(f"Gagal menyimpan peminjaman: {e}", "danger")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("index"))


@app.route("/api/room_schedule/<int:room_id>")
def api_room_schedule(room_id):
    date_str = request.args.get("date")
    try:
        booking_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except Exception:
        return jsonify({"error": "Invalid date format"}), 400

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT start_time, end_time
                FROM booking_room
                WHERE id_sports_room = %s AND booking_date = %s AND status != 'Reject'
            """,
                (room_id, booking_date),
            )
            bookings = cursor.fetchall()

            # Konversi jika ada timedelta (defensif)
            for b in bookings:
                for k, v in b.items():
                    if isinstance(v, timedelta):
                        b[k] = str(v)

            return jsonify(bookings)
        except Error as e:
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            conn.close()

    return jsonify({"error": "Database error"}), 500


@app.route("/history")
@login_required
def history():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT b.name AS building_name, sr.name AS room_name,
                       br.start_time, br.end_time, br.status
                FROM booking_room br
                JOIN sports_room sr ON br.id_sports_room = sr.id
                JOIN building b ON sr.id_building = b.id
                WHERE br.id_user = %s
                ORDER BY br.start_time DESC
            """
            cursor.execute(query, (session["user_id"],))
            bookings = cursor.fetchall()
            return render_template("history.html", bookings=bookings)
        except Error as e:
            flash(f"Error retrieving booking history: {e}", "danger")
            return render_template("history.html", bookings=[])
        finally:
            cursor.close()
            conn.close()
    flash("Database connection failed.", "danger")
    return render_template("history.html", bookings=[])


@app.route("/admin/bookings")
@admin_required
def admin_bookings():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT br.id, u.username, u.email, b.name AS building_name,
                       sr.name AS room_name, br.start_time, br.end_time, br.status
                FROM booking_room br
                JOIN users u ON br.id_user = u.id
                JOIN sports_room sr ON br.id_sports_room = sr.id
                JOIN building b ON sr.id_building = b.id
                WHERE u.role != 'admin'
                ORDER BY br.created_at DESC
            """
            cursor.execute(query)
            bookings = cursor.fetchall()
            return render_template("admin_bookings.html", bookings=bookings)
        except Error as e:
            flash(f"Error loading bookings: {e}", "danger")
            return render_template("admin_bookings.html", bookings=[])
        finally:
            cursor.close()
            conn.close()
    flash("Database connection error.", "danger")
    return render_template("admin_bookings.html", bookings=[])


@app.route("/admin/booking/<int:booking_id>/<string:action>")
@admin_required
def update_booking_status(booking_id, action):
    if action not in ["approve", "reject"]:
        flash("Invalid action.", "danger")
        return redirect(url_for("admin_bookings"))

    status = "Approve" if action == "approve" else "Reject"

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE booking_room SET status = %s WHERE id = %s",
                (status, booking_id),
            )
            conn.commit()
            flash(f"Booking #{booking_id} has been {status.lower()}d.", "success")
        except Error as e:
            flash(f"Failed to update booking: {e}", "danger")
        finally:
            cursor.close()
            conn.close()
    else:
        flash("Database connection failed.", "danger")

    return redirect(url_for("admin_bookings"))


@app.route("/admin/history")
@admin_required
def admin_booking_history():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT br.id, u.username, u.email, b.name AS building_name,
                       sr.name AS room_name, br.start_time, br.end_time, br.status
                FROM booking_room br
                JOIN users u ON br.id_user = u.id
                JOIN sports_room sr ON br.id_sports_room = sr.id
                JOIN building b ON sr.id_building = b.id
                WHERE u.role != 'admin'
                ORDER BY br.start_time DESC
            """
            cursor.execute(query)
            history = cursor.fetchall()
            return render_template("admin_history.html", bookings=history)
        except Error as e:
            flash(f"Failed to load history: {e}", "danger")
            return render_template("admin_history.html", bookings=[])
        finally:
            cursor.close()
            conn.close()
    flash("Database error.", "danger")
    return render_template("admin_history.html", bookings=[])


@app.route("/admin/manage")
@admin_required
def admin_manage():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM building ORDER BY id")
            buildings = cursor.fetchall()

            cursor.execute(
                """
                SELECT sr.*, b.name AS building_name 
                FROM sports_room sr 
                JOIN building b ON sr.id_building = b.id
                ORDER BY sr.id
            """
            )
            rooms = cursor.fetchall()

            return render_template(
                "admin_manage.html", buildings=buildings, rooms=rooms
            )
        except Error as e:
            flash(f"Database error: {e}", "danger")
            return render_template("admin_manage.html", buildings=[], rooms=[])
        finally:
            cursor.close()
            conn.close()
    flash("Database connection error.", "danger")
    return render_template("admin_manage.html", buildings=[], rooms=[])


@app.route("/admin/building/<int:building_id>/edit", methods=["POST"])
@admin_required
def edit_building(building_id):
    name = request.form.get("name")
    description = request.form.get("description")
    file = request.files.get("image_file")

    # Basic validation
    if not name or not description:
        flash("Name and description are required.", "danger")
        return redirect(url_for("admin_manage"))

    conn = get_db_connection()
    if not conn:
        flash("Database connection error.", "danger")
        return redirect(url_for("admin_manage"))

    cursor = conn.cursor(dictionary=True)
    try:
        # Get current image URL
        cursor.execute("SELECT image_url FROM building WHERE id = %s", (building_id,))
        result = cursor.fetchone()
        old_image_url = result["image_url"] if result else None

        # Handle new file upload
        image_url = old_image_url
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)
            image_url = f"/{file_path.replace(os.sep, '/')}"

        # Update DB
        cursor.execute(
            """
            UPDATE building
            SET name = %s, description = %s, image_url = %s, updated_at = NOW()
            WHERE id = %s
        """,
            (name, description, image_url, building_id),
        )
        conn.commit()
        flash("Building updated successfully.", "success")
    except Error as e:
        flash(f"Update failed: {e}", "danger")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("admin_manage"))


@app.route("/admin/sports_room/<int:room_id>/edit", methods=["POST"])
@admin_required
def edit_sports_room(room_id):
    name = request.form.get("name")
    capacity = request.form.get("capacity")
    facility = request.form.get("facility")
    file = request.files.get("image_file")

    conn = get_db_connection()
    if not conn:
        flash("Database connection error.", "danger")
        return redirect(url_for("admin_manage"))

    cursor = conn.cursor(dictionary=True)
    try:
        # Ambil URL lama
        cursor.execute("SELECT image_url FROM sports_room WHERE id = %s", (room_id,))
        result = cursor.fetchone()
        old_image_url = result["image_url"] if result else None

        image_url = old_image_url
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)
            image_url = f"/{file_path.replace(os.sep, '/')}"

        cursor.execute(
            """
            UPDATE sports_room
            SET name = %s, capacity = %s, facility = %s, image_url = %s, updated_at = NOW()
            WHERE id = %s
        """,
            (name, capacity, facility, image_url, room_id),
        )
        conn.commit()
        flash("Sports room updated successfully.", "success")
    except Error as e:
        flash(f"Update failed: {e}", "danger")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("admin_manage"))


@app.route("/admin/sports_room/add", methods=["POST"])
@admin_required
def add_sports_room():
    name = request.form.get("name")
    id_building = request.form.get("id_building")
    capacity = request.form.get("capacity")
    facility = request.form.get("facility")
    file = request.files.get("image_file")

    image_url = ""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)
        image_url = f"/{file_path.replace(os.sep, '/')}"

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO sports_room (id_building, name, capacity, facility, image_url)
                VALUES (%s, %s, %s, %s, %s)
            """,
                (id_building, name, capacity, facility, image_url),
            )
            conn.commit()
            flash("Sports room added successfully.", "success")
        except Error as e:
            flash(f"Error: {e}", "danger")
        finally:
            cursor.close()
            conn.close()
    return redirect(url_for("admin_manage"))


@app.route("/admin/sports_room/<int:room_id>/delete", methods=["POST"])
@admin_required
def delete_sports_room(room_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM sports_room WHERE id = %s", (room_id,))
            conn.commit()
            flash("Sports room deleted.", "info")
        except Error as e:
            flash(f"Delete failed: {e}", "danger")
        finally:
            cursor.close()
            conn.close()
    return redirect(url_for("admin_manage"))


@app.route("/api/buildings")
def get_buildings():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT id, name, code, description, image_url FROM building"
            )
            buildings = cursor.fetchall()
            return jsonify(buildings)
        except Error as e:
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            conn.close()
    return jsonify({"error": "Database connection failed"}), 500


@app.route("/api/buildings_with_sports_flag")
def buildings_with_sports_flag():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT b.id, b.name, b.code, b.description, b.image_url,
                       EXISTS (
                           SELECT 1 FROM sports_room sr WHERE sr.id_building = b.id
                       ) AS has_sports_room
                FROM building b
                ORDER BY b.name
            """
            cursor.execute(query)
            buildings = cursor.fetchall()
            return jsonify(buildings)
        except Error as e:
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            conn.close()
    return jsonify({"error": "Database connection failed"}), 500


# @app.route("/api/bookings/active/<building_code>")
# def get_active_bookings(building_code):
#     now = datetime.now()
#     conn = get_db_connection()
#     if conn:
#         cursor = conn.cursor(dictionary=True)
#         try:
#             query = """
#                 SELECT sr.name AS room_name, br.start_time, br.end_time
#                 FROM booking_room br
#                 JOIN sports_room sr ON br.id_sports_room = sr.id
#                 JOIN building b ON sr.id_building = b.id
#                 WHERE b.code = %s AND br.status = 'Approve' AND br.end_time >= %s
#                 ORDER BY br.start_time ASC
#             """
#             cursor.execute(query, (building_code, now))
#             bookings = cursor.fetchall()
#             return jsonify(bookings)
#         except Error as e:
#             return jsonify({"error": str(e)}), 500
#         finally:
#             cursor.close()
#             conn.close()
#     return jsonify({"error": "DB connection failed"}), 500


@app.route("/api/bookings/active/<building_code>")
def get_active_bookings(building_code):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT u.username, br.booking_date, br.start_time, br.end_time
            FROM booking_room br
            JOIN users u ON br.id_user = u.id
            JOIN sports_room sr ON br.id_sports_room = sr.id
            JOIN building b ON sr.id_building = b.id
            WHERE b.code = %s
              AND br.status = 'Approve'
              AND br.booking_date >= CURDATE()
            ORDER BY br.booking_date, br.start_time
        """,
            (building_code,),
        )
        bookings = cursor.fetchall()

        # 🔧 Convert any timedelta to string just in case
        for b in bookings:
            for key, val in b.items():
                if isinstance(val, timedelta):
                    b[key] = str(val)

        return jsonify(bookings)
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route("/api/room_booked_dates/<int:room_id>")
def api_booked_dates(room_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT DISTINCT booking_date
                FROM booking_room
                WHERE id_sports_room = %s AND status = 'Approve'
            """,
                (room_id,),
            )
            dates = [row[0].isoformat() for row in cursor.fetchall()]
            return jsonify(dates)
        except Error as e:
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            conn.close()
    return jsonify({"error": "Database error"}), 500


# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=True)
