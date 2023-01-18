from typing import Optional

from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class User(UserBase):
    id: int
    is_active: Optional[bool] = True

    class Config:
        orm_mode = True

class UserInDB(User):
	hashed_password: str