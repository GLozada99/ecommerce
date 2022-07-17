override SHELL := /bin/bash

.PHONY: build
build:
	docker-compose build

.PHONY: logs
logs:
	docker-compose logs

.PHONY: run-dev
run-dev:
	python manage.py runserver

.PHONY: run-prod
run-prod:
	docker-compose --env-file ./.env up web -d

.PHONY: migrate
migrate:
	python manage.py makemigrations
	python manage.py migrate

.PHONY: db-start
db-start:
	docker-compose --env-file ./.env up db -d

.PHONY: db-stop
db-stop:
	docker-compose stop db

.PHONY: stop
stop:
	docker-compose stop
