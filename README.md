# Health Tracker

Health Tracker to aplikacja webowa służąca do monitorowania zdrowia i aktywności użytkownika.  
Projekt powstał w technologii trójwarstwowej (model - widok - kontroler) z wykorzystaniem języka Python i frameworka Flask.

---

## Funkcjonalności

- Rejestracja i logowanie użytkownika 
- Dodawanie codziennych wpisów zdrowotnych (kroki, sen, kalorie, waga) 
- Wyznaczanie i zarządzanie celami zdrowotnymi 
- Dashboard z wykresami aktywności 
- Powiadomienia o osiągnięciu celów 
- Ustawienia użytkownika (system jednostek, powiadomienia) 
- Testy jednostkowe dla modeli i tras 

---

## Technologie użyte w projekcie

- **Python 3.10.8**
- **Flask** – framework webowy
- **SQLAlchemy** – ORM
- **SQLite** – lekka baza danych
- **Flask-Login** – zarządzanie sesjami użytkowników
- **Chart.js** – wykresy w dashboardzie
- **HTML5 + Bootstrap 5** – frontend

---

## Instalacja projektu

1. **Sklonuj repozytorium**:

```bash
git clone https://github.com/twoj-uzytkownik/health-tracker.git
cd health-tracker

2. Utwórz i aktywuj środowisko wirtualne:

python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate


3. Zainstaluj zależności:

pip install -r requirements.txt


4. Utwórz plik bazy danych i zainicjalizuj ją:

python
>>> from health_tracker import create_app
>>> app = create_app()
>>> app.app_context().push()
>>> from health_tracker.extensions import db
>>> db.create_all()
>>> exit()


5. Uruchom aplikację:

python run.py

6. Testowanie

python -m pytest


7. Struktura katalogów

health_tracker/
    ├── templates/     # Szablony HTML
    ├── static/        # Pliki statyczne (CSS, JS, obrazki)
    ├── models.py      # Modele bazy danych
    ├── routes.py      # Ścieżki (kontrolery)
    ├── extensions.py  # Rozszerzenia Flask (DB, LoginManager)
    ├── config.py      # Konfiguracja aplikacji
    ├── test_config.py # Konfiguracja aplikacji testowej
tests/
    ├── test_models.py
    ├── test_routes.py
venv/                  # Środowisko wirtualne
README.md              # Ten plik
requirements.txt       # Lista wymaganych pakietów
run.py                 # Plik uruchamiający aplikację


8. Autor

Projekt stworzony przez: Kamil Kwiek
W ramach przedmiotu Projektowanie wielowarstwowych aplikacji biznesowych L3.