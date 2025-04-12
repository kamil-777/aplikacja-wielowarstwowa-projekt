from flask import Flask
from health_tracker.extensions import db
from health_tracker.routes import main

def create_app():
    app = Flask(__name__)
    app.config.from_object("health_tracker.config.Config")

    db.init_app(app)

    app.register_blueprint(main)

    return app
 