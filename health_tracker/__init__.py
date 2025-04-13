from flask import Flask
from health_tracker.extensions import db, login_manager
from health_tracker.routes import main
from health_tracker.models import User

def create_app():
    app = Flask(__name__)
    app.config.from_object("health_tracker.config.Config")

    db.init_app(app)
    login_manager.init_app(app)

    # Ładowanie użytkownika z bazy
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    login_manager.login_view = "main.login"  # gdzie przekierować niezalogowanych
    login_manager.login_message = "Zaloguj się, aby uzyskać dostęp"

    app.register_blueprint(main)

    return app