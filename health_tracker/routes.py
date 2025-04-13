from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime

from health_tracker.models import db, HealthEntry, User, Goal, UserSettings, Notification
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

        # Sprawdzenie czy użytkownik osiągnął cel kroków
        goal = Goal.query.filter_by(user_id=current_user.id, type="steps").first()
        if goal and not goal.is_achieved and int(steps) >= goal.target_value:
            goal.is_achieved = True
            notification = Notification(
                user_id=current_user.id,
                message=f"🎉 Brawo! Osiągnąłeś cel: {goal.target_value} kroków."
            )
            db.session.add(notification)

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

@main.route("/notifications")
@login_required
def notifications():
    user_notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
    return render_template("notifications.html", notifications=user_notifications)

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

        settings = UserSettings(user_id=user.id)
        db.session.add(settings)

        welcome_note = Notification(
            user_id=user.id,
            message="👋 Witaj w Health Tracker! Zacznij śledzić swoje zdrowie już teraz!"
        )
        db.session.add(welcome_note)

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

@main.route("/settings", methods=["GET", "POST"])
@login_required
def user_settings():
    settings = UserSettings.query.filter_by(user_id=current_user.id).first()

    if not settings:
        # Utwórz domyślne ustawienia, jeśli nie istnieją
        settings = UserSettings(user_id=current_user.id)
        db.session.add(settings)
        db.session.commit()

    if request.method == "POST":
        settings.unit_system = request.form["unit_system"]
        settings.notifications_enabled = "notifications_enabled" in request.form
        db.session.commit()
        flash("Ustawienia zostały zapisane.")
        return redirect(url_for("main.user_settings"))

    return render_template("settings.html", settings=settings)


@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Wylogowano.")
    return redirect(url_for("main.login"))
