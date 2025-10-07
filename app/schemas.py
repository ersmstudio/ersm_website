<<<<<<< Updated upstream
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    avatar_url: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    avatar_url: Optional[str] = None
    password: Optional[str] = None

class UserOut(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    avatar_url: Optional[str] = None  # ✅ لتضمينه في المخرجات

    class Config:
        orm_mode = True
=======
# Pydantic schemas go here
>>>>>>> Stashed changes
