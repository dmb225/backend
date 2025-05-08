**backend** is a template for back-end projects

# Dependencies
- postgresql-server-dev-all
- libpq-dev

# Installation
- python3 -m venv venv
- source venv/bin/activate
- make install

# Run

## command line interface
- make cli

## web server gateway inferface

### flask
- make flask

## production-ready system
- make build-web
- make prod-up
- make prod-down

### tests
- http://localhost:8080/users?filter_age__lt=30
- http://localhost:8080/users?filter_age__eq=30
- http://localhost:8080/users?filter_age__gt=30

## Tests
- make test

# Endpoints
- /users: Return the list of all users
