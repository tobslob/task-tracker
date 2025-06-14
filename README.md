# Task Tracker Application

This repository contains a FastAPI backend and a React frontend. Both services can be started together using Docker Compose.

## Prerequisites

- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) installed.

## Running the Application

From the repository root run:

```bash
docker-compose up --build
```

The backend will be available on [http://localhost:8000](http://localhost:8000) and the React frontend on [http://localhost:3000](http://localhost:3000).

The compose configuration seeds the SQLite database on startup using
`seed_db.py` so the app loads with sample data. On the first run it also
creates a superuser defined by the environment variables
`SUPERUSER_EMAIL`, `SUPERUSER_PASSWORD` and `SUPERUSER_NAME` (defaults are set
in `docker-compose.yml`). If the account already exists the seeder will skip it
so you can safely restart the containers.

If you need to allow additional origins for CORS, update the
`BACKEND_CORS_ORIGINS` variable in `docker-compose.yml` to a JSON list, for
example:

```yaml
BACKEND_CORS_ORIGINS: '["http://localhost:3000", "http://localhost:3001"]'
