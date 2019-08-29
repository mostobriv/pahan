from traffic.logger import Logger
import time
import asyncio


# thx to @andgein for the idea of abstract classes <3
class AbstractSlicer:
    def __init__(self):
        self._logger = Logger('Slicer')

    async def slice_pcap(self, path: str):
        raise NotImplementedError()


class Slicer(AbstractSlicer):

    def __init__(self):
        super().__init__()

    async def slice_pcap(self, path: str):
        self._logger.debug(f'Started slicing of {path}')
        try:
            proc = await asyncio.create_subprocess_shell(f"tshark -q -X lua_script:tcp-stream-splitter.lua -X lua_script1:{path} -n -r {path}")
            retcode = await proc.wait()
        except Exception as e:
            self._logger.error(f'Got an exception {e}', e)
        self._logger.debug(f'Finished slicing of {path} with {retcode} return status code')