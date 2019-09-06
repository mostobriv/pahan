#!/usr/bin/env python3

"""
Description: abstract stream-file to database putter, and a concrete redis
implementation. Stream file format is taken from the lua script and is
"streams/%s.parts/%s-%s_%s-%s_%d.pcap"
"""

from traffic.logger import Logger
import re
import asyncio
import aioredis
import os.path as path

from typing import NamedTuple, Optional, Tuple


class TrafficInfo(NamedTuple):
    pcap_file : str
    stream_index : int
    src_addr : str
    src_port : int
    dst_addr : str
    dst_port : int

class AbstractDbControl:
    def __init__(self) -> None:
        self._logger = Logger("Slicer")

    _fname_re = re.compile("(\w+)-(\d+)_(\w+)-(\d+)_(\d+).pcap")
    def _parse_file_name(self, name : str, pcap_name : str) -> TrafficInfo:
        # a:name - name of the stream file
        # a:pcap_name - name of the original pcap that was split
        base_name = path.basename(name)
        m = self._fname_re.match(base_name)
        if m is None:
            raise LookupError("Malformed stream file name")
        return TrafficInfo(pcap_file = pcap_name
                          ,src_addr = m.group(1)
                          ,src_port = int(m.group(2))
                          ,dst_addr = m.group(3)
                          ,dst_port = int(m.group(4))
                          ,stream_index = int(m.group(5))
                          )

    async def put_chunk(self, file_name : str, orig_pcap_name : str) -> None:
        """
        Put one stream into the database
        """
        raise NotImplementedError()

class RedisControl(AbstractDbControl):
    def __init__(self) -> None:
        """
        Dummy class constructor, !!!do not call!!!
        """
        super().__init__()
        # an anonymous class to appease mypy
        self.redis = type("RedisMock", (object,), {})()
    # Async class constructor
    @classmethod
    async def new(cls
                 ,addr : str, loop : asyncio.AbstractEventLoop
                 ,pool_size : Optional[Tuple[int, int]] #None to create single connection
                 ) -> None:
        self = cls()
        if pool_size is not None:
            self.redis = await aioredis.create_redis_pool(
                 addr
                ,minsize  = pool_size[0]
                ,max_size = pool_size[1]
                ,loop = loop
            )
        else:
            self.redis = await aioredis.create_redis(
                addr, loop=loop
            )

    """
    Redis database format is the following:
    1. The stream is kept in a hash
    2. "orig_pcap_name#stream_index" for a key
    3. The fields are the following:
    """
    FieldSrcPort = "SrcPort"
    FieldSrcAddr = "SrcAddr"
    FieldDstPort = "DstPort"
    FieldDstAddr = "DstAddr"
    FieldContent = "Content"

    async def put_chunk(self, file_name : str, orig_name : str) -> None:
        # don't need all path info for this
        orig_name = path.basename(orig_name)
        info = self._parse_file_name(file_name, orig_name)
        key = f"{info.pcap_file}#{info.stream_index}"
        # maybe run those concurrently? I don't actually think it matters that much
        await self.redis.hset(key, self.FieldSrcPort, info.src_port)
        await self.redis.hset(key, self.FieldSrcAddr, info.src_addr)
        await self.redis.hset(key, self.FieldDstPort, info.dst_port)
        await self.redis.hset(key, self.FieldDstAddr, info.dst_addr)
        #
        with open(file_name, "rb") as file:
            content = file.read()
            await self.redis.hset(key, self.FieldContent, content)
