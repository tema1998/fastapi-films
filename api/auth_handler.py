from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException

import settings
from api.actions.auth import authenticate_user, _create_new_user, get_current_user_from_token
from api.models import UserCreate, Token
from api.utils import create_access_token
from db.models import User
from db.session import connect_db

auth_router = APIRouter()


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


@auth_router.get("/test_auth_endpoint")
async def sample_endpoint_under_jwt(current_user: User = Depends(get_current_user_from_token),):
    return {"Success": True, "current_user": current_user}


@auth_router.post('/signup', name='user:create')
async def create_user(body: UserCreate, db: AsyncSession = Depends(connect_db)):
    return await _create_new_user(body, db)
