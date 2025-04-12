from health_tracker import create_app
from health_tracker import db

app = create_app()

# Tworzenie tabel w bazie danych
# with app.app_context():
#     db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
