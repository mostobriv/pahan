from traffic.logger import Logger
import time
import os

class Slicer:

    def __init__(self):
        self._logger = Logger(self)

    def slice_pcap_tshark(self, path: str):
        self._logger.debug(f'Started slicing of {path}')
        try:
            os.system(f"tshark -q -X lua_script:tcp-stream-splitter.lua -X lua_script1:{path} -n -r {path}")
        except Exception as e:
            self._logger.error(f'Got an exception {e}', e)
        self._logger.debug(f'Finished slicing of {path}')