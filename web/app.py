from backends.logger import Logger
from backends.database import AbstractDBControl

import asyncio
from aiohttp import web
from typing import Optional
import json


class AbstractWebApp:
    def __init__(self):
        self._logger = Logger('WebApp')


class WebApp(AbstractWebApp):
    DEFAULT_PORT = 8888
    DEFAULT_ADDR = '127.0.0.1'

    def __init__(self, addr: Optional[str]=None, 
                       port: Optional[int]=None,
                       database: Optional[AbstractDBControl]=None):
        super().__init__()
        
        self.addr = self.DEFAULT_ADDR if addr is None else addr
        self.port = self.DEFAULT_PORT if port is None else port

        self._logger.debug(f'http://{self.addr}:{self.port}')

        self.app = web.Application()
        self.app.router.add_get('/', self._root_handler)
        self.app.router.add_get('/{index}', self._get_stream_handler)

        self.database = database
        
        self.finish = False
        
        self.runner = web.AppRunner(self.app)

    async def _get_stream_handler(self, request):
        index = int(request.match_info.get('index'))
        stream = await self.database.get_stream(index)
        self._logger.debug(f'Got stream: {stream}')
        return web.json_response(stream)

    async def _root_handler(self, request):
        self._logger.debug('Incoming request')
        return web.Response(text='huypizda')
                