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

# Run resume parser app
resume_parser:
	PYTHONPATH=. \
	LOG_LEVEL=INFO \
	LOG_FILE=./llama_index.log \
	streamlit run src/presentation/llama_index/resume_parser.py

# Run single agent
single_agent:
	PYTHONPATH=. \
	LOG_LEVEL=INFO \
	LOG_FILE=./llama_index.log \
	python src/presentation/llama_index/single_agent.py

# Run multi-agent
multi_agent:
	PYTHONPATH=. \
	LOG_LEVEL=INFO \
	LOG_FILE=./llama_index.log \
	python src/presentation/llama_index/multi_agent.py

# Run memory-aware-agent
memory_aware_agent:
	PYTHONPATH=. \
	LOG_LEVEL=INFO \
	LOG_FILE=./llama_index.log \
	python src/presentation/llama_index/memory_aware_agent.py

# Run memory-aware-chat
memory_aware_chat:
	PYTHONPATH=. \
	LOG_LEVEL=INFO \
	LOG_FILE=./llama_index.log \
	python src/presentation/llama_index/memory_aware_chat.py

# Run simple agent without memory
simple_agent_wo_memory:
	PYTHONPATH=. \
	LOG_LEVEL=INFO \
	LOG_FILE=./llama_index.log \
	python src/presentation/llama_index/simple_agent_without_memory.py


# Run simple chat without memory
simple_chat_wo_memory:
	PYTHONPATH=. \
	LOG_LEVEL=INFO \
	LOG_FILE=./llama_index.log \
	python src/presentation/llama_index/simple_chat_without_memory.py

# Run llm workflow
llm_workflow:
	PYTHONPATH=. \
	LOG_LEVEL=INFO \
	LOG_FILE=./llama_index.log \
	python src/presentation/llama_index/workflow.py

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
