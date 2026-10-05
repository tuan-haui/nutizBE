from pydantic import BaseModel
from typing import Optional

class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    progress: Optional[int] = 0
    filename: Optional[str] = None
    error: Optional[str] = None
