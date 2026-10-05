from fastapi import APIRouter
from app.api.v1 import health, youtube, media, jobs, karaoke

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(youtube.router, prefix="/youtube", tags=["youtube"])
api_router.include_router(karaoke.router, prefix="/karaoke", tags=["karaoke"])
api_router.include_router(media.router, prefix="/media", tags=["media"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
