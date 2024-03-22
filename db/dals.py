#Block for interaction with DB in business context
from sqlalchemy import Integer, select
from sqlalchemy.orm import joinedload

from api.utils import Hasher
from db.models import User, Film, Series


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


class FilmDAL:
    def __init__(self, db_session):
        self.db_session = db_session

    async def get_film_by_id(self, film_id: Integer):
        query = select(Film).options(joinedload(Film.actors)).options(joinedload(Film.directors)).where(Film.id == film_id)
        result = await self.db_session.execute(query)
        film_row = result.unique().fetchone()
        if film_row is not None:
            return film_row[0]


class SeriesDAL:
    def __init__(self, db_session):
        self.db_session = db_session

    async def get_series_by_id(self, series_id: Integer):
        query = select(Series).options(joinedload(Series.actors)).options(joinedload(Series.directors)).where(Series.id == series_id)
        result = await self.db_session.execute(query)
        series_row = result.unique().fetchone()
        if series_row is not None:
            return series_row[0]
