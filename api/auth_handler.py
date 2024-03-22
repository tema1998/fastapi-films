from datetime import timedelta
from typing import Union

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException

import settings
from api.models import UserCreate, Token
from api.utils import Hasher, create_access_token
from db.dals import UserDAL
from db.models import User
from db.session import connect_db

auth_router = APIRouter()


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


@auth_router.post('/token', response_model=Token)
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


@auth_router.get("/test_auth_endpoint")
async def sample_endpoint_under_jwt(current_user: User = Depends(get_current_user_from_token),):
    return {"Success": True, "current_user": current_user}


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


@auth_router.post('/user', name='user:create')
async def create_user(body: UserCreate, db: AsyncSession = Depends(connect_db)):
    return await _create_new_user(body, db)
