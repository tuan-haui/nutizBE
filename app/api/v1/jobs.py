from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.schemas.job import JobStatusResponse
from app.services.job_service import job_service
import os

router = APIRouter()

@router.get("/{job_id}", response_model=JobStatusResponse)
def get_job_status(job_id: str):
    status = job_service.get_job_status(job_id)
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
        
    filename = None
    if status['status'] == 'completed' and status.get('result'):
        filename = os.path.basename(status['result'])
        
    return {
        "job_id": status["job_id"],
        "status": status["status"],
        "progress": 100 if status["status"] == 'completed' else 0,
        "filename": filename,
        "error": status["error"]
    }

@router.get("/{job_id}/download")
def download_completed_file(job_id: str):
    status = job_service.get_job_status(job_id)
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
        
    if status['status'] != 'completed' or not status.get('result'):
        raise HTTPException(status_code=400, detail="Job is not completed yet")
        
    filepath = status['result']
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found on server")
        
    return FileResponse(filepath, filename=os.path.basename(filepath))

@router.delete("/{job_id}")
def cancel_job(job_id: str):
    success = job_service.cancel_job(job_id)
    if not success:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job_id": job_id, "status": "cancelled"}
