override SHELL := /bin/bash

.PHONY: build
build:
	docker-compose build

.PHONY: run-dev
run-dev:
	python manage.py runserver

.PHONY: db-start
db-start:
	docker-compose --env-file ./.env up db -d

.PHONY: db-stop
db-stop:
	docker-compose stop db
