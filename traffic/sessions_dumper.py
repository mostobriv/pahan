from backends.logger import Logger


from scapy.all import Raw
from collections import defaultdict
from itertools import groupby
from functools import reduce
import asyncio
import asyncpg

import json
import base64


class AbstractSessionsDumper:
    def __init__(self):
        self._logger = Logger('SessionsDumper')


    async def dump(self, sessions):
        raise NotImplementedError()


class SHolder:

    __slots__ = ['session', 'timestamp']

    def __init__(self, session, timestamp):
        self.session = session
        self.timestamp = timestamp


class SessionsDumper(AbstractSessionsDumper):

    def __init__(self):
        super().__init__()

    async def retrieve(self, sessions):
        loop = asyncio.get_event_loop()
        sessions = await loop.run_in_executor(None, self._retrieve_inner, sessions)
        return sessions
        
            
    def _retrieve_inner(self, indirect_sessions):
        tcp_data = list()
        for _, v in indirect_sessions.items():
            tcp_data.append(SHolder([(pack['IP'].src, pack['Raw'].load) for pack in v if Raw in pack], v[0].time))

        ordered_sessions = list()
        for s in sorted(tcp_data, key=lambda x: x.timestamp):
            dump = list()
            for src, data in groupby(s.session, key=lambda x: x[0]):
                buf = reduce(lambda summ, x: summ + x[1], data, bytes())
                dump.append(json.dumps({"src_ip": src, 
                                        "data": base64.b64encode(buf).decode() 
                                    }
                                ))
            ordered_sessions.append(json.dumps(dump))

        return ordered_sessions