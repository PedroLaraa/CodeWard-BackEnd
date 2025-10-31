from pydantic import BaseModel, EmailStr
from datetime import datetime

# --- USER ---
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- TOKEN ---
class TokenOut(BaseModel):
    id: int
    token: str
    created_at: datetime

    class Config:
        from_attributes = True

class Dependency(BaseModel):
    name: str
    version: str
    ecosystem: str
