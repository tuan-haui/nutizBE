from fastapi import APIRouter, Depends, Query
from app.schemas.karaoke import KaraokeSearchResponse, KaraokeSearchItem, KaraokeResolveRequest, KaraokeResolveResponse
from app.services.youtube_service import YoutubeService
from app.services.ytdlp_service import ytdlp_service
import yt_dlp

router = APIRouter()

def get_youtube_service() -> YoutubeService:
    return YoutubeService(ytdlp_service)

@router.get("/search", response_model=KaraokeSearchResponse)
def search_karaoke(q: str = Query(...)):
    # Using yt-dlp to search
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'default_search': 'ytsearch10',
    }
    items = []
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Append "karaoke" to the query if not present to prioritize karaoke videos
        search_query = q if "karaoke" in q.lower() else f"{q} karaoke"
        info = ydl.extract_info(search_query, download=False)
        for entry in info.get('entries', []):
            items.append(KaraokeSearchItem(
                id=entry.get('id'),
                title=entry.get('title'),
                duration=entry.get('duration'),
                thumbnail=entry.get('thumbnail') or (entry.get('thumbnails')[0]['url'] if entry.get('thumbnails') else None),
                channel=entry.get('channel'),
                url=entry.get('url')
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
