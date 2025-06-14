# Task Tracker Application

This repository contains a FastAPI backend and a React frontend. Both services can be started together using Docker Compose or separately for development.

## Prerequisites

- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) installed (optional for Docker setup).
- [Git](https://git-scm.com/) installed for cloning the repository.
- [Python 3.8+](https://www.python.org/) and [Node.js](https://nodejs.org/) installed for running the backend and frontend separately.

## Cloning the Repository

To clone the repository and its submodule (`task-tracker-frontend`), run the following commands:

```bash
git clone --recurse-submodules https://github.com/tobslob/task-tracker.git
cd task-tracker
```

If you have already cloned the repository without the submodule, you can initialize and update the submodule with:

```bash
git submodule init
git submodule update
```

## Running the Application with Docker

From the repository root run:

```bash
docker-compose up --build
```

You might likely face this ```sh: react-scripts: command not found after running npm start``` after build.

Solution

```bash
cd task-tracker-frontend
npm install
cd ../ #back to the repository root
docker-compose down
docker-compose up
```

The backend will be available on [http://localhost:8000](http://localhost:8000) and the React frontend on [http://localhost:3000](http://localhost:3000).

## Running the Application Without Docker

### Backend Setup

1. Navigate to the `backend` directory:

   ```bash
   cd backend
   ```

2. Create and activate a Python virtual environment (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Seed the database with sample data (required for first-time setup):

   ```bash
   python seed_db.py
   ```

5. Start the FastAPI server:

   ```bash
   uvicorn app.main:app --reload
   ```

   The backend will be available on [http://localhost:8000](http://localhost:8000).

### Frontend Setup

1. Navigate to the `task-tracker-frontend` directory:

   ```bash
   cd task-tracker-frontend
   ```

2. Install Node.js dependencies:

   ```bash
   npm install
   ```

3. Start the React development server:

   ```bash
   npm start
   ```

   The frontend will be available on [http://localhost:3000](http://localhost:3000).

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
