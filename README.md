**backend** is a template for back-end projects

# Dependencies
- postgresql-server-dev-all
- libpq-dev

# Installation
- python3 -m venv venv
- source venv/bin/activate
- make install

# Try applications
- make lint
- make test
- make cli
- make llm
- make rag
- make resume_parser
- make single_agent
- make flask
- make fastapi

# Run production-ready flask app
- make build-web
- make init-postgres
- make prod-up
- make prod-psql
- make prod-down

# APIs
- Flask
    - http://127.0.0.1:5000/docs
- FastAPI
    - http://127.0.0.1:8000/docs
