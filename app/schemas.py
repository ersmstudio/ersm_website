from pydantic import BaseModel, EmailStr
from typing import Optional

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

    class Config:
        orm_mode = True