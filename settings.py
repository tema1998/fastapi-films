import os

from envparse import Env
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

env = Env()


SECRET_KEY = env.str(
    'SECRET_KEY',
    default="secret"
)


DATABASE_URL = env.str(
    'REAL_DATABASE_URL',
    default="postgresql+asyncpg://pguser:123321@localhost:5432/postgres"
)

ALGORITHM: str = env.str("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=30)