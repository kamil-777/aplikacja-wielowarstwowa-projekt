from flask import Blueprint, render_template, request, redirect, url_for
from health_tracker.models import db, HealthEntry, User
from health_tracker.extensions import db

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return "<h1>Strona główna Health Tracker</h1>"

@main.route("/add", methods=["GET", "POST"])

def add_entry():
    if request.method == "POST":
        steps = request.form["steps"]
        sleep_hours = request.form["sleep_hours"]
        calories = request.form["calories"]
        weight = request.form["weight"]

        # Tymczasowo bierzemy użytkownika o ID 1
        user = User.query.get(1)

        if not user:
            user = User(username="default_user")
            db.session.add(user)
            db.session.commit()

        entry = HealthEntry(
            steps=int(steps),
            sleep_hours=float(sleep_hours),
            calories=int(calories),
            weight=float(weight),
            user_id=user.id
        )

        db.session.add(entry)
        db.session.commit()
        return redirect(url_for("main.index"))

    return render_template("add_entry.html")
