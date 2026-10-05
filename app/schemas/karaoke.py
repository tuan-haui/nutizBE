from pydantic import BaseModel
from typing import List, Optional

class KaraokeSearchItem(BaseModel):
    id: str
    title: str
    duration: Optional[int] = None
    thumbnail: Optional[str] = None
    channel: Optional[str] = None
    url: str

class KaraokeSearchResponse(BaseModel):
    query: str
    items: List[KaraokeSearchItem]

class KaraokeResolveRequest(BaseModel):
    url: str

class KaraokeResolveResponse(BaseModel):
    video_id: str
    title: str
    duration: Optional[int] = None
    audio_url: str
