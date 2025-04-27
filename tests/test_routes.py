# tests/test_routes.py

import pytest
from flask import url_for

def test_register_and_login(client, db):
    """
    Test rejestracji nowego użytkownika i późniejszego logowania
    """
    # Rejestracja
    response = client.post("/register", data={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert "Zaloguj się" in response.data.decode('utf-8')

    # Logowanie
    response = client.post("/login", data={
        "username": "testuser",
        "password": "password"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert "Health Tracker" in response.data.decode('utf-8')

def test_protected_pages_require_login(client):
    """
    Test sprawdza, że strony wymagające logowania przekierowują niezalogowanego użytkownika
    """
    # Dodaj logout na początku testu!
    client.get('/logout', follow_redirects=True)

    protected_urls = ['/add', '/dashboard', '/goals', '/notifications', '/settings']

    for url in protected_urls:
        response = client.get(url, follow_redirects=False)
        assert response.status_code == 302
        assert '/login' in response.headers['Location']


def test_logout_redirects_to_login(client, db):
    """
    Test sprawdza, że po wylogowaniu następuje przekierowanie do ekranu logowania
    """
    client.post("/register", data={
        "username": "logoutuser",
        "email": "logout@example.com",
        "password": "password"
    }, follow_redirects=True)

    client.post("/login", data={
        "username": "logoutuser",
        "password": "password"
    }, follow_redirects=True)

    response = client.get("/logout", follow_redirects=True)

    assert response.status_code == 200
    assert "Zaloguj się" in response.data.decode('utf-8')

def test_register_with_existing_username(client, db):
    """
    Test próby rejestracji użytkownika z istniejącą nazwą użytkownika
    """
    client.post("/register", data={
        "username": "duplicateuser",
        "email": "duplicate@example.com",
        "password": "password"
    }, follow_redirects=True)

    response = client.post("/register", data={
        "username": "duplicateuser",
        "email": "new@example.com",
        "password": "newpassword"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert "Nazwa użytkownika jest już zajęta." in response.data.decode('utf-8')


def test_add_health_entry(client, db):
    """
    Test dodawania wpisu zdrowotnego (HealthEntry) przez zalogowanego użytkownika
    """

    # Najpierw rejestrujemy i logujemy użytkownika
    client.post("/register", data={
        "username": "healthuser",
        "email": "health@example.com",
        "password": "password"
    }, follow_redirects=True)

    client.post("/login", data={
        "username": "healthuser",
        "password": "password"
    }, follow_redirects=True)

    # Dodajemy wpis zdrowotny
    response = client.post("/add", data={
        "steps": "8000",
        "sleep_hours": "7.5",
        "calories": "2500",
        "weight": "70.5"
    }, follow_redirects=True)

    # Sprawdzamy czy dodanie było poprawne
    assert response.status_code == 200
    assert "Health Tracker" in response.data.decode("utf-8")

    # Opcjonalnie możemy też sprawdzić, czy w bazie pojawił się wpis
    from health_tracker.models import HealthEntry
    entries = HealthEntry.query.all()
    assert len(entries) == 1
    assert entries[0].steps == 8000
    assert entries[0].sleep_hours == 7.5
    assert entries[0].calories == 2500
    assert entries[0].weight == 70.5


def test_goal_achievement_and_notification(client, db):
    """
    Test osiągnięcia celu: użytkownik dodaje wpis HealthEntry i otrzymuje nowe powiadomienie
    """

    # Rejestracja i logowanie użytkownika
    client.post("/register", data={
        "username": "goaluser",
        "email": "goal@example.com",
        "password": "password"
    }, follow_redirects=True)

    client.post("/login", data={
        "username": "goaluser",
        "password": "password"
    }, follow_redirects=True)

    from health_tracker.models import Goal, db as _db, User

    user = User.query.filter_by(username="goaluser").first()

    # Tworzenie celu
    new_goal = Goal(type="steps", target_value=5000, user_id=user.id)
    _db.session.add(new_goal)
    _db.session.commit()

    # Dodanie wpisu spełniającego cel
    response = client.post("/add", data={
        "steps": "6000",  # Więcej niż 5000
        "sleep_hours": "7.0",
        "calories": "2200",
        "weight": "72.0"
    }, follow_redirects=True)

    assert response.status_code == 200

    # Sprawdzamy czy cel został osiągnięty
    updated_goal = Goal.query.get(new_goal.id)
    assert updated_goal.is_achieved is True

    # Sprawdzamy czy mamy 2 powiadomienia: powitalne + za osiągnięcie celu
    from health_tracker.models import Notification
    notifications = Notification.query.filter_by(user_id=user.id).all()
    assert len(notifications) == 2

    # Sprawdzamy czy jedno z powiadomień jest o osiągnięciu celu
    messages = [n.message for n in notifications]
    assert any("Brawo" in message for message in messages)



def test_add_goal(client, db):
    """
    Test dodawania nowego celu przez użytkownika
    """

    # Rejestracja i logowanie
    client.post("/register", data={
        "username": "goalcreator",
        "email": "goalcreator@example.com",
        "password": "password"
    }, follow_redirects=True)

    client.post("/login", data={
        "username": "goalcreator",
        "password": "password"
    }, follow_redirects=True)

    # Dodanie celu
    response = client.post("/goals", data={
        "goal_type": "steps",
        "target_value": "8000"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert "8000" in response.data.decode('utf-8')  # Sprawdzamy, czy nowy cel pojawia się na stronie

    # Sprawdzamy w bazie danych
    from health_tracker.models import Goal, User

    user = User.query.filter_by(username="goalcreator").first()
    goals = Goal.query.filter_by(user_id=user.id).all()

    assert len(goals) == 1
    assert goals[0].type == "steps"
    assert goals[0].target_value == 8000


def test_update_user_settings(client, db):
    """
    Test aktualizacji ustawień użytkownika
    """

    # Rejestracja i logowanie
    client.post("/register", data={
        "username": "settingsuser",
        "email": "settingsuser@example.com",
        "password": "password"
    }, follow_redirects=True)

    client.post("/login", data={
        "username": "settingsuser",
        "password": "password"
    }, follow_redirects=True)

    # Aktualizacja ustawień
    response = client.post("/settings", data={
        "unit_system": "imperial",
        # nie podajemy "notifications_enabled", co oznacza że powinno być False
    }, follow_redirects=True)

    assert response.status_code == 200
    assert "Ustawienia zostały zapisane" in response.data.decode('utf-8')

    # Sprawdzenie w bazie danych
    from health_tracker.models import User, UserSettings

    user = User.query.filter_by(username="settingsuser").first()
    settings = UserSettings.query.filter_by(user_id=user.id).first()

    assert settings.unit_system == "imperial"
    assert settings.notifications_enabled is False
    
def test_registration_without_password(client, db):
    """
    Test próby rejestracji użytkownika bez podania hasła
    """

    response = client.post("/register", data={
        "username": "usernopass",
        "email": "nopass@example.com",
        "password": ""  # brak hasła
    }, follow_redirects=True)

    # Sprawdzamy, że rejestracja nie powiodła się
    assert response.status_code == 200
    assert "Hasło jest wymagane" in response.data.decode('utf-8')

