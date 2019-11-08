FROM python:3.7

ENV DEBIAN_FRONTEND noninteractive
RUN apt update && apt-get install -qy \
    build-essential \
    tcpdump

RUN pip install \
    coloredlogs \
    aiohttp \
    asyncio \
    scapy \
    memory_profiler \
    asyncpg

RUN mkdir /pahan/
WORKDIR /pahan/

ADD traffic/ traffic/
ADD web/ web/
# RUN mkdir logs/
# ADD dumps/ dumps/
ADD pahan.py pahan.py
ADD settings.py settings.py

CMD python /pahan/pahan.py
