# Makefile

.PHONY: install cli flask test


# Install dependencies
install:
	pip install -r requirements/dev.txt && pre-commit install

# Run linting
lint:
	ruff check src --fix && mypy src

# Run tests (including integration tests)
test:
	python manage.py test -- --integration

# Run CLI
cli:
	PYTHONPATH=. \
	LOG_LEVEL=INFO \
	LOG_FILE=./cli.log \
	python src/presentation/cli/main.py

# Run llama_index app
llm:
	PYTHONPATH=. \
	LOG_LEVEL=INFO \
	LOG_FILE=./llama_index.log \
	python src/presentation/llama_index/llm.py

# Run llama_index app
rag:
	PYTHONPATH=. \
	LOG_LEVEL=INFO \
	LOG_FILE=./llama_index.log \
	streamlit run src/presentation/llama_index/rag.py


# Run Flask app
flask:
	POSTGRES_USER=postgres \
	POSTGRES_PASSWORD=postgres \
	POSTGRES_HOSTNAME=localhost \
	POSTGRES_PORT=5433 \
	APPLICATION_DB=application \
	FLASK_APP=src/presentation/flask/main.py \
	FLASK_CONFIG=development \
	LOG_LEVEL=INFO \
	LOG_FILE=./flask.log \
	flask run -h 0.0.0.0

# Run fastapi app
fastapi:
	LOG_LEVEL=INFO \
	LOG_FILE=./fastapi.log \
	fastapi dev src/presentation/fastapi/main.py

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
	python manage.py compose exec db psql -U postgres -d application

# Autogenerate migrations
alembic-generate:
	POSTGRES_USER=postgres \
	POSTGRES_PASSWORD=postgres \
	POSTGRES_HOSTNAME=localhost \
	APPLICATION_DB=application \
	alembic revision --autogenerate -m "Initial"

# Apply migrations
alembic-upgrade:
	POSTGRES_USER=postgres \
	POSTGRES_PASSWORD=postgres \
	POSTGRES_HOSTNAME=localhost \
	APPLICATION_DB=application \
	alembic upgrade head

# Stop production system
prod-down:
	python manage.py compose down
