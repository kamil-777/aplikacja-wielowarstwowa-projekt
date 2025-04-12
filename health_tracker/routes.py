from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from health_tracker.models import db, HealthEntry, User, Goal
from health_tracker.extensions import db

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")


@main.route("/add", methods=["GET", "POST"])
@login_required
def add_entry():
    if request.method == "POST":
        steps = request.form["steps"]
        sleep_hours = request.form["sleep_hours"]
        calories = request.form["calories"]
        weight = request.form["weight"]

        entry = HealthEntry(
            steps=int(steps),
            sleep_hours=float(sleep_hours),
            calories=int(calories),
            weight=float(weight),
            user_id=current_user.id
        )

        db.session.add(entry)
        db.session.commit()
        return redirect(url_for("main.index"))

    return render_template("add_entry.html")

@main.route("/goals", methods=["GET", "POST"])
@login_required
def manage_goals():
    if request.method == "POST":
        goal_type = request.form["goal_type"]
        target_value = request.form["target_value"]

        new_goal = Goal(
            type=goal_type,
            target_value=float(target_value),
            user_id=current_user.id
        )

        db.session.add(new_goal)
        db.session.commit()
        return redirect(url_for("main.manage_goals"))

    goals = Goal.query.filter_by(user_id=current_user.id).all()
    return render_template("goals.html", goals=goals)

@main.route("/goals/delete/<int:goal_id>", methods=["POST"])
@login_required
def delete_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    if goal.user_id != current_user.id:
        flash("Nie masz dostępu do tego celu.")
        return redirect(url_for("main.manage_goals"))

    db.session.delete(goal)
    db.session.commit()
    return redirect(url_for("main.manage_goals"))

@main.route("/dashboard")
@login_required
def dashboard():
    entries = HealthEntry.query.filter_by(user_id=current_user.id).all()

    entry_ids = [entry.id for entry in entries]
    steps = [entry.steps for entry in entries]
    calories = [entry.calories for entry in entries]
    sleep = [entry.sleep_hours for entry in entries]
    weight = [entry.weight for entry in entries]

    return render_template(
        "dashboard.html",
        entry_ids=entry_ids,
        steps=steps,
        calories=calories,
        sleep=sleep,
        weight=weight
    )

@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        if User.query.filter_by(username=username).first():
            flash("Nazwa użytkownika jest już zajęta.")
            return redirect(url_for("main.register"))

        if User.query.filter_by(email=email).first():
            flash("Użytkownik z tym adresem e-mail już istnieje.")
            return redirect(url_for("main.register"))

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Rejestracja zakończona sukcesem! Zaloguj się.")
        return redirect(url_for("main.login"))

    return render_template("register.html")

@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Zalogowano pomyślnie!")
            return redirect(url_for("main.index"))
        else:
            flash("Nieprawidłowe dane logowania.")
            return redirect(url_for("main.login"))

    return render_template("login.html")

@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Wylogowano.")
    return redirect(url_for("main.login"))
