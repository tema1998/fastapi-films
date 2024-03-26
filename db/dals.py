#Block for interaction with DB in business context
from sqlalchemy import Integer, select
from sqlalchemy.orm import joinedload

from api.utils import Hasher
from db.models import User, Movie, Genre, Category, Actor


class UserDAL:
    def __init__(self, db_session):
        self.db_session = db_session

    async def create_user(self, username: str, password: str, email: str):
        new_user = User(
            username=username,
            password=Hasher.get_password_hash(password),
            email=email,
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def get_user_by_email(self, email: str):
        query = select(User).where(User.email == email)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]


class MoviesDAL:
    def __init__(self, db_session):
        self.db_session = db_session

    async def get_movie_by_id(self, movie_id: int):
        query = select(Movie).options(joinedload(Movie.actors)).options(joinedload(Movie.directors)).join(Category).join(Genre).where(Movie.id ==movie_id)
        result = await self.db_session.execute(query)
        movie_row = result.unique().fetchone()
        if movie_row is not None:
            return movie_row[0]

    async def get_movies_by_category(self, category: str):
        query = (select(Movie).options(joinedload(Movie.actors)).options(joinedload(Movie.directors)).join(Category).
                 filter(Category.title == category))
        result = await self.db_session.execute(query)
        movies = result.unique().fetchall()
        if movies is not None:
            return movies

    async def get_movies_by_genre(self, genre: str):
        query = select(Movie).join(Genre).filter(Genre.title == genre)
        result = await self.db_session.execute(query)
        movies = result.unique().fetchall()
        if movies is not None:
            return movies

    async def get_movies_by_actor(self, actor_id: int):
        query = select(Movie).options(joinedload(Movie.actors)).where(Movie.actors.any(id=actor_id))
        result = await self.db_session.execute(query)
        movies = result.unique().fetchall()
        if movies is not None:
            return movies
