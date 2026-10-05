from pydantic import BaseModel, HttpUrl
from typing import Optional

class MediaDownloadRequest(BaseModel):
    url: HttpUrl
    format: str = "mp3"
    quality: Optional[str] = None

class MediaConvertRequest(BaseModel):
    job_id: str
    format: str
    bitrate: Optional[str] = None

class AudioTrimRequest(BaseModel):
    job_id: str
    start: int
    end: int

class AudioNormalizeRequest(BaseModel):
    job_id: str

class JobResponse(BaseModel):
    job_id: str
    status: str
