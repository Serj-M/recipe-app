import os

from app.helpers.config_generator import EnvInstaller

# Parse a .env file and then load all the variables found as environment variables.
EnvInstaller()

PORT = os.environ.get('PORT')

TARGET = os.environ.get('TARGET')
VERSION_APP = os.environ.get('VERSION_APP')


DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')


DATABASE_URL = (
    f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
)


class REDIS_PARAMS:
    """ Redis params """
    REDIS_HOST = os.environ.get('REDIS_HOST')
    REDIS_PORT = os.environ.get('REDIS_PORT')


class REDIS_CACHE_EX:
    """ Redis cach time live (sec) """
    default = os.environ.get('cache_ex_default')
    one_day: int = 86400
    one_hour = 3600
