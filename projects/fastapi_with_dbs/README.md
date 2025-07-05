# FastAPI + dependency-injector Setup

This is a FastAPI application using dependency-injector and PostgreSQL/Redis.


## Setup with uv (Python 3.13)

This project uses [uv](https://github.com/astral-sh/uv) for fast Python package management.

1. **Activate the virtual environment:**
   ```bash
   source .venv/bin/activate
   ```

2. **Install dependencies (if needed):**
   ```bash
   uv sync
   ```

3. **Start the containers:**
   ```bash
   docker-compose up -d
   ```

4. **Run the application:**
   ```bash
   uv run main.py

## API Endpoints

- `GET /health` - Health check
- `GET /sample` - Sample endpoint that uses both Redis and PostgreSQL

## Python Version

This project requires Python 3.13 and uses uv for dependency management.


## Features

- Async FastAPI app
- Dependency injection with `dependency-injector`
- PostgreSQL database integration
- Redis cache integration
- Clean architecture with separate containers and routes

## Major Learnings Point
- Dependency injection with `dependency-injector`
-  PostgreSQL database integration - using `asyncpg`
-  Redis cache integration - using `redis`
-  docker-compose for containerization