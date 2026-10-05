from fastapi import APIRouter, Depends, Query
from app.schemas.youtube import (
    YouTubeUrlRequest, YouTubeExtractRequest, 
    VideoInfoResponse, VideoFormatsResponse, ExtractMediaResponse
)
from app.services.youtube_service import YoutubeService
from app.services.ytdlp_service import ytdlp_service

router = APIRouter()

def get_youtube_service() -> YoutubeService:
    return YoutubeService(ytdlp_service)

@router.get("/info", response_model=VideoInfoResponse)
def get_video_info(
    url: str = Query(..., description="YouTube video URL"),
    youtube_service: YoutubeService = Depends(get_youtube_service)
):
    return youtube_service.get_info(url)

@router.post("/formats", response_model=VideoFormatsResponse)
def get_video_formats(
    request: YouTubeUrlRequest,
    youtube_service: YoutubeService = Depends(get_youtube_service)
):
    return youtube_service.get_formats(str(request.url))

@router.post("/extract", response_model=ExtractMediaResponse)
def extract_media_url(
    request: YouTubeExtractRequest,
    youtube_service: YoutubeService = Depends(get_youtube_service)
):
    return youtube_service.extract_media(str(request.url), request.type)
