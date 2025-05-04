# Installation
- cd python
- python3 -m venv venv
- source venv/bin/activate
- pip install -r requirements/dev.txt
- pre-commit install

# Run

## command line interface
- PYTHONPATH=. python src/presentation/cli.py

## Tests
- pytest -svv
