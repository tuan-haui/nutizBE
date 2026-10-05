from fastapi import APIRouter
from app.core.config import settings
from typing import Dict, Any

router = APIRouter()

@router.get("")
def health_check() -> Dict[str, Any]:
    return {
        "status": "ok",
        "service": "youtube-media-api",
        "version": settings.VERSION,
    }

@router.get("/dependencies")
def health_dependencies() -> Dict[str, Any]:
    return {
        "status": "ok",
        "dependencies": {
            "yt_dlp": "ok",
            "ffmpeg": "ok",
            "storage": "ok"
        }
    }
