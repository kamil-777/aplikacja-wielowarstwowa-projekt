from health_tracker import create_app
from health_tracker import db

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
