from backends.logger import Logger

import os
import glob


class AbstractPcapStorage:

    def __init__(self):
        self._logger = Logger('PcapStorage')
    
    def get_list_of_pcaps(self):
        raise NotImplementedError()


class DirectoryPcapStorage(AbstractPcapStorage):

    def __init__(self, directory: str):
        super().__init__()
        self.directory = directory

    def get_list_of_pcaps(self, port=None):
        if port is None:
            return glob.iglob('%s/**/*.pcap' % self.directory, recursive=True)
        else:
            return glob.iglob('%s/**/%s/**/*.pcap' % self.directory, recursive=True)
