# Makefile

.PHONY: install cli flask test


# Install dependencies
install:
	pip install -r requirements/dev.txt && pre-commit install

# Run CLI
cli:
	PYTHONPATH=. python src/presentation/cli.py

# Run Flask app
flask:
	FLASK_APP=src/presentation/wsgi.py FLASK_CONFIG=development flask run -h 0.0.0.0

# Init postgres database
init-postgres:
	python manage.py init-postgres

# Build production web docker image
build-web:
	python manage.py compose build web

# Run production-ready system
prod-up:
	python manage.py compose up -d

# Run psql
prod-psql:
	python manage.py compose exec db psql -U postgres

# Stop production system
prod-down:
	python manage.py compose down

# Run integration tests using manage.py
test:
	python manage.py test -- --integration
