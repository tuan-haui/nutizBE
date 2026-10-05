# YouTube Media API

Backend for iloveu.studio

## Development

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Running with Docker (Recommended)

Requires Docker and Docker Compose.

```bash
docker-compose up -d
```

This will start:
- FastAPI server on port 8000
- Redis server on port 6379
- RQ Worker for background media processing

## Local Development (Without Docker)

You need to have `redis-server` and `ffmpeg` installed on your machine.

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Terminal 1 - Start server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2 - Start worker
python -m app.workers.media_worker
```
