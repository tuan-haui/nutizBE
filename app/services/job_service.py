import uuid
from typing import Dict, Any, Optional
from redis import Redis
from rq import Queue
from app.core.config import settings

class JobService:
    def __init__(self):
        self.redis = Redis.from_url(settings.REDIS_URL)
        self.queue = Queue('default', connection=self.redis)

    def enqueue_job(self, func, *args, **kwargs) -> str:
        job = self.queue.enqueue(func, *args, **kwargs)
        return job.id

    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        from rq.job import Job
        from rq.exceptions import NoSuchJobError
        
        try:
            job = Job.fetch(job_id, connection=self.redis)
            status = job.get_status()
            
            # Map RQ status to our API status
            if status == 'queued':
                status = 'queued'
            elif status == 'started':
                status = 'processing'
            elif status == 'finished':
                status = 'completed'
            elif status == 'failed':
                status = 'failed'
            elif status == 'canceled':
                status = 'cancelled'
                
            return {
                "job_id": job.id,
                "status": status,
                "result": job.result,
                "error": str(job.exc_info) if job.exc_info else None
            }
        except NoSuchJobError:
            return None

    def cancel_job(self, job_id: str) -> bool:
        from rq.job import Job
        from rq.exceptions import NoSuchJobError
        
        try:
            job = Job.fetch(job_id, connection=self.redis)
            job.cancel()
            return True
        except NoSuchJobError:
            return False

job_service = JobService()
