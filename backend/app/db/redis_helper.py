from json import dumps, loads
from fastapi import Request
from aioredis import Redis
from loguru import logger
from functools import wraps


class ClientCache:
    """ Client Redis """

    def __init__(self, params: any):
        self.client: Redis = self.__get_client(params)

    def cache(self, ex: int = 500):
        """
        Decorator
        :param ex cache lifetime (in seconds)
        """
        def function(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                result: dict = await self.get_cache(request=kwargs.get("q"), key=None)
                if result:
                    return result
                result = await func(*args, **kwargs)
                if isinstance(result, dict | list):
                    await self.set_cache(request=kwargs.get("q"), key=None, data=result, ex=ex)
                return result
            return wrapper
        return function

    @staticmethod
    def __get_client(params) -> [Redis, None]:
        """
        get client Redis
        :param params connection
        """

        try:
            client = Redis(host=params.REDIS_HOST, port=params.REDIS_PORT)
            logger.info(f'Redis connect success!')
            return client
        except Exception as err:
            logger.error(f'err connect: {err}')
            return

    async def get_cache(self, key: str = None, request: Request = None) -> [dict, None]:
        """
        Get data from cache
        :param key: the key used to find the data (optional)
        :param request: request from which the search key is generated (optional)
        :return: cached data, if available
        """

        if not self.client:
            return
        key_ = key if key else await self.key_generate(request)
        try:
            d = await self.client.get(name=key_)
            if d:
                logger.debug(f'\n\tfrom Redis by key: {key_}')
                return loads(d)
        except Exception as err:
            logger.error(f'err get data cache: {err}')

    async def set_cache(self, key: str = None, request: Request = None, data: dict | list = None, ex=500):
        """
        Write data to cache
        :param key which is used to write the data (optional)
        :param request for the key used to write the data (optional)
        :param data to be written
        :param ex cache lifetime (in seconds)
        :info - either the key or the request must be passed
        """

        if not self.client:
            return
        try:
            key_ = key if key else await self.key_generate(request)
            await self.client.set(name=key_, value=dumps(data), ex=ex)
            logger.debug(f'\n\tAdd cache in Redis with key: {key_} \n\tLifetime {ex}')
        except Exception as err:
            logger.error(f'err set cache: {err}')

    async def key_generate(self, request: Request) -> str:
        """ Generating a key from query data """
        if not request:
            return ""
        body = await request.json() if await request.body() else ""
        key = request.url.path + "/" + request.url.query + self._body_to_key(body)
        logger.debug(f'\n\tRedis generate key {key}')
        return key

    @staticmethod
    def _body_to_key(body: dict) -> str:
        """ Converting the body of the request into a key """
        if not isinstance(body, dict):
            return ""
        key_value = str()
        for key in body:
            key_value += f'{key}-{body[key]}_'
        return key_value

    async def close_client(self):
        await self.client.close()
