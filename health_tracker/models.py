from datetime import date
from health_tracker.extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):  # 👈 dziedziczymy po UserMixin
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)  # 👈 nowość
    password_hash = db.Column(db.String(256), nullable=False)       # 👈 nowość

    # Istniejące relacje
    goals = db.relationship('Goal', backref='user', lazy=True)
    entries = db.relationship('HealthEntry', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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
    
class Goal(db.Model):
    __tablename__ = 'goals'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)  # np. "steps", "calories", "sleep"
    target_value = db.Column(db.Float, nullable=False)
    current_value = db.Column(db.Float, default=0.0)
    is_achieved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Goal {self.type} ({self.target_value})>"    
