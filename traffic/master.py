from traffic.slicer import AbstractSlicer
from traffic.configurator import Configurator
from web.app import AbstractWebApp
from backends.logger import Logger

import asyncio
from aiohttp import web
import time
from typing import Optional

class Master:

    def __init__(self, 
                slicer: Optional[AbstractSlicer],
                webapp: Optional[AbstractWebApp]):

        self.slicer = slicer
        self.webapp = webapp

        self._logger = Logger(self)


    @classmethod
    def from_configurator(cls, configurator: Configurator):
        return cls(
            configurator.get_slicer(),
            configurator.get_webapp()
        )


    def run(self, loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()

        task = asyncio.wait([self._run_webapp(), self._run_slicer()], loop=loop)
        loop.run_until_complete(task)


    async def _run_webapp(self):
        runner = web.AppRunner(self.webapp.app)
        await runner.setup()
        site = web.TCPSite(runner, self.webapp.addr, self.webapp.port)
        await site.start()
        
        while True:
            if self.webapp.finish == True:
                await runner.cleanup()
                return
            else:
                await asyncio.sleep(60)


    async def _run_slicer(self):
        
        while True:
            try:
                await self.slicer.slice_pcaps()

            except Exception as e:
                self._logger.error(f'Can\'t properly slice pcaps from slicer-storage: {e}', e)
            
            await asyncio.sleep(30)
