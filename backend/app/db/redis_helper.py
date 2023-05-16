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
        Декоратор кеширования результатов

        :param ex время жизни данных в кэше (сек)
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
        Получение клиента Redis

        :param params: параметры подключения
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
        Получение данных из кэша

        :param key: ключ, по которому осуществляется поиск данных (не обязательное)
        :param request: запрос, на основе которого формируется ключ поиска (не обязательное)
        :return: кешированные данные, при наличии
        """

        if not self.client:
            return
        key_ = key if key else await self.key_generate(request)
        try:
            d = await self.client.get(name=key_)
            if d:
                logger.debug(f'\n\tИз Redis получен кэш по ключу: {key_}')
                return loads(d)
        except Exception as err:
            logger.error(f'err get data cache: {err}')

    async def set_cache(self, key: str = None, request: Request = None, data: dict | list = None, ex=500):
        """
        Запись данных в кэш

        :param key ключ, по которому осуществляется запись данных (не обязательное)
        :param request запрос, на основе которого формируется ключ записи (не обязательное)
        :param data записываемые данные
        :param ex время жизни данных в кэше (сек)

        :info - должен быть передан key или request
        """

        if not self.client:
            return
        try:
            key_ = key if key else await self.key_generate(request)
            await self.client.set(name=key_, value=dumps(data), ex=ex)
            logger.debug(f'\n\tВ Redis добавлен кэш с ключом: {key_} \n\tВремя жизни {ex}')
        except Exception as err:
            logger.error(f'err set cache: {err}')

    async def key_generate(self, request: Request) -> str:
        """ Формирование ключа по данным запроса """
        if not request:
            return ""
        body = await request.json() if await request.body() else ""
        key = request.url.path + "/" + request.url.query + self._body_to_key(body)
        logger.debug(f'\n\tRedis generate key {key}')
        return key

    @staticmethod
    def _body_to_key(body: dict) -> str:
        """ Преобразование тела запроса в ключ """
        if not isinstance(body, dict):
            return ""
        key_value = str()
        for key in body:
            key_value += f'{key}-{body[key]}_'
        return key_value

    async def close_client(self):
        """"""
        await self.client.close()
