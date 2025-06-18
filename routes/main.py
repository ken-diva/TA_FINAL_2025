from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash
from flask_login import login_required, current_user
from utils.database import (
    get_all_buildings,
    get_sports_rooms_by_building,
    get_building_by_id,
    get_sports_room_by_id,
)

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """3D Campus Map homepage - accessible to all users"""
    return render_template("index.html")


@main_bp.route("/dashboard")
@login_required
def dashboard():
    """User dashboard"""
    buildings = get_all_buildings()
    return render_template("dashboard.html", buildings=buildings)


@main_bp.route("/building/<int:building_id>")
@login_required
def view_building(building_id):
    """View building with 3D map"""
    building = get_building_by_id(building_id)
    if not building:
        flash("Building not found.", "error")
        return redirect(url_for("main.index"))

    sports_rooms = get_sports_rooms_by_building(building_id)
    return render_template(
        "building.html", building=building, sports_rooms=sports_rooms
    )


@main_bp.route("/api/building/<building_name>")
def api_building_info(building_name):
    """API endpoint to get building information by name"""
    # Map building names to database records
    building_mapping = {
        "Sport Center": "SCA",
        "Track Running": "FCB",
        "Lapangan Basket Outdoor 1": "SCA",
        "Lapangan Basket Outdoor 2": "SCA",
    }

    # Check if it's a sports building we have in database
    building_code = building_mapping.get(building_name)
    if building_code:
        # Get building from database
        buildings = get_all_buildings()
        building = next((b for b in buildings if b["code"] == building_code), None)

        if building:
            # Get sports rooms for this building
            sports_rooms = get_sports_rooms_by_building(building["id"])

            # Get bookings for sports rooms
            from utils.database import execute_query

            bookings = []
            if sports_rooms:
                room_ids = [room["id"] for room in sports_rooms]
                if room_ids:
                    placeholders = ",".join(["%s"] * len(room_ids))
                    query = f"""
                        SELECT br.*, sr.name as room_name 
                        FROM booking_room br 
                        JOIN sports_room sr ON br.id_sports_room = sr.id 
                        WHERE br.id_sports_room IN ({placeholders}) 
                        AND br.status = 'Approve'
                        AND br.end_time > NOW()
                        ORDER BY br.start_time
                    """
                    bookings = execute_query(query, room_ids, fetch=True) or []

            return jsonify(
                {
                    "name": building["name"],
                    "code": building["code"],
                    "capacity": sports_rooms[0]["capacity"] if sports_rooms else None,
                    "facilities": sports_rooms[0]["facility"] if sports_rooms else None,
                    "image_url": building["image_url"],
                    "bookings": bookings,
                }
            )

    # Return generic info for non-sports buildings
    return jsonify(
        {
            "error": "Building not found in database",
            "name": building_name,
            "code": building_name,
            "capacity": None,
            "facilities": None,
            "image_url": None,
        }
    )


@main_bp.route("/api/building/<int:building_id>/rooms")
@login_required
def api_building_rooms(building_id):
    """API endpoint to get rooms for a building (for 3D map integration)"""
    sports_rooms = get_sports_rooms_by_building(building_id)
    return jsonify({"success": True, "rooms": sports_rooms})
