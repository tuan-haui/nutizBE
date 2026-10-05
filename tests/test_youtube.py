from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, MagicMock

client = TestClient(app)

def test_get_video_info():
    with patch("app.services.ytdlp_service.YtDlpService.get_info") as mock_get_info:
        mock_get_info.return_value = {
            "id": "xxxxx",
            "title": "Example Song",
            "description": "Desc",
            "duration": 245,
            "thumbnail": "http://example.com/thumb.jpg",
            "channel_id": "UC123",
            "channel": "Test Channel",
            "view_count": 100,
            "upload_date": "20261005",
            "webpage_url": "https://www.youtube.com/watch?v=xxxxx"
        }
        
        response = client.get("/api/v1/youtube/info?url=https://www.youtube.com/watch?v=xxxxx")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "xxxxx"
        assert data["title"] == "Example Song"
        assert data["channel"]["id"] == "UC123"

def test_get_video_formats():
    with patch("app.services.ytdlp_service.YtDlpService.get_formats") as mock_get_formats:
        mock_get_formats.return_value = {
            "id": "xxxxx",
            "formats": [
                {
                    "format_id": "18",
                    "ext": "mp4",
                    "resolution": "360p",
                    "fps": 30,
                    "filesize": 123456,
                    "vcodec": "avc1",
                    "acodec": "mp4a"
                }
            ]
        }
        
        response = client.post(
            "/api/v1/youtube/formats", 
            json={"url": "https://www.youtube.com/watch?v=xxxxx"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["video_id"] == "xxxxx"
        assert len(data["formats"]) == 1
        assert data["formats"][0]["format_id"] == "18"
        assert data["formats"][0]["has_video"] == True
        assert data["formats"][0]["has_audio"] == True

def test_extract_media_url():
    with patch("app.services.ytdlp_service.YtDlpService.extract_audio") as mock_extract_audio:
        mock_extract_audio.return_value = {
            "id": "xxxxx",
            "title": "Example Song",
            "duration": 245,
            "url": "https://googlevideo.com/videoplayback?...",
            "ext": "m4a"
        }
        
        response = client.post(
            "/api/v1/youtube/extract", 
            json={"url": "https://www.youtube.com/watch?v=xxxxx", "type": "audio"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["video_id"] == "xxxxx"
        assert data["media"]["url"] == "https://googlevideo.com/videoplayback?..."
        assert data["media"]["type"] == "audio"
