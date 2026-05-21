from typing import Optional
from pydantic import UUID4, BaseModel, EmailStr, Field



class UserCreate(BaseModel):
    username: str 
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

