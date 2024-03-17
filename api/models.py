from pydantic import BaseModel
from typing import Optional


class UserLogin(BaseModel):
    username: str
    password: str


class UserCreate(BaseModel):
    username: Optional[str] = None
    password: str
    email: str



