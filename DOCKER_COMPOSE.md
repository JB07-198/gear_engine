# Docker Compose Setup for Gear Engine

This Docker Compose configuration runs the full Gear Engine stack locally.

## Services

- **Redis**: In-memory store for Celery task queue.
- **Backend**: FastAPI server on port 8000.
- **Worker**: Celery worker for background export tasks.
- **Frontend**: React dev server on port 5173.

## Quick Start

```bash
docker-compose up
```

Then open `http://localhost:5173` in your browser.

## Environment Variables

Edit the `docker-compose.yml` to customize:

- `REQUIRE_AUTH`: Set to `true` to enable JWT authentication.
- `JWT_SECRET`: Set a strong secret for JWT signing (default: 'your-secret-key-change-me').
- `VITE_API_BASE`: Frontend API base URL (default: http://localhost:8000).

## Services URLs

- **Backend API**: http://localhost:8000
- **Frontend**: http://localhost:5173
- **Redis**: localhost:6379

## Building Images

To rebuild images:

```bash
docker-compose build
```

## Stopping

```bash
docker-compose down
```

To remove volumes:

```bash
docker-compose down -v
```

## Production Deployment

For production, use environment files and set:
- `REQUIRE_AUTH=true`
- `JWT_SECRET=<strong-random-secret>`
- Serve frontend as static files (not dev server).
- Use a production database (PostgreSQL) instead of SQLite.
- Set up proper logging and monitoring.

