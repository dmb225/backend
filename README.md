**backend** is a template for back-end projects

# Dependencies
- postgresql-server-dev-all
- libpq-dev

# Installation
- python3 -m venv venv
- source venv/bin/activate
- make install

# Run

## Command line interface
- make cli

## Web server gateway inferface

### Flask
- make flask

## Production-ready system

### Build
- make build-web

### Init postgres
- make init-postgres

### Run prod
- make prod-up

### Run psql
- make prod-psql

### Stop prod
- make prod-down

## Tests
- make test

# Endpoints
- /users: Return the list of all users
    - /users?filter_age__lt=30
    - /users?filter_age__eq=30
    - /users?filter_age__gt=30
