from fastapi import APIRouter, Depends, HTTPException
from app.schemas.media import MediaDownloadRequest, JobResponse
from app.services.job_service import job_service
from app.services.ytdlp_service import ytdlp_service
from app.services.storage_service import storage_service

router = APIRouter()

def download_audio_task(url: str, format: str, quality: str):
    file_path = ytdlp_service.download_audio(url, format, quality)
    return storage_service.upload_file(file_path)

def download_video_task(url: str, format: str, quality: str):
    file_path = ytdlp_service.download_video(url, format, quality)
    return storage_service.upload_file(file_path)

@router.post("/audio", response_model=JobResponse)
def download_audio(request: MediaDownloadRequest):
    job_id = job_service.enqueue_job(
        download_audio_task, 
        str(request.url), 
        request.format, 
        request.quality or "192"
    )
    return {"job_id": job_id, "status": "queued"}

@router.post("/video", response_model=JobResponse)
def download_video(request: MediaDownloadRequest):
    job_id = job_service.enqueue_job(
        download_video_task, 
        str(request.url), 
        request.format, 
        request.quality or "720p"
    )
    return {"job_id": job_id, "status": "queued"}

from app.services.ffmpeg_service import ffmpeg_service
from app.schemas.media import MediaConvertRequest, AudioTrimRequest

def convert_audio_task(file_path: str, format: str, bitrate: str):
    out_path = ffmpeg_service.convert_audio(file_path, format, bitrate)
    return storage_service.upload_file(out_path)

def trim_audio_task(file_path: str, start: int, end: int):
    out_path = ffmpeg_service.trim_audio(file_path, start, end)
    return storage_service.upload_file(out_path)

@router.post("/convert/audio", response_model=JobResponse)
def convert_audio(request: MediaConvertRequest):
    status = job_service.get_job_status(request.job_id)
    if not status or not status.get('result'):
        raise HTTPException(status_code=400, detail="Original job not completed")
    job_id = job_service.enqueue_job(
        convert_audio_task, 
        status['result'], 
        request.format, 
        request.bitrate or "192k"
    )
    return {"job_id": job_id, "status": "queued"}

@router.post("/audio/trim", response_model=JobResponse)
def trim_audio(request: AudioTrimRequest):
    status = job_service.get_job_status(request.job_id)
    if not status or not status.get('result'):
        raise HTTPException(status_code=400, detail="Original job not completed")
    job_id = job_service.enqueue_job(
        trim_audio_task, 
        status['result'], 
        request.start, 
        request.end
    )
    return {"job_id": job_id, "status": "queued"}
