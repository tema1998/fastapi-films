from typing import Union

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException

import settings
from api.models import UserCreate
from api.utils import Hasher
from db.dals import UserDAL
from db.models import User
from db.session import connect_db


async def _get_user_by_email_for_auth(email:str, session: AsyncSession):
    async with session.begin():
        user_dal = UserDAL(session)
        return await user_dal.get_user_by_email(
            email=email,
        )


async def authenticate_user(email: str, password: str, db: AsyncSession) -> Union[User, None]:
    user = await _get_user_by_email_for_auth(email=email, db=db)
    if user is None:
        return
    if not Hasher.get_password_hash(password) == user.password:
        return
    return user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


async def get_current_user_from_token(
        token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(connect_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await _get_user_by_email_for_auth(email=username, db=db)
    if user is None:
        raise credentials_exception
    return user


async def _create_new_user(body: UserCreate, session):
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

