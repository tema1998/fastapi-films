import os

from envparse import Env
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

env = Env()

dir_path = os.path.dirname(os.path.realpath(__file__))
root_dir = dir_path[:-3]
config = Config(f'{root_dir}.env')

SECRET_KEY = config('SECRET_KEY', cast=Secret)
#DATABASE_URL = f'sqlite:///{root_dir}' + config('DB_NAME', cast=str)

DATABASE_URL = env.str(
    'REAL_DATABASE_URL',
    default="postgresql+asyncpg://postgres@0.0.0.0:5432/postgres"
)