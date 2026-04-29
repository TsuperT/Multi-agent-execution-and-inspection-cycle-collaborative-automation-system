from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

class TaskCreate(BaseModel):
    data: Dict[str, Any]

class TaskResponse(BaseModel):
    id: int
    data: Dict[str, Any]
    status: str
    check_status: str
    result: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True