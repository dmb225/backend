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

# Run integration tests using manage.py
test:
	python manage.py test -- --integration
