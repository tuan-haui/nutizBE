from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict, Any

class YouTubeUrlRequest(BaseModel):
    url: HttpUrl

class YouTubeExtractRequest(BaseModel):
    url: HttpUrl
    type: str = "best" # audio, video, best

class ChannelInfo(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None

class VideoInfoResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    duration: Optional[int] = None
    thumbnail: Optional[str] = None
    channel: Optional[ChannelInfo] = None
    view_count: Optional[int] = None
    upload_date: Optional[str] = None
    webpage_url: str

class FormatInfo(BaseModel):
    format_id: str
    ext: str
    resolution: Optional[str] = None
    fps: Optional[int] = None
    filesize: Optional[int] = None
    abr: Optional[float] = None
    has_video: bool
    has_audio: bool

class VideoFormatsResponse(BaseModel):
    video_id: str
    formats: List[FormatInfo]

class MediaInfo(BaseModel):
    url: str
    type: str
    format: str
    mime_type: Optional[str] = None
    duration: Optional[int] = None

class ExtractMediaResponse(BaseModel):
    video_id: str
    title: str
    duration: Optional[int] = None
    media: MediaInfo
