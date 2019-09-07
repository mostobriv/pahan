from traffic.logger import Logger
from traffic.pcap_storage import DirectoryPcapStorage

import glob
import os.path
import asyncio
from traffic.database import Redis
from typing import Optional

AbstractEventLoop = asyncio.AbstractEventLoop

# thx to @andgein for the idea of abstract classes <3
class AbstractCrawler:
    def __init__(self):
        self._logger = Logger('Crawler')


    async def crawl(self):
        raise NotImplementedError()


class Crawler(AbstractCrawler):

    def __init__(self, directory: str) -> None:
        super().__init__()
        self.storage = DirectoryPcapStorage(directory)
        self._database = Redis()

    async def init_database(self, loop : Optional[AbstractEventLoop] = None) -> None:
        if loop is None:
            loop = asyncio.get_event_loop()
        self._database = await Redis.new("redis://localhost", loop, (5, 10))

    async def crawl(self) -> None:
        db_tasks = []
        for file_name in self.storage.get_list_of_pcaps():
            self._logger.debug(f'Found pcap: {file_name}')

            task = asyncio.ensure_future(self._database.put_stream(file_name))
            db_tasks.append(task)
        if len(db_tasks) != 0:
            await asyncio.wait(db_tasks)
