from traffic.logger import Logger
from traffic.pcap_storage import DirectoryPcapStorage

import time
import asyncio


# thx to @andgein for the idea of abstract classes <3
class AbstractSlicer:
    def __init__(self):
        self._logger = Logger('Slicer')


    async def slice_pcap(self, path: str):
        raise NotImplementedError()


class Slicer(AbstractSlicer):

    def __init__(self, directory: str):
        super().__init__()
        self.storage = DirectoryPcapStorage(directory)

    async def _slice_one_pcap(self, path: str):
        self._logger.debug(f'Slicing pcap: {path}')
        try:
            proc = await asyncio.create_subprocess_shell(f"tshark -q -X lua_script:tcp-stream-splitter.lua -X lua_script1:{path} -n -r {path}")
            retcode = await proc.wait()
        except Exception as e:
            self._logger.error(f'Got an exception {e}', e)
        self._logger.debug(f'Finished slicing of {path} with {retcode} return status code')


    async def slice_pcaps(self):
        for file_name in self.storage.get_list_of_pcaps():
            await self._slice_one_pcap(file_name)