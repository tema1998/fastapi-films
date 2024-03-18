from pydantic import BaseModel
from typing import Optional


class UserLogin(BaseModel):
    username: str
    password: str


class UserCreate(BaseModel):
    username: Optional[str] = None
    password: str
    email: str


class TunedModel(BaseModel):
    class Config:
        """Pydantic will convert to JSON even not dict"""
        orm_mode = True


class ShowFilm(BaseModel):
    id: int
    title: str
    description: str
    created_at: str
    censor_age: str
    actors: str
    directors: str
    genres: str
    link: str

