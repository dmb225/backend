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

# Build production web docker image
build-web:
	python manage.py prod build web

# Run production-ready system
prod-up:
	python manage.py prod up -d

# Stop production system
prod-down:
	python manage.py prod down

# Run integration tests using manage.py
test:
	python manage.py test -- --integration
