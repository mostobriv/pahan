from traffic.logger import Logger


from scapy.all import Raw
from collections import defaultdict
from itertools import groupby
from functools import reduce

import json


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

    def dump(self, sessions):
        tcp_data = list()
        for _, v in sessions.items():
            tcp_data.append(SHolder([(pack['IP'].src, pack['Raw'].load) for pack in v if Raw in pack], v[0].time))

    # Primary key is time of first incoming package from pcap

        import time, os
        foo = str(time.time()).replace('.', '_')
        os.system(f'mkdir dumps/tasty_tests/{foo}')
        ctr = 0
        for s in sorted(tcp_data, key=lambda x: x.timestamp):
            bar = str(ctr)

            with open(f'dumps/tasty_tests/{foo}/{bar}', 'wb') as f:
                for src, data in groupby(s.session, key=lambda x: x[0]):
                    buf = reduce(lambda summ, x: summ + x[1], data, bytes())
                    f.write(b'\n' + b'=' * 100 + b'\n')
                    f.write(f'{src}\n'.encode())
                    f.write(b'=' * 100 + b'\n')
                    f.write(buf)
            ctr+= 1