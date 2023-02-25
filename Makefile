override SHELL := /bin/bash

include .env

.PHONY: build
build:
	docker-compose build

.PHONY: logs
logs:
	docker-compose logs

.PHONY: db-start
db-start:
	docker-compose --env-file ./.env up -d db

.PHONY: db-stop
db-stop:
	docker-compose stop db

.PHONY: db-start-dev
db-start-dev:
	docker-compose --env-file ./.env up -d db-dev

.PHONY: db-stop-dev
db-stop-dev:
	docker-compose stop db-dev

.PHONY: stop
stop:
	docker-compose stop

.PHONY: runserver
runserver:
	poetry run python manage.py runserver

.PHONY: run
run:
	poetry run pkill gunicorn || true
	poetry run authbind gunicorn ecommerce.wsgi --bind 0.0.0.0:$(PORT) --daemon

.PHONY: migrate
migrate:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

.PHONY: set-data
set-data:
	$(MAKE) migrate
	poetry run python manage.py createcategories
	poetry run python manage.py createproducts
	poetry run python manage.py createslides
	DJANGO_SUPERUSER_PASSWORD=$(DJANGO_SUPERUSER_PASSWORD) \
	DJANGO_SUPERUSER_USERNAME=$(DJANGO_SUPERUSER_USERNAME) \
	DJANGO_SUPERUSER_EMAIL=$(DJANGO_SUPERUSER_EMAIL) \
	poetry run python manage.py createsuperuser --no-input
	poetry run python manage.py addgoogleauth
	poetry run python manage.py creategroups

.PHONY: set-data-light
set-data-light:
	$(MAKE) migrate
	DJANGO_SUPERUSER_PASSWORD=$(DJANGO_SUPERUSER_PASSWORD) \
	DJANGO_SUPERUSER_USERNAME=$(DJANGO_SUPERUSER_USERNAME) \
	DJANGO_SUPERUSER_EMAIL=$(DJANGO_SUPERUSER_EMAIL) \
	poetry run python manage.py createsuperuser --no-input
	poetry run python manage.py addgoogleauth
	poetry run python manage.py creategroups

.PHONY: reset-db
reset-db:
	poetry run python manage.py reset_db --noinput
	$(MAKE) set-data

.PHONY: reset-db-light
reset-db-light:
	poetry run python manage.py reset_db --noinput
	$(MAKE) set-data-light
