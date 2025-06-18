from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from utils.database import (
    get_sports_room_by_id,
    create_booking,
    get_user_bookings,
    check_room_availability,
    get_all_bookings,
    update_booking_status,
)

booking_bp = Blueprint("booking", __name__)


@booking_bp.route("/room/<int:room_id>")
@login_required
def book_room(room_id):
    """Show booking form for a specific room"""
    room = get_sports_room_by_id(room_id)
    if not room:
        flash("Room not found.", "error")
        return redirect(url_for("main.dashboard"))

    return render_template("booking/book_room.html", room=room)


@booking_bp.route("/room/<int:room_id>", methods=["POST"])
@login_required
def submit_booking(room_id):
    """Submit a booking request"""
    room = get_sports_room_by_id(room_id)
    if not room:
        flash("Room not found.", "error")
        return redirect(url_for("main.dashboard"))

    start_date = request.form.get("start_date")
    start_time = request.form.get("start_time")
    end_date = request.form.get("end_date")
    end_time = request.form.get("end_time")

    if not all([start_date, start_time, end_date, end_time]):
        flash("All fields are required.", "error")
        return render_template("booking/book_room.html", room=room)

    try:
        # Combine date and time
        start_datetime = datetime.strptime(
            f"{start_date} {start_time}", "%Y-%m-%d %H:%M"
        )
        end_datetime = datetime.strptime(f"{end_date} {end_time}", "%Y-%m-%d %H:%M")

        # Validation
        if start_datetime >= end_datetime:
            flash("End time must be after start time.", "error")
            return render_template("booking/book_room.html", room=room)

        if start_datetime < datetime.now():
            flash("Booking time cannot be in the past.", "error")
            return render_template("booking/book_room.html", room=room)

        # Check availability
        if not check_room_availability(room_id, start_datetime, end_datetime):
            flash("Room is not available for the selected time period.", "error")
            return render_template("booking/book_room.html", room=room)

        # Create booking
        if create_booking(current_user.id, room_id, start_datetime, end_datetime):
            flash(
                "Booking request submitted successfully! Waiting for approval.",
                "success",
            )
            return redirect(url_for("booking.my_bookings"))
        else:
            flash("Failed to submit booking request.", "error")

    except ValueError:
        flash("Invalid date or time format.", "error")

    return render_template("booking/book_room.html", room=room)


@booking_bp.route("/my-bookings")
@login_required
def my_bookings():
    """Show user's bookings"""
    bookings = get_user_bookings(current_user.id)
    return render_template("booking/my_bookings.html", bookings=bookings)


@booking_bp.route("/check-availability")
@login_required
def check_availability():
    """AJAX endpoint to check room availability"""
    room_id = request.args.get("room_id")
    start_datetime = request.args.get("start_datetime")
    end_datetime = request.args.get("end_datetime")

    if not all([room_id, start_datetime, end_datetime]):
        return jsonify({"available": False, "message": "Missing parameters"})

    try:
        start_dt = datetime.fromisoformat(start_datetime)
        end_dt = datetime.fromisoformat(end_datetime)

        available = check_room_availability(int(room_id), start_dt, end_dt)

        return jsonify(
            {
                "available": available,
                "message": (
                    "Available"
                    if available
                    else "Room is already booked for this time period"
                ),
            }
        )
    except (ValueError, TypeError):
        return jsonify({"available": False, "message": "Invalid date format"})
