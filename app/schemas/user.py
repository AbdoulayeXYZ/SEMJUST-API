from typing import Optional
from pydantic import BaseModel, EmailStr, constr

from app.models.user import Role

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: Role = Role.USER
    is_active: bool = True

class UserCreate(UserBase):
    password: constr(min_length=8)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[constr(min_length=8)] = None
    role: Optional[Role] = None
    is_active: Optional[bool] = None

class UserInDBBase(UserBase):
    id: int
    is_superuser: bool

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[int] = None 