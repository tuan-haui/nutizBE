from fastapi import APIRouter, Depends, Query
from app.schemas.karaoke import KaraokeSearchResponse, KaraokeSearchItem, KaraokeResolveRequest, KaraokeResolveResponse
from app.services.youtube_service import YoutubeService
from app.services.ytdlp_service import ytdlp_service

router = APIRouter()

def get_youtube_service() -> YoutubeService:
    return YoutubeService(ytdlp_service)

@router.get("/search", response_model=KaraokeSearchResponse)
def search_karaoke(
    q: str = Query(...),
    youtube_service: YoutubeService = Depends(get_youtube_service)
):
    items = []
    # Append "karaoke" to the query if not present to prioritize karaoke videos
    search_query = q if "karaoke" in q.lower() else f"{q} karaoke"
    
    info = youtube_service.search(search_query, max_results=10)
    
    for entry in info.get('entries', []):
        items.append(KaraokeSearchItem(
            id=entry.get('id'),
            title=entry.get('title'),
            duration=entry.get('duration'),
            thumbnail=entry.get('thumbnail') or (entry.get('thumbnails')[0]['url'] if entry.get('thumbnails') else None),
            channel=entry.get('channel'),
            url=(entry.get('webpage_url') or f"https://www.youtube.com/watch?v={entry.get('id')}")
        ))
        
    return KaraokeSearchResponse(query=q, items=items)

@router.post("/resolve", response_model=KaraokeResolveResponse)
def resolve_karaoke_media(
    request: KaraokeResolveRequest,
    youtube_service: YoutubeService = Depends(get_youtube_service)
):
    extracted = youtube_service.extract_media(request.url, "audio")
    return KaraokeResolveResponse(
        video_id=extracted.video_id,
        title=extracted.title,
        duration=extracted.duration,
        audio_url=extracted.media.url
    )
