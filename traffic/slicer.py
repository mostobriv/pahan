from traffic.logger import Logger
from traffic.pcap_storage import DirectoryPcapStorage

import time
import asyncio
from asyncio.subprocess import PIPE


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
            proc = await asyncio.create_subprocess_shell(f"tshark -q -X lua_script:traffic/tcp-stream-splitter.lua -X lua_script1:{path} -n -r {path}", 
                                                stdout=PIPE, stderr=PIPE)
            stdout, stderr = await proc.communicate()
            retcode = proc.returncode
        except Exception as e:
            self._logger.error(f'Got an exception {e}', e)
        self._logger.debug(f'Finished slicing of {path} with {retcode} return status code')
        if retcode != 0:
            self._logger.warning(f'Process stdout: {stdout}')
            self._logger.warning(f'Process stderr: {stderr}')


    async def slice_pcaps(self):

        workers_total = 5

        async def worker(name, queue):
           while not queue.empty():
                try:
                    file_name = await queue.get()
                    await self._slice_one_pcap(file_name)
                    queue.task_done()
                except Exception as e:
                    self._logger.error(f'Got an exception inside of worker: {e}', e)
    
        q = asyncio.Queue()
        for file_name in self.storage.get_list_of_pcaps():
            q.put_nowait(file_name)
        
        await asyncio.wait([worker('slicer_worker_%d' % i, q) for i in range(workers_total)])