# Installation
- cd python
- python3 -m venv venv
- source venv/bin/activate
- pip install -r requirements/dev.txt
- pre-commit install

# Run

## command line interface
- PYTHONPATH=. python src/presentation/cli.py

## web server gateway inferface

### flask
- FLASK_APP=src/presentation/wsgi.py FLASK_CONFIG="development" flask run -h "0.0.0.0"

## Tests
- pytest -svv
- pytest -svv --integration (includes integration tests)

# Endpoints
- /users: Return the list of all users
