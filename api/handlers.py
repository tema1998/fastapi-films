from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException

from api.models import UserCreate
from db.dals import UserDAL
from db.models import User
from db.session import connect_db
from api.auth import check_auth_token

router = APIRouter()


# @router.post('/login', name='user:login')
# def login(user_form: UserLoginForm = Body(..., embed=True), database=Depends(connect_db)):
#     user = database.query(User).filter(User.username == user_form.username).one_or_none()
#     if not user or get_password_hash(user_form.password) != user.password:
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


# @router.get('/user', name='user:get')
# def get_user(token: AuthToken = Depends(check_auth_token), database=Depends(connect_db)):
#     user = database.query(User).filter(User.id == token.user_id).one_or_none()
#
#     return {'id': user.id, 'email': user.email, 'nickname': user.nickname}
