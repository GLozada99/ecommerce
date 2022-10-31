override SHELL := /bin/bash

include .env

.PHONY: build
build:
	docker-compose build

.PHONY: logs
logs:
	docker-compose logs

.PHONY: run-dev
run-dev:
	$(MAKE) db-start-dev
	python manage.py runserver

.PHONY: run-prod
run-prod:
	$(MAKE) db-start
	docker-compose --env-file ./.env up -d web

.PHONY: run
run:
	pkill gunicorn
	gunicorn ecommerce.wsgi --bind 0.0.0.0:8000 --daemon

.PHONY: migrate
migrate:
	python manage.py makemigrations
	python manage.py migrate

.PHONY: db-start
db-start:
	docker-compose --env-file ./.env up -d --no-recreate db

.PHONY: db-stop
db-stop:
	docker-compose stop db

.PHONY: db-start-dev
db-start-dev:
	docker-compose --env-file ./.env up -d --no-recreate db-dev

.PHONY: db-stop-dev
db-stop-dev:
	docker-compose stop db-dev

.PHONY: stop
stop:
	docker-compose stop

.PHONY: set-data
set-data:
	$(MAKE) migrate
	python manage.py createcategories
	python manage.py createproducts
	python manage.py createslides
	DJANGO_SUPERUSER_PASSWORD=$(DJANGO_SUPERUSER_PASSWORD) \
	DJANGO_SUPERUSER_USERNAME=$(DJANGO_SUPERUSER_USERNAME) \
	DJANGO_SUPERUSER_EMAIL=$(DJANGO_SUPERUSER_EMAIL) \
	python manage.py createsuperuser --no-input

.PHONY: reset-db
reset-db:
	python manage.py reset_db --noinput
	$(MAKE) set-data
