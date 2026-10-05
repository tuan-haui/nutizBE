from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "youtube-media-api",
        "version": "1.0.0"
    }

def test_health_dependencies():
    response = client.get("/api/v1/health/dependencies")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "dependencies": {
            "yt_dlp": "ok",
            "ffmpeg": "ok",
            "storage": "ok"
        }
    }
