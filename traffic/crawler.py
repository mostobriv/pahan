import glob
import os.path
from traffic.logger import Logger


class Crawler:

    def __init__(self, directory: str):
        self._logger = Logger(self)
        self.directory = directory

    def crawl(self):
        self._logger.info('Crawling into %s' % os.path.abspath(self.directory))
        for file_name in glob.glob('%s/**/*.pcap' % self.directory, recursive=True):
            self._logger.debug(f'Found pcap: {file_name}')
