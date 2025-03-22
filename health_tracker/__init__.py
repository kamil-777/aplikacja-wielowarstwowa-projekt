from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object("health_tracker.config.Config")

    db.init_app(app)

    from health_tracker.routes import main
    app.register_blueprint(main)

    return app
