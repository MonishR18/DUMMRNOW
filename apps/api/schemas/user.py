from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    name: str
    username: str
    email: EmailStr
    role: str = "CLIENT"
    college: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(min_length=8)

class UserUpdate(BaseModel):
    name: Optional[str] = None
    profile_image: Optional[str] = None
    bio: Optional[str] = None
    skills: Optional[str] = None
    expertise: Optional[str] = None
    college: Optional[str] = None

class UserResponse(UserBase):
    id: int
    profile_image: Optional[str] = None
    bio: Optional[str] = None
    skills: Optional[str] = None
    expertise: Optional[str] = None
    rating: int = 0
    completed_orders: int = 0
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[str] = None

class RefreshToken(BaseModel):
    refresh_token: str

class PasswordReset(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(min_length=8)
