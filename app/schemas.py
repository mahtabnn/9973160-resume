from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class ProjectRequestCreate(BaseModel):
    name: str
    email: EmailStr
    description: str

class ProjectRequestOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    description: str
    status: str
    admin_notes: Optional[str] = ""
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class ProjectRequestUpdate(BaseModel):
    status: Optional[str]
    admin_notes: Optional[str]

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"