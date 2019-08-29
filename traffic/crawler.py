import glob
import os.path
from traffic.logger import Logger
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
        self.directory = directory
    

    async def crawl(self):
        self._logger.info('Crawling into %s' % os.path.abspath(self.directory))
        for file_name in glob.glob('%s/**/*.parts/*.pcap' % self.directory, recursive=True):
            self._logger.debug(f'Found pcap: {file_name}')
