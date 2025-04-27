# tests/conftest.py

import pytest
from health_tracker import create_app
from health_tracker.extensions import db as _db

@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.from_object('health_tracker.test_config.TestConfig')  # <- tutaj wczytujesz test config

    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()

@pytest.fixture(scope="function")
def db(app):
    yield _db
    _db.session.remove()
    _db.drop_all()
    _db.create_all()

@pytest.fixture()
def client(app):
    return app.test_client()