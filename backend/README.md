# Task Tracker Application

This project implements a simple task tracker API using **FastAPI**.

## Features

* User registration and authentication with JWT
* CRUD operations for tasks
* RESTful API exposed under `/api/v1`

## Development

Create a `.env` file based on `.env.example`, install the dependencies and run the application with:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

If you see an error like `AttributeError: module 'bcrypt' has no attribute '__about__'`,
ensure the correct bcrypt backend is installed by reinstalling the requirements:

```bash
pip install --force-reinstall -r requirements.txt
```

To run the unit tests:

```bash
pytest
```

By default the application uses a local SQLite database stored in the project
directory. If you want to connect to MySQL or PostgreSQL instead, provide a
full connection string via the `DATABASE_URL` environment variable.

Set the `BACKEND_CORS_ORIGINS` variable to a comma-separated list of frontend
origins that are allowed to make authenticated requests. The default value is
`http://localhost:3000` for development.

### Using In-memory Database

Set the `DB_MEMORY` environment variable to `1` along with `DB=sqlite` to run the
application against an in-memory SQLite database. This is useful for local
testing where persistence is not required.

### PostgreSQL driver

If you connect to a PostgreSQL database, ensure the `psycopg2-binary` package is
installed. This repository lists it in `requirements.txt` to provide a
prebuilt driver that works across platforms, avoiding architecture errors on
macOS and Linux.

## Seeding the Database

To load a large set of sample users and tasks into the configured database, run:

```bash
python seed_db.py
```

This will recreate the tables and insert over a hundred sample users and several
hundred tasks from the files in the `seeds/` directory.
