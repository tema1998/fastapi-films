#Block for interaction with DB in business context
from sqlalchemy import Integer, select

from db.models import User, Film


class UserDAL:
    def __init__(self, db_session):
        self.db_session = db_session

    async def create_user(self, username: str, password: str, email: str):
        new_user = User(
            username=username,
            password=password,
            email=email,
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user


class FilmDAL:
    def __init__(self, db_session):
        self.db_session = db_session

    async def get_film_by_id(self, film_id: Integer):
        query = select(Film).where(Film.id == film_id)
        result = await self.db_session.execute(query)
        film_row = result.fetchone()
        if film_row is not None:
            return film_row[0]