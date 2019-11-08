from traffic.logger import Logger
from traffic.pcap_storage import DirectoryPcapStorage
from traffic.sessions_dumper import SessionsDumper

import time
import asyncio
from asyncio.subprocess import PIPE
from scapy.all import AsyncSniffer, IPSession, ARP, IP, TCP, ICMP, UDP



class AbstractSlicer:
    def __init__(self):
        self._logger = Logger('Slicer')


    async def slice_pcap(self, path: str):
        raise NotImplementedError()


# dirty hack from internet
# You can accomplish this by just sorting a list of the attributes that make our stream unique. 
# Here is a function called full_duplex() that will reassemble all of the same protocols that 
# the default session assembly process currently supports but will do it with bi-directional streams.
def full_duplex(packets):
    sess = "Other"
    if 'Ether' in packets:
        if 'IP' in packets:
            if 'TCP' in packets:
                sess = str(sorted(["TCP", packets[IP].src, packets[TCP].sport, packets[IP].dst, packets[TCP].dport], key=str))
            elif 'UDP' in packets:
                sess = str(sorted(["UDP", packets[IP].src, packets[UDP].sport, packets[IP].dst, packets[UDP].dport], key=str))
            elif 'ICMP' in packets:
                sess = str(sorted(["ICMP", packets[IP].src, packets[IP].dst, packets[ICMP].code, packets[ICMP].type,
                                   packets[ICMP].id], key=str))
            else:
                sess = str(sorted(["IP", packets[IP].src, packets[IP].dst, packets[IP].proto], key=str))
        elif 'ARP' in packets:
            sess = str(sorted(["ARP", packets[ARP].psrc, packets[ARP].pdst], key=str))
        else:
            sess = packets.sprintf("Ethernet type=%04xr,Ether.type%")
    return sess


class Slicer(AbstractSlicer):

    def __init__(self, pcaps_directory: str, database=None):
        super().__init__()
        self.storage = DirectoryPcapStorage(pcaps_directory)
        self.sessions_dumper = SessionsDumper()

        self.db = database


    async def _slice_one_pcap(self, path: str):
        load_delay = 1

        self._logger.debug(f'Slicing pcap: {path}')
        try:
            sn = AsyncSniffer(filter='tcp',  offline=path, session=IPSession)
            
            sn.start()
            while sn.running:
                await asyncio.sleep(load_delay)
            
            sessions = sn.results.sessions(full_duplex)
            await self.sessions_dumper.save(sessions)
        except Exception as e:
            self._logger.error(f'Got an exception {e}', e)

        self._logger.debug(f'Finished slicing of {path} with total {len(sessions)} sessions')



    async def slice_pcaps(self):
        await self.db.push_stream()

        workers_total = 5
        q = asyncio.Queue(workers_total * 3)
        feeder_is_alive = True

        async def worker(name, queue):
            nonlocal feeder_is_alive
            while feeder_is_alive or not queue.empty():
                try:
                    file_name = await queue.get()
                    await self._slice_one_pcap(file_name)
                except Exception as e:
                    self._logger.error(f'Got an exception inside of {name}: {e}', e)
    
        
        async def feeder(name, queue):
            nonlocal feeder_is_alive
            for file_name in self.storage.get_list_of_pcaps():
                try:
                    await q.put(file_name)
                except Exception as e:
                    self._logger.error(f'Got an exception inside of {name}: {e}', e)
            feeder_is_alive = False
        
        # TODO: verify that workers-blocking bug won't appear again
        # it's happening when feeder does not spawns first, some workers simply blocking themselves
        # while waiting for getting tasks from queue
        # Changed asyncio.wait to asyncio.gather to control order of spawned coroutines, but all the same,
        # consider about proper patch
        
        worker_pool = [worker('slicer_worker_%d' % i, q) for i in range(workers_total)]
        await asyncio.gather(feeder('feeder', q), *worker_pool)

        self._logger.debug('slicer is done')