from traffic.slicer import AbstractSlicer
from traffic.crawler import AbstractCrawler
from traffic.configurator import Configurator
from traffic.logger import Logger

import asyncio
import time

class Masta:

    def __init__(self, 
                slicer: AbstractSlicer,
                crawler: AbstractCrawler):
        self.slicer = slicer
        self.crawler = crawler

        self._logger = Logger(self)


    @classmethod
    def from_configurator(cls, configurator: Configurator):
        return cls(
            configurator.get_slicer(),
            configurator.get_crawler()
        )


    def run(self, loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()
        task = asyncio.wait([self._run_slicer(), self._run_crawler()], loop=loop)
        loop.run_until_complete(task)


    async def _run_slicer(self):
        while True:
            try:
                await self.slicer.slice_pcaps()

            except Exception as e:
                self._logger.error(f'Can\'t properly slice pcaps from slicer-storage: {e}', e)
            
            await asyncio.sleep(500)


    async def _run_crawler(self):
        pass
