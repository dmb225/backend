**backend** is a template for back-end projects

# Dependencies
- postgresql-server-dev-all
- libpq-dev

# Installation
- python3 -m venv venv
- source venv/bin/activate
- make install

# Development commands
- make test
- make cli
- make flask
- make fastapi

# Production commands
- make build-web
- make init-postgres
- make prod-up
- make prod-psql
- make prod-down

# Endpoints
- /users: Return the list of all users
    - /users?filter_age__lt=30
    - /users?filter_age__eq=30
    - /users?filter_age__gt=30
