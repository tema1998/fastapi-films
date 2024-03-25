import datetime

from pydantic import BaseModel, Field
from typing import Optional, List

from sqlalchemy import Select
from sqlalchemy.orm import Query
from sqlalchemy.orm.collections import InstrumentedList

from db.models import Actor, Director


class UserLogin(BaseModel):
    username: str
    password: str


class UserCreate(BaseModel):
    username: Optional[str] = None
    password: str
    email: str


class ActorsBase(BaseModel):
    id: int
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class DirectorsBase(BaseModel):
    id: int
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class ShowFilmOrSeries(BaseModel):
    id: int
    title: str
    description: str
    image: str
    created_at: datetime.datetime
    censor_age: str

    genres: int
    link: str

    class Config:
        orm_mode = True


class ShowFilmOrSeriesSchema(ShowFilmOrSeries):
    actors: List[ActorsBase]
    directors: List[DirectorsBase]


class Token(BaseModel):
    access_token: str
    token_type: str


class ShowFilmOrSeriesShort(BaseModel):
    id: int
    title: str
    image: str
    censor_age: str
    link: str

    class Config:
        orm_mode = True
