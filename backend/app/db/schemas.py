# backend/app/db/schemas.py
from pydantic import BaseModel
from typing import Dict, Any
import datetime

class ResumeBase(BaseModel):
    github_username: str

class ResumeCreate(ResumeBase):
    resume_data: Dict[str, Any]

class Resume(ResumeBase):
    id: int
    resume_data: Dict[str, Any]
    created_at: datetime.datetime
    updated_at: datetime.datetime | None = None

    class Config:
        orm_mode = True
