# Makefile for Health Tracker (Docker + Flask Project)

# Zmienna z nazwą kontenera
PROJECT_NAME=aplikacja-wielowarstwowa-projekt

# Polecenia
.PHONY: build up down restart logs shell prune

# Buduj obraz
build:
	docker-compose build

# Odpal aplikację
up:
	docker-compose up --build

# Zatrzymaj kontener
down:
	docker-compose down

# Restartuj kontener
restart: down up

# Podgląd logów
logs:
	docker-compose logs -f

# Wejdź do kontenera
shell:
	docker exec -it $$(docker ps -q -f name=${PROJECT_NAME}_web) /bin/sh

# Wyczyść nieużywane obrazy i kontenery
prune:
	docker system prune -af
