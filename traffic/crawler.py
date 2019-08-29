from traffic.logger import Logger
from traffic.pcap_storage import DirectoryPcapStorage

import glob
import os.path
import asyncio


# thx to @andgein for the idea of abstract classes <3
class AbstractCrawler:
    def __init__(self):
        self._logger = Logger('Crawler')


    async def crawl(self):
        raise NotImplementedError()


class Crawler(AbstractCrawler):

    def __init__(self, directory: str):
        super().__init__()
        self.storage = DirectoryPcapStorage(directory)


    async def crawl(self):
        for file_name in self.storage.get_list_of_pcaps():
            self._logger.debug(f'Found pcap: {file_name}')
