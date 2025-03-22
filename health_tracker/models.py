from datetime import date
from health_tracker.extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)

    # Relation 1:N – one user can have more entries
    entries = db.relationship("HealthEntry", backref="user", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"

class HealthEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=date.today)
    steps = db.Column(db.Integer, nullable=False)
    sleep_hours = db.Column(db.Float, nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"<HealthEntry {self.date} | {self.steps} steps>"
