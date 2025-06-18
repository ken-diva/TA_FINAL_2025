from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from functools import wraps
from utils.database import (
    get_all_bookings,
    update_booking_status,
    get_all_buildings,
    get_all_sports_rooms,
    get_building_by_id,
    get_sports_room_by_id,
)

admin_bp = Blueprint("admin", __name__)


def admin_required(f):
    """Decorator to require admin role"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash("You need admin privileges to access this page.", "error")
            return redirect(url_for("main.dashboard"))
        return f(*args, **kwargs)

    return decorated_function


@admin_bp.route("/dashboard")
@login_required
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    bookings = get_all_bookings()
    buildings = get_all_buildings()
    sports_rooms = get_all_sports_rooms()

    # Count statistics
    pending_bookings = len([b for b in bookings if b["status"] == "Pending"])
    total_buildings = len(buildings)
    total_rooms = len(sports_rooms)

    stats = {
        "pending_bookings": pending_bookings,
        "total_buildings": total_buildings,
        "total_rooms": total_rooms,
        "total_bookings": len(bookings),
    }

    return render_template(
        "admin/dashboard.html", stats=stats, recent_bookings=bookings[:10]
    )


@admin_bp.route("/bookings")
@login_required
@admin_required
def manage_bookings():
    """Manage all bookings"""
    status_filter = request.args.get("status", "all")
    bookings = get_all_bookings()

    if status_filter != "all":
        bookings = [b for b in bookings if b["status"].lower() == status_filter.lower()]

    return render_template(
        "admin/manage_bookings.html", bookings=bookings, status_filter=status_filter
    )


@admin_bp.route("/booking/<int:booking_id>/approve", methods=["POST"])
@login_required
@admin_required
def approve_booking(booking_id):
    """Approve a booking"""
    if update_booking_status(booking_id, "Approve"):
        flash("Booking approved successfully.", "success")
    else:
        flash("Failed to approve booking.", "error")

    return redirect(url_for("admin.manage_bookings"))


@admin_bp.route("/booking/<int:booking_id>/reject", methods=["POST"])
@login_required
@admin_required
def reject_booking(booking_id):
    """Reject a booking"""
    if update_booking_status(booking_id, "Reject"):
        flash("Booking rejected successfully.", "success")
    else:
        flash("Failed to reject booking.", "error")

    return redirect(url_for("admin.manage_bookings"))


@admin_bp.route("/buildings")
@login_required
@admin_required
def manage_buildings():
    """Manage buildings"""
    buildings = get_all_buildings()
    return render_template("admin/manage_buildings.html", buildings=buildings)


@admin_bp.route("/buildings/<int:building_id>")
@login_required
@admin_required
def view_building_details(building_id):
    """View building details and its rooms"""
    from utils.database import get_sports_rooms_by_building

    building = get_building_by_id(building_id)
    if not building:
        flash("Building not found.", "error")
        return redirect(url_for("admin.manage_buildings"))

    rooms = get_sports_rooms_by_building(building_id)
    return render_template(
        "admin/building_details.html", building=building, rooms=rooms
    )


@admin_bp.route("/rooms")
@login_required
@admin_required
def manage_rooms():
    """Manage sports rooms"""
    rooms = get_all_sports_rooms()
    return render_template("admin/manage_rooms.html", rooms=rooms)


@admin_bp.route("/api/booking/<int:booking_id>/status", methods=["POST"])
@login_required
@admin_required
def update_booking_status_api(booking_id):
    """API endpoint to update booking status"""
    data = request.get_json()
    new_status = data.get("status")

    if new_status not in ["Pending", "Approve", "Reject"]:
        return jsonify({"success": False, "message": "Invalid status"})

    if update_booking_status(booking_id, new_status):
        return jsonify(
            {"success": True, "message": f"Booking {new_status.lower()}d successfully"}
        )
    else:
        return jsonify({"success": False, "message": "Failed to update booking status"})
