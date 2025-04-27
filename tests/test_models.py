import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from health_tracker.models import User, Goal, HealthEntry, Notification, UserSettings

def test_create_user(db):
    user = User(username="janek", email="janek@example.com")
    user.set_password("sekret")
    db.session.add(user)
    db.session.commit()
    assert user.id is not None
    assert user.check_password("sekret")

def test_create_goal(db):
    user = User(username="celowy", email="celowy@example.com", password_hash="hash")
    db.session.add(user)
    db.session.commit()

    goal = Goal(type="steps", target_value=10000, user_id=user.id)
    db.session.add(goal)
    db.session.commit()

    assert goal in user.goals

def test_create_health_entry(db):
    user = User(username="zdrowy", email="zdrowy@example.com", password_hash="hash")
    db.session.add(user)
    db.session.commit()

    entry = HealthEntry(steps=8000, sleep_hours=7.5, calories=2500, weight=72.3, user_id=user.id)
    db.session.add(entry)
    db.session.commit()

    assert entry in user.entries

def test_create_notification(db):
    user = User(username="noty", email="noty@example.com", password_hash="hash")
    db.session.add(user)
    db.session.commit()

    note = Notification(user_id=user.id, message="Test message")
    db.session.add(note)
    db.session.commit()

    assert note in user.notifications

def test_user_settings(db):
    user = User(username="ustawiony", email="ustawiony@example.com", password_hash="hash")
    db.session.add(user)
    db.session.commit()

    settings = UserSettings(user_id=user.id, unit_system="imperial", notifications_enabled=False)
    db.session.add(settings)
    db.session.commit()

    assert user.settings.unit_system == "imperial"
    assert not user.settings.notifications_enabled
