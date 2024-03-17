#Block for interaction with DB in business context
from db.models import User


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