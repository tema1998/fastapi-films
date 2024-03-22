import json
import uuid
from datetime import timedelta
from typing import Union

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException

import settings
from api.models import UserCreate, ShowFilm, ShowSeries, ShowFilmSchema, ShowSeriesSchema, Token
from api.utils import Hasher, create_access_token
from db.dals import UserDAL, FilmDAL, SeriesDAL
from db.models import User, AuthToken
from db.session import connect_db
from api.auth import check_auth_token

router = APIRouter()


async def _get_user_by_email_for_auth(email:str, db: AsyncSession):
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            return await user_dal.get_user_by_email(
                email=email,
            )


async def authenticate_user(email: str, password: str, db: AsyncSession) -> Union[User, None]:
    user = await _get_user_by_email_for_auth(email=email, db=db)
    if user is None:
        print('not user')
        return
    if not Hasher.get_password_hash(password) == user.password:
        print('not password')
        return
    return user


@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(connect_db)):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "other_custom_data": [1, 2, 3 ,4]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}




# @router.post('/login', name='user:login')
# def login(user_form: UserLoginForm = Body(..., embed=True), database=Depends(connect_db)):
#     user = database.query(User).filter(User.username == user_form.username).one_or_none()
#     if not user or Hasher.get_password_hash(user_form.password) != user.password:
#         return {'error': 'Email/password invalid'}
#
#     auth_token = AuthToken(token=str(uuid.uuid4()), user_id=user.id)
#     database.add(auth_token)
#     database.commit()
#     return {'auth_token': auth_token.token}


async def _create_new_user(body: UserCreate, db):
    async with db as session:
        async with session.begin():
            exists_username_query = select(User.id).filter(User.username == body.username)
            exists_username = await session.execute(exists_username_query)
            if exists_username.one_or_none():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Username already exists')
            exists_email_query = select(User.id).filter(User.email == body.email)
            exists_email = await session.execute(exists_email_query)
            if exists_email.one_or_none():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already exists')

            user_dal = UserDAL(session)
            user = await user_dal.create_user(
                username=body.username,
                password=body.password,
                email=body.email
            )
            return {'user_id': user.id}


@router.post('/user', name='user:create')
async def create_user(body: UserCreate, db: AsyncSession = Depends(connect_db)):
    return await _create_new_user(body, db)


async def _get_film_by_id(film_id, db):
    async with db as session:
        async with session.begin():
            film_dal = FilmDAL(session)
            film = await film_dal.get_film_by_id(
                film_id=film_id
            )
            if film is not None:
                return ShowFilmSchema(
                    id=film.id,
                    title=film.title,
                    description=film.description,
                    created_at=film.created_at,
                    censor_age=film.censor_age,
                    actors=jsonable_encoder(film.actors),
                    directors=jsonable_encoder(film.directors),
                    genres=film.genres,
                    link=film.link
                )


@router.get('/films', response_model=ShowFilmSchema)
async def get_film_by_id(film_id: int, db: AsyncSession = Depends(connect_db)):
    film = await _get_film_by_id(film_id, db)
    if film is None:
        raise HTTPException(status_code=404, detail=f"Film with id={film_id} not found")
    return film


async def _get_series_by_id(series_id, db):
    async with db as session:
        async with session.begin():
            series_dal = SeriesDAL(session)
            series = await series_dal.get_series_by_id(
                series_id=series_id
            )
            if series is not None:
                return ShowSeriesSchema(
                    id=series.id,
                    title=series.title,
                    description=series.description,
                    created_at=series.created_at,
                    censor_age=series.censor_age,
                    actors=jsonable_encoder(series.actors),
                    directors=jsonable_encoder(series.directors),
                    genres=series.genres,
                    link=series.link
                )


@router.get('/series', response_model=ShowSeriesSchema)
async def get_series_by_id(series_id: int, db: AsyncSession = Depends(connect_db)):
    series = await _get_series_by_id(series_id, db)
    if series is None:
        raise HTTPException(status_code=404, detail=f"Film with id={series_id} not found")
    return series
