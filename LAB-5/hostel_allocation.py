"""Hostel room allocation system.

Reads a YAML room configuration, allocates beds by block and gender,
vacates rooms, calculates fees, orders students by seniority, runs a
room lottery, counts vacant beds and exposes a small Flask page for
looking up a student's room.
"""
import os
import random

import yaml
from flask import Flask, request
from markupsafe import escape

# Global hostel state
rooms = {}
allocations = {}
waitlist = []
app = Flask(__name__)

CONFIG = """
blocks:
  A: {gender: M, rooms: 3, capacity: 2, fee: 4000}
  B: {gender: F, rooms: 2, capacity: 3, fee: 3500}
"""

DAYS_PER_MONTH = 30


def load_config(text=CONFIG):
    """Parse the YAML config and create the rooms for every block."""
    config = yaml.safe_load(text)
    for block, info in config["blocks"].items():
        for n in range(1, info["rooms"] + 1):
            rooms[block + str(n)] = {
                "gender": info["gender"],
                "capacity": info["capacity"],
                "fee": info["fee"],
                "occupants": [],
            }
    return config


def allocate_room(student_id, name, gender, year, preferred=None):
    """Allocate a bed to a student and return the room number.

    Preferred rooms are tried first. A room is only used if it belongs
    to a block for the student's gender and still has a free bed.
    Returns the existing room if the student is already allocated, and
    None if the year is invalid or no bed is free (the student is then
    put on the waitlist).
    """
    if not isinstance(year, int) or isinstance(year, bool):
        return None
    if student_id in allocations:
        return allocations[student_id]["room"]
    for room_no in (preferred or []) + list(rooms):
        room = rooms.get(room_no)
        if room is None or room["gender"] != gender:
            continue
        if len(room["occupants"]) >= room["capacity"]:
            continue
        room["occupants"].append(student_id)
        allocations[student_id] = {"name": name, "room": room_no,
                                   "year": year}
        return room_no
    if student_id not in waitlist:
        waitlist.append(student_id)
    return None


def vacate_room(student_id):
    """Remove a student from their room and from the allocations."""
    allocation = allocations.pop(student_id, None)
    if allocation is not None:
        rooms[allocation["room"]]["occupants"].remove(student_id)


def monthly_fee(student_id, days_stayed):
    """Return the fee owed; a partial month is billed as a full month."""
    if student_id not in allocations:
        raise ValueError(f"{student_id} has no room allocated")
    room = rooms[allocations[student_id]["room"]]
    months = -(-days_stayed // DAYS_PER_MONTH)
    return months * room["fee"]


def priority_order(students):
    """Order students by seniority, highest year first."""
    return sorted(students, key=lambda s: s["year"], reverse=True)


def room_lottery(student_ids):
    """Return the student ids in a random order."""
    return random.SystemRandom().sample(student_ids, len(student_ids))


def vacant_beds():
    """Count the free beds across all rooms."""
    return sum(room["capacity"] - len(room["occupants"])
               for room in rooms.values())


def connect_warden_db():
    """Connect to the warden database using env-provided credentials."""
    return db_connect(
        host="localhost",
        user="warden",
        password=os.environ.get("WARDEN_DB_PASSWORD", ""),
    )


def db_connect(host, user, password):
    """Return a stub connection description."""
    return {"host": host, "user": user, "connected": len(password) > 0}


@app.route("/room")
def room_lookup():
    """Show the room allocated to the student given by ?id=."""
    sid = request.args.get("id", "")
    return "<h1>Room for " + str(escape(sid)) + ": " + \
        str(escape(allocations.get(sid))) + "</h1>"


def run_portal():
    """Run the lookup portal locally with the debugger disabled."""
    app.run(host="127.0.0.1", debug=False)


def main():
    """Run a demonstration of the allocation system."""
    load_config()
    print("Rooms:", list(rooms.keys()))
    print("S1 ->", allocate_room("S1", "Arjun", "M", 1))
    print("S2 ->", allocate_room("S2", "Kabir", "M", 2))
    print("S3 ->", allocate_room("S3", "Rohan", "M", 3))
    print("S4 (female) ->", allocate_room("S4", "Diya", "F", 1))
    print("S1 again ->", allocate_room("S1", "Arjun", "M", 1))
    print("S5 year '2' ->", allocate_room("S5", "Vikram", "M", "2"))
    print("Occupants of A1:", rooms["A1"]["occupants"])
    vacate_room("S2")
    print("Occupants of A1 after S2 left:", rooms["A1"]["occupants"])
    print("Fee for S1, 45 days:", monthly_fee("S1", 45))
    students = [{"year": 1}, {"year": 4}, {"year": 2}]
    print("Priority (seniors first?):",
          [s["year"] for s in priority_order(students)])
    print("Lottery:", room_lottery(["S6", "S7", "S8"]))
    print("Vacant beds:", vacant_beds())
    print("Warden DB:", connect_warden_db())
    print("Waitlist:", waitlist)


if __name__ == "__main__":
    main()
