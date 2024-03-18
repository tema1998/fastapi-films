from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException

from api.models import UserCreate, ShowFilm
from db.dals import UserDAL, FilmDAL
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


async def _get_film_by_id(film_id, db):
    async with db as session:
        async with session.begin():
            film_dal = FilmDAL(session)
            film = await film_dal.get_film_by_id(
                film_id=film_id
            )
            if film is not None:
                return ShowFilm(
                    id = film.id,
                    title = film.title,
                    description = film.description,
                    created_at = film.created_at,
                    censor_age = film.censor_age,
                    actors = film.actors,
                    directors = film.directors,
                    genres = film.genres,
                    link = film.link
                )


@router.get('/', response_model=ShowFilm)
async def get_film_by_id(film_id: int, db: AsyncSession = Depends(connect_db)):
    film = await _get_film_by_id(film_id, db)
    if film is None:
        raise HTTPException(status_code=404, detail=f"Film with id={film_id} not found")
    return film
